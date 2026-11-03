# Payload Analysis – mParivahan Android Application

## 1. Objective

This analysis examines the embedded payload contained in the first-stage mParivahan APK, documents the recovery algorithm, and records the recovered second-stage APK's metadata and integrity information.

The objective is to understand the staged application structure and preserve reproducible evidence of the recovery process.

## 2. Evidence Information

| Attribute | Value |
|---|---|
| First-stage APK | `mParivahan__(4).apk` |
| First-stage package | `com.wehfejg.asdfhew` |
| Embedded payload | `assets/dbliqgnjl.dat` |
| Payload recovery script | `decode_payload.py` |
| Recovered artifact | `output/recovered_payload.apk` |
| Second-stage package | `com.messege.mp` |
| Application label | mParivahan |
| Second-stage version | 1.9 |
| Version code | 10 |

## 3. Embedded Payload Identification

The first-stage APK contains an asset named:

`assets/dbliqgnjl.dat`

The existing recovery script identifies this asset as the input to its decoding process.

The script opens the original APK as a ZIP archive and retrieves the specified asset using Python's `zipfile` module.

### Relevant code

```python
APK = Path("original/mParivahan__(4).apk")
OUT = Path("output/recovered_payload.apk")

ASSET = "assets/dbliqgnjl.dat"

with zipfile.ZipFile(APK, "r") as z:
    info = z.getinfo(ASSET)
```

### Logic explanation

- `zipfile.ZipFile()` opens the APK archive.
- `getinfo()` retrieves metadata for the specified embedded asset.
- The script reads the asset directly from the archive.
- The extracted data is processed without modifying the original APK.

## 4. Payload Decoding Algorithm

The recovery script uses a Linear Congruential Generator (LCG)-based XOR transformation.

### Algorithm parameters

| Parameter | Value |
|---|---|
| Initial state | `0x4394d` |
| Multiplier | `0x19660d` |
| Increment | `0x3c6ef35f` |
| State width | 32 bits |
| Keystream byte | Highest 8 bits of updated state |

### Relevant code

```python
STATE = 0x4394d
MULT  = 0x19660d
ADD   = 0x3c6ef35f
```

The script first reads and discards a 16-byte header:

```python
discarded = src.read(0x10)
```

The remaining data is processed in chunks:

```python
buf = bytearray(src.read(0x20000))

if not buf:
    break

for i in range(len(buf)):
    STATE = (STATE * MULT + ADD) & 0xffffffff
    key = (STATE >> 24) & 0xff
    buf[i] ^= key

dst.write(buf)
```

### Logic explanation

1. The first 16 bytes are skipped before decoding.
2. The remaining asset is read in chunks of up to 128 KiB.
3. The LCG updates its state for each byte.
4. The upper eight bits of the updated state form the XOR key byte.
5. Each input byte is XORed with the generated key byte.
6. The transformed bytes are written to the recovered output file.

The state update can be expressed as:

`X(n+1) = (a × X(n) + c) mod 2^32`

The output byte is obtained from the upper eight bits of the updated state.

This is an LCG-based XOR transformation. It should not be described as a proven cryptographic encryption algorithm.

### Forensic significance

The recovery script documents a mechanism for transforming an embedded asset into a separate APK-like artifact. The 16-byte skip and LCG parameters are important for reproducing the recovery process.

## 5. Recovered Second-Stage APK

The recovery process produced:

`output/recovered_payload.apk`

### Recovered APK metadata

| Attribute | Value |
|---|---|
| Application label | mParivahan |
| Package name | `com.messege.mp` |
| Version name | 1.9 |
| Version code | 10 |
| Minimum SDK | 24 |
| Target SDK | 35 |
| Compile SDK | 35 |

The recovered artifact was identified as a ZIP archive and passed the recorded ZIP integrity test.

### SHA-256

```text
53d51811ce4451f0573aa5a4d9b29be2b84546112d9764da29f7780a4d731f6d
```

The SHA-256 value matches the previously recorded recovery hash.

## 6. Second-Stage Permissions

The recovered application's manifest metadata contains several permission declarations relevant to further static analysis.

| Permission category | Examples |
|---|---|
| SMS access and transmission | `READ_SMS`, `RECEIVE_SMS`, `SEND_SMS`, `BROADCAST_SMS` |
| Phone information | `READ_PHONE_STATE`, `READ_PHONE_NUMBERS` |
| Network access | `INTERNET`, `ACCESS_NETWORK_STATE` |
| Wi-Fi management | `ACCESS_WIFI_STATE`, `CHANGE_WIFI_STATE` |
| Background execution | `RECEIVE_BOOT_COMPLETED`, `WAKE_LOCK` |
| Foreground services | `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_DATA_SYNC` |
| Alarm scheduling | `SCHEDULE_EXACT_ALARM`, `USE_EXACT_ALARM` |
| Battery management | `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` |

These permissions indicate declared application capabilities. Their presence alone does not establish that the corresponding operations were executed successfully.

Detailed behaviour is documented separately in the SMS, Firebase, and other analysis reports.

## 7. Signing Certificate Information

The recovered APK's recorded certificate information is:

| Attribute | Value |
|---|---|
| Subject | `CN=editor` |
| Issuer | `CN=editor` |
| Serial number | `231bc320` |
| Signature algorithm | `SHA256withRSA` |
| Public key | RSA 2048-bit |
| SHA-256 fingerprint | `62:15:F0:0B:AA:4B:F1:8B:AB:57:92:FC:79:6B:FC:55:55:91:72:40:F1:4F:7C:7E:67:2D:95:68:88:D7:5C:96` |

The subject and issuer values are identical, indicating a self-issued certificate according to the recorded certificate output.

The certificate information does not establish the identity of the application developer or distributor.

## 8. Tooling and Analysis Limitations

An attempt to decode the recovered APK using Apktool 2.7.0-dirty failed during resource-table parsing.

Recorded error:

```text
Could not decode arsc file
Expected: 0x001c0001, got: 0x00740068
```

This indicates a resource-table parsing failure in the attempted tooling workflow.

However, the recovered APK passed the ZIP integrity test, and package metadata and DEX artifacts were available through other analysis steps.

The Apktool failure must not be interpreted as proof of APK corruption.

## 9. Forensic Findings

1. The first-stage APK contains an embedded asset named `assets/dbliqgnjl.dat`.
2. The existing recovery script applies a 16-byte header skip followed by an LCG-based XOR transformation.
3. The recovery script produces a separate second-stage APK artifact.
4. The recovered artifact identifies itself as package `com.messege.mp`, version 1.9.
5. The recovered APK passed the recorded ZIP integrity test.
6. The recovered APK's SHA-256 matches the earlier recorded recovery hash.
7. Its manifest declares permissions associated with SMS, phone information, networking, and background execution.
8. Apktool could not decode its resource table using the recorded version.

## 10. Conclusion

Static examination of the first-stage APK and its existing recovery artifacts identifies a staged application structure.

An embedded asset is processed using an LCG-based XOR transformation, producing a second-stage APK identified as `com.messege.mp`.

The recovered artifact's hash is consistent with the previously recorded value, and its ZIP archive integrity test completed successfully.

The second-stage manifest declares permissions relevant to SMS handling, phone information access, networking, and background operation. These declarations provide leads for further code-level analysis but do not independently prove execution or successful data collection.

This report documents static recovery and artifact examination. It does not establish successful installation on a device, successful execution, data exfiltration, or financial impact.