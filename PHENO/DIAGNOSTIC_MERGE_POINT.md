{# PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}

PROCEDURE GenerateDiagnosticMergePoint(stepIDPrefix, entry_point_id, testCaseID, trackOriginPath, nextPassageID) {
    // Primary goal: Create a passage that tests the convergence of multiple paths into a single outcome
    // Structure: Single passage that can be targeted from multiple sources and tracks arrival path

    // Define UID for this passage
    DEFINE mergeUID = entry_point_id
    DEFINE mergeName = "Test Case " + testCaseID + ": Merge Point Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateMergeContent() {
        RETURN "Testing path merge functionality (arrival from multiple sources)"
    }
    
    // Generate SLPN for this passage
    DEFINE mergeContent = CreateMergeContent()
    DEFINE originTracking = ""
    
    // Add optional origin path tracking - use $source_path as a literal, not template syntax
    IF trackOriginPath {
        originTracking = "UAS:asp=arrival_path;uty=SET;val=\"$source_path\";\n"
    }
    
    DEFINE slpnPassage = "BOT:lin=\"" + mergeContent + "\";\n" +
                         originTracking +
                         "UAS:asp=MERGE_POINT_REACHED;uty=SET;val=true;\n" +
                         "brn=BRN:bds=\"Proceed to Next Test\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Continue\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing path merge functionality"
        VALIDATE slpnPassage CONTAINS "MERGE_POINT_REACHED"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify origin tracking if enabled
        IF trackOriginPath {
            VALIDATE slpnPassage CONTAINS "arrival_path"
        }
    }
    
    ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}
