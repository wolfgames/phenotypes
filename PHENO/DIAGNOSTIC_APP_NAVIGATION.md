{# PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}

PROCEDURE GenerateDiagnosticAppNavigation(stepIDPrefix, entry_point_id, testCaseID, targetApp, returnPassageID) {
    // Primary goal: Create a passage that tests navigation between different application interfaces
    // Structure: Single passage that navigates to a specific application and sets state

    // Define UID for this passage
    DEFINE navUID = entry_point_id
    DEFINE navName = "Test Case " + testCaseID + ": Application Navigation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateNavContent(targetApp) {
        RETURN "Testing application navigation to " + targetApp
    }
    
    // Generate SLPN for this passage
    DEFINE navContent = CreateNavContent(targetApp)
    
    DEFINE appTypeMap = {
        "EVIDENCE": "EVIDENCE",
        "DEDUCTION": "DEDUCTION",
        "NOTES": "NOTES",
        "MAP": "MAP",
        "CASE_FILE": "CASE_FILE"
    }
    
    // Lookup the app type or default to the provided value
    DEFINE appType = appTypeMap[targetApp] ? appTypeMap[targetApp] : targetApp
    
    DEFINE slpnPassage = "BOT:lin=\"" + navContent + "\";\n" +
                         "SET:evt=NAV_TO_" + appType + "_APP;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=" + appType + ";tgt=" + targetApp.toLowerCase() + "_app;\n" +
                         "SET:evt=RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\";"
    
    // Validation check
    PROCEDURE ValidateAppNavigation(slpnPassage, targetApp, returnPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing application navigation"
        VALIDATE slpnPassage CONTAINS "NAV_TO_" + appType + "_APP;val=true"
        VALIDATE slpnPassage CONTAINS "ACT:aty=MOVE;amt=AMT:typ=" + appType
        VALIDATE slpnPassage CONTAINS "RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\""
    }
    
    ValidateAppNavigation(slpnPassage, targetApp, returnPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}
