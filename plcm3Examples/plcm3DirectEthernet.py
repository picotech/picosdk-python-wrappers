#
# Copyright (C) 2026 Pico Technology Ltd. See LICENSE file for terms.
#
# PICOLOG CM3 DIRECT ETHERNET EXAMPLE (NO SDK)
# ######################################################################

"""
Pure-Ethernet PicoLog CM3 client.

Talks to a PicoLog CM3 current data logger over raw UDP - no SDK, no DLL,
standard library only. Modelled on pt104Examples/pt104DirectEthernet.py and on
the C# example at github.com/picotech/picosdk-ethernet-protocol-examples
(plcm3/c-sharp).

Before this will work the CM3's Ethernet module must already have been enabled
and given an IP address over USB, using the Ethernet Settings utility installed
with PicoLog. The module is disabled by default to save power. Once an IP and
port are assigned the unit can run from USB power or PoE.

The CM3 measures the AC voltage produced by a current clamp, so the current
reading below is only as good as CLAMP_MV_PER_AMP. The supplied TA138 clamp is
1 mV/A.
"""

import socket
import time
import threading

# ----------------------------------------------------------------------
# --------------------------- USER SETTINGS ----------------------------
# ----------------------------------------------------------------------

# Set these to match your unit. They are used only if the broadcast discovery
# below finds nothing - on a network where broadcast traffic is blocked, for
# instance. DEVICE_PORT is the port the unit listens on, as reported in its
# broadcast reply and by the Ethernet Settings utility; 1 is typical.
DEVICE_IP   = "192.168.0.100"
DEVICE_PORT = 1

DISCOVERY_TIMEOUT = 1.0     # seconds to collect broadcast replies, per interface

# Which local interface to broadcast from. Leave empty to try every local
# address in turn, which is what you want on a machine with more than one
# network interface: a broadcast sent from the wildcard address goes out of the
# default-route interface only, so a CM3 on any other subnet never hears it.
DISCOVERY_BIND_IP = ""

# Low nibble of the start-converting argument: one bit per channel.
# 0x01 = ch1, 0x02 = ch2, 0x04 = ch3, so 0x07 = all three.
ENABLED_CHANNELS = 0x07

# High nibble of the start-converting argument: the input range, shared by
# every enabled channel. The two documented values come from the C# example
# (UdpPLCM3.cs), which names them 0x00 = 10 kOhm and 0x01 = 375 Ohm.
#
# This nibble is NOT the driver's PLCM3_DATA_TYPES enum, despite both being
# range selectors. That enum is per-channel, set by PLCM3SetChannel, and
# begins PLCM3_OFF = 0 - whereas this nibble is shared by all channels and
# streams data quite happily at 0x00. Its 1 mV and 10 mV entries would also
# differ by a factor of ten, and measured here 0x00 and 0x01 returned the same
# counts for the same input. Treat anything other than 0x00 as unverified.
GAIN = 0x00

# Mains noise rejection filter.
MAINS_60HZ = False          # False = 50 Hz, True = 60 Hz

# Current clamp sensitivity per channel, millivolts out per amp in. The
# supplied TA138 is 1 mV/A. Set a channel to None to report millivolts only,
# which is what you want for a channel fed from a voltage source rather than
# through a clamp.
CLAMP_MV_PER_AMP = {
    1: 1.0,
    2: 1.0,
    3: 1.0,
}

# ----------------------------------------------------------------------
# Protocol constants - see the PicoLog CM3 Programmer's Guide
# ----------------------------------------------------------------------
CMD_MAINS_FREQUENCY = 0x30      # + 0x00 for 50 Hz, 0x01 for 60 Hz
CMD_START_CONVERTING = 0x31     # + (gain << 4 | channel bitmask)
CMD_READ_EEPROM = 0x32
CMD_UNLOCK = 0x33
CMD_KEEP_ALIVE = 0x34           # must be sent at least every 15 s

CMD_LOCK = b"lock"              # ASCII, reply starts "Lock"
CMD_BROADCAST = b"fff"          # discovery payload

DISCOVERY_PORT = 23             # broadcast goes from port 23 to port 23

# The reply prefix is matched case-insensitively: the CM3 firmware answers
# "Eeprom=" where the C# example's constant says "EEPROM=".
EEPROM_PREFIX = b"eeprom="

