{# PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}

PROCEDURE GenerateDiagnosticExitPoint(stepIDPrefix, entry_point_id, testCaseID, testOutcome, resultData) {
    // Primary goal: Create a passage that tests proper system termination and outcome recording
    // Structure: Single passage that records final state and signals test completion
    // Input: resultData is an object of key-value pairs to record as test results

    // Define UID for this passage
    DEFINE exitUID = entry_point_id
    DEFINE exitName = "Test Case " + testCaseID + ": Exit Point"
    
    // Create descriptive text for the test
    PROCEDURE CreateExitContent(testOutcome) {
        RETURN "Test case complete. Validating final state. Outcome: " + testOutcome
    }
    
    // Create result data recording
    PROCEDURE CreateResultRecording(testCaseID, resultData) {
        DEFINE resultCommands = ""
        
        // Record overall test completion
        resultCommands += "SET:evt=TC" + testCaseID + "_COMPLETE;val=true;\n"
        resultCommands += "SET:var=test_outcome;val=\"" + testOutcome + "\";\n"
        
        // Record each result data point
        FOR EACH key, value IN resultData {
            DEFINE dataType = GetDataType(value)
            
            IF dataType == "boolean" {
                resultCommands += "SET:evt=TC" + testCaseID + "_RESULT_" + key + ";val=" + value + ";\n"
            } ELSE {
                resultCommands += "SET:var=TC" + testCaseID + "_RESULT_" + key + ";val=" + (typeof(value) == "string" ? "\"" + value + "\"" : value) + ";\n"
            }
        }
        
        RETURN resultCommands
    }
    
    // Generate SLPN for this passage
    DEFINE exitContent = CreateExitContent(testOutcome)
    DEFINE resultCommands = CreateResultRecording(testCaseID, resultData)
    
    DEFINE slpnPassage = "BOT:lin=\"" + exitContent + "\";\n" +
                         resultCommands + "\n" +
                         "brn=BRN:bds=\"Test Complete\";brp=once;bpr=option-list;bit=ada;ops=BOP:onm=\"Finalize Test\";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME;"
    
    // Validation check
    PROCEDURE ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Test case complete"
        VALIDATE slpnPassage CONTAINS "Outcome: " + testOutcome
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_COMPLETE;val=true"
        VALIDATE slpnPassage CONTAINS "test_outcome;val=\"" + testOutcome + "\""
        VALIDATE slpnPassage CONTAINS "brn=BRN:bds=\"Test Complete\""
        VALIDATE slpnPassage CONTAINS "act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME"
        
        // Verify result data points are recorded
        FOR EACH key IN resultData {
            VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_RESULT_" + key
        }
    }
    
    ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}
