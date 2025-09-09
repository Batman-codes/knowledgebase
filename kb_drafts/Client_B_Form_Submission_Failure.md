# Client B Form Submission Failure
**status:approved**
**Problem**  
Client B experiences a failure during form submission, where the form hangs after clicking Submit.

**Environment**  
- Submission endpoint: /submitForm

**Steps**  
1. Attempt to submit the form.
2. Observe the console for any errors.

**Expected**  
The form should submit successfully without hanging.

**Actual**  
- The console displays a "400 Bad Request" error for the /submitForm endpoint.

**Resolution**  
- Identify that the 'participantType' was missing in the payload, which is now mandatory.
- Implement a hotfix to add fallback logic that auto-sets `participantType='General'` if it is missing.
- Retest the form submission.

**Notes**  
- After implementing the fix, form submission works correctly. The Client B team will be informed of the resolution.