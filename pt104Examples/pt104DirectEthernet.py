#
# Copyright (C) 2026 Pico Technology Ltd. See LICENSE file for terms.
#
# PT-104 DIRECT ETHERNET EXAMPLE (NO SDK)
# ######################################################################

"""
Pure‑Ethernet PT‑104 client – mode.

Assumptions (as you confirmed):
* The PT‑104 has already been configured (via usb with picolog app) to output
  temperature directly.
* The configuration is 4 channels with PT100 4 wires with average enabled.
* No SDK/DLL is used – everything is done with raw UDP packets.
"""

import socket
import struct
import time
import threading
import codecs

# ----------------------------------------------------------------------
# --------------------------- USER SETTINGS ----------------------------
# ----------------------------------------------------------------------
DEVICE_IP   = "172.26.178.124"   # ← change if needed
DEVICE_PORT = 1                  # listening port reported by the PT‑104
DEVICE_ADDR = (DEVICE_IP, DEVICE_PORT)

# Lookup table for Resistance (Ohms) to Temperature (Celsius)
# Format: (Temperature, Resistance)
RESISTANCE_TEMP_LOOKUP = [
    (-50, 80.306282), (-49, 80.703340), (-48, 81.100257), (-47, 81.497036), (-46, 81.893677),
    (-45, 82.290179), (-44, 82.686545), (-43, 83.082774), (-42, 83.478868), (-41, 83.874827),
    (-40, 84.270652), (-39, 84.666343), (-38, 85.061901), (-37, 85.457327), (-36, 85.852622),
    (-35, 86.247785), (-34, 86.642818), (-33, 87.037721), (-32, 87.432495), (-31, 87.827140),
    (-30, 88.221657), (-29, 88.616046), (-28, 89.010309), (-27, 89.404445), (-26, 89.798455),
    (-25, 90.192339), (-24, 90.586099), (-23, 90.979734), (-22, 91.373246), (-21, 91.766634),
    (-20, 92.159898), (-19, 92.553041), (-18, 92.946061), (-17, 93.338960), (-16, 93.731737),
    (-15, 94.124394), (-14, 94.516930), (-13, 94.909346), (-12, 95.301643), (-11, 95.693820),
    (-10, 96.085879), (-9, 96.477819), (-8, 96.869641), (-7, 97.261345), (-6, 97.652931),
    (-5, 98.044401), (-4, 98.435753), (-3, 98.826989), (-2, 99.218109), (-1, 99.609112),
    (0, 100.000000), (1, 100.390772), (2, 100.781429), (3, 101.171970), (4, 101.562396),
    (5, 101.952706), (6, 102.342901), (7, 102.732980), (8, 103.122944), (9, 103.512792),
    (10, 103.902525), (11, 104.292142), (12, 104.681644), (13, 105.071030), (14, 105.460301),
    (15, 105.849456), (16, 106.238496), (17, 106.627420), (18, 107.016229), (19, 107.404922),
    (20, 107.793500), (21, 108.181962), (22, 108.570309), (23, 108.958540), (24, 109.346656),
    (25, 109.734656), (26, 110.122541), (27, 110.510310), (28, 110.897964), (29, 111.285502),
    (30, 111.672925), (31, 112.060232), (32, 112.447424), (33, 112.834500), (34, 113.221461),
    (35, 113.608306), (36, 113.995036), (37, 114.381650), (38, 114.768149), (39, 115.154532),
    (40, 115.540800), (41, 115.926952), (42, 116.312989), (43, 116.698910), (44, 117.084716),
    (45, 117.470406), (46, 117.855981), (47, 118.241440), (48, 118.626784), (49, 119.012012),
    (50, 119.397125), (51, 119.782122), (52, 120.167004), (53, 120.551770), (54, 120.936421),
    (55, 121.320956), (56, 121.705376), (57, 122.089680), (58, 122.473869), (59, 122.857942),
    (60, 123.241900), (61, 123.625742), (62, 124.009469), (63, 124.393080), (64, 124.776576),
    (65, 125.159956), (66, 125.543221), (67, 125.926370), (68, 126.309404), (69, 126.692322),
    (70, 127.075125), (71, 127.457812), (72, 127.840384), (73, 128.222840), (74, 128.605181),
    (75, 128.987406), (76, 129.369516), (77, 129.751510), (78, 130.133389), (79, 130.515152),
    (80, 130.896800), (81, 131.278332), (82, 131.659749), (83, 132.041050), (84, 132.422236),
    (85, 132.803306), (86, 133.184261), (87, 133.565100), (88, 133.945824), (89, 134.326432),
    (90, 134.706925), (91, 135.087302), (92, 135.467564), (93, 135.847710), (94, 136.227741),
    (95, 136.607656), (96, 136.987456), (97, 137.367140), (98, 137.746709), (99, 138.126162),
    (100, 138.505500), (101, 138.884722), (102, 139.263829), (103, 139.642820), (104, 140.021696),
    (105, 140.400456), (106, 140.779101), (107, 141.157630), (108, 141.536044), (109, 141.914342),
    (110, 142.292525), (111, 142.670592), (112, 143.048544), (113, 143.426380), (114, 143.804101),
    (115, 144.181706), (116, 144.559196), (117, 144.936570), (118, 145.313829), (119, 145.690972),
    (120, 146.068000), (121, 146.444912), (122, 146.821709), (123, 147.198390), (124, 147.574956),
    (125, 147.951406), (126, 148.327741), (127, 148.703960), (128, 149.080064), (129, 149.456052),
    (130, 149.831925), (131, 150.207682), (132, 150.583324), (133, 150.958850), (134, 151.334261),
    (135, 151.709556), (136, 152.084736), (137, 152.459800), (138, 152.834749), (139, 153.209582),
    (140, 153.584300), (141, 153.958902), (142, 154.333389), (143, 154.707760), (144, 155.082016),
    (145, 155.456156), (146, 155.830181), (147, 156.204090), (148, 156.577884), (149, 156.951562),
    (150, 157.325125), (151, 157.698572), (152, 158.071904), (153, 158.445120), (154, 158.818221),
    (155, 159.191206), (156, 159.564076), (157, 159.936830), (158, 160.309469), (159, 160.681992),
    (160, 161.054400), (161, 161.426692), (162, 161.798869), (163, 162.170930), (164, 162.542876),
    (165, 162.914706), (166, 163.286421), (167, 163.658020), (168, 164.029504), (169, 164.400872),
    (170, 164.772125), (171, 165.143262), (172, 165.514284), (173, 165.885190), (174, 166.255981),
    (175, 166.626656), (176, 166.997216), (177, 167.367660), (178, 167.737989), (179, 168.108202),
    (180, 168.478300), (181, 168.848282), (182, 169.218149), (183, 169.587900), (184, 169.957536),
    (185, 170.327056), (186, 170.696461), (187, 171.065750), (188, 171.434924), (189, 171.803982),
    (190, 172.172925), (191, 172.541752), (192, 172.910464), (193, 173.279060), (194, 173.647541),
    (195, 174.015906), (196, 174.384156), (197, 174.752290), (198, 175.120309), (199, 175.488212),
    (200, 175.856000)
]