CHANNEL_COUNT = 3
SAMPLES_PER_CHANNEL = 4         # four measurements per channel per packet
PACKET_SIZE = SAMPLES_PER_CHANNEL * 5   # index byte + 4 data bytes, each

# A channel's four measurements arrive under consecutive indices:
# ch1 = 0x00..0x03, ch2 = 0x04..0x07, ch3 = 0x08..0x0B.
CHANNEL_BY_FIRST_INDEX = {0x00: 1, 0x04: 2, 0x08: 3}

KEEP_ALIVE_INTERVAL = 9.0       # comfortably under the 15 s unlock timeout

# Only these two range codes are documented; anything else is reported as
# unknown rather than silently mislabelled as one of them.
RANGE_NAMES = {0x00: "10 kOhm", 0x01: "375 Ohm"}


def range_name(gain: int) -> str:
    """Human-readable name for a gain nibble."""
    return RANGE_NAMES.get(gain, f"unknown range {gain:#04x}")

# ----------------------------------------------------------------------
# UDP helpers
# ----------------------------------------------------------------------
def udp_send(sock: socket.socket, payload: bytes, addr):
    """Send a UDP packet."""
    sock.sendto(payload, addr)


def udp_recv(sock: socket.socket, timeout: float = 2.0) -> bytes:
    """
    Receive a UDP packet; return empty bytes if nothing usable arrives.

    Both failure modes have to be caught. A timeout is the ordinary one. The
    other is Windows-specific: if an earlier sendto drew an ICMP port
    unreachable - the device is off, or DEVICE_IP names a host with nothing
    listening on DEVICE_PORT - the *next* recvfrom on this socket raises
    ConnectionResetError (WSAECONNRESET). Letting that propagate would end the
    example with a traceback instead of the "no data" message below.
    """
    sock.settimeout(timeout)
    try:
        data, _ = sock.recvfrom(4096)
        return data
    except socket.timeout:
        return b""
    except OSError:
        return b""


# ----------------------------------------------------------------------
# Device discovery (UDP broadcast)
# ----------------------------------------------------------------------
def parse_broadcast_reply(reply: bytes):
    """
    Parse one reply to the discovery broadcast.

    Every CM3 answers with "CM3 Mac:XXXXXX Lock:Y Port:ZZ Serial:SSSSSS" where
      XXXXXX is the 6-byte MAC address of the unit replying,
      Y      is 0x00 for unlocked and 0x01 for locked,
      ZZ     is the 2-byte port it listens on, most significant byte first,
      SSSSSS is the ASCII serial number.

    The fields are found by searching for their ASCII tags rather than by fixed
    offset, because the padding between them is not guaranteed.

    Returns a dict, or None if this is not a well-formed CM3 reply.
    """
    if not reply.startswith(b"CM3"):
        return None

    try:
        i = reply.index(b"Mac:") + 4
        mac_bytes = reply[i:i + 6]
        if len(mac_bytes) < 6:
            return None
        mac = ":".join(f"{b:02X}" for b in mac_bytes)

        i = reply.index(b"Lock:", i) + 5
        locked = reply[i] != 0x00

        i = reply.index(b"Port:", i) + 5
        port = int.from_bytes(reply[i:i + 2], byteorder="big")

        i = reply.index(b"Serial:", i) + 7
        serial = reply[i:].decode("ascii", errors="ignore").strip("\x00").strip()
    except (ValueError, IndexError):
        # ValueError - a tag is missing; IndexError - the reply is truncated.
        return None

    return {"mac": mac, "locked": locked, "port": port, "serial": serial}


def local_addresses():
    """
    Every local IPv4 address to try broadcasting from, most specific first.

    The empty string (INADDR_ANY) is included last as a fallback for hosts
    where the interface list comes back incomplete.
    """
    if DISCOVERY_BIND_IP:
        return [DISCOVERY_BIND_IP]

    try:
        addresses = socket.gethostbyname_ex(socket.gethostname())[2]
    except socket.error:
        addresses = []

    return [a for a in addresses if not a.startswith("127.")] + [""]


