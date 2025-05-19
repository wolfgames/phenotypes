{# PHENOTYPE: DIAGNOSTIC_EVIDENCE_REVEAL #}

PROCEDURE GenerateDiagnosticEvidenceReveal(stepIDPrefix, entry_point_id, testCaseID, evidenceID, nextPassageID) {
    // Primary goal: Create a passage that tests the evidence reveal mechanism
    // Structure: Single passage that reveals evidence and tracks the reveal state

    // Define UID for this passage
    DEFINE revealUID = entry_point_id
    DEFINE revealName = "Test Case " + testCaseID + ": Evidence Reveal Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateRevealContent() {
        RETURN "Testing evidence reveal functionality"
    }
    
    // Generate SLPN for this passage
    DEFINE revealContent = CreateRevealContent()
    
    DEFINE slpnPassage = "BOT:lin=\"" + revealContent + "\";\n" +
                         "ACT:aty=REVEAL;aet=" + evidenceID + ";\n" +
                         "SET:evt=" + evidenceID + "_REVEALED;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;"
    
    // Validation check
    PROCEDURE ValidateEvidenceReveal(slpnPassage, evidenceID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing evidence reveal"
        VALIDATE slpnPassage CONTAINS "ACT:aty=REVEAL;aet=" + evidenceID
        VALIDATE slpnPassage CONTAINS evidenceID + "_REVEALED;val=true"
        VALIDATE slpnPassage CONTAINS "ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app"
    }
    
    ValidateEvidenceReveal(slpnPassage, evidenceID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_EVIDENCE_REVEAL #}