# Define a dictionary to hold the structured "Data" variables based on the memory map
data_variables = {
    "Reserved_1": None,
    "Batch": None,
    "Calibration_Date": None,
    "Ch1_Calibration": None,
    "Ch2_Calibration": None,
    "Ch3_Calibration": None,
    "Ch4_Calibration": None,
    "MAC_Address": None,
    "Reserved_2": None,
    "Checksum": None,
    "status": "empty"
}

# Define a dictionary to hold measurement packet data
measurement_data = {
    "Channel_1": [0, 0, 0, 0],  # Indices 00-03
    "Channel_2": [0, 0, 0, 0],  # Indices 04-07
    "Channel_3": [0, 0, 0, 0],  # Indices 08-0B
    "Channel_4": [0, 0, 0, 0]   # Indices 0C-0F
}

# ----------------------------------------------------------------------
def interpolate_temperature(resistance):
    """
    Performs linear interpolation on the RESISTANCE_TEMP_LOOKUP table.
    """
    if resistance is None or resistance == 0:
        return None

    # Sort the table just in case (though it is provided sorted by temp)
    # We need it sorted by Resistance for searching
    table = sorted(RESISTANCE_TEMP_LOOKUP, key=lambda x: x[1])
    
    # Handle cases outside the table range (extrapolation)
    if resistance <= table[0][1]:
        p1, p2 = table[0], table[1]
    elif resistance >= table[-1][1]:
        p1, p2 = table[-2], table[-1]
    else:
        # Find the two points to interpolate between
        p1, p2 = None, None
        for i in range(len(table) - 1):
            if table[i][1] <= resistance <= table[i+1][1]:
                p1, p2 = table[i], table[i+1]
                break
    
    # Linear Interpolation Formula: y = y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
    # y = Temperature, x = Resistance
    t1, r1 = p1
    t2, r2 = p2
    
    temperature = t1 + (resistance - r1) * ((t2 - t1) / (r2 - r1))
    return temperature

