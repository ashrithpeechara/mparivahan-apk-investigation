# mParivahan – Android Malware & Digital Forensics Investigation

**An independent investigation into a suspicious Android application impersonating the Indian mParivahan service.**

![Platform](https://img.shields.io/badge/Platform-Android-green)
![Research](https://img.shields.io/badge/Research-Mobile%20DFIR-blue)
![Analysis](https://img.shields.io/badge/Analysis-Static%20Analysis-orange)
![Status](https://img.shields.io/badge/Investigation-Ongoing-yellow)

---

## Investigation Overview

This repository documents the technical investigation of a suspicious Android application distributed as `mParivahan__(4).apk`.

The investigation identified a staged Android application architecture, an embedded second-stage APK, a deceptive vehicle-service interface, UPI PIN collection logic, SMS-related monitoring and remote-command capabilities, Firebase backend integration, Telegram notification functionality, and a custom Android VPN service.

The primary objective was to investigate the application's internal architecture, identify suspicious functionality, examine associated backend infrastructure, extract indicators of compromise, and reconstruct its potential attack chain.

The investigation combines Android application analysis, reverse engineering, mobile malware research, backend artefact examination, and digital forensic documentation.

**Investigation classification:** Android malware analysis and suspected credential-harvesting investigation.

**Report status:** Interim findings – ongoing investigation.

---

## Investigation Analytics

The following statistics represent artefacts and records documented during the investigation.

### Application Analysis

| Metric | Result |
|---|---:|
| Original APK examined | 1 |
| Recovered second-stage APK | 1 |
| Application stages identified | 2 |
| Package identifiers identified | 2 |
| HTML interface resources identified | 7 |
| DEX artifacts with recorded hashes | 1 |
| APK SHA-256 hashes recorded | 2 |
| Total recorded SHA-256 hashes | 3 |

### Backend Dataset Analysis

A supplied Firebase-related JSON capture was parsed and examined.

| Dataset Metric | Count |
|---|---:|
| Top-level device records | 599 |
| SIM entries | 616 |
| Action entries | 671 |
| Records containing phone-number fields | 434 |
| Records containing UPI-PIN-like fields | 61 |
| Records containing FCM-token fields | 571 |
| Records containing network-IP fields | 509 |

**Important:** These are counts from the supplied dataset, not confirmed victim counts. The provenance, authorization context, authenticity, and historical origin of the dataset have not been independently established.

The presence of a field does not prove that it contains valid information or that the application successfully collected or transmitted it.

### Infrastructure Analysis

| Finding | Result |
|---|---|
| Firebase project identified | `yeh-u-880f4` |
| Firebase database hostname | Identified |
| Telegram API integration | Identified in code |
| Firebase canary request | HTTP 401 |
| Custom Android VPN service | Identified |
| Confirmed remote VPN tunnel | Not established |
| Confirmed successful Telegram delivery | Not established |

---

## Application Identification

**Original sample**

| Attribute | Value |
|---|---|
| Filename | `mParivahan__(4).apk` |
| Stage-one package | `com.wehfejg.asdfhew` |
| Stage-one main activity | `com.wehfejg.asdfhew.MainActivity` |
| Embedded payload | `assets/dbliqgnjl.dat` |
| Stage-two package | `com.messege.mp` |
| Stage-two version | `1.9` |
| Stage-two version code | `10` |
| Application label | `mParivahan` |
| Target SDK | `35` |
| Minimum SDK | `24` |

The first-stage application uses a WebView-based installer interface and contains an embedded payload that is decoded using an XOR/LCG-style routine.

The recovered second-stage application is installed through Android's `PackageInstaller` workflow.

This indicates a staged installation architecture rather than a single self-contained application.

---

## Cryptographic Evidence

The following SHA-256 values were recorded in the investigation report.

| Evidence Artifact | SHA-256 |
|---|---|
| Original APK | `7aafca5e4619f67015899f26181aad2f2d3d29b4b92532b896e6300309103810` |
| Stage-two APK | `53d51811ce4451f0573aa5a4d9b29be2b84546112d9764da29f7780a4d731f6d` |
| Stage-two DEX | `3a32aa441a3ee65e9c74687f845481d7a44f5d7284de44b96977eb1b95c4b858` |

These hashes are reproduced from existing investigation notes and must be recalculated against the preserved evidence before formal submission.

---

## Key Technical Findings

### 1. Staged APK Installation

The first-stage APK contains an embedded payload named `assets/dbliqgnjl.dat`.

The reviewed implementation includes:

- Embedded payload decoding.
- XOR/LCG-style decoding logic.
- WebView-based installer presentation.
- Android PackageInstaller integration.
- Secondary application deployment.

**Assessment:** Staged APK delivery capability identified through static code analysis.

### 2. Deceptive Vehicle-Service Interface

The second-stage APK contains seven identified HTML resources:

- `index.html`
- `method.html`
- `paytm.html`
- `pin.html`
- `final.html`
- `loading.html`
- `error.html`

The interface imitates a vehicle-service and payment workflow.

The observed resource logic includes:

- Mobile number and vehicle number input.
- A simulated ₹1 registration fee.
- UPI payment-method selection.
- A simulated six-digit UPI PIN keypad.
- A Firebase field named `upiPin`.
- A deliberately displayed server-error state.
- A subsequent PIN-entry opportunity.

**Assessment:** Strong evidence of a deceptive interface designed to solicit UPI PIN information. Successful credential theft has not been independently confirmed.

### 3. SMS Monitoring and Remote Commands

The reviewed application code references:

- `READ_SMS`
- `RECEIVE_SMS`
- `SEND_SMS`
- `CALL_PHONE`
- `READ_PHONE_STATE`
- `RECEIVE_BOOT_COMPLETED`
- `INTERNET`

Relevant code identifiers include:

- `handleSendSmsCommand`
- `pullPendingSendSms`
- `acknowledgeSendSms`
- `applyForwardSmsFromAdmin`
- `SmsHelper.sendSmsWithRetry`

Relevant backend paths include:

- `/actions/forwardSms`
- `/sendMessage`
- `/sendSms`

**Assessment:** SMS processing, forwarding and remote-command capabilities identified in static analysis. Successful SMS exfiltration or remote command execution is not established.

### 4. Device Profiling

The method `proceedWithServiceLogic()` references the collection or preparation of:

- Android ID.
- Device model.
- Android version and SDK.
- Root-status information.
- Storage information.
- CPU architecture.
- Carrier and phone-number fields.
- Battery information.
- SIM information.
- Network/public IP information.
- Device profile information.

The implementation also references boot-completion handling, foreground services, wake locks and background communication helpers.

**Assessment:** Device profiling and background-operation capabilities identified. Actual collection and transmission require further validation.

### 5. Firebase Backend Investigation

The identified Firebase Realtime Database hostname is:

`yeh-u-880f4-default-rtdb.firebaseio.com`

The application references device registration, device status, SMS records, notifications and remote-command-related database paths.

Important fields include:

- `devices`
- `deviceMessages`
- `actions`
- `ping`
- `pingAck`
- `fcmToken`
- `deviceModel`
- `phoneNumber`
- `simCards`
- `networkIp`
- `isOnline`
- `upiPin`

The supplied Firebase dataset was parsed into 599 top-level device records, 616 SIM entries and 671 action entries.

A subsequent recorded request to `/vapt-canary.json` returned HTTP 401 Unauthorized with the response:

`{"error":"Permission denied"}`

**Assessment:** Firebase backend integration identified. Potential backend exposure remains unconfirmed because the original dataset's provenance and access-control context are unresolved.

### 6. Telegram Integration

The application references Telegram Bot API functionality through:

`https://api.telegram.org/bot<TOKEN>/sendMessage`

The reviewed code is designed to send selected device/SMS-related information through Telegram when configured.

**Assessment:** Telegram notification capability identified. Successful message delivery has not been independently established.

### 7. Android VPN Service

The first-stage implementation contains a custom Android VPN service configuration.

Recorded configuration includes:

| Parameter | Value |
|---|---|
| IPv4 route | `0.0.0.0/0` |
| DNS address | `10.0.0.1` |
| IPv6 address | `fd00::2` |
| Application filtering | Present |

**Assessment:** Custom VPN functionality identified. The remote VPN endpoint, tunnel protocol and successful traffic forwarding remain unverified.

---

## Reconstructed Attack Chain

The following represents a hypothesized attack chain derived from static evidence.

1. Distribution of a deceptive mParivahan-themed Android APK.
2. Installation of the first-stage application.
3. Presentation of an installer/updater-like interface.
4. Decoding and deployment of the embedded second-stage APK.
5. Presentation of a fake vehicle-service and payment workflow.
6. Solicitation of mobile, vehicle and UPI PIN information.
7. Potential collection of device and SIM information.
8. Potential SMS monitoring and remote-command processing.
9. Firebase backend integration for device records and command coordination.
10. Potential Telegram-based notification or information transfer.

This is a reconstructed capability chain, not a confirmed execution timeline.

---

## Investigation Scope and Coverage

| Investigation Domain | Current Assessment |
|---|---|
| Original APK identification | Examined |
| APK integrity metadata | Hashes recorded |
| Stage-one architecture | Examined |
| Embedded payload recovery | Completed |
| Stage-two identification | Examined |
| HTML resource analysis | Examined |
| UPI PIN collection logic | Identified |
| SMS-related functionality | Identified |
| Device profiling logic | Identified |
| Firebase integration | Identified |
| Supplied Firebase dataset parsing | Completed |
| Firebase canary validation | Request denied |
| Telegram integration | Identified |
| Android VPN implementation | Identified |
| Successful malicious execution | Not established |
| Confirmed victim attribution | Not established |
| Financial loss verification | Not established |

---

## Evidence Integrity and Limitations

The investigation follows an evidence-oriented approach:

- Preserve original application samples.
- Record SHA-256 hashes.
- Maintain a distinction between original evidence and extracted artefacts.
- Document observed resources, code references and backend indicators.
- Redact credentials, personal information and sensitive backend records.
- Avoid presenting static code capabilities as confirmed execution.
- Preserve the acquisition context and timestamps of supporting evidence.

The investigation does not establish:

- A verified number of compromised victims.
- Successful UPI PIN theft.
- Successful SMS exfiltration.
- Confirmed financial transactions.
- Confirmed Firebase public exposure.
- Successful Telegram information delivery.
- A functioning remote VPN tunnel.
- Attribution to a particular individual or malware family.

---

## MITRE ATT&CK

Potential ATT&CK Mobile technique mappings are maintained as investigative hypotheses.

Mappings must be validated against the actual implementation and current MITRE ATT&CK Mobile documentation before being treated as confirmed techniques.

---

## Research Conclusion

The investigation identified a staged Android application containing a deceptive vehicle-service interface and multiple suspicious capabilities.

The strongest findings concern the UPI PIN collection logic, embedded secondary application, SMS-related functionality, device profiling and Firebase integration.

The supplied backend dataset provides additional investigative leads, including 599 top-level device records and 671 action entries. However, dataset provenance and authorization remain unresolved.

The application also contains Telegram integration and a custom VPN service, although successful external communication and tunnelling have not been independently established.

The investigation remains ongoing, with further validation required to establish operational behaviour, backend access conditions and the complete scope of potential impact.

---

## Disclaimer

This repository is maintained for educational, cybersecurity research and digital forensic investigation purposes.

The analysis concerns a suspicious APK distributed under the mParivahan name. It does not establish that the legitimate mParivahan application or its developers are responsible for the behaviour identified in this sample.

No original APK samples, private credentials, unredacted personal information or sensitive victim records are intentionally published here.

All analysis must be conducted in a controlled environment and in accordance with applicable laws and authorization requirements.

**Research Area:** Android Malware Analysis | Mobile Digital Forensics | DFIR

**Investigation Status:** Ongoing

*Evidence-driven research. Reproducible analysis. Responsible disclosure.*