def broadcast_from(local_ip):
    """
    Send the discovery broadcast out of one local interface and collect the
    replies for DISCOVERY_TIMEOUT seconds. Returns a list of info dicts.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    found = []
    try:
        # Port 23 is privileged on some systems and may be taken by a telnet
        # service or blocked by the firewall.
        sock.bind((local_ip, DISCOVERY_PORT))
        udp_send(sock, CMD_BROADCAST, ("255.255.255.255", DISCOVERY_PORT))

        deadline = time.time() + DISCOVERY_TIMEOUT
        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                break
            sock.settimeout(remaining)
            try:
                reply, addr = sock.recvfrom(4096)
            except socket.timeout:
                break

            # Our own broadcast comes back to us; parse_broadcast_reply
            # rejects it along with anything else that is not a CM3.
            info = parse_broadcast_reply(reply)
            if info is None:
                continue
            info["ip"] = addr[0]
            found.append(info)
    except OSError as e:
        print(f"[!] Discovery from {local_ip or 'any interface'} failed: {e}")
    finally:
        sock.close()

    return found


def find_device():
    """
    Broadcast for CM3s and return the address of the first usable one.

    Sends "fff" to 255.255.255.255:23 from local port 23, out of each local
    interface in turn, and collects the replies. Units already locked by
    another host are listed but skipped.

    Returns (address_tuple, info_dict) - info_dict is None when discovery found
    nothing and the configured DEVICE_IP is being used instead.
    """
    candidates = []
    seen = set()
    for local_ip in local_addresses():
        for info in broadcast_from(local_ip):
            if info["mac"] in seen:
                continue
            seen.add(info["mac"])
            candidates.append(info)

    if not candidates:
        print("[!] No CM3 replied to the discovery broadcast.")
        print(f"[i] Falling back to configured device {DEVICE_IP}:{DEVICE_PORT}")
        return (DEVICE_IP, DEVICE_PORT), None

    print(f"[+] Discovery found {len(candidates)} CM3 unit(s):")
    for info in candidates:
        state = "locked by another host" if info["locked"] else "available"
        print(f"    Serial {info['serial']:<12} {info['ip']}:{info['port']}"
              f"  MAC {info['mac']}  ({state})")

    for info in candidates:
        if not info["locked"]:
            return (info["ip"], info["port"]), info

    # Everything found reports itself locked. That includes the common case of
    # a unit still locked to THIS machine after an ungraceful exit, which the
    # device only releases 15 s after the last keep-alive. A real address we
    # have seen reply beats a configured one that may name nothing at all, so
    # try it anyway and let lock_device's reply settle it.
    first = candidates[0]
    print("[!] Every CM3 found reports itself locked - trying the first one "
          "anyway, in case it is still locked to this machine.")
    return (first["ip"], first["port"]), first


# ----------------------------------------------------------------------
# Lock the device (ASCII "lock") and interpret the reply
# ----------------------------------------------------------------------
def lock_device(sock: socket.socket, dest) -> bool:
    """
    Claim the unit for this host.

    The device answers "Lock Success" or "Lock Success (already locked to this
    machine)". Anything else means another host owns it.
    """
    udp_send(sock, CMD_LOCK, dest)

    reply = udp_recv(sock, timeout=2.0)
    if not reply:
        print("[!] No reply to lock request - proceeding anyway.")
        return False

    txt = reply.decode(errors="ignore")
    if txt.startswith("Lock"):
        if "already locked" in txt.lower():
            print("[i] Device already locked to this machine.")
        else:
            print("[+] Lock acquired successfully.")
        return True

    print(f"[!] Lock request failed / unexpected reply: {reply!r}")
    return False


# ----------------------------------------------------------------------
# Read the calibration EEPROM (0x32)
# ----------------------------------------------------------------------
def read_eeprom(sock: socket.socket, dest, expected_mac=None):
    """
    Read and report the EEPROM contents.

    The reply is "Eeprom=" followed by the raw EEPROM image. Four 32-bit
    little-endian calibration constants live at offsets 37, 41, 45 and 49, and
    the 6-byte MAC address at offset 53, all relative to the end of the prefix.

    Note that the calibration constants are NOT used to scale the readings: the
    CM3 conversion below is a fixed 2.5 V reference scaling, exactly as in the
    C# example. They are read here for completeness and to let us confirm we
    are still talking to the unit that answered the broadcast.
    """
    udp_send(sock, bytes([CMD_READ_EEPROM]), dest)

    resp = udp_recv(sock, timeout=2.0)
    if not resp:
        print("[!] No reply to read-EEPROM command.")
        return None

    if resp[:len(EEPROM_PREFIX)].lower() != EEPROM_PREFIX:
        print(f"[!] Unexpected read-EEPROM reply: {resp[:32]!r}...")
        return None

    image = resp[len(EEPROM_PREFIX):]
    if len(image) < 59:
        print(f"[!] EEPROM image too short ({len(image)} bytes).")
        return None

    calibration = [
        int.from_bytes(image[offset:offset + 4], byteorder="little")
        for offset in (37, 41, 45, 49)
    ]
    mac = ":".join(f"{b:02X}" for b in image[53:59])

    print("\n--- EEPROM ---")
    for i, value in enumerate(calibration):
        print(f"Calibration {i}       : {value}")
    print(f"MAC address         : {mac}")

    if expected_mac is not None and mac != expected_mac:
        print(f"[!] MAC mismatch - broadcast reported {expected_mac}, "
              f"EEPROM reports {mac}.")

    return {"calibration": calibration, "mac": mac}


# ----------------------------------------------------------------------
# Mains noise rejection (0x30)
# ----------------------------------------------------------------------
def set_mains(sock: socket.socket, dest, sixty_hertz: bool):
    """0x30 followed by 0x00 for 50 Hz or 0x01 for 60 Hz."""
    udp_send(sock, bytes([CMD_MAINS_FREQUENCY, 0x01 if sixty_hertz else 0x00]),
             dest)
    print(f"[+] Mains rejection set to {'60' if sixty_hertz else '50'} Hz.")


# ----------------------------------------------------------------------
# Start converting (0x31)
# ----------------------------------------------------------------------
def start_converting(sock: socket.socket, dest, channels: int, gain: int):
    """
    0x31 followed by one byte: low nibble is the channel bitmask, high nibble
    selects the range (0 = 10 kOhm, 1 = 375 Ohm). For example 0x11 enables
    channel 1 on the 375 Ohm range.

    Sending a channel mask of 0 stops conversion.
    """
    argument = ((gain & 0x0F) << 4) | (channels & 0x0F)
    udp_send(sock, bytes([CMD_START_CONVERTING, argument]), dest)

    enabled = [str(ch) for ch in range(1, CHANNEL_COUNT + 1)
               if channels & (1 << (ch - 1))]
    print(f"[+] Converting started on channel(s) {', '.join(enabled)} "
          f"({range_name(gain)} range) - data will now stream.")


def clamp_sensitivity(channel: int):
    """
    The clamp sensitivity for a channel in mV/A, or None if it has no clamp.

    A channel missing from CLAMP_MV_PER_AMP counts as having no clamp. So does
    a value of zero or less, which cannot be divided by - but that is a
    configuration mistake rather than an intent to read volts, so say so.
    """
    sensitivity = CLAMP_MV_PER_AMP.get(channel)
    if sensitivity is None:
        return None
    if sensitivity <= 0:
        print(f"[!] Ch{channel} clamp sensitivity {sensitivity} is not "
              f"usable - reporting millivolts only.")
        return None
    return sensitivity


def describe_clamp(channel: int) -> str:
    """How a channel's scaling should be described in the setup block."""
    sensitivity = clamp_sensitivity(channel)
    if sensitivity is None:
        return "no clamp, millivolts only"
    return f"{sensitivity} mV/A"


