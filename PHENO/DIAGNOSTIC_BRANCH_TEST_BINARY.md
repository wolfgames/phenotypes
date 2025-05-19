{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}

PROCEDURE GenerateDiagnosticBranchTestBinary(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditionValue, pathAPassageID, pathBPassageID) {
    // Primary goal: Create a passage that tests binary branching based on a condition
    // Structure: Single passage with condition-based branching to two different paths

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Binary Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateBranchContent() {
        RETURN "Testing binary branching condition"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateBranchContent()
    
    // Create two branch options for true and false conditions
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=ada;" +
                        "ops=BOP:onm=\"If " + conditionVar + " = " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathAPassageID + ";" +
                        "ops=BOP:onm=\"If " + conditionVar + " ≠ " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=ne;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathBPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing binary branching condition"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS pathAPassageID
        VALIDATE slpnPassage CONTAINS pathBPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        VALIDATE slpnPassage CONTAINS "ops=BOP"
    }
    
    ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}
