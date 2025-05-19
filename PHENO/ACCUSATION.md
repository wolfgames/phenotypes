{# PHENOTYPE: ACCUSATION #}

PROCEDURE GenerateAccusation(stepIDPrefix, entry_point_id, suspects, requiredEvidenceMap) {
    // Primary goal: Create multi-step accusation process with evidence review per suspect.
    // Structure: 1. Intro -> 2..N+1. Suspect Review/Confirm -> N+2. Final Choice
    // Generates 2 + N passages, where N is the number of suspects.
    // Input: suspects list contains { id, name, resolutionStepID }
    // Input: requiredEvidenceMap maps suspect.id to list of required evidence aspects (e.g., evidenceID_unlocked)

    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Intro["_INTRO"] --> Review1["_REVIEW_suspect1"]
        Review1 --> Review2["_REVIEW_suspect2"]
        Review1 -- "Accuse 1 (Conditional)" --> Resolution1[resolutionStepID_1 (External)]
        Review2 --> ReviewN["..."]
        Review2 -- "Accuse 2 (Conditional)" --> Resolution2[resolutionStepID_2 (External)]
        ReviewN --> FinalChoice["_FINAL_CHOICE"]
        ReviewN -- "Accuse N (Conditional)" --> ResolutionN[resolutionStepID_N (External)]
        FinalChoice -- "Accuse 1 (Conditional)" --> Resolution1
        FinalChoice -- "Accuse 2 (Conditional)" --> Resolution2
        FinalChoice -- "Accuse N (Conditional)" --> ResolutionN
    ```
    */

    DEFINE introUID = entry_point_id
    DEFINE finalChoiceUID = stepIDPrefix + "_FINAL_CHOICE"
    DEFINE introName = "Make Your Accusation - Intro"
    DEFINE finalChoiceName = "Make Your Accusation - Final Decision"
    
    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // == Passage 1: Introduction ==
    PROCEDURE CreateAccusationIntro(uid, name, suspects, firstSuspectReviewUID) {
        DEFINE content = "[SEE: Final accusation interface] [LEARN: The time has come to name the culprit.] [DO: Review each suspect one last time before making your final decision.]"
        // Option to start reviewing the first suspect
        DEFINE options = "BOP:onm=\\\"Begin Final Review\\\";ods=\\\"Review the suspects before accusing\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + firstSuspectReviewUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Point of Accusation\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE firstSuspectReviewUID = stepIDPrefix + "_REVIEW_" + suspects[0].id
    DEFINE slpnPassageIntro = CreateAccusationIntro(introUID, introName, suspects, firstSuspectReviewUID)
    allPassages += slpnPassageIntro
    passageCounter++

    // == Passages 2 to N+1: Suspect Review/Confirm ==
    FOR EACH suspect IN suspects INDEX i {
        DEFINE reviewUID = stepIDPrefix + "_REVIEW_" + suspect.id
        DEFINE reviewName = "Review - " + suspect.name
        DEFINE nextReviewUID = IF i == suspects.length - 1 THEN finalChoiceUID ELSE stepIDPrefix + "_REVIEW_" + suspects[i + 1].id
        DEFINE requiredEvidence = requiredEvidenceMap[suspect.id]
        DEFINE evidenceCondition = CreateEvidenceCondition(requiredEvidence) // Use existing helper

        PROCEDURE CreateSuspectReviewPassage(uid, name, suspectName, evidenceCondition, nextReviewUID, finalChoiceUID) {
            DEFINE content = "[SEE: Profile of " + suspectName + "] [LEARN: Reviewing the case against " + suspectName + ". Do you have the necessary evidence?] [DO: Proceed to next suspect or make final decision.]"
            
            // Options: Accuse now (if evidence met), or move to next suspect/final choice
            DEFINE options = "BOP:onm=\\\"Accuse " + suspectName + " Now\\\";ods=\\\"Make the final accusation\\\";" +
                           "cnd=" + evidenceCondition + ";" + // Condition checks evidence
                           "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspect.resolutionStepID + "|" + // Target is the resolution passage for this suspect
                           "BOP:onm=\\\"Review Next / Decide\\\";ods=\\\"Move to the next suspect or the final decision screen\\\";" +
                           "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextReviewUID // Target next review passage or final choice passage
            
            RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Final Review: " + suspectName + "\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";" // Re-playable to allow revisiting
        }
        
        DEFINE slpnPassageReview = CreateSuspectReviewPassage(reviewUID, reviewName, suspect.name, evidenceCondition, nextReviewUID, finalChoiceUID)
        allPassages += "\n\n" + slpnPassageReview
        passageCounter++
    }

    // == Passage N+2: Final Choice Screen (Fallback/Overview) ==
    PROCEDURE CreateFinalChoicePassage(uid, name, suspects, requiredEvidenceMap) {
        DEFINE content = "[SEE: All suspect profiles] [DO: Make your final, definitive accusation based on the evidence.]"
        DEFINE options = ""
        
        FOR EACH suspect IN suspects INDEX i {
            IF i > 0 { options += "|" }
            DEFINE requiredEvidence = requiredEvidenceMap[suspect.id]
            DEFINE evidenceCondition = CreateEvidenceCondition(requiredEvidence)
            options += "BOP:onm=\\\"Accuse " + suspect.name + "\\\";ods=\\\"Final choice: This is the culprit\\\";" +
                       "cnd=" + evidenceCondition + ";" +
                       "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspect.resolutionStepID
        }
        
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Who Is Guilty?\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassageFinalChoice = CreateFinalChoicePassage(finalChoiceUID, finalChoiceName, suspects, requiredEvidenceMap)
    allPassages += "\n\n" + slpnPassageFinalChoice
    passageCounter++

    // Validation check
    PROCEDURE ValidateAccusationSequence(passageCounter, suspects) {
        VALIDATE passageCounter == suspects.length + 2
        // Check links: Intro -> Review_Suspect0
        // Check links: Review_Suspect_i -> Review_Suspect_i+1 OR FinalChoice OR Resolution
        // Check links: FinalChoice -> Resolution
    }
    
    ValidateAccusationSequence(passageCounter, suspects)
    
    RETURN allPassages
}

{# END_PHENOTYPE: ACCUSATION #}
