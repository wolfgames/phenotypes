{# PHENOTYPE: NARRATIVE_CUTSCENE_SEQUENCE #}

PROCEDURE GenerateCutsceneSequence(stepIDPrefix, entry_point_id, sequenceTitle, cutsceneShots, nextPassageID) {
    // Primary goal: Create cinematic, omniscient narrative cutscenes showing story context, montages, or emotional moments.
    // Integration: Builds on INTRO_SEQUENCE to deliver impactful, director-style narrative scenes with third-person perspective.
    // Structure: Linear sequence of emotionally charged shots that reveal story elements not directly witnessed by the player.

    // --- Generation Context ---
    // Entry Point Construction: The primary passage will use the provided entry_point_id as targetable entry point.
    // Targeting Requirements: The nextPassageID MUST be a valid subsequent passage UID or application target for the final slide transition.
    // Graph Structure: Linear sequence of connected cinematic shots, creating a montage with narrative impact.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating unique passage UIDs.
    // entry_point_id: (String) Entry point ID for the first slide in the sequence.
    // sequenceTitle: (String) Title for the overall cutscene sequence.
    // cutsceneShots: (List) List of cinematic shot objects with structure:
    //   { 
    //     shotName: (String) Brief descriptor of the shot,
    //     narration: (String) Omniscient narrator text describing the scene or context,
    //     backgroundImage: (String) Image for the slide background,
    //     imageDescription: (String) Description of the visual scene,
    //     emotionalTone: (String) The emotional impact intended (suspense, dread, hope, etc.),
    //     timeContext: (String) Optional temporal context (past, present, future, specific time)
    //   }
    // nextPassageID: (String) The passage to transition to after the cutscene sequence.

    // --- Logic ---
    DEFINE allPassages = ""
    DEFINE passageCounter = 0
    DEFINE shotsPerGroup = 3 // Maximum 3 shots per passage/group

    DEFINE numShots = cutsceneShots.length
    DEFINE numGroups = CEIL(numShots / shotsPerGroup)

    // Ensure at least 3 steps in the cutscene sequence
    IF numShots < 3 {
        // Pad with empty shots if needed
        FOR i = numShots TO 2 {
            DEFINE padShot = {}
            padShot.shotName = ""
            padShot.narration = ""
            padShot.backgroundImage = "default_bg"
            padShot.imageDescription = ""
            padShot.emotionalTone = ""
            padShot.timeContext = ""
            cutsceneShots.push(padShot)
        }
        numShots = 3
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

        DEFINE firstShotInGroupIndex = groupIndex * shotsPerGroup
        DEFINE passageName = sequenceTitle + " - Part " + (groupIndex + 1)
        DEFINE allStepsInGroup = ""

        FOR shotIndexInGroup = 0 TO shotsPerGroup - 1 {
            DEFINE actualShotIndex = firstShotInGroupIndex + shotIndexInGroup
            IF actualShotIndex >= numShots { BREAK } // Stop if we run out of shots

            DEFINE shot = cutsceneShots[actualShotIndex]

            // Compose main text for BREAKDOWN card
            DEFINE mainText = shot.narration
            IF shot.emotionalTone {
                mainText += " [" + shot.emotionalTone + "]"
            }
            IF shot.timeContext {
                mainText += " [" + shot.timeContext + "]"
            }

            // Compose introStep
            DEFINE introStep = "STP:typ=introStep;"
            introStep += "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + shot.backgroundImage + ";imd=\"" + shot.imageDescription + "\";"
            introStep += "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + mainText + "\";"

            // Button logic
            DEFINE isFirstStep = (groupIndex == 0) AND (shotIndexInGroup == 0)
            DEFINE isLastStep = (groupIndex == numGroups - 1) AND ((shotIndexInGroup == shotsPerGroup - 1) OR (actualShotIndex == numShots - 1))
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
        DEFINE slpnPassage = "PSG:uid=" + currentGroupPassageUID + ";nam=\"" + passageName + "\";tag=NARRATIVE_CUTSCENE_SEQUENCE|NARRATIVE|INTRO;" +
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
DEFINE crimeMontage = []

DEFINE shot1 = {}
shot1.shotName = "Empty Street"
shot1.narration = "The city sleeps as midnight approaches, unaware of what's about to unfold."
shot1.backgroundImage = "empty_street_night"
shot1.imageDescription = "An empty street illuminated only by flickering streetlights, rain falling gently"
shot1.emotionalTone = "suspense"
shot1.timeContext = "11:45 PM, Night of the Murder"
crimeMontage[0] = shot1

DEFINE shot2 = {}
shot2.shotName = "Apartment Window"
shot2.narration = "In apartment 4B, the light still burns as shadows move across the curtains."
shot2.backgroundImage = "apartment_window_night"
shot2.imageDescription = "Apartment window with silhouettes visible through thin curtains"
shot2.emotionalTone = "tension"
crimeMontage[1] = shot2

DEFINE shot3 = {}
shot3.shotName = "The Aftermath"
shot3.narration = "By morning, everything has changed. What remains tells only part of the story."
shot3.backgroundImage = "crime_scene_morning"
shot3.imageDescription = "Police tape across an apartment door, officers gathering outside"
shot3.emotionalTone = "mystery"
shot3.timeContext = "7:30 AM, Next Morning"
crimeMontage[2] = shot3

// Example with 4 shots to test grouping
DEFINE shot4 = {}
shot4.shotName = "Detective Arrives"
shot4.narration = "Detective Miles arrives, surveying the scene with a grim expression."
shot4.backgroundImage = "detective_arrival_scene"
shot4.imageDescription = "Detective Miles looking at the cordoned-off area."
shot4.emotionalTone = "serious"
crimeMontage[3] = shot4

GenerateCutsceneSequence("CASE_01_INTRO", "ENTRY_POINT_1", "The Night Of", crimeMontage, "INVESTIGATION_HUB_1")
*/

// --- Sample SLPN Output from above example (assuming 4 shots, 3 per group) ---
/*
// Group 1 (3 shots)
PSG:uid=ENTRY_POINT_1;nam="The Night Of - Part 1";tag=NARRATIVE_CUTSCENE_SEQUENCE|NARRATIVE|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CASE_01_INTRO_GROUP_1;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=empty_street_night;imd="An empty street illuminated only by flickering streetlights, rain falling gently";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="The city sleeps as midnight approaches, unaware of what's about to unfold. [suspense] [11:45 PM, Night of the Murder]";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=apartment_window_night;imd="Apartment window with silhouettes visible through thin curtains";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="In apartment 4B, the light still burns as shadows move across the curtains. [tension]";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=crime_scene_morning;imd="Police tape across an apartment door, officers gathering outside";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="By morning, everything has changed. What remains tells only part of the story. [mystery] [7:30 AM, Next Morning]";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=SECONDARY;tex="Continue";

// Group 2 (1 shot)
PSG:uid=CASE_01_INTRO_GROUP_1;nam="The Night Of - Part 2";tag=NARRATIVE_CUTSCENE_SEQUENCE|NARRATIVE|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_1;STP:typ=introStep;cmp=CMP:typintroStepBG;bgt=IMAGE;img=detective_arrival_scene;imd="Detective Miles looking at the cordoned-off area.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="Detective Miles arrives, surveying the scene with a grim expression. [serious]";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Continue";
*/

{# END_PHENOTYPE: NARRATIVE_CUTSCENE_SEQUENCE #}