def get_channel_temperatures(resistances):
    """
    Converts a dictionary of resistances to temperatures.
    """
    temps = {}
    for ch, res in resistances.items():
        temps[ch] = interpolate_temperature(res)
    return temps

def calculate_resistances(eeprom_vars, measurements):
    """
    Calculates resistance (in MOhms) for each channel using the formula:
    result = ((cal * (m3 - m2)) / (m1 - m0)) / 1,000,000
    """
    results = {}
    
    # Mapping EEPROM calibration keys to measurement storage keys
    channels = [
        ("Channel_1", "Ch1_Calibration"),
        ("Channel_2", "Ch2_Calibration"),
        ("Channel_3", "Ch3_Calibration"),
        ("Channel_4", "Ch4_Calibration")
    ]
    
    for m_key, c_key in channels:
        cal = eeprom_vars.get(c_key)
        m = measurements.get(m_key)
        
        # Ensure we have the calibration and measurement data
        if cal is None or m is None:
            results[m_key] = None
            continue
            
        try:
            # Formula updated to divide by 1,000,000 for Ohms
            numerator = cal * (m[3] - m[2])
            denominator = (m[1] - m[0])
            
            if denominator == 0:
                print(f"Warning: Division by zero for {m_key} (m1 - m0 = 0).")
                results[m_key] = 0.0
            else:
                # Calculate and convert to Ohms
                results[m_key] = (numerator / denominator) / 1_000_000.0
        except Exception as e:
            print(f"Error calculating {m_key}: {e}")
            results[m_key] = None
            
    return results

def parse_pkt_data(pkt, storage):
    """
    Parses a 'pkt' variable containing indexed 32-bit values.
    Format: [Index Byte] [4 Bytes Data (MSB First)]
    """
    if not isinstance(pkt, bytes):
        print("Error: pkt must be of type 'bytes'")
        return

    # Process packet in chunks of 5 bytes (1 index + 4 data)
    for i in range(0, len(pkt), 5):
        chunk = pkt[i:i+5]
        if len(chunk) < 5:
            break
            
        index = chunk[0]
        # Convert 4 bytes to integer (Big Endian / MSB First as specified)
        value = int.from_bytes(chunk[1:5], byteorder='big')
        
        # Map indices to the appropriate channel array
        if 0x00 <= index <= 0x03:
            storage["Channel_1"][index] = value
        elif 0x04 <= index <= 0x07:
            storage["Channel_2"][index - 4] = value
        elif 0x08 <= index <= 0x0B:
            storage["Channel_3"][index - 8] = value
        elif 0x0C <= index <= 0x0F:
            storage["Channel_4"][index - 12] = value

    print(f"Success: Parsed packet data into measurement storage.")

