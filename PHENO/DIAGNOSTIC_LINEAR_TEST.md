{# PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}

PROCEDURE GenerateDiagnosticLinearTest(stepIDPrefix, entry_point_id, testCaseID, stepNumber, totalSteps, stateChanges, nextPassageID) {
    // Primary goal: Create a straightforward test passage that modifies state and proceeds linearly
    // Structure: Single passage that tests simple progression and state modification

    // Define UID for this passage
    DEFINE linearUID = entry_point_id // Use the provided entry_point_id
    DEFINE linearName = "Test Case " + testCaseID + ": Linear Test Step " + stepNumber
    
    // Create descriptive text for the test step
    PROCEDURE CreateLinearContent(stepNumber, totalSteps) {
        RETURN "Testing linear progression (Step " + stepNumber + " of " + totalSteps + ")"
    }
    
    // Create state change commands
    PROCEDURE CreateStateChangeCommands(stateChanges, stepNumber) {
        DEFINE changeCommands = ""
        
        // Loop through all state changes and create SET commands
        FOR EACH key, value IN stateChanges {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                changeCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                changeCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        // Add a completed flag for this step
        changeCommands += "SET:evt=TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE;val=true;"
        
        RETURN changeCommands
    }
    
    // Generate SLPN for this passage
    DEFINE linearContent = CreateLinearContent(stepNumber, totalSteps)
    DEFINE changeCommands = CreateStateChangeCommands(stateChanges, stepNumber)
    
    DEFINE slpnPassage = "BOT:lin=\"" + linearContent + "\";\n" +
                         changeCommands + "\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing linear progression"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all state changes are set
        FOR EACH key IN stateChanges {
            VALIDATE slpnPassage CONTAINS key
        }
        
        // Verify step completion flag
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE"
    }
    
    ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}
