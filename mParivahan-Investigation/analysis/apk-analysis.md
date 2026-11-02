# APK Initial Triage and Identification

## 1. Objective

The objective of the initial APK triage was to identify the application package, establish its basic file characteristics, calculate its cryptographic hash and extract Android application metadata before proceeding with deeper static analysis.

## 2. Evidence Information

| Attribute | Value |
|---|---|
| Evidence filename | `mParivahan__(4).apk` |
| Evidence location | `/home/white_evil/Desktop/mParivahan__(4).apk` |
| File size | 7.9 MB |
| File format | ZIP-based Android application package |
| SHA-256 | `7aafca5e4619f67015899f26181aad2f2d3d29b4b92532b896e6300309103810` |

## 3. Tools Used

- `ls`: File metadata inspection.
- `file`: File format identification.
- `sha256sum`: Cryptographic hash calculation.
- `aapt`: Android application metadata extraction.

## 4. Analysis Performed

### 4.1 File Identification

The `file` utility identified the supplied APK as a ZIP archive using the DEFLATE compression method.

The file size was approximately 7.9 MB.

### 4.2 Cryptographic Hash Verification

The SHA-256 hash was calculated using `sha256sum`.

The resulting hash matched the SHA-256 value recorded in the previous investigation report.

This establishes consistency with the previously recorded hash.

The original APK was not modified during this triage.

### 4.3 APK Metadata Extraction

The Android Asset Packaging Tool (`aapt`) was used to extract application metadata.

| Attribute | Observed value |
|---|---|
| Application label | mParivahan |
| Package name | `com.wehfejg.asdfhew` |
| Version name | 1.0 |
| Version code | 1 |
| Minimum SDK | 24 |
| Target SDK | 34 |
| Compile SDK | 34 |
| Main activity | `com.wehfejg.asdfhew.MainActivity` |

### 4.4 Initial Permission Observations

The metadata output identified the following requested permissions:

- `REQUEST_INSTALL_PACKAGES`
- `INTERNET`
- `ACCESS_NETWORK_STATE`
- `CHANGE_WIFI_STATE`
- `ACCESS_WIFI_STATE`
- `QUERY_ALL_PACKAGES`
- `com.wehfejg.asdfhew.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

The `REQUEST_INSTALL_PACKAGES` permission is particularly relevant for further investigation because the previous analysis identified an embedded second-stage payload and a package installation mechanism.

The permission itself does not establish that another APK was successfully installed.

The network-related permissions will be examined further during code-level analysis to determine how the application uses network functionality.

### 4.5 APK Internal Structure

An Android APK is a ZIP-based package containing application code, resources, configuration information and potentially additional bundled files.

The following components are relevant to the investigation:

| Component | Purpose |
|---|---|
| `AndroidManifest.xml` | Application metadata, permissions and component declarations |
| `classes.dex` | Compiled Android application code |
| `classes2.dex` and additional DEX files | Additional compiled application code, if present |
| `res/` | Application resources |
| `assets/` | Additional files bundled with the application |
| `resources.arsc` | Compiled Android resource table |
| `META-INF/` | May contain signature-related metadata associated with APK v1 signing |
| `lib/` | Native libraries, if included |

**Investigation status:** The internal archive listing has not yet been examined in this phase. The presence of these components in the supplied mParivahan APK must be verified through archive inspection.

### 4.6 APK Signing Information

APK signing information is important for establishing the application's signing identity and examining its integrity-related metadata.

The investigation will examine:

- APK signing certificate.
- Certificate subject and issuer.
- Certificate validity period.
- Signature scheme information.
- Signing certificate fingerprints.

The presence or absence of `META-INF` files alone is not sufficient to determine whether an APK is signed, since newer APK signing schemes use a signing block outside the ordinary ZIP entries.

**Investigation status:** Signing certificate analysis is pending.

## 5. Preliminary Assessment

The initial triage established the identity and basic technical characteristics of the supplied APK.

The application requests package-installation and network-related permissions. These observations provide leads for subsequent manifest and code-level analysis.

The package identifier, application label and main activity have been identified.

No malicious functionality is concluded from metadata alone.

## 6. Limitations

- The initial `aapt` output contained an unknown resource-table chunk warning.
- Permission declarations do not establish that the corresponding functionality was executed.
- The internal archive structure has not yet been independently documented.
- APK signing and certificate details have not yet been assessed.
- No runtime behaviour was examined.
- The previous SHA-256 record establishes consistency but does not independently establish the APK's source or authenticity.

## 7. Next Investigation Stage

Proceed with APK archive inspection and detailed AndroidManifest.xml analysis.

The next stage will examine:

1. Internal APK directory structure.
2. DEX files and compiled application code.
3. Embedded assets and potential payloads.
4. `META-INF` and APK signing information.
5. AndroidManifest.xml permissions and application components.
6. Exported components and intent filters.

## 8. Evidence Screenshots

### 8.1 APK File Identification

![APK File Identification](../screenshots/apk-analysis/MP-APK-001-file-identification.png)

### 8.2 SHA-256 Verification

![SHA-256 Verification](../screenshots/apk-analysis/MP-APK-002-sha256-verification.png)

### 8.3 APK Metadata Extraction

![APK Metadata](../screenshots/apk-analysis/MP-APK-003-aapt-metadata.png)