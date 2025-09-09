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