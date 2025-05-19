{# PHENOTYPE: SUSPECT_CONFRONTATION #}

PROCEDURE GenerateSuspectConfrontation(stepIDPrefix, entry_point_id, suspectID, suspectName, evidencePresentedName, suspectReaction, nextStepPassage, additionalEvidenceID, finalConfrontationStepID) {
    // Primary goal: Create a 4-passage sequence for confronting a suspect with evidence.
    // Structure: 1. Approach -> 2. Present Evidence -> 3. Reaction -> 4. Options

    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Approach["_APPROACH"] --> Present["_PRESENT"]
        Present --> Reaction["_REACTION"]
        Reaction --> Options["_OPTIONS"]
        Options -- "Step Back" --> NextStep[nextStepPassage (External)]
        Options -- "Press Further (Conditional)" --> FinalConfront[finalConfrontationStepID (External)]
    ```
    */
    
    // Define UIDs
    DEFINE approachUID = entry_point_id
    DEFINE presentUID = stepIDPrefix + "_PRESENT"
    DEFINE reactionUID = stepIDPrefix + "_REACTION"
    DEFINE optionsUID = stepIDPrefix + "_OPTIONS"

    DEFINE approachName = "Approaching " + suspectName
    DEFINE presentName = "Presenting Evidence to " + suspectName
    DEFINE reactionName = suspectName + "'s Reaction"
    DEFINE optionsName = "Confrontation Options - " + suspectName

    DEFINE allPassages = ""

    // == Passage 1: Approach ==
    PROCEDURE CreateApproachPassage(uid, name, suspectName, nextPassageUID) {
        DEFINE content = "[SEE: Preparing to confront " + suspectName + "] [FEEL: Tension, determination] [DO: Initiate the confrontation.]"
        DEFINE options = "BOP:onm=\\"Confront " + suspectName + "\\";ods=\\"Present the evidence directly\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\"" + name + "\\";tag=SUSPECT_CONFRONTATION;CNT;BOT:lin=\\"" + content + "\\";brn=BRN:bds=\\"Initiate Confrontation\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateApproachPassage(approachUID, approachName, suspectName, presentUID)
    allPassages += slpnPassage1

    // == Passage 2: Present Evidence ==
    PROCEDURE CreatePresentPassage(uid, name, evidencePresentedName, suspectName, nextPassageUID) {
        DEFINE content = "[LEARN: You present the \'" + evidencePresentedName + "\' to " + suspectName + ".] [DO: Observe their reaction closely.]"
        DEFINE options = "BOP:onm=\\"See Reaction\\";ods=\\"How do they respond? \\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\"" + name + "\\";tag=SUSPECT_CONFRONTATION;CNT;BOT:lin=\\"" + content + "\\";brn=BRN:bds=\\"Evidence Presented\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreatePresentPassage(presentUID, presentName, evidencePresentedName, suspectName, reactionUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Reaction ==
    PROCEDURE CreateReactionPassage(uid, name, suspectReaction, nextPassageUID) {
        DEFINE content = "[SEE: " + suspectName + " reacts.] [LEARN: Reaction: '" + suspectReaction + "'] [FEEL: Assess their response - truth, deflection, anger?]"
        DEFINE options = "BOP:onm=\\"Decide Next Move\\";ods=\\"Consider your options\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\"" + name + "\\";tag=SUSPECT_CONFRONTATION;CNT;BOT:lin=\\"" + content + "\\";brn=BRN:bds=\\"Suspect Reaction\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateReactionPassage(reactionUID, reactionName, suspectReaction, optionsUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Options ==
    PROCEDURE CreateOptionsPassage(uid, name, suspectID, nextStepPassage, additionalEvidenceID, finalConfrontationStepID) {
        DEFINE content = "[DO: How do you proceed? Press further or step back?]"
        DEFINE options = ""
        
        // Conditional option to press further if additional evidence exists
        IF additionalEvidenceID AND finalConfrontationStepID {
            options += "BOP:onm=\\"Press Further\\";ods=\\"Present additional evidence\\";" +
                      "cnd=CND:typ=checkAspect;asp=" + additionalEvidenceID + "_found;cmp=EQ;val=true;" + // Check if the addtl evidence is found/unlocked
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + finalConfrontationStepID
        }

        // Option to return to investigation hub/next step
        IF options != "" { options += "|" }
        options += "BOP:onm=\\"Step Back\\";ods=\\"Return to investigation, consider implications\\";" +
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextStepPassage // Target the main hub or next logical step

        RETURN "PSG:uid=" + uid + ";nam=\\"" + name + "\\";tag=SUSPECT_CONFRONTATION;CNT;BOT:lin=\\"" + content + "\\";brn=BRN:bds=\\"Confrontation Options\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage4 = CreateOptionsPassage(optionsUID, optionsName, suspectID, nextStepPassage, additionalEvidenceID, finalConfrontationStepID)
    allPassages += "\n\n" + slpnPassage4

    // Validation check
    PROCEDURE ValidateSuspectConfrontationSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, nextStepPassage) {
        VALIDATE slpnPassage1 CONTAINS approachUID AND presentUID
        VALIDATE slpnPassage2 CONTAINS presentUID AND reactionUID AND evidencePresentedName
        VALIDATE slpnPassage3 CONTAINS reactionUID AND optionsUID AND suspectReaction
        VALIDATE slpnPassage4 CONTAINS optionsUID AND nextStepPassage // Also check for conditional option if applicable
    }
    
    ValidateSuspectConfrontationSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, nextStepPassage)
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix is SUSPECT_CONFRONTATION_14, suspectID is 'marcus', suspectName is "Marcus Reynolds", 
// evidencePresentedName is "Security Footage", suspectReaction is "Fine! I left...", nextStepPassage is INVESTIGATION_HUB_2_MAIN, 
// additionalEvidenceID is 'fingerprint_match', finalConfrontationStepID is FINAL_CONFRONTATION_15.
// Output includes 4 passages: _APPROACH, _PRESENT, _REACTION, _OPTIONS, linked sequentially.
// _OPTIONS passage includes a conditional link to FINAL_CONFRONTATION_15 (if fingerprint_match_found is true) and a link to INVESTIGATION_HUB_2_MAIN.

{# END_PHENOTYPE: SUSPECT_CONFRONTATION #}
