# Security Policy

Pico Technology Ltd is committed to the security of its products and the
software it distributes. This repository contains example code that supports the use of Pico Technology products this includes but is not limited to; PicoScope® oscilloscopes, PicoLog® data loggers, PicoSource™ Agile Synthesizer, PicoVNA® Vector Network Analyzers.

This policy describes how to report a security vulnerability and how we handle
vulnerabilities, in line with our obligations as a manufacturer under the EU
Cyber Resilience Act (Regulation (EU) 2024/2847) and coordinated vulnerability
disclosure good practice (ISO/IEC 29147 and 30111).

## Reporting a vulnerability

Please report suspected security vulnerabilities **privately** — do not open a
public GitHub issue for a security problem.

Preferred channel:

- **GitHub private vulnerability reporting** — use the *"Report a vulnerability"*
  button under this repository's **Security** tab.

Alternative channel:

- **Email:** support@picotech.com — please encrypt sensitive details where
  possible.

When reporting, please include:

- the affected file(s), example project and driver (e.g. `ps6000a`, `psospa`);
- the version / commit hash you tested against;
- a description of the issue and its potential impact;
- steps to reproduce, and a proof of concept if available;
- any suggested remediation.

## Our commitment (response targets)

| Stage | Target |
| --- | --- |
| Acknowledge receipt | within 5 working days |
| Initial assessment / triage | within 10 working days |
| Status updates | at least every 30 days until resolution |
| Fix or mitigation for confirmed issues | without undue delay, prioritised by severity |

We follow a coordinated disclosure approach: we ask that you give us a
reasonable opportunity to remediate before any public disclosure, and we will
credit reporters who wish to be acknowledged.

## Supported versions

Security fixes are applied to the `master` branch. We recommend always building
from the latest `master`. Older tags/commits are not maintained.

| Version | Supported |
| --- | --- |
| Latest `master` | ✅ |
| Older commits / tags | ❌ |

## Support period

In line with CRA Article 13, the security support period for this example code
is **the supported lifetime of the associated PicoSDK release**.
During this period, identified vulnerabilities affecting the examples will be
addressed on `master`. This period must be confirmed and published by Pico's
compliance function.

## Scope

**In scope:** vulnerabilities in the example source code in this repository
(including the shared helpers under `shared/`).

**Out of scope / report elsewhere:**

- The PicoSDK drivers, runtime libraries and firmware (`libps*`, device
  firmware) — these are separate products; see the "Pico Technology Ltd Coordinated Vulnerability Disclosure Policy" section on the https://www.picotech.com/about/legal-information page for more information.
- Any Third-party libraries vendored here — we will forward upstream
  where appropriate; see [SBOM](sbom/).
- Vulnerabilities requiring physical access or a already-compromised host.

## Third-party components

A Software Bill of Materials (SBOM) maybe located in this repository [`sbom/`], if not this can be provided on request. (email: support@picotech.com).
