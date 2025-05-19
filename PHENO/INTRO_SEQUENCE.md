{# PHENOTYPE: INTRO_SEQUENCE #}

PROCEDURE GenerateIntroSequenceWithTheories(stepIDPrefix, entry_point_id, caseTitle, theories, choicePrompt) {
    // Primary goal: Introduce competing case theories with evidence snippets and let the player choose one to pursue first.
    // Structure: 1. Intro -> 2. Theory 1 -> 3. Theory 2 -> 4. Theory 3 -> 5. Choice Branch
    // Input: theories is a list of objects: { id, name, description, evidence: {alias, description, details}, type: "TRUE_POSITIVE"|"FALSE_POSITIVE"|"FALSE_NEGATIVE", targetPassageID }

    // --- Input Validation (Example) ---
    VALIDATE theories.length == 3 // Expect exactly 3 theories for the true/false positive/negative structure
    // Ensure each theory has the required fields
    FOR EACH theory IN theories {
        VALIDATE theory.id AND theory.name AND theory.description AND theory.evidence AND theory.type AND theory.targetPassageID
        VALIDATE theory.evidence.alias AND theory.evidence.description AND theory.evidence.details
    }
    // --- End Validation ---

    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // Define UIDs
    DEFINE introPassageUID = entry_point_id
    DEFINE finalChoiceUID = stepIDPrefix + "_THEORY_CHOICE"
    DEFINE theoryPassageUIDs = []
    FOR EACH theory IN theories INDEX i {
        theoryPassageUIDs[i] = stepIDPrefix + "_THEORY_" + theory.id
    }

    // == Passage 1: Introduction to Theories ==
    DEFINE introName = caseTitle + " - Initial Theories"
    DEFINE nextTheoryPassageUID = theoryPassageUIDs[0]

    PROCEDURE CreateTheoriesIntroPassage(uid, name, nextPassageUID) {
        DEFINE introContent = "[LEARN: The initial evidence suggests several possibilities. Let's review the leading theories.] [DO: Examine each theory and the evidence supporting it.]"
        // Create the single step for the intro command
        DEFINE introStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=theory_board;imd=\"Concept art of an investigation board with multiple paths.\";" +
                           "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + introContent + "\";" +
                           "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Review First Theory\";" // No ops/brn here
        // Define the move action at the command level
        DEFINE introAction = "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        // Combine into the intro command
        RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=INTRO_SEQUENCE|NARRATIVE|INTRO;" +
               "cmd=CMD:typ=intro;" + introAction + ";" + introStep
    }

    DEFINE slpnIntroPassage = CreateTheoriesIntroPassage(introPassageUID, introName, nextTheoryPassageUID)
    allPassages += slpnIntroPassage
    passageCounter++

    // == Passages 2 to N: Theory Presentation Passages ==
    FOR EACH theory IN theories INDEX i {
        DEFINE theoryUID = theoryPassageUIDs[i]
        DEFINE theoryName = caseTitle + " - Theory: " + theory.name
        // Determine the next passage: either the next theory or the final choice
        DEFINE nextPassageUID = IF i == theories.length - 1 THEN finalChoiceUID ELSE theoryPassageUIDs[i + 1]
        DEFINE buttonText = IF i == theories.length - 1 THEN "Review Choices" ELSE "Consider Next Theory"

        PROCEDURE CreateTheoryPassage(uid, name, theoryData, nextPassageUID, buttonText) {
            // Add subtle hints based on theory type
            DEFINE hint = SWITCH theoryData.type {
                CASE "TRUE_POSITIVE": "This evidence seems quite direct."
                CASE "FALSE_POSITIVE": "Is this evidence as conclusive as it seems?"
                CASE "FALSE_NEGATIVE": "This contradicts other findings... but doesn't rule this out entirely."
                DEFAULT: "Consider how this fits the narrative."
            }
            DEFINE theoryContent = "[LEARN: Theory: '" + theoryData.description + "'. Supporting Evidence: '" + theoryData.evidence.details + "'] [DO: " + hint + "]"
            // Create the single step for the intro command
            DEFINE theoryStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + theoryData.evidence.alias + ";imd=\"" + theoryData.evidence.description + "\";" +
                              "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + theoryContent + "\";" +
                              "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"" + buttonText + "\";" // No ops/brn here
            // Define the move action at the command level
            DEFINE theoryAction = "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
            // Combine into the intro command
            RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=INTRO_SEQUENCE|NARRATIVE|INTRO|THEORY;" +
                   "cmd=CMD:typ=intro;" + theoryAction + ";" + theoryStep
        }

        DEFINE slpnTheoryPassage = CreateTheoryPassage(theoryUID, theoryName, theory, nextPassageUID, buttonText)
        allPassages += "\n\n" + slpnTheoryPassage
        passageCounter++
    }

    // == Passage N+1: Theory Choice Branch ==
    DEFINE choiceName = caseTitle + " - Choose Initial Path"

    PROCEDURE CreateTheoryChoicePassage(uid, name, theories, choicePrompt) {
        DEFINE branchOptions = ""
        FOR EACH theory IN theories INDEX i {
            IF i > 0 { branchOptions += "|" }
            branchOptions += "BOP:onm=\"Pursue: " + theory.name + "\";img=\"" + theory.evidence.alias + "\";ods=\"" + theory.description + "\";" +
                           "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + theory.targetPassageID // Target the specific path start
        }
        // Format the SLPN using CMD:typ=branch
        RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=INTRO_SEQUENCE|NARRATIVE|INTRO|CHOICE;" +
               "cmd=CMD:typ=branch;bds=\"" + choicePrompt + "\";brp=once;bpr=option-list;bit=ada;ops=" + branchOptions
    }

    DEFINE slpnChoicePassage = CreateTheoryChoicePassage(finalChoiceUID, choiceName, theories, choicePrompt)
    allPassages += "\n\n" + slpnChoicePassage
    passageCounter++

    // Final Validation
    PROCEDURE ValidateTheoryIntroSequence(passageCounter, theories) {
        VALIDATE passageCounter == theories.length + 2
        // Add more specific validations: Check links between intro -> theory1 -> ... -> choice
        // Check branch options link to correct targetPassageIDs
    }

    ValidateTheoryIntroSequence(passageCounter, theories)

    RETURN allPassages
}

{# END_PHENOTYPE: INTRO_SEQUENCE #}
