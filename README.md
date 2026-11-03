# mParivahan APK Investigation

<p align="center">
  <img src="https://img.shields.io/badge/Investigation-Android%20Malware%20Analysis-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Analysis-Static-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Android-green?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-yellow?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Forensics-DFIR-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Research%20Documentation-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Dynamic%20Analysis-Not%20Performed-lightgrey?style=flat-square" />
</p>

**Project:** Static Security Analysis of a Suspicious Android Application  
**Investigation type:** Android APK Analysis | Malware Research | Digital Forensics  
**Analysis approach:** Static analysis  
**Dynamic analysis:** Not performed  
**Status:** Static investigation documentation

---

## 1. Overview

This repository documents the static investigation of an Android application distributed under the name **mParivahan**.

The investigation identified a multi-stage APK structure, an embedded secondary APK payload, payment-related PIN collection functionality, SMS-related capabilities, Telegram notification functionality, Firebase backend integration and an Android VPN service.

The objective is to understand the application's architecture, identify potentially harmful capabilities, preserve technical evidence and document findings with appropriate confidence levels.

The investigation distinguishes between:

- Behaviour directly demonstrated by recovered application code.
- Configuration values and indicators identified during static analysis.
- Observations from supplied investigative material.
- Behaviour that remains unverified without runtime evidence.

**Important:** The presence of a capability in application code does not automatically prove that it was successfully executed on a victim device.

## 2. Investigation Scope

The investigation covers:

1. APK identification and integrity verification.
2. Android manifest analysis.
3. Embedded payload extraction and examination.
4. UPI PIN collection functionality.
5. SMS-related functionality and remote command processing.
6. Telegram notification functionality.
7. VPN service implementation.
8. Firebase backend integration.
9. Indicator identification and classification.

The investigation was conducted through static inspection of APK contents, DEX instructions, manifest information, HTML/JavaScript resources and supplied investigative material.

Dynamic execution, live command execution, network interception and production-backend testing are outside the scope of this investigation.

## 3. Repository Structure

```text
mParivahan-Investigation/
│
├── README.md
│
├── analysis/
│   ├── apk-analysis.md
│   ├── manifest-analysis.md
│   ├── payload-analysis.md
│   ├── upi-analysis.md
│   ├── sms-analysis.md
│   ├── firebase-analysis.md
│   ├── telegram-analysis.md
│   └── vpn-analysis.md
│
├── ioc/
│   └── indicators.csv
│
└── scripts/
    ├── hash_verification.py
    └── analysis-scripts.py
```

Each analysis document covers a specific component of the investigation.

## 4. APK Identification

### 4.1 Original APK

| Attribute | Value |
|---|---|
| Application label | mParivahan |
| Package name | `com.wehfejg.asdfhew` |
| Version | 1.0 |
| Version code | 1 |
| Minimum SDK | 24 |
| Target SDK | 34 |
| Main activity | `com.wehfejg.asdfhew.MainActivity` |
| Embedded payload | `assets/dbliqgnjl.dat` |
| SHA-256 | `7aafca5e4619f67015899f26181aad2f2d3d29b4b92532b896e6300309103810` |

### 4.2 Recovered Second-Stage APK

| Attribute | Value |
|---|---|
| Application label | mParivahan |
| Package name | `com.messege.mp` |
| Version | 1.9 |
| Version code | 10 |
| Minimum SDK | 24 |
| Target SDK | 35 |
| Compile SDK | 35 |
| SHA-256 | `53d51811ce4451f0573aa5a4d9b29be2b84546112d9764da29f7780a4d731f6d` |

The second-stage APK was recovered from the embedded payload using the identified decoding routine.

The recovered APK passed ZIP integrity validation. This confirms archive readability, not the independent correctness of every decoding operation.

### 4.3 DEX Identification

The recovered second-stage DEX SHA-256 is:

```text
3a32aa441a3ee65e9c74687f845481d7a44f5d7284de44b96977eb1b95c4b858
```

### 4.4 Signing Certificate

