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