def parse_and_store_data(raw_input, data_store):
    """
    Parses a bytes object or string by stripping the command prefix 
    and correcting escape sequences to reach the 128-byte payload.
    """
    #print(f"DEBUG1:{raw_input!r}")
    
    # 1. Convert input to bytes
    if isinstance(raw_input, str):
        # latin-1 preserves byte-value integrity for characters 0-255
        raw_bytes = raw_input.encode('latin-1')
    elif isinstance(raw_input, bytes):
        raw_bytes = raw_input
    else:
        print("Error: Input must be a bytes object or string.")
        return       
    #print(f"DEBUG2:{raw_bytes!r}")

    # 2. Extract Data after the '=' prefix
    if b'=' in raw_bytes:
        data_payload = raw_bytes.split(b'=', 1)[1]
    else:
        data_payload = raw_bytes
    
    #print(f"DEBUG3: {data_payload!r}")

    # 3. Fix literal escaping (e.g., b'\\x00' -> b'\x00')
    try:
        if b'\\' in data_payload:
            data_payload = codecs.escape_decode(data_payload)[0]
    except Exception as e:
        print(f"Warning during unescape: {e}")

    # 4. Final Alignment and Validation
    actual_len = len(data_payload)
    if actual_len < 128:
        data_payload = data_payload.ljust(128, b'\x00')
    elif actual_len > 128:
        data_payload = data_payload[:128]
    #print(f"DEBUG4: {data_payload!r}")
    try:
        # Helper to decode ASCII and strip null/whitespace
        def decode_text(b_slice):
            return b_slice.decode('ascii', errors='ignore').split('\x00')[0].strip()

        # Helper for LSB-first 4-byte integers (Little Endian)
        def to_int_lsb(b_slice):
            return int.from_bytes(b_slice, byteorder='little')

        # --- Adjusted Parsing Alignment ---
        
        # 0 to 19: Reserved
        data_store["Reserved_1"] = data_payload[0:19].hex().upper()
        
        # 19 to 29: Batch (10 bytes)
        data_store["Batch"] = decode_text(data_payload[19:29])
        
        # 29 to 37: Calibration Date (8 bytes)
        data_store["Calibration_Date"] = decode_text(data_payload[29:37])
        
        # 37 to 53: 4 Channels @ 4 bytes each
        data_store["Ch1_Calibration"] = to_int_lsb(data_payload[37:41])
        data_store["Ch2_Calibration"] = to_int_lsb(data_payload[41:45])
        data_store["Ch3_Calibration"] = to_int_lsb(data_payload[45:49])
        data_store["Ch4_Calibration"] = to_int_lsb(data_payload[49:53])
        
        # 53 to 59: MAC Address (6 bytes)
        mac_bytes = data_payload[53:59]
        data_store["MAC_Address"] = ":".join(f"{b:02x}" for b in mac_bytes).upper()
        
        # 59 to 126: Reserved
        data_store["Reserved_2"] = data_payload[59:126].hex().upper()
        
        # 126 to 128: Checksum
        data_store["Checksum"] = data_payload[126:128].hex().upper()
        
        data_store["status"] = "parsed_successfully"
        print(f"Success: Parsed {len(data_payload)} bytes using adjusted offsets.")

    except Exception as e:
        data_store["status"] = "error_parsing"
        print(f"Error during parsing: {e}")

# ----------------------------------------------------------------------
# UDP helpers
# ----------------------------------------------------------------------
def udp_send(sock: socket.socket, payload: bytes, addr):
    """Send a UDP packet."""
    sock.sendto(payload, addr)