| Attribute | Value |
|---|---|
| Subject | CN=editor |
| Issuer | CN=editor |
| Serial number | 231bc320 |
| Signature algorithm | SHA256withRSA |
| Key size | RSA 2048 |
| SHA-256 fingerprint | `62:15:F0:0B:AA:4B:F1:8B:AB:57:92:FC:79:6B:FC:55:55:91:72:40:F1:4F:7C:7E:67:2D:95:68:88:D7:5C:96` |

The matching subject and issuer indicate a self-issued certificate. The certificate does not establish the identity of the developer.

## 5. Key Findings

### 5.1 Multi-stage APK structure

The original APK contains an embedded payload at:

```text
assets/dbliqgnjl.dat
```

The investigation recovered a second-stage APK with a different package identifier and application version.

This establishes a multi-stage application structure.

### 5.2 UPI PIN collection

The second-stage application contains HTML-based payment pages and a custom PIN-entry interface.

The recovered JavaScript:

- Implements masked PIN input.
- Supports four- and six-digit PIN entry.
- Contains automatic and manual submission behaviour.
- Attempts to submit a `upiPin` field to a device-specific Firebase record.
- Presents a subsequent payment-success interface.

The recovered code establishes attempted PIN submission functionality. Successful storage or use of the submitted PIN has not been independently established.

### 5.3 SMS functionality

The application contains incoming SMS notification and remote SMS command-processing functionality.

The recovered implementation includes:

- SMS command retrieval through Firebase.
- Command validation and duplicate checks.
- Destination and message processing.
- SIM selection.
- Android `SmsManager` invocation.
- Retry handling.
- Firebase command acknowledgement.
- Incoming SMS notification construction.

The SMS notification implementation also invokes Telegram messaging functionality.

Static code does not prove successful carrier delivery, execution of a victim-device command or successful forwarding of an SMS to an external recipient.

### 5.4 Telegram integration

The second-stage APK contains a Telegram notification code path associated with incoming SMS processing.

The notification can include:

- Device model.
- SIM-related information.
- SMS sender.
- Incoming SMS content, limited to 500 characters.

The application retrieves bot-token-to-chat mappings and invokes a Telegram message-sending method.

Successful Telegram authentication and message delivery remain unverified.

### 5.5 Firebase backend

The application references:

```text
yeh-u-880f4-default-rtdb.firebaseio.com
```

Firebase is associated with multiple application capabilities, including:

- Device-related records.
- Device telemetry fields.
- Remote SMS command processing.
- SMS command acknowledgement.
- UPI PIN submission.
- Messaging-related data structures.

A supplied Firebase JSON capture contained hundreds of records and several categories of sensitive fields. Its provenance and completeness have not been independently authenticated.

A request to a specific canary path returned HTTP 401 Permission denied. This result applies only to that request and does not establish the security posture of the entire database.

### 5.6 VPN service

The first-stage APK implements an Android `VpnService`.

Recovered instructions configure:

- IPv4 virtual address `10.0.0.2/32`.
- IPv6 virtual address `fd00::2/128`.
- IPv4 default route `0.0.0.0/0`.
- IPv6 default route `::/0`.
- DNS server `10.0.0.1`.

The service attempts to establish a VPN interface and starts a worker thread.

The inspected worker performs a single read from the VPN file descriptor. Continuous packet processing, bidirectional forwarding and a remote VPN endpoint were not demonstrated.

An array-indexing issue was also identified in the application-exclusion configuration, so successful exclusion of all listed applications cannot be claimed.

## 6. Technical Analysis Summary

| Area | Main observation | Assessment |
|---|---|---|
| APK structure | Embedded second-stage APK | Confirmed |
| Manifest | Application components and permissions identified | Confirmed |
| Payload | Encoded embedded payload recovered | Confirmed |
| UPI | PIN-entry and Firebase submission logic | Confirmed |
| SMS | Remote SMS command-processing logic | Confirmed |
| Telegram | Incoming SMS notification and send-method invocation | Confirmed |
| Firebase | Central backend integration | Confirmed |
| VPN | Android VPN interface configuration | Confirmed |
| VPN forwarding | Complete packet-forwarding implementation | Not demonstrated |

## 7. Analysis Documents

