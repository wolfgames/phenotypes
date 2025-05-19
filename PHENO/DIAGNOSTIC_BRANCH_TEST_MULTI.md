{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}

PROCEDURE GenerateDiagnosticBranchTestMulti(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditions, defaultPassageID) {
    // Primary goal: Create a passage that tests multi-way branching based on different values of a condition
    // Structure: Single passage with multi-way branching based on variable value
    // Input: conditions is a list of objects { value: valueToCheck, targetPassageID: passageIDForThisValue }

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Multi-way Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateMultiBranchContent() {
        RETURN "Testing multi-way branching conditions"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateMultiBranchContent()
    
    // Start with the branch header and bot line
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=ada;"
    
    // Loop through conditions to create branch options
    FOR EACH condition IN conditions {
        slpnPassage += "ops=BOP:onm=\"If " + conditionVar + " = " + condition.value + "\";" +
                      "chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + condition.value + ";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + condition.targetPassageID + ";"
    }
    
    // Add the default case (fallback option)
    slpnPassage += "ops=BOP:onm=\"Default Case\";act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + defaultPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing multi-way branching conditions"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS defaultPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        
        // Verify all target passages are included
        FOR EACH condition IN conditions {
            VALIDATE slpnPassage CONTAINS condition.targetPassageID
        }
    }
    
    ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}
