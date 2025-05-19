{# PHENOTYPE: EVIDENCE_VERIFICATION #}

PROCEDURE GenerateEvidenceVerification(stepIDPrefix, entry_point_id, evidenceID, evidenceName, verificationType, analysisDetails, findings, returnPassage) {
    // Primary goal: Create sequence confirming evidence analysis results (4 passages).
    // Structure: 1. Analysis Start -> 2. Process Details -> 3. Results/Findings -> 4. Confirmation/Return
    
    // Define UIDs
    DEFINE startUID = entry_point_id
    DEFINE processUID = stepIDPrefix + "_PROCESS"
    DEFINE resultsUID = stepIDPrefix + "_RESULTS"
    DEFINE confirmUID = stepIDPrefix + "_CONFIRM"

    DEFINE startName = "Verifying " + evidenceName
    DEFINE processName = "Analysis Process - " + evidenceName
    DEFINE resultsName = "Analysis Results - " + evidenceName
    DEFINE confirmName = "Verification Complete - " + evidenceName

    DEFINE allPassages = ""

    // == Passage 1: Analysis Start ==
    PROCEDURE CreateStartPassage(uid, name, evidenceName, verificationType, nextPassageUID) {
        DEFINE content = "[SEE: Analysis interface for " + evidenceName + "] [LEARN: Verification Type: " + verificationType + "] [DO: Begin detailed analysis]"
        DEFINE options = "BOP:onm=\\\"Review Process\\\";img=\\\"verification_" + evidenceID + "_start\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=EVIDENCE_VERIFICATION|START;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Start\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateStartPassage(startUID, startName, evidenceName, verificationType, processUID)
    allPassages += slpnPassage1

    // == Passage 2: Process Details ==
    PROCEDURE CreateProcessPassage(uid, name, analysisDetails, nextPassageUID) {
        DEFINE content = "[LEARN: Analysis Process: '" + analysisDetails + "'] [DO: Await results] [SEE: Analysis in progress]"
        DEFINE options = "BOP:onm=\\\"View Findings\\\";img=\\\"verification_" + evidenceID + "_process\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=EVIDENCE_VERIFICATION|PROCESS;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Analysis Details\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateProcessPassage(processUID, processName, analysisDetails, resultsUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Results/Findings ==
    PROCEDURE CreateResultsPassage(uid, name, findings, verificationType, nextPassageUID) {
        DEFINE formattedFindings = FormatFindings(verificationType, findings)
        DEFINE content = "[SEE: Analysis results visualization] [LEARN: Findings: '" + formattedFindings + "'] [DO: Confirm and note results]"
        DEFINE options = "BOP:onm=\\\"Confirm Results\\\";img=\\\"verification_" + evidenceID + "_results\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=EVIDENCE_VERIFICATION|RESULTS;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Results\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateResultsPassage(resultsUID, resultsName, findings, verificationType, confirmUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Confirmation/Return ==
    PROCEDURE CreateConfirmPassage(uid, name, evidenceID, returnPassage) {
        DEFINE content = "[INFO: Verification complete. Findings logged.] [SEE: Evidence marked as verified]"
        DEFINE options = "BOP:onm=\\\"Return to Investigation\\\";img=\\\"verification_" + evidenceID + "_complete\\\";" +
                       "act=UAS:asp=" + evidenceID + "_verified;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=EVIDENCE_VERIFICATION|CONFIRM;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Complete\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage4 = CreateConfirmPassage(confirmUID, confirmName, evidenceID, returnPassage)
    allPassages += "\n\n" + slpnPassage4
    
    // Validation check
    PROCEDURE ValidateEvidenceVerificationSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, evidenceID, returnPassage, verificationType, analysisDetails, findings) {
        VALIDATE slpnPassage1 CONTAINS startUID AND processUID AND verificationType
        VALIDATE slpnPassage2 CONTAINS processUID AND resultsUID AND analysisDetails
        VALIDATE slpnPassage3 CONTAINS resultsUID AND confirmUID AND FormatFindings(verificationType, findings)
        VALIDATE slpnPassage4 CONTAINS confirmUID AND returnPassage AND evidenceID + "_verified"
    }
    
    ValidateEvidenceVerificationSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, evidenceID, returnPassage, verificationType, analysisDetails, findings)
    
    RETURN allPassages
}

{# END_PHENOTYPE: EVIDENCE_VERIFICATION #}
