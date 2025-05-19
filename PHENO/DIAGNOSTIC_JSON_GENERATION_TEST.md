{# PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}

PROCEDURE GenerateDiagnosticJSONGenerationTest(stepIDPrefix, entry_point_id, testCaseID, slpnInput, expectedJSON, nextPassageID) {
    // Primary goal: Create a passage that tests SLPN-to-JSON transformation
    // Structure: Single passage that displays both SLPN input and expected JSON output for verification

    // Define UID for this passage
    DEFINE jsonGenUID = entry_point_id
    DEFINE jsonGenName = "Test Case " + testCaseID + ": JSON Generation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateJSONGenContent() {
        RETURN "Testing SLPN to JSON conversion"
    }
    
    // Format SLPN and JSON for display
    PROCEDURE FormatSLPNAndJSON(slpnInput, expectedJSON) {
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = slpnInput.replace(/"/g, '\\"')
        DEFINE jsonString = JSON.stringify(expectedJSON, null, 2)
        
        RETURN "SLPN Input: '" + escapedSLPN + "', Expected JSON: '" + jsonString + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE jsonGenContent = CreateJSONGenContent()
    DEFINE formattedData = FormatSLPNAndJSON(slpnInput, expectedJSON)
    
    DEFINE slpnPassage = "BOT:lin=\"" + jsonGenContent + "\";\n" +
                         "SET:var=json_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=JSON_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing SLPN to JSON conversion"
        VALIDATE slpnPassage CONTAINS "json_test_data"
        VALIDATE slpnPassage CONTAINS "JSON_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}
