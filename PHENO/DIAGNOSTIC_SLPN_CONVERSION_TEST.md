{# PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}

PROCEDURE GenerateDiagnosticSLPNConversionTest(stepIDPrefix, entry_point_id, testCaseID, journeyFormat, expectedSLPN, nextPassageID) {
    // Primary goal: Create a passage that tests conversion from journey format to SLPN notation
    // Structure: Single passage that displays both journey input and expected SLPN output for verification

    // Define UID for this passage
    DEFINE conversionUID = entry_point_id
    DEFINE conversionName = "Test Case " + testCaseID + ": SLPN Conversion Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateConversionContent() {
        RETURN "Testing journey to SLPN conversion"
    }
    
    // Format journey and SLPN for display
    PROCEDURE FormatJourneyAndSLPN(journeyFormat, expectedSLPN) {
        DEFINE journeyString = JSON.stringify(journeyFormat, null, 2)
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = expectedSLPN.replace(/"/g, '\\"')
        
        RETURN "Journey Format: '" + journeyString + "', Expected SLPN: '" + escapedSLPN + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE conversionContent = CreateConversionContent()
    DEFINE formattedData = FormatJourneyAndSLPN(journeyFormat, expectedSLPN)
    
    DEFINE slpnPassage = "BOT:lin=\"" + conversionContent + "\";\n" +
                         "SET:var=conversion_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=CONVERSION_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing journey to SLPN conversion"
        VALIDATE slpnPassage CONTAINS "conversion_test_data"
        VALIDATE slpnPassage CONTAINS "CONVERSION_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}
