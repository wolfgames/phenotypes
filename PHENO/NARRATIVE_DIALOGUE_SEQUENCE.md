{# PHENOTYPE: NARRATIVE_DIALOGUE_SEQUENCE #}

PROCEDURE GenerateDialogueSequence(stepIDPrefix, entry_point_id, sequenceTitle, dialogueExchanges, nextPassageID) {
    // Primary goal: Create immersive dialogue/monologue scenes using the intro sequence functionality.
    // Integration: Builds on INTRO_SEQUENCE to deliver character interactions, flashbacks, and internal monologues.
    // Structure: Converts series of dialogue exchanges into a sequence of slides ending with transition to next gameplay step.

    // --- Generation Context ---
    // Entry Point Construction: The primary passage will use the provided entry_point_id as targetable entry point.
    // Targeting Requirements: The nextPassageID MUST be a valid subsequent passage UID or application target for the final slide transition.
    // Graph Structure: Linear sequence of connected dialogue slides, potentially ending with transition to gameplay.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating unique passage UIDs.
    // entry_point_id: (String) Entry point ID for the first slide in the sequence.
    // sequenceTitle: (String) Title for the overall dialogue sequence.
    // dialogueExchanges: (List) List of dialogue exchange objects with structure:
    //   { 
    //     speakerName: (String) Character name speaking the line,
    //     speakerImage: (String) Optional image alias for character portrait (not used as overlay),
    //     dialogue: (String) The spoken text,
    //     backgroundImage: (String) Image for the slide background,
    //     backgroundDescription: (String) Description of the scene,
    //     emotion: (String) Optional emotional tone for context,
    //     isThought: (Boolean) Optional flag for internal thoughts vs spoken dialogue
    //   }
    // nextPassageID: (String) The passage to transition to after the dialogue sequence.

    // --- Logic ---
    DEFINE allPassages = ""
    DEFINE passageCounter = 0
    DEFINE exchangesPerGroup = 3 // Maximum 3 exchanges per passage/group

    DEFINE numExchanges = dialogueExchanges.length
    DEFINE numGroups = CEIL(numExchanges / exchangesPerGroup)

    // Ensure at least 3 steps in the intro sequence
    IF numExchanges < 3 {
        // Pad with empty exchanges if needed
        FOR i = numExchanges TO 2 {
            DEFINE padExchange = {}
            padExchange.speakerName = ""
            padExchange.speakerImage = ""
            padExchange.dialogue = ""
            padExchange.backgroundImage = "default_bg"
            padExchange.backgroundDescription = ""
            padExchange.emotion = ""
            padExchange.isThought = false
            dialogueExchanges.push(padExchange)
        }
        numExchanges = 3
        numGroups = 1
    }

    FOR groupIndex = 0 TO numGroups - 1 {
        DEFINE currentGroupPassageUID = ""
        DEFINE nextGroupPassageUID = ""

        // Determine current group's passage UID
        IF groupIndex == 0 {
            currentGroupPassageUID = entry_point_id
        } ELSE {
            currentGroupPassageUID = stepIDPrefix + "_GROUP_" + groupIndex
        }

        // Determine next group's passage UID or final target
        IF groupIndex == numGroups - 1 {
            nextGroupPassageUID = nextPassageID // Last group transitions to overall nextPassageID
        } ELSE {
            nextGroupPassageUID = stepIDPrefix + "_GROUP_" + (groupIndex + 1)
        }

        DEFINE passageName = sequenceTitle + " - Part " + (groupIndex + 1)
        DEFINE allStepsInGroup = ""

        FOR exchangeIndexInGroup = 0 TO exchangesPerGroup - 1 {
            DEFINE actualExchangeIndex = (groupIndex * exchangesPerGroup) + exchangeIndexInGroup
            IF actualExchangeIndex >= numExchanges { BREAK } // Stop if we run out of exchanges

            DEFINE exchange = dialogueExchanges[actualExchangeIndex]

            // Format dialogue content for TITLE card
            DEFINE titleText = exchange.speakerName
            IF exchange.emotion {
                titleText += " (" + exchange.emotion + ")"
            }
            DEFINE mainText = exchange.dialogue
            IF exchange.isThought {
                mainText = "[THOUGHT] " + mainText
            }
            // Optionally, add background description as secondary text
            DEFINE secondaryText = exchange.backgroundDescription

            // Compose introStep
            DEFINE introStep = "STP:typ=introStep;"
            introStep += "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + exchange.backgroundImage + ";imd=\"" + exchange.backgroundDescription + "\";"
            introStep += "cmp=CMP:typ=introStepText;txt=TITLE;ttl=\"" + titleText + "\";lin=\"" + mainText + "\";"

            // Button logic
            DEFINE isFirstStep = (groupIndex == 0) AND (exchangeIndexInGroup == 0)
            DEFINE isLastStep = (groupIndex == numGroups - 1) AND ((exchangeIndexInGroup == exchangesPerGroup - 1) OR (actualExchangeIndex == numExchanges - 1))
            IF isFirstStep {
                introStep += "cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex=\"Continue\";"
            } ELSE IF isLastStep {
                introStep += "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Continue\";"
            } ELSE {
                introStep += "cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex=\"Continue\";"
            }
            allStepsInGroup += introStep
        }
        
        DEFINE introAction = "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextGroupPassageUID
        DEFINE slpnPassage = "PSG:uid=" + currentGroupPassageUID + ";nam=\"" + passageName + "\";tag=NARRATIVE_DIALOGUE_SEQUENCE|NARRATIVE|INTRO;" +
                             "cmd=CMD:typ=intro;" + introAction + ";" + allStepsInGroup

        IF passageCounter > 0 {
            allPassages += "\n\n"
        }
        allPassages += slpnPassage
        passageCounter++
    }
    
    RETURN allPassages
}

// Example usage:
/*
DEFINE detectiveDialogue = []
DEFINE exchange1 = {}
exchange1.speakerName = "Detective Chen"
exchange1.speakerImage = "concerned"
exchange1.dialogue = "Where were you on the night of the murder?"
exchange1.backgroundImage = "interrogation_room"
exchange1.backgroundDescription = "Stark interrogation room with single light above table"
exchange1.emotion = "tension"
detectiveDialogue[0] = exchange1

DEFINE exchange2 = {}
exchange2.speakerName = "James Reynolds"
exchange2.speakerImage = "nervous"
exchange2.dialogue = "I told you already. I was at the cinema alone."
exchange2.backgroundImage = "interrogation_room_suspect"
exchange2.backgroundDescription = "Suspect fidgeting with handcuffs"
exchange2.emotion = "anxiety"
detectiveDialogue[1] = exchange2

DEFINE exchange3 = {}
exchange3.speakerName = "Detective Chen"
exchange3.speakerImage = "skeptical"
exchange3.dialogue = "Alone, you say? Can anyone corroborate that?"
exchange3.backgroundImage = "interrogation_room_close_up_detective"
exchange3.backgroundDescription = "Detective Chen leaning forward, eyes narrowed"
exchange3.emotion = "doubt"
detectiveDialogue[2] = exchange3

DEFINE exchange4 = {}
exchange4.speakerName = "James Reynolds"
exchange4.speakerImage = "flustered"
exchange4.dialogue = "I... I don't know. I didn't see anyone I knew."
exchange4.backgroundImage = "interrogation_room_suspect_sweating"
exchange4.backgroundDescription = "James Reynolds looking down, avoiding eye contact"
exchange4.emotion = "fear"
detectiveDialogue[3] = exchange4

GenerateDialogueSequence("CASE_01_INTERROGATION", "ENTRY_POINT_3", "First Interrogation", detectiveDialogue, "SUSPECT_PROFILE_4")
*/

// --- Sample SLPN Output from above example (assuming 4 exchanges, 3 per group) ---
/*
// Group 1 (3 exchanges)
PSG:uid=ENTRY_POINT_3;nam="First Interrogation - Part 1";tag=NARRATIVE_DIALOGUE_SEQUENCE|NARRATIVE|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CASE_01_INTERROGATION_GROUP_1;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=interrogation_room;imd="Stark interrogation room with single light above table";cmp=CMP:typ=introStepText;txt=TITLE;ttl="Detective Chen (tension)";lin="Where were you on the night of the murder?";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=interrogation_room_suspect;imd="Suspect fidgeting with handcuffs";cmp=CMP:typ=introStepText;txt=TITLE;ttl="James Reynolds (anxiety)";lin="I told you already. I was at the cinema alone.";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=interrogation_room_close_up_detective;imd="Detective Chen leaning forward, eyes narrowed";cmp=CMP:typ=introStepText;txt=TITLE;ttl="Detective Chen (doubt)";lin="Alone, you say? Can anyone corroborate that?";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";

// Group 2 (1 exchange)
PSG:uid=CASE_01_INTERROGATION_GROUP_1;nam="First Interrogation - Part 2";tag=NARRATIVE_DIALOGUE_SEQUENCE|NARRATIVE|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=SUSPECT_PROFILE_4;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=interrogation_room_suspect_sweating;imd="James Reynolds looking down, avoiding eye contact";cmp=CMP:typ=introStepText;txt=TITLE;ttl="James Reynolds (fear)";lin="I... I don't know. I didn't see anyone I knew.";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Continue";
*/

{# END_PHENOTYPE: NARRATIVE_DIALOGUE_SEQUENCE #}