def udp_recv(sock: socket.socket, timeout: float = 2.0) -> bytes:
    """Receive a UDP packet; return empty bytes on timeout."""
    sock.settimeout(timeout)
    try:
        data, _ = sock.recvfrom(4096)
        return data
    except socket.timeout:
        return b""

# ----------------------------------------------------------------------
# Keep‑alive thread (0x34) – required every ≤ 15 s
# ----------------------------------------------------------------------
def start_keep_alive(sock: socket.socket, dest):
    """Continuously send 0x34 (keep‑alive) every ~9 s."""
    def loop():
        while True:
            udp_send(sock, b"\x34", dest)   # 0x34 = Keep‑alive
            time.sleep(9)                  # a little under 10 s
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    return t

# ----------------------------------------------------------------------
# Lock the device (ASCII "lock") and interpret the reply
# ----------------------------------------------------------------------
def lock_device(sock: socket.socket, dest) -> bool:
    LOCK_CMD = b"lock"                 # ASCII lock command per the manual
    udp_send(sock, LOCK_CMD, dest)

    reply = udp_recv(sock, timeout=2.0)
    if not reply:
        print("⚠️  No reply to lock request – proceeding anyway.")
        return False

    txt = reply.decode(errors="ignore").lower()
    if "lock success" in txt:
        if "already locked" in txt:
            print("ℹ️  Device already locked to this machine.")
        else:
            print("✅  Lock acquired successfully.")
        return True
    else:
        print(f"⚠️  Lock request failed / unexpected reply: {reply!r}")
        return False

# ----------------------------------------------------------------------
# Send the “read_EEPROM” command (0x32 )
# ----------------------------------------------------------------------
def read_EEPROM(sock: socket.socket, dest):
    """
    0x32 = read_EEPROM
    """
    START_CMD = b'\x32'
    udp_send(sock, START_CMD, dest)

    # Optional diagnostic reply (usually “Converting”)
    resp = udp_recv(sock, timeout=1.0)
    if resp:
        temp = resp.decode(errors="ignore").lower()
        # 2. Parse and store into our variables
        
        if "eeprom=" in temp:
            print("✅  read_EEPROM started – done")
        else:
            print(f"ℹ️  Unexpected read_EEPROM reply: {resp!r}")
    else:
        print("⚠️  No immediate reply to read_EEPROM command (still OK).")

    parse_and_store_data(resp, data_variables)
    # 3. Display results
    print("\n--- Parsed EEPROM data ---")
    for key, value in data_variables.items():
        if key != "status":
            print(f"{key.replace('_', ' '):<20}: {value}")

# ----------------------------------------------------------------------
# Send the “mains rejection” command (0x30, 0x00 )
# ----------------------------------------------------------------------
def mains_rejection(sock: socket.socket, dest):
    """
    0x30 = mains_rejection command
    0x00 = For 50Hz
    """
    START_CMD = b'\x30\x00'
    udp_send(sock, START_CMD, dest)

    # Optional diagnostic reply (usually “Converting”)
    resp = udp_recv(sock, timeout=1.0)
    if resp:
        txt = resp.decode(errors="ignore").lower()
        if "" in txt:
            print("✅  mains rejection started OK")
        else:
            print(f"ℹ️  Unexpected mains rejection reply: {resp!r}")
    else:
        print("⚠️  No immediate reply to mains rejection command (still OK).")

# ----------------------------------------------------------------------
# Send the “start converting” command (0x31 0x0F)
# ----------------------------------------------------------------------
def start_converting(sock: socket.socket, dest):
    """
    0x31 = start converting
    0x0F = enable channels 1‑4 (bits 0‑3 = 1) and gain ×1 (bits 4‑7 = 0)
    """
    START_CMD = b'\x31\x0F'
    udp_send(sock, START_CMD, dest)

    # Optional diagnostic reply (usually “Converting”)
    resp = udp_recv(sock, timeout=1.0)
    if resp:
        txt = resp.decode(errors="ignore").lower()
        if "converting" in txt:
            print("✅  Converter started – data will now stream.")
        else:
            print(f"ℹ️  Unexpected start‑convert reply: {resp!r}")
    else:
        print("⚠️  No immediate reply to start‑convert command (still OK).")


