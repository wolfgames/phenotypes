{# PHENOTYPE: CASE_RESOLUTION #}

PROCEDURE GenerateCaseResolution(stepIDPrefix, entry_point_id, culpritID, culpritName, caseExplanation, evidenceConnections, epilogueText) {
    // Primary goal: Create satisfying multi-passage case conclusion.
    // Structure: 1. Verdict -> 2. Full Explanation -> 3. Evidence Recap -> 4. Epilogue/End
    // Generates 4 passages.

    // Define UIDs
    DEFINE verdictUID = entry_point_id
    DEFINE explainUID = stepIDPrefix + "_explain"
    DEFINE recapUID = stepIDPrefix + "_recap"
    DEFINE endUID = stepIDPrefix + "_end"

    DEFINE verdictName = "Case Resolution - Verdict"
    DEFINE explainName = "Case Resolution - Explanation"
    DEFINE recapName = "Case Resolution - Evidence Recap"
    DEFINE endName = "Case Closed"

    DEFINE allPassages = ""

    // == Passage 1: Verdict ==
    PROCEDURE CreateVerdictPassage(uid, name, culpritName, nextPassageUID) {
        DEFINE content = "[SEE: Conclusion scene with " + culpritName + " facing justice] [LEARN: The culprit has been identified: " + culpritName + "] [DO: Review the case resolution]"
        DEFINE options = "BOP:onm=\\\"Hear Full Story\\\";img=\\\"verdict_" + culpritID + "\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verdict Delivered\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateVerdictPassage(verdictUID, verdictName, culpritName, explainUID)
    allPassages += slpnPassage1

    // == Passage 2: Full Explanation ==
    PROCEDURE CreateExplanationPassage(uid, name, caseExplanation, nextPassageUID) {
        DEFINE formattedExplanation = FormatLongText(caseExplanation, 240) 
        DEFINE content = "[LEARN: The Full Story: '" + formattedExplanation + "'] [DO: Review the evidence that sealed the case] [SEE: Timeline of the crime]"
        DEFINE options = "BOP:onm=\\\"Review Key Evidence\\\";img=\\\"explanation_" + culpritID + "\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Full Explanation\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateExplanationPassage(explainUID, explainName, caseExplanation, recapUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Evidence Recap ==
    PROCEDURE CreateRecapPassage(uid, name, evidenceConnections, nextPassageUID) {
        DEFINE formattedConnections = String.join(evidenceConnections, ", ")
        DEFINE content = "[SEE: Visualization of connected evidence] [LEARN: Key Evidence: '" + formattedConnections + "'] [DO: Conclude the investigation]"
        DEFINE options = "BOP:onm=\\\"Case Closed\\\";img=\\\"evidence_recap_" + culpritID + "\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Evidence Recap\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateRecapPassage(recapUID, recapName, evidenceConnections, endUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Epilogue/End ==
    PROCEDURE CreateEndPassage(uid, name, epilogueText) {
        DEFINE formattedEpilogue = FormatLongText(epilogueText, 240)
        DEFINE content = "[LEARN: Epilogue: '" + formattedEpilogue + "'] [SEE: Credits and acknowledgments] [INFO: Case Complete]"
        DEFINE endTarget = "HOME"
        DEFINE options = "BOP:onm=\\\"Finish\\\";img=\\\"epilogue_complete\\\";" +
                       "act=UAS:asp=case_complete;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=application;tgt=" + endTarget
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Closed\\\";brp=once;bpr=block-panel;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage4 = CreateEndPassage(endUID, endName, epilogueText)
    allPassages += "\n\n" + slpnPassage4
    
    // Validation check
    PROCEDURE ValidateCaseResolutionSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, culpritName, caseExplanation, evidenceConnections, epilogueText) {
        VALIDATE slpnPassage1 CONTAINS verdictUID AND explainUID AND culpritName
        VALIDATE slpnPassage2 CONTAINS explainUID AND recapUID AND FormatLongText(caseExplanation, 240)
        VALIDATE slpnPassage3 CONTAINS recapUID AND endUID AND String.join(evidenceConnections, ", ")
        VALIDATE slpnPassage4 CONTAINS endUID AND FormatLongText(epilogueText, 240) AND "case_complete;uty=SET;val=true"
    }
    ValidateCaseResolutionSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, culpritName, caseExplanation, evidenceConnections, epilogueText)
    
    RETURN allPassages
}

// Helper function
FUNCTION FormatLongText(text, maxLength) {
    IF text.length > maxLength {
        RETURN text.substring(0, maxLength - 3) + "..."
    } ELSE {
        RETURN text
    }
}

{# END_PHENOTYPE: CASE_RESOLUTION #}