def print_channel_setup(channels: int, gain: int):
    """
    Report how each channel is configured, so the readings below can be read
    against the scaling that produced them.
    """
    print("\n--- Channel setup ---")
    for channel in range(1, CHANNEL_COUNT + 1):
        if not channels & (1 << (channel - 1)):
            print(f"Ch{channel}  disabled")
            continue

        scaling = describe_clamp(channel)
        print(f"Ch{channel}  enabled     {range_name(gain)} range     {scaling}")


def stop_converting(sock: socket.socket, dest):
    """Start converting with no channels enabled, which stops conversion."""
    udp_send(sock, bytes([CMD_START_CONVERTING, 0x00]), dest)


# ----------------------------------------------------------------------
# Keep-alive thread (0x34) - required at least every 15 s
# ----------------------------------------------------------------------
def start_keep_alive(sock: socket.socket, dest, stop_event: threading.Event):
    """Send 0x34 every KEEP_ALIVE_INTERVAL seconds until stop_event is set."""
    def loop():
        while not stop_event.wait(KEEP_ALIVE_INTERVAL):
            try:
                udp_send(sock, bytes([CMD_KEEP_ALIVE]), dest)
            except OSError as e:
                if stop_event.is_set():
                    # Socket closed while shutting down - expected.
                    return
                # A transient send failure must not kill the thread: without
                # the keep-alive the CM3 unlocks itself after 15 s and stops
                # streaming, which would show up only as silence.
                print(f"[!] Keep-alive send failed ({e}) - still trying.")

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    return thread


