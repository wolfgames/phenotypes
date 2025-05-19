{# PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}

PROCEDURE GenerateDiagnosticLoopTest(stepIDPrefix, entry_point_id, testCaseID, loopVarName, maxIterations, exitPassageID) {
    // Primary goal: Create a passage that tests cyclical progression with iteration counter and exit condition
    // Structure: Single self-referencing passage with counter that exits after a certain number of iterations

    // Define UID for this passage
    DEFINE loopUID = entry_point_id
    DEFINE loopName = "Test Case " + testCaseID + ": Loop Test"
    
    // Create descriptive text for the test that includes the dynamic counter
    PROCEDURE CreateLoopContent(loopVarName) {
        RETURN "Testing loop functionality (iteration $" + loopVarName + ")"
    }
    
    // Generate SLPN for this passage
    DEFINE loopContent = CreateLoopContent(loopVarName)
    
    // Create a separate check passage to handle the conditional logic
    DEFINE checkPassageUID = entry_point_id + "_check"
    DEFINE loopPassages = ""
    
    // First passage - increment the counter
    DEFINE slpnPassage = "BOT:lin=\"" + loopContent + "\";\n" +
                         "UAS:asp=" + loopVarName + ";uty=SET;val=$" + loopVarName + " + 1;\n" +
                         "brn=BRN:bds=\"Loop Control\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Proceed\";ods=\"Continue to next step\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkPassageUID + ";"
    
    // Check passage - evaluate and branch
    DEFINE checkPassage = "PSG:uid=" + checkPassageUID + ";nam=\"" + loopName + " - Check\";\n" +
                         "BOT:lin=\"Evaluating loop condition...\";\n" +
                         "brn=BRN:bds=\"Loop Evaluation\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Exit Loop\";chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations + ";" +
                         "UAS:asp=LOOP_TEST_COMPLETE;uty=SET;val=true;" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + exitPassageID + ";" +
                         "ops=BOP:onm=\"Continue Loop\";chk=CHK:asp=" + loopVarName + ";cty=lt;vlu=" + maxIterations + ";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + entry_point_id + ";"
    
    // Combine the passages
    loopPassages = slpnPassage + "\n\n" + checkPassage
    
    // Validation check
    PROCEDURE ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID) {
        // Verify that required elements are present
        VALIDATE loopPassages CONTAINS "Testing loop functionality"
        VALIDATE loopPassages CONTAINS loopVarName + ";uty=SET;val=$" + loopVarName + " + 1"
        VALIDATE loopPassages CONTAINS "chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations
        VALIDATE loopPassages CONTAINS "LOOP_TEST_COMPLETE;uty=SET;val=true"
        VALIDATE loopPassages CONTAINS exitPassageID
        VALIDATE loopPassages CONTAINS "tgt=" + entry_point_id
        VALIDATE loopPassages CONTAINS "brn=BRN"
        VALIDATE loopPassages CONTAINS checkPassageUID
    }
    
    ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID)
    
    RETURN loopPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}
