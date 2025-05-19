{# PHENOTYPE: DEDUCTION_SUCCESS #}

PROCEDURE GenerateDeductionSuccess(stepIDPrefix, entry_point_id, suspectID, suspectName, nextStepTarget) {
    // Primary goal: Create success feedback sequence (4 passages) with new evidence and next step.
    // Structure: 1. Initial Confirmation -> 2. Explanation -> 3. Unlock New Evidence -> 4. Next Step
    
    // Define UIDs for the 4 passages
    DEFINE msgUID = entry_point_id
    DEFINE explainUID = stepIDPrefix + "_EXPLAIN"
    DEFINE unlockUID = stepIDPrefix + "_UNLOCK"
    DEFINE nextUID = stepIDPrefix + "_NEXT"

    DEFINE msgName = suspectName + " - Deduction Success"
    DEFINE explainName = suspectName + " - Explanation"
    DEFINE unlockName = suspectName + " - New Evidence"
    DEFINE nextName = suspectName + " - Next Step"

    DEFINE allPassages = ""

    // == Passage 1: Initial Confirmation ==
    PROCEDURE CreateMsgPassage(uid, name, nextPassageUID) {
        DEFINE content = "[SEE: Success feedback] [LEARN: Your deduction was correct.] [FEEL: A step closer to solving the case.]"
        DEFINE options = "BOP:onm=\\\"Continue\\\";ods=\\\"Learn more about the lie\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_SUCCESS|CONFIRM;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Correct\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateMsgPassage(msgUID, msgName, explainUID)
    allPassages += slpnPassage1

    // == Passage 2: Explanation ==
    PROCEDURE CreateExplainPassage(uid, name, suspectName, nextPassageUID) {
        DEFINE content = "[LEARN: " + suspectName + " lied about their involvement in the crime.] [DO: Understand the implications.]"
        DEFINE options = "BOP:onm=\\\"Reveal New Evidence\\\";ods=\\\"Discover the evidence that exposes the lie\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_SUCCESS|EXPLANATION;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Lie Exposed\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateExplainPassage(explainUID, explainName, suspectName, unlockUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Unlock New Evidence ==
    PROCEDURE CreateUnlockPassage(uid, name, suspectID, nextPassageUID) {
        DEFINE content = "[LEARN: New evidence has been added to your case file.] [DO: Review this new information.]"
        // Set an aspect to indicate the new evidence is available
        DEFINE options = "BOP:onm=\\\"Continue\\\";ods=\\\"Proceed to the next step\\\";" +
                       "act=UAS:asp=" + suspectID + "_new_evidence;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_SUCCESS|UNLOCK;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"New Evidence\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateUnlockPassage(unlockUID, unlockName, suspectID, nextUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Next Step ==
    PROCEDURE CreateNextPassage(uid, name, nextStepTarget) {
        DEFINE content = "[DO: What's next?]"
        // Options: Review new evidence or return to the investigation hub
        DEFINE options = "BOP:onm=\\\"Review New Evidence\\\";ods=\\\"Investigate the new information\\\";" +
                       "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspectID + "_NEW_EVIDENCE|" + // Target the new evidence phenotype
                       "BOP:onm=\\\"Return to Investigation\\\";ods=\\\"Continue the investigation\\\";" +
                       "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextStepTarget // Target the investigation hub
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_SUCCESS|NEXT;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Next Step\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage4 = CreateNextPassage(nextUID, nextName, nextStepTarget)
    allPassages += "\n\n" + slpnPassage4

    // Validation check
    PROCEDURE ValidateDeductionSuccessSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, suspectID, nextStepTarget) {
        VALIDATE slpnPassage1 CONTAINS msgUID AND explainUID
        VALIDATE slpnPassage2 CONTAINS explainUID AND unlockUID AND suspectName
        VALIDATE slpnPassage3 CONTAINS unlockUID AND nextUID AND suspectID + "_new_evidence"
        VALIDATE slpnPassage4 CONTAINS nextUID AND nextStepTarget AND suspectID + "_NEW_EVIDENCE"
    }
    
    ValidateDeductionSuccessSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, suspectID, nextStepTarget)
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix is DEDUCTION_SUCCESS_10, suspectID is 'marcus', nextStepTarget is INVESTIGATION_HUB_2_MAIN.
// Output includes:
// PSG:uid=DEDUCTION_SUCCESS_10_MSG;...;ops=BOP:onm="Continue";...;tgt=DEDUCTION_SUCCESS_10_EXPLAIN;
// PSG:uid=DEDUCTION_SUCCESS_10_EXPLAIN;...;ops=BOP:onm="Reveal New Evidence";...;tgt=DEDUCTION_SUCCESS_10_UNLOCK;
// PSG:uid=DEDUCTION_SUCCESS_10_UNLOCK;...;ops=BOP:onm="Continue";...;tgt=DEDUCTION_SUCCESS_10_NEXT;
// PSG:uid=DEDUCTION_SUCCESS_10_NEXT;...;ops=BOP:onm="Review New Evidence";...;tgt=marcus_NEW_EVIDENCE|BOP:onm="Return to Investigation";...;tgt=INVESTIGATION_HUB_2_MAIN;

{# END_PHENOTYPE: DEDUCTION_SUCCESS #}