# ----------------------------------------------------------------------
# Measurement packet parsing
# ----------------------------------------------------------------------
def parse_measurement(field: bytes) -> int:
    """
    Turn one 4-byte measurement field into a 28-bit reading.

    The field is [status nibble][top nibble of data][3 more data bytes], most
    significant byte first. The high nibble of the first byte stays at 0x2 on
    every channel and sample; the low nibble is real data.

    Note that the C# example's ParseMeasure() reads only the low three bytes
    and so drops that nibble. That goes unnoticed while readings stay under
    2^24 counts (about 156 mV), but wraps silently above it - measured against
    a 500 mV peak 50 Hz sine, keeping the nibble gives 351.6 mV RMS against an
    expected 353.6 mV, while dropping it gives 39.1 mV.
    """
    return ((field[0] & 0x0F) << 24) | int.from_bytes(field[1:4],
                                                      byteorder="big")


def parse_packet(pkt: bytes):
    """
    Parse one 20-byte measurement packet.

    Each packet carries all four measurements for a single channel, as four
    consecutive [index byte][4 data bytes] groups:

        00XXXXXXXX 01XXXXXXXX 02XXXXXXXX 03XXXXXXXX   channel 1
        04XXXXXXXX 05XXXXXXXX 06XXXXXXXX 07XXXXXXXX   channel 2
        08XXXXXXXX 09XXXXXXXX 0aXXXXXXXX 0bXXXXXXXX   channel 3

    Returns (channel_number, [m0, m1, m2, m3]) or None if the packet is not a
    valid measurement packet - which is how the textual replies (discovery
    echoes, lock responses) get filtered out.

    Every measurement datagram observed from a CM3 has been exactly this size,
    carrying one channel; the device interleaves channels across datagrams
    rather than packing several into one. A longer datagram would mean that
    assumption is wrong, so it is reported rather than quietly truncated.
    """
    if len(pkt) < PACKET_SIZE:
        return None

    if len(pkt) > PACKET_SIZE and pkt[0] in CHANNEL_BY_FIRST_INDEX:
        print(f"[!] Measurement packet is {len(pkt)} bytes, expected "
              f"{PACKET_SIZE} - only the first channel in it is being read.")

    first_index = pkt[0]
    channel = CHANNEL_BY_FIRST_INDEX.get(first_index)
    if channel is None:
        return None

    measurements = []
    for i in range(SAMPLES_PER_CHANNEL):
        chunk = pkt[i * 5:(i * 5) + 5]
        if chunk[0] != first_index + i:
            # Indices are not consecutive - not a packet for one channel.
            return None
        measurements.append(parse_measurement(chunk[1:5]))

    return channel, measurements


def to_millivolts(mean_counts: float) -> float:
    """
    Convert averaged ADC counts to millivolts.

    A 2.5 V reference over a 2^28 full-scale span, so
    mV = 2.5 * counts * 1000 / 2^28. Full scale is therefore 2500 mV, which
    comfortably covers the 0 to 1 V AC input range in the datasheet.

    Confirmed on the 10 kOhm range against a 50 Hz sine of 500 mV peak
    (353.553 mV RMS, since the CM3 reads true RMS): 351.6 mV, an error of
    -0.55%, inside the datasheet's +/-2.5% below 1 V RMS.

    The same scaling holds on both GAIN settings: driven from a voltage
    source, the 10 kOhm and 375 Ohm ranges returned the same counts for the
    same input, so the range selection does not need its own scale factor.

    Caveat worth knowing before trusting absolute values: this scaling is
    fixed, and takes no account of the per-unit calibration constants that
    read_eeprom pulls out of the EEPROM. The C# example ignores them too, and
    the unit measured here carried the round default of 100000000 in all four.
    A unit calibrated differently would carry a gain error that this example
    cannot see. Check against PicoLog 6 if the absolute value matters.
    """
    return (2.5 * mean_counts * 1000.0) / (2 ** 28)


