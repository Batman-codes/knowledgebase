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

---

# Export Feature Failure Resolution
**status:approved**
**Problem**  
Client A is experiencing a failure with the export feature, resulting in a 500 error.

**Environment**  
- Export service

**Steps**  
1. Amit deployed a minor update related to the export service.
2. Amit reviewed the logs and identified a null pointer exception in ExportController.
3. Amit patched the issue and redeployed the export service.

**Expected**  
The export feature should function without errors.

**Actual**  
The export feature was failing with a 500 error prior to the patch.

**Resolution**  
After Amit implemented the patch and redeployed the export service, the issue was resolved, and the export feature is now working correctly.

**Notes**  
- The issue was traced back to a null pointer exception in the code.

---

# Funding Step Failure for Client A
**status:approved**
**Problem**  
Client A faced an issue during the funding step where the process failed with the message: "You cannot proceed with this transaction right now."

**Environment**  
Sandbox environment.

**Steps**  
1. Review logs for the sandbox environment.
2. Identify any timeout issues.
3. Check the retry logic configuration.
4. Adjust the retry logic to allow multiple attempts.

**Expected**  
Funding process should complete successfully after applying the fix.

**Actual**  
Funding process fails initially due to a gateway timeout and incorrect retry logic configuration.

**Resolution**  
- Fix the retry logic configuration to allow more than one attempt.
- After applying the fix, the funding process works and completes successfully.

**Notes**  
- Logs indicated a gateway timeout issue.
- The retry logic was stopping after one attempt due to a wrong configuration.

---

# NullReferenceException in PaymentService for Client C
**status:approved**
**Problem**  
A NullReferenceException was observed in the logs for Client C.

**Environment**  
- Client C's system

**Steps**  
1. Review the logs for Client C.
2. Identify the occurrence of NullReferenceException in PaymentService.

**Expected**  
No exceptions should be present in the logs.

**Actual**  
A NullReferenceException was found in the PaymentService logs.

**Resolution**  
Investigate the cause of the NullReferenceException in PaymentService and implement necessary fixes.

**Notes**  
- Ensure to monitor the logs after applying the fix to confirm resolution.