| Document | Description |
|---|---|
| [APK Analysis](analysis/apk-analysis.md) | APK identity, hashes, structure and initial examination |
| [Manifest Analysis](analysis/manifest-analysis.md) | Permissions, activities, services and receivers |
| [Payload Analysis](analysis/payload-analysis.md) | Embedded payload decoding and second-stage identification |
| [UPI Analysis](analysis/upi-analysis.md) | Payment interface and PIN submission functionality |
| [SMS Analysis](analysis/sms-analysis.md) | Incoming SMS, remote SMS commands and SMS execution logic |
| [Telegram Analysis](analysis/telegram-analysis.md) | Telegram notification construction and bot integration |
| [VPN Analysis](analysis/vpn-analysis.md) | VPN service, routing, application exclusions and packet handling |
| [Firebase Analysis](analysis/firebase-analysis.md) | Backend paths, device data, remote commands and PIN submission |

## 8. Indicator Register

The structured indicator register is maintained separately:

```text
ioc/indicators.csv
```

It contains technical indicators identified during the investigation, their classifications, evidence sources and confidence levels.

Not every listed indicator is inherently malicious. Shared infrastructure such as Firebase and Telegram must be evaluated in the context of the application's behaviour.

## 9. Tools and Techniques

The investigation used or referenced the following tools and techniques:

| Tool / Technique | Purpose |
|---|---|
| SHA-256 | File integrity identification |
| APKTool | APK resource and manifest examination |
| AAPT / AAPT2 | Android package metadata inspection |
| JADX | DEX decompilation |
| Androguard | Direct DEX instruction inspection |
| Baksmali | Smali-level examination |
| Python | Payload decoding and analysis scripting |
| ZIP integrity checks | Recovered APK archive validation |
| Static HTML/JavaScript inspection | Payment interface and PIN submission analysis |
| Firebase JSON examination | Supplied backend capture analysis |

JADX encountered instruction-decoding errors in several methods. Where necessary, direct DEX instruction inspection was used instead of relying on reconstructed Java source.

## 10. Evidence Handling and Safety

The investigation should preserve:

- Original APK.
- Recovered second-stage APK.
- DEX files.
- Extraction and decoding scripts.
- SHA-256 hashes.
- Analysis logs.
- Supplied backend capture.
- Final investigation reports.

Original evidence should remain unchanged. Analysis should be performed on verified working copies.

Sensitive information must not be published in the public repository, including:

- Actual UPI PIN-like values.
- Phone numbers.
- FCM tokens.
- Telegram bot tokens.
- Telegram chat identifiers.
- Device identifiers.
- Private IP and network records where they could expose sensitive case information.
- Raw Firebase records containing personal data.

## 11. Limitations

This investigation is based primarily on static analysis.

The following remain outside the established evidence:

- Successful execution of all identified capabilities.
- Successful PIN storage.
- Actual financial transactions.
- Successful SMS delivery.
- Successful Telegram message delivery.
- Successful FCM delivery.
- Complete device telemetry transmission.
- Successful VPN traffic forwarding.
- Identity of the application developer or backend operator.
- Authenticity and completeness of all supplied Firebase records.
- Number of affected individuals or devices.

These limitations must be considered when interpreting the findings.

## 12. Overall Assessment

The investigated APK contains multiple capabilities that present potential security and privacy risks.

The strongest findings include:

1. Embedded second-stage APK recovery.
2. UPI PIN-entry functionality with attempted Firebase submission.
3. Remote SMS command-processing functionality.
4. Incoming SMS notification construction and Telegram send-method invocation.
5. Firebase integration across several application features.
6. An Android VPN service with broad routing configuration but no demonstrated complete packet-forwarding path.

The combination of financial-information handling, remote SMS functionality and external messaging integration warrants further investigation.

However, static code evidence must not be presented as proof of successful compromise, financial fraud, data exfiltration or victim impact without additional corroborating evidence.

---

## 13. Disclaimer

This repository is intended for cybersecurity research, malware analysis, digital forensics and defensive security education.

The analysis is based on the artifacts and information available to the investigator. Findings are subject to the stated limitations and should not be treated as a substitute for a complete forensic examination or an independently validated incident investigation.

No sensitive victim information, authentication credentials or private backend records should be published through this repository.
