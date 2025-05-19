{# PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}

PROCEDURE GenerateDiagnosticEntryPoint(stepIDPrefix, entry_point_id, testCaseID, testDescription, initialState, nextPassageID) {
    // Primary goal: Create the entry point for a test sequence that initializes the testing environment
    // Structure: Single passage that sets up initial conditions and directs to the first test passage

    // Define UID for this passage
    DEFINE entryUID = entry_point_id // Use the provided entry_point_id
    DEFINE entryName = "Test Case " + testCaseID + ": Entry Point"
    
    // Create descriptive text for the test initialization
    PROCEDURE CreateEntryContent(testDescription) {
        RETURN "Diagnostic Test Case " + testCaseID + ": " + testDescription
    }
    
    // Create state initialization commands
    PROCEDURE CreateInitialStateCommands(initialState) {
        DEFINE stateCommands = ""
        
        // Loop through all initial state variables and create SET commands
        FOR EACH key, value IN initialState {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                stateCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                stateCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        RETURN stateCommands
    }
    
    // Generate SLPN for this passage
    DEFINE entryContent = CreateEntryContent(testDescription)
    DEFINE stateCommands = CreateInitialStateCommands(initialState)
    
    DEFINE slpnPassage = "BOT:lin=\"" + entryContent + "\";\n" +
                        stateCommands + "\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateEntryPoint(slpnPassage, initialState, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Diagnostic Test Case"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all initial state variables are set
        FOR EACH key IN initialState {
            VALIDATE slpnPassage CONTAINS key
        }
    }
    
    ValidateEntryPoint(slpnPassage, initialState, nextPassageID)
    
    RETURN slpnPassage
}

// Helper function to determine data type for setting state variables correctly
FUNCTION GetDataType(value) {
    IF typeof(value) == "boolean" {
        RETURN "boolean"
    } ELSE IF typeof(value) == "number" {
        RETURN "number"
    } ELSE {
        RETURN "string"
    }
}

{# END_PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}