# ----------------------------------------------------------------------
# Main routine
# ----------------------------------------------------------------------
def main():
    # --------------------------------------------------------------
    # 0. Find a CM3, or fall back to the configured address
    # --------------------------------------------------------------
    device_addr, info = find_device()
    expected_mac = info["mac"] if info else None
    if info:
        print(f"\n[+] Using serial {info['serial']} at "
              f"{device_addr[0]}:{device_addr[1]}")

    # --------------------------------------------------------------
    # 1. Create a UDP socket - the OS picks a free local port, and the
    #    device streams its data back to whichever port we send from.
    # --------------------------------------------------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))

    stop_event = threading.Event()

    try:
        # ----------------------------------------------------------
        # 2. Lock the device for this host. The example carries on either
        #    way - lock_device reports what happened - and the shutdown
        #    below unlocks unconditionally.
        # ----------------------------------------------------------
        lock_device(sock, device_addr)

        # ----------------------------------------------------------
        # 3. Read the calibration EEPROM
        # ----------------------------------------------------------
        read_eeprom(sock, device_addr, expected_mac)

        # ----------------------------------------------------------
        # 4. Configure and start the converter
        # ----------------------------------------------------------
        set_mains(sock, device_addr, MAINS_60HZ)
        print_channel_setup(ENABLED_CHANNELS, GAIN)
        start_converting(sock, device_addr, ENABLED_CHANNELS, GAIN)

        # ----------------------------------------------------------
        # 5. Keep the link alive - the device unlocks itself after 15 s
        #    without a keep-alive
        # ----------------------------------------------------------
        start_keep_alive(sock, device_addr, stop_event)
        print(f"[+] Keep-alive started (0x34 every {KEEP_ALIVE_INTERVAL:.0f} s).")

        print("\nWaiting for streamed data... (Ctrl-C to stop)\n")

        # ----------------------------------------------------------
        # 6. Receive and decode measurement packets. Each enabled
        #    channel takes 720 ms to convert, so with all three enabled
        #    a given channel updates roughly every 2.2 s.
        # ----------------------------------------------------------
        while True:
            pkt = udp_recv(sock, timeout=5.0)
            if not pkt:
                print("[!] No data for 5 s - is the converter still running?")
                continue

            parsed = parse_packet(pkt)
            if parsed is None:
                # Textual reply or partial packet - ignore it.
                continue

            channel, measurements = parsed

            # Average the four measurements. See the Programmer's Guide for
            # the other measurement types the CM3 can report.
            mean_counts = sum(measurements) / len(measurements)
            millivolts = to_millivolts(mean_counts)

            line = (f"Ch{channel}  counts={mean_counts:>12.1f}   "
                    f"{millivolts:>10.4f} mV")

            # A channel with no clamp fitted reports millivolts only, rather
            # than inventing a current from a voltage input.
            sensitivity = CLAMP_MV_PER_AMP.get(channel)
            if sensitivity is not None and sensitivity > 0:
                line += f"   {millivolts / sensitivity:>10.4f} A"

            print(line)

    except KeyboardInterrupt:
        print("\n[i] Stopped by user.")
    finally:
        # ----------------------------------------------------------
        # 7. Stop converting, release the lock, close the socket
        # ----------------------------------------------------------
        stop_event.set()
        try:
            stop_converting(sock, device_addr)
            # Unlock unconditionally, as the C# example's Dispose() does. A
            # lost lock reply leaves have_lock False even though we went on to
            # use the device, and that is exactly when leaving it locked for
            # the full 15 s timeout hurts the next run most. Unlocking a
            # device we never held is harmless.
            udp_send(sock, bytes([CMD_UNLOCK]), device_addr)
            print("[i] Unlock command sent.")
        except OSError as e:
            print(f"[!] Error during shutdown: {e}")
        finally:
            sock.close()


if __name__ == "__main__":
    main()
