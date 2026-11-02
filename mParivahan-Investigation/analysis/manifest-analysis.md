# Android Manifest Analysis — mParivahan

## 1. Objective

This stage examines the Android manifest of the suspected mParivahan APK to identify application metadata, requested permissions, application components, exported component declarations and security-relevant configuration.

The analysis focuses on the original Stage 1 APK.

## 2. Evidence Information

| Attribute | Value |
|---|---|
| Evidence filename | `mParivahan__(4).apk` |
| Package name | `com.wehfejg.asdfhew` |
| Application label | mParivahan |
| Version name | 1.0 |
| Version code | 1 |
| Minimum SDK | 24 |
| Target SDK | 34 |
| Compile SDK | 34 |
| Manifest location | `AndroidManifest.xml` |

## 3. Analysis Methodology

The binary Android manifest was examined using Android SDK Build Tools.

Command:

```bash
aapt2 dump xmltree \
  --file AndroidManifest.xml \
  "/home/white_evil/Desktop/mParivahan__(4).apk"
```

The command successfully extracted the important manifest entries.

### Parser observations

The extraction produced the following warning:

```text
warn: unexpected chunk type 0.
```

The output also contained unusual `android:name=false` entries and malformed-looking structures.

These entries were not treated as genuine manifest attributes without independent verification.

The manifest information documented below is based on the identifiable package metadata, permission declarations and component entries in the AAPT2 output.

## 4. Application Metadata

The manifest identifies the application as:

```text
Package: com.wehfejg.asdfhew
Label: mParivahan
Version: 1.0
Version Code: 1
Minimum SDK: 24
Target SDK: 34
Compile SDK: 34
```

**Observation:**

The application targets Android API level 34 and supports a minimum API level of 24 according to its declared SDK configuration.

## 5. Requested Permissions

The following permissions were identified in the manifest:

| Permission | Declared purpose |
|---|---|
| `android.permission.REQUEST_INSTALL_PACKAGES` | Allows the application to request installation of APK packages. |
| `android.permission.INTERNET` | Allows network communication. |
| `android.permission.ACCESS_NETWORK_STATE` | Allows access to network connectivity information. |
| `android.permission.CHANGE_WIFI_STATE` | Allows changing Wi-Fi connectivity state. |
| `android.permission.ACCESS_WIFI_STATE` | Allows access to Wi-Fi state information. |
| `android.permission.QUERY_ALL_PACKAGES` | Allows querying installed packages, subject to Android platform restrictions. |
| `com.wehfejg.asdfhew.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION` | Application-defined permission. |

### Custom permission

The application declares a custom permission:

```text
com.wehfejg.asdfhew.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
```

Its protection level was extracted as:

```text
protectionLevel = 0x00000002
```

This corresponds to a signature-level permission.

### Security observations

The combination of package-installation, installed-package querying and network-related permissions warrants further investigation.

These declarations indicate available application capabilities; they do not independently establish malicious behaviour.

The corresponding code must be examined to determine how these capabilities are used.

## 6. Application Configuration

The following application attributes were identified:

| Attribute | Value |
|---|---|
| `allowBackup` | `false` |
| `extractNativeLibs` | `false` |
| `appComponentFactory` | `androidx.core.app.CoreComponentFactory` |

These values represent application configuration and are not independently classified as malicious indicators.

## 7. Application Components

### 7.1 Main Activity

```text
Class: com.wehfejg.asdfhew.MainActivity
Exported: true
Launch Mode: 1 (singleTop)
```

The activity declares the following intent filter:

```text
android.intent.action.MAIN
android.intent.category.LAUNCHER
```

**Observation:**

`MainActivity` is the application's declared launcher activity and is marked as exported.

Its actual functionality, initialization sequence and interaction with other application components require source-code analysis.

### 7.2 VPN Service

```text
Class: com.wehfejg.asdfhew.VpnKillService
Permission: android.permission.BIND_VPN_SERVICE
Exported: false
```

Declared service action:

```text
android.net.VpnService
```

**Observation:**

The application declares a service extending the Android VPN service framework.

The component declaration establishes the presence of VPN-service functionality in the application structure.

Its actual traffic handling, routing, filtering and connection behaviour have not been established by the manifest alone.

### 7.3 Broadcast Receiver

```text
Class: com.wehfejg.asdfhew.RcvJbrzn
Exported: true
```

Declared intent filter actions:

```text
android.intent.action.PACKAGE_ADDED
android.intent.action.MY_PACKAGE_REPLACED
```

Declared data scheme:

```text
package
```

**Observation:**

The receiver is configured to receive package-related broadcast events.

Its implementation must be examined to establish how it processes these events and whether it performs any additional operations.

## 8. Source-Code Correlation

JADX 1.5.3 was used to generate Java source files for the application components.

The following files were generated:

```text
MainActivity.java
VpnKillService.java
RcvJbrzn.java
```

However, JADX reported resource parsing errors and multiple DEX instruction decoding failures.

The generated files contain class declarations and method signatures, but several method bodies could not be recovered.

Consequently:

- Manifest declarations are treated as structural evidence.
- Method names are not treated as proof of implementation behaviour.
- JADX-generated exception placeholders are not treated as original application instructions.
- Behavioural conclusions require independently recovered code or corroborating evidence.

## 9. Security-Relevant Findings

The following items were identified as investigation leads:

| ID | Observation | Assessment |
|---|---|---|
| MF-01 | `REQUEST_INSTALL_PACKAGES` permission | Investigate APK installation-related code. |
| MF-02 | `QUERY_ALL_PACKAGES` permission | Investigate installed-package enumeration. |
| MF-03 | VPN service declaration | Investigate VPN configuration and traffic handling. |
| MF-04 | Exported package-related broadcast receiver | Investigate broadcast handling and triggered operations. |
| MF-05 | Network and Wi-Fi permissions | Investigate network-related functionality. |

These observations are not independent proof of malicious activity.

## 10. Limitations

The manifest extraction generated an unexpected chunk warning and unusual parser output.

JADX also reported:

```text
Failed to parse 'resources.pb'/'.arsc' file
```

and multiple DEX instruction decoding errors.

Although the application component source files were generated, their method implementations were not consistently recoverable.

The current manifest analysis does not establish:

- Successful installation of another APK.
- Actual VPN traffic interception or redirection.
- Successful execution of receiver-triggered operations.
- Actual collection or transmission of device information.
- Successful network communication with any external service.

## 11. Conclusion

The manifest examination identified several security-relevant capabilities in the original mParivahan APK, including package-installation requests, installed-package querying, network access, a declared VPN service and an exported broadcast receiver.

These declarations provide useful leads for subsequent static investigation.

The manifest alone does not establish the application's runtime behaviour or prove that any of these capabilities were used maliciously.

Further investigation should correlate these declarations with the recovered DEX information, application code and previously collected Stage 1 and Stage 2 evidence.

**Analysis status:** Manifest extraction completed. Behavioural verification remains part of the broader static investigation.