# ----------------------------------------------------------------------
# Main routine – receive raw temperature packets and print °C
# ----------------------------------------------------------------------
def main():

    # --------------------------------------------------------------
    # 0️⃣  Create a UDP socket (bind to any free local port)
    # --------------------------------------------------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", 0))                     # OS picks a free local port

    # --------------------------------------------------------------
    # 1️⃣  Lock the device
    # --------------------------------------------------------------
    have_lock = lock_device(sock, DEVICE_ADDR)

    # --------------------------------------------------------------
    # 2️⃣  Set read_EEPROM
    # --------------------------------------------------------------
    read_EEPROM(sock, DEVICE_ADDR)

    # --------------------------------------------------------------
    # 2️⃣  Set mains_rejection
    # --------------------------------------------------------------
    mains_rejection(sock, DEVICE_ADDR)

    # --------------------------------------------------------------
    # 2️⃣  Tell the logger to start converting (stream data)
    # --------------------------------------------------------------
    start_converting(sock, DEVICE_ADDR)

    # --------------------------------------------------------------
    # 3️⃣  Start keep‑alive (required whether we own the lock or not)
    # --------------------------------------------------------------
    start_keep_alive(sock, DEVICE_ADDR)
    print(f"✅ Keep‑alive started (0x34 every ~9 s) → {DEVICE_IP}:{DEVICE_PORT}")

    print("\nWaiting for streamed data… (Ctrl‑C to stop)\n")

    # --------------------------------------------------------------
    # 4️⃣  Receive and decode measurement packets
    # --------------------------------------------------------------
    try:
        while True:
            pkt = udp_recv(sock, timeout=3.0)
            if not pkt:
                continue

            # --------------------------------------------------
            # a) Discard any textual packets (Lock replies, Alive, etc.)
            # --------------------------------------------------
            if pkt.startswith(b'PT104') or pkt.startswith(b'Lock') or pkt.startswith(b'Alive'):
                continue

            # --------------------------------------------------
            # b) Binary measurement data: 5 bytes per channel
            # --------------------------------------------------
            if len(pkt) < 20:          # 4 channels × 5 bytes = 20 bytes
                # Incomplete packet – ignore it.
                continue
            
            parse_pkt_data(pkt, measurement_data)  
            # Display raw channel data
            # print("\n--- Measurement Packet Results ---")
            # for channel, vals in measurement_data.items():
            #     print(f"{channel:<20}: {vals}")

            # Calculate Results
            res_results = calculate_resistances(data_variables, measurement_data)
            print("\n--- Calculated Resistances (Ohms) ---")
            for channel, res in res_results.items():
                if res is not None:
                    print(f"{channel:<20}: {res:.6f} Ohms")
                else:
                    print(f"{channel:<20}: Data Missing")

            # Convert to Temperature
            temperatures = get_channel_temperatures(res_results)
            print("\n--- Temperature Results (Celsius) ---")
            for ch, temp in temperatures.items():
                if temp is not None:
                    print(f"{ch:<20}: {temp:.2f} °C")
                else:
                    print(f"{ch:<20}: Invalid Data")
            # The logger up dates
            # roughly every 720 ms per active channel.
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    finally:
        # ----------------------------------------------------------
        # Optional: cleanly unlock the device if we own the lock
        # ----------------------------------------------------------
        if have_lock:
            udp_send(sock, b"lock", DEVICE_ADDR)   # sending “lock” again releases it
            print("🔓 Unlock command sent.")
        sock.close()

if __name__ == "__main__":
    main()