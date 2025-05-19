{# PHENOTYPE: DEDUCTION_FAILURE #}

PROCEDURE GenerateDeductionFailure(stepIDPrefix, entry_point_id, suspectID, suspectName, attemptedStatement, puzzleStepID, hint) {
    // Primary goal: Create failure feedback sequence (3 passages) with hint and retry.
    // Structure: 1. Initial Fail Msg -> 2. Hint/Suggestion -> 3. Retry Option
    // Assumption: puzzleStepID is the UID of the DEDUCTION_PUZZLE's *_FINAL_CHOICE* passage.
    
    // Define UIDs
    DEFINE failUID = entry_point_id
    DEFINE hintUID = stepIDPrefix + "_HINT"
    DEFINE retryUID = stepIDPrefix + "_RETRY"

    DEFINE failName = suspectName + " - Incorrect Deduction"
    DEFINE hintName = suspectName + " - Hint"
    DEFINE retryName = suspectName + " - Try Again?"

    DEFINE allPassages = ""

    // == Passage 1: Initial Fail Msg ==
    PROCEDURE CreateFailMsgPassage(uid, name, attemptedStatement, nextPassageUID) {
        DEFINE content = "[SEE: Error feedback] [LEARN: The statement '" + attemptedStatement + "' appears consistent with the known evidence.] [FEEL: Reassessment needed.]"
        DEFINE options = "BOP:onm=\\\"Get Hint\\\";ods=\\\"Receive guidance on the analysis\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_FAILURE|FAIL;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Incorrect\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateFailMsgPassage(failUID, failName, attemptedStatement, hintUID)
    allPassages += slpnPassage1

    // == Passage 2: Hint/Suggestion ==
    PROCEDURE CreateHintPassage(uid, name, hintText, nextPassageUID) {
        DEFINE content = "[LEARN: Hint: '" + hintText + "'] [DO: Re-evaluate the statements and evidence based on this hint.]"
        DEFINE options = "BOP:onm=\\\"Try Again\\\";ods=\\\"Re-attempt the deduction puzzle\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_FAILURE|HINT;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Hint Provided\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateHintPassage(hintUID, hintName, hint, retryUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Retry Option ==
    PROCEDURE CreateRetryPassage(uid, name, puzzleStepID, suspectID) {
        // This passage mainly serves to reset the attempt flag and send back to the puzzle choice.
        DEFINE content = "[DO: Ready to try the deduction again?]"
        // Reset the _made flag and move back to the puzzle choice passage
        DEFINE options = "BOP:onm=\\\"Retry Deduction\\\";ods=\\\"Go back to the statement selection\\\";" +
                       "act=UAS:asp=deduction_attempt_" + suspectID + "_made;uty=SET;val=false|" + // Reset attempt flag
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + puzzleStepID // Link back to the DEDUCTION_PUZZLE *FINAL_CHOICE* passage
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_FAILURE|RETRY;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Retry\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    // NOTE: This generates only 3 passages for failure, which feels more natural than forcing a 4th.
    DEFINE slpnPassage3 = CreateRetryPassage(retryUID, retryName, puzzleStepID, suspectID)
    allPassages += "\n\n" + slpnPassage3

    // Validation check
    PROCEDURE ValidateDeductionFailureSequence(slpnPassage1, slpnPassage2, slpnPassage3, suspectID, puzzleStepID) {
        VALIDATE slpnPassage1 CONTAINS failUID AND hintUID
        VALIDATE slpnPassage2 CONTAINS hintUID AND retryUID AND hint
        VALIDATE slpnPassage3 CONTAINS retryUID AND puzzleStepID AND "deduction_attempt_" + suspectID + "_made;uty=SET;val=false"
    }
    
    ValidateDeductionFailureSequence(slpnPassage1, slpnPassage2, slpnPassage3, suspectID, puzzleStepID)
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix is DEDUCTION_FAILURE_11, suspectID is 'marcus', attemptedStatement is "Statement A", 
// puzzleStepID is "DEDUCTION_PUZZLE_9_FINAL_CHOICE", hint is "Check the security logs again."
// Output includes 3 passages: _MSG, _HINT, _RETRY.
// _RETRY passage resets the deduction_attempt_marcus_made aspect and links back to DEDUCTION_PUZZLE_9_FINAL_CHOICE.

{# END_PHENOTYPE: DEDUCTION_FAILURE #}
