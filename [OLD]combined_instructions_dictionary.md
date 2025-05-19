{# PHENOTYPE: CASE_HOOK #}

PROCEDURE GenerateIntroductionHook(
    stepIDPrefix,                   // Base prefix for UIDs (e.g., "CASE_HOOK_0")
    entry_point_id,                 // UID for the very first passage (e.g., "CH_TheShepherdsFlock_ENTRY")
    caseTitle,                      // The main title of the case (e.g., "The Shepherd's Flock")

    // --- Hook & Initial Presentation (Used across first 1-2 passages) ---
    hookVisual_ImageAlias,          // Primary visual for the hook (e.g., "ethan_thompson_split_face_forensic")
    hookVisual_ImageDescription,    // Detailed description for the image (e.g., "Split image: Ethan Thompson's kind face...")
    hookIntroText,                  // Punchy, evocative text introducing the core event (e.g., "Professor Ethan Thompson, pillar of the community, found dead...")
    
    victimName,                     // Name of the victim (e.g., "Ethan Thompson")
    victimDescription_Brief,        // Short description of the victim (e.g., "a beloved university professor")

    crimeScene_LocationName,        // Name of the crime scene (e.g., "his university office")
    crimeScene_BriefDescription,    // Short description of the scene (e.g., "a usually quiet space, now holding a dark secret")
    
    apparentMurderMode,             // Description of how the murder appears to have been committed (e.g., "Initial signs pointed to nature, but toxicology screams murder via pesticide.")
    
    // --- Context & Stakes (Used in a subsequent intro step) ---
    contextSummary,                 // Core facts of the situation (e.g., "Beloved professor dies unexpectedly. Toxicology reveals foul play. A thermos was found.")
    characterStakes_Optional,       // Optional: What's at stake for characters/community (e.g., "A community loses a respected figure; secrets spill.")
    moralQuestion_Optional,         // Optional: Underlying moral dilemma (e.g., "What twisted path leads to murder for a cause?")
    contextImageAlias_Optional,     // Optional: Image for the context screen (e.g., "case_file_open")
    contextImageDesc_Optional,      // Optional: Description for context image

    // --- Choice & Confirmation ---
    choicePromptText,               // Text for the accept/decline decision point (e.g., "This is a complex case. Are you ready to uncover the truth?")
    
    acceptActionConfig,             // REQUIRED: { targetID: "UID_OR_APPTARGET", targetType: "passage" | "application", setAspects_Optional: [{ name: "aspectName", value: "aspectValue", type: "boolean" | "string" | "number" }] }
    rejectActionConfig,             // REQUIRED: { targetID: "UID_OR_APPTARGET", targetType: "passage" | "application", setAspects_Optional: [{ name: "aspectName", value: "aspectValue", type: "boolean" | "string" | "number" }] }
    
    acceptMessage_Optional,         // Optional: Custom text for the accept confirmation screen
    declineMessage_Optional         // Optional: Custom text for the decline confirmation screen
) {
    // Primary goal: Create an irresistible hook sequence (now typically 3 main passages before confirm/decline)
    // Structure: 1. Visual Hook & Victim Intro -> 2. Scene, Method & Context -> 3. Accept/Reject Choice -> 4. Confirmation/Transition (Accept) -> 5. Confirmation/Transition (Decline)
    // Uses multi-step CMD:typ=intro for richer initial passages.

    // --- Define UIDs for the passages ---
    DEFINE hookPassageUID = entry_point_id
    DEFINE detailsPassageUID = stepIDPrefix + "_details"
    DEFINE choicePassageUID = stepIDPrefix + "_choice"
    DEFINE confirmAcceptUID = stepIDPrefix + "_confirm_ACCEPT"
    DEFINE confirmDeclineUID = stepIDPrefix + "_confirm_DECLINE"

    // --- Define Passage Names ---
    DEFINE hookName = caseTitle + " - The Discovery"
    DEFINE detailsName = caseTitle + " - Initial Briefing"
    DEFINE choiceName = caseTitle + " - Your Decision"
    DEFINE confirmAcceptName = caseTitle + " - Case Accepted"
    DEFINE confirmDeclineName = caseTitle + " - Case Declined"

    DEFINE allPassages = ""

    // --- Helper Functions for Content Formatting ---
    FUNCTION FormatValueForSLPN(value, type) {
        IF type == "string" { RETURN "\\\"" + EscapeStringForSLPN(value) + "\\\"" }
        IF type == "boolean" { RETURN ToString(value).toLowerCase() } // true or false
        RETURN ToString(value) // Numbers
    }

    FUNCTION EscapeStringForSLPN(text) {
        // Basic escape for quotes. Add more as needed.
        RETURN text.replace("\"", "\\\"")
    }
    
    FUNCTION BuildActionString(actionConfig) {
        DEFINE actionsList = []
        IF actionConfig.setAspects_Optional {
            FOR EACH aspect IN actionConfig.setAspects_Optional {
                actionsList.push("UAS:asp=" + aspect.name + ";uty=SET;val=" + FormatValueForSLPN(aspect.value, aspect.type))
            }
        }
        actionsList.push("ACT:aty=MOVE;amt=AMT:typ=" + actionConfig.targetType + ";tgt=" + actionConfig.targetID)
        RETURN JOIN(actionsList, "|")
    }

    // == Passage 1: Visual Hook & Victim Introduction ==
    // Content for Intro Step 1.1
    DEFINE hook_step1_title = caseTitle + ": A Life Cut Short"
    DEFINE hook_step1_subtitle = EscapeStringForSLPN(hookIntroText + " The victim: " + victimName + ", " + victimDescription_Brief + ".")
    
    DEFINE slpnPassage1 = "PSG:uid=" + hookPassageUID + ";nam=\"" + hookName + "\";tag=CASE_HOOK|INTRO|HOOK;" +
                           "cmd=CMD:typ=intro;" +
                               "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + detailsPassageUID + ";" +
                               "STP:typ=introStep;" + // Single step in this first passage
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + hookVisual_ImageAlias + ";imd=\"" + EscapeStringForSLPN(hookVisual_ImageDescription) + "\";" +
                                   "cmp=CMP:typ=introStepText;txt=TITLE;mnt=\"" + EscapeStringForSLPN(hook_step1_title) + "\";sbt=\"" + hook_step1_subtitle + "\";" +
                                   "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Investigate Further...\";"
    allPassages += slpnPassage1

    // == Passage 2: Scene, Method & Context Briefing ==
    // Content for Intro Step 2.1 (Scene & Method)
    DEFINE details_step1_linesArray = [
        "The incident occurred at " + crimeScene_LocationName + ", " + crimeScene_BriefDescription + ".",
        apparentMurderMode
    ]
    DEFINE details_step1_lines = JOIN(EscapeStringForSLPN(details_step1_linesArray), "|")

    // Content for Intro Step 2.2 (Context & Stakes)
    DEFINE details_step2_linesArray = [contextSummary]
    IF characterStakes_Optional { details_step2_linesArray.push("The ramifications are significant: " + characterStakes_Optional) }
    IF moralQuestion_Optional { details_step2_linesArray.push("This case forces us to ask: " + moralQuestion_Optional) }
    DEFINE details_step2_lines = JOIN(EscapeStringForSLPN(details_step2_linesArray), "|")

    DEFINE details_bg_image = contextImageAlias_Optional || "default_context_image"
    DEFINE details_bg_imagedesc = EscapeStringForSLPN(contextImageDesc_Optional || "Reviewing initial case details.")

    DEFINE slpnPassage2 = "PSG:uid=" + detailsPassageUID + ";nam=\"" + detailsName + "\";tag=CASE_HOOK|INTRO|CONTEXT;" +
                           "cmd=CMD:typ=intro;" +
                               "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + choicePassageUID + ";" +
                               "STP:typ=introStep;" + // Step 2.1
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + (crimeScene_ImageAlias_Optional || "default_scene_image") + ";imd=\"" + EscapeStringForSLPN(crimeScene_BriefDescription) + "\";" + // Use specific scene image if available
                                   "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + details_step1_lines + "\";" +
                                   "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"What's the situation?\";" +
                               "STP:typ=introStep;" + // Step 2.2
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + details_bg_image + ";imd=\"" + details_bg_imagedesc + "\";" +
                                   "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + details_step2_lines + "\";" +
                                   "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Consider the Case\";"
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Accept/Reject Choice ==
    DEFINE slpnPassage3 = "PSG:uid=" + choicePassageUID + ";nam=\"" + choiceName + "\";tag=CASE_HOOK|INTRO|CHOICE;" +
                           "cmd=CMD:typ=branch;bds=\"" + EscapeStringForSLPN(choicePromptText) + "\";brp=once;bpr=option-list;bit=ada;" +
                               "ops=BOP:onm=\"Accept Case\";img=\"accept_case_icon\";imd=\"Take on the investigation.\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + confirmAcceptUID + "|" +
                               "BOP:onm=\"Decline Case\";img=\"decline_case_icon\";imd=\"Pass on this case for now.\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + confirmDeclineUID + ";"
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Confirmation / Transition (Accept) ==
    DEFINE acceptActionsString = BuildActionString(acceptActionConfig)
    DEFINE acceptConfirmText = EscapeStringForSLPN(acceptMessage_Optional || "Case accepted. We're counting on you. Preparing your full briefing now.")

    DEFINE slpnPassage4_Accept = "PSG:uid=" + confirmAcceptUID + ";nam=\"" + confirmAcceptName + "\";tag=CASE_HOOK|INTRO;" +
                                "cmd=CMD:typ=intro;" +
                                    "act=" + acceptActionsString + ";" +
                                    "STP:typ=introStep;" +
                                        "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_accepted_graphic;imd=\"Confirmation: Case accepted.\";" +
                                        "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + acceptConfirmText + "\";" +
                                        "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Begin Investigation\";"
    allPassages += "\n\n" + slpnPassage4_Accept

    // == Passage 5: Confirmation / Transition (Decline) ==
    DEFINE rejectActionsString = BuildActionString(rejectActionConfig)
    DEFINE declineConfirmText = EscapeStringForSLPN(declineMessage_Optional || "Understood. Some cases are best left to others. Returning to main menu.")

    DEFINE slpnPassage4_Decline = "PSG:uid=" + confirmDeclineUID + ";nam=\"" + confirmDeclineName + "\";tag=CASE_HOOK|INTRO;" +
                                 "cmd=CMD:typ=intro;" +
                                     "act=" + rejectActionsString + ";" +
                                     "STP:typ=introStep;" +
                                         "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_declined_graphic;imd=\"Confirmation: Case declined.\";" +
                                         "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + declineConfirmText + "\";" +
                                         "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Okay\";"
    allPassages += "\n\n" + slpnPassage4_Decline

    // --- Validation (Conceptual) ---
    PROCEDURE ValidateRevisedHookSequence(slpn1, slpn2, slpn3, slpn4a, slpn4d, inputs) {
        VALIDATE slpn1 CONTAINS inputs.hookVisual_ImageAlias AND inputs.hookIntroText AND inputs.victimName
        VALIDATE slpn2 CONTAINS inputs.crimeScene_LocationName AND inputs.apparentMurderMode AND inputs.contextSummary
        IF inputs.characterStakes_Optional { VALIDATE slpn2 CONTAINS inputs.characterStakes_Optional }
        VALIDATE slpn3 CONTAINS inputs.choicePromptText AND confirmAcceptUID AND confirmDeclineUID
        VALIDATE slpn4a CONTAINS BuildActionString(inputs.acceptActionConfig)
        IF inputs.acceptActionConfig.setAspects_Optional {
            FOR EACH aspect IN inputs.acceptActionConfig.setAspects_Optional {
                VALIDATE slpn4a CONTAINS aspect.name
            }
        }
        VALIDATE slpn4d CONTAINS BuildActionString(inputs.rejectActionConfig)
    }
    // Pass a structure containing all inputs to the validation function for thorough checking.
    // ValidateRevisedHookSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4_Accept, slpnPassage4_Decline, {input parameters...})

    RETURN allPassages
}
//example output:
//PSG:uid=CH_SF_ENTRY;nam="The Shepherd's Flock - The Discovery";tag=CASE_HOOK|INTRO|HOOK;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_details;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=ethan_thompson_split;imd="Split image: Ethan Thompson's kind face on a university bio vs. a forensic photo of the strange discoloration on his skin.";cmp=CMP:typ=introStepText;txt=TITLE;mnt="The Shepherd's Flock: A Life Cut Short";sbt="Professor Ethan Thompson, pillar of the community, found dead in his office. The victim: Professor Ethan Thompson, a beloved university professor known for his kindness.";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Investigate Further...";

PSG:uid=CH_SF_details;nam="The Shepherd's Flock - Initial Briefing";tag=CASE_HOOK|INTRO|CONTEXT;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_choice;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=office_chalk_outline;imd="a place of learning, now stained by tragedy";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="The incident occurred at his university office, a place of learning, now stained by tragedy.|Initial signs pointed to natural causes, but toxicology reports scream murder. The method: a potent pesticide.";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="What's the situation?";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_file_shepherds_flock;imd="The initial case file for 'The Shepherd's Flock' investigation.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="A respected professor's life cut short. Early reports were misleading, but advanced toxicology confirms foul play. A thermos, potentially crucial, was recovered from the scene.|The university community is shaken, a family is devastated, and unsettling secrets are beginning to surface.|This case forces us to ask: What could drive someone to commit such a calculated act against a man like him?";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Consider the Case";

PSG:uid=CH_SF_choice;nam="The Shepherd's Flock - Your Decision";tag=CASE_HOOK|INTRO|CHOICE;cmd=CMD:typ=branch;bds="This case, 'The Shepherd's Flock,' promises to be challenging. Are you prepared to delve into its depths?";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Accept Case";img="accept_case_icon";imd="Take on the investigation.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_confirm_ACCEPT|BOP:onm="Decline Case";img="decline_case_icon";imd="Pass on this case for now.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_confirm_DECLINE;

PSG:uid=CH_SF_confirm_ACCEPT;nam="The Shepherd's Flock - Case Accepted";tag=CASE_HOOK|INTRO;cmd=CMD:typ=intro;act=UAS:asp=CaseIntroduced_ShepherdsFlock;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=SUSPECT_INTRODUCTION_THROUGH_DIALOGUE_1;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_accepted_graphic;imd="Confirmation: Case accepted.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="Case accepted. 'The Shepherd's Flock' needs your expertise. Preparing your investigation dashboard now.";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Begin Investigation";

PSG:uid=CH_SF_confirm_DECLINE;nam="The Shepherd's Flock - Case Declined";tag=CASE_HOOK|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_declined_graphic;imd="Confirmation: Case declined.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="Understood. We'll assign 'The Shepherd's Flock' to another team. Returning you to case selection.";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Okay";
{# END_PHENOTYPE: CASE_HOOK #}

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


{# PHENOTYPE: INVESTIGATION_HUB #}
PROCEDURE GenerateInvestigationHub(stepIDPrefix, entry_point_id, caseStatus, currentObjectives, availableLocations, unlockedFeatures, conditionalPaths) { // Added entry_point_id
    // Primary goal: Create central investigation hub and related informational passages.
    // Structure: 1. Main Hub Passage -> Links to 2. Case Briefing, 3. Objectives, 4. Notes Passage.
    // Generates 4 passages total.
    
    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Hub["_MAIN (Hub)"] --> Loc1["Location 1 (External)"]
        Hub --> LocN["... Locations (External)"]
        Hub --> Feat1["Feature 1 (External)"]
        Hub --> FeatN["... Features (External)"]
        Hub --> EvReview["EVIDENCE (Application)"]
        Hub --> Briefing["_BRIEFING (Generated)"]
        Hub --> Objectives["_OBJECTIVES (Generated)"]
        Hub --> Notes["_NOTES (Generated)"]
        Briefing --> Hub
        Objectives --> Hub
        Notes --> Hub
    ```
    */
    
    // Define UIDs
    DEFINE hubUID = entry_point_id // Use entry_point_id for the first passage
    DEFINE briefingUID = stepIDPrefix + "_briefing" // Derived IDs for internal passages
    DEFINE objectivesUID = stepIDPrefix + "_objectives"
    DEFINE notesUID = stepIDPrefix + "_notes"

    DEFINE hubName = "Investigation Hub"
    DEFINE briefingName = "Case Briefing"
    DEFINE objectivesName = "Current Objectives"
    DEFINE notesName = "Investigator Notes"

    DEFINE allPassages = ""

    // == Passage 1: Main Investigation Hub ==
    PROCEDURE CreateStatusSummary(caseStatus) {
        // Format the current case information for player reference
        DEFINE seeComponent = "[SEE: Investigation board with evidence and leads]"
        DEFINE doComponent = "[DO: Select your next investigative focus]"
        DEFINE learnComponent = "[LEARN: " + SummarizeCase(caseStatus) + "]"
        
        DEFINE statusSummary = seeComponent + " " + doComponent + " " + learnComponent
        
        RETURN statusSummary
    }
    
    PROCEDURE CreateNavigationOptions(availableLocations, unlockedFeatures, conditionalPaths, derivedBriefingUID, derivedObjectivesUID, derivedNotesUID, hubUID) { // Pass derived UIDs
        // Modified to include links to briefing, objectives, and notes
        DEFINE options = ""
        DEFINE optionIndex = 0

        // Add location options
        FOR EACH location IN availableLocations {
            IF optionIndex > 0 {
                options += "|"
            }
            
            // Check if this location has conditional access
            IF HasConditionalAccess(location.id, conditionalPaths) {
                DEFINE condition = GetCondition(location.id, conditionalPaths)
                options += "BOP:onm=\\"" + location.name + "\\";ods=\\"" + location.description + 
                          "\\";cnd=" + condition + ";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + location.targetPassage
            } ELSE {
                options += "BOP:onm=\\"" + location.name + "\\";ods=\\"" + location.description + 
                          "\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + location.targetPassage
            }
            
            optionIndex++
        }
        
        // Add unlocked feature options
        FOR EACH feature IN unlockedFeatures {
            IF optionIndex > 0 {
                options += "|"
            }
            
            // Check if this feature has conditional access
            IF HasConditionalAccess(feature.id, conditionalPaths) {
                DEFINE condition = GetCondition(feature.id, conditionalPaths)
                options += "BOP:onm=\\"" + feature.name + "\\";ods=\\"" + feature.description + 
                          "\\";cnd=" + condition + ";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + feature.targetPassage
            } ELSE {
                options += "BOP:onm=\\"" + feature.name + "\\";ods=\\"" + feature.description + 
                          "\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + feature.targetPassage
            }
            
            optionIndex++
        }
        
        // Add evidence review option
        IF optionIndex > 0 { options += "|" }
        options += "BOP:onm=\\\"Review Evidence\\\";ods=\\\"Examine collected evidence\\\";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=EVIDENCE;"
        optionIndex++

        // Add links to auxiliary hub passages
        IF optionIndex > 0 { options += "|" }
        options += "BOP:onm=\"View Case Briefing\";ods=\"Review the full case summary\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + derivedBriefingUID
        optionIndex++
        
        IF optionIndex > 0 { options += "|" }
        options += "BOP:onm=\"Check Objectives\";ods=\"See current investigation goals\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + derivedObjectivesUID
        optionIndex++

        IF optionIndex > 0 { options += "|" }
        options += "BOP:onm=\"Open Notes\";ods=\"Review your investigator notes\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + derivedNotesUID
        optionIndex++
        
        RETURN options
    }
    
    DEFINE statusSummary = CreateStatusSummary(SummarizeCase(caseStatus)) // Use summarized version for main hub
    DEFINE navigationOptions = CreateNavigationOptions(availableLocations, unlockedFeatures, conditionalPaths, briefingUID, objectivesUID, notesUID, hubUID) // Pass derived UIDs
    DEFINE slpnHubPassage = "PSG:uid=" + hubUID + ";nam=\\\"" + hubName + "\\\";CNT;BOT:lin=\\\"" + 
                           statusSummary + "\\\";brn=BRN:bds=\\\"Investigation Options\\\";brp=re-playable;bpr=block-panel;bit=ada;ops=" + 
                           navigationOptions + ";"
    allPassages += slpnHubPassage

    // == Passage 2: Case Briefing ==
    PROCEDURE CreateBriefingPassage(uid, name, fullCaseStatus, returnHubUID) { // Use returnHubUID param name
        DEFINE see = "[SEE: Detailed case file and evidence board connections]"
        DEFINE learn = "[LEARN: Full Case Details: " + fullCaseStatus + "]"
        DEFINE content = see + " " + learn
        DEFINE options = "BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Briefing\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnBriefingPassage = CreateBriefingPassage(briefingUID, briefingName, caseStatus, hubUID) // Use full caseStatus here
    allPassages += "\n\n" + slpnBriefingPassage

    // == Passage 3: Current Objectives ==
    PROCEDURE CreateObjectivesPassage(uid, name, objectivesList, returnHubUID) { // Use returnHubUID param name
        DEFINE see = "[SEE: List of current tasks and leads]"
        DEFINE learn = "[LEARN: Objectives: " + FormatObjectives(objectivesList) + "]" // Needs FormatObjectives helper
        DEFINE content = see + " " + learn
        DEFINE options = "BOP:onm=\\\"Return to Hub\\\";ods=\\\"Go back to main investigation view\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=INVESTIGATION_HUB|OBJECTIVES;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Current Objectives\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnObjectivesPassage = CreateObjectivesPassage(objectivesUID, objectivesName, currentObjectives, hubUID)
    allPassages += "\n\n" + slpnObjectivesPassage

    // == Passage 4: Investigator Notes ==
    PROCEDURE CreateNotesPassage(uid, name, returnHubUID) { // Use returnHubUID param name
        // This passage might dynamically load notes via application logic rather than static content.
        DEFINE see = "[SEE: Your personal notebook interface]"
        DEFINE do = "[DO: Review, add, or organize your notes]"
        DEFINE content = see + " " + do + " [INFO: Notes are managed by the application]"
        DEFINE options = "BOP:onm=\\\"Return to Hub\\\";ods=\\\"Close notebook and return to hub\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=INVESTIGATION_HUB|NOTES;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Investigator Notes\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnNotesPassage = CreateNotesPassage(notesUID, notesName, hubUID)
    allPassages += "\n\n" + slpnNotesPassage

    // Validation check
    PROCEDURE ValidateInvestigationHub(slpnHubPassage, slpnBriefingPassage, slpnObjectivesPassage, slpnNotesPassage) {
        VALIDATE slpnHubPassage CONTAINS "Review Evidence" AND briefingUID AND objectivesUID AND notesUID
        VALIDATE slpnBriefingPassage CONTAINS hubUID
        VALIDATE slpnObjectivesPassage CONTAINS hubUID
        VALIDATE slpnNotesPassage CONTAINS hubUID
    }
    
    ValidateInvestigationHub(slpnHubPassage, slpnBriefingPassage, slpnObjectivesPassage, slpnNotesPassage)
    
    RETURN allPassages
}

// Helper functions
FUNCTION SummarizeCase(caseStatus) {
    // Create a concise summary of the current case status
    // In a real implementation, this would analyze the status object and extract key points
    IF caseStatus.length > 100 {
        RETURN caseStatus.substring(0, 97) + "..."
    } ELSE {
        RETURN caseStatus
    }
}

FUNCTION HasConditionalAccess(id, conditionalPaths) {
    // Check if a location/feature has conditional access requirements
    FOR EACH path IN conditionalPaths {
        IF path.id == id {
            RETURN true
        }
    }
    RETURN false
}

FUNCTION GetCondition(id, conditionalPaths) {
    // Get the condition string for a conditional path
    FOR EACH path IN conditionalPaths {
        IF path.id == id {
            RETURN path.condition
        }
    }
    RETURN ""
}

FUNCTION FormatObjectives(objectivesList) {
    // Simple formatter for objectives
    IF objectivesList IS_EMPTY { RETURN "No specific objectives assigned yet." }
    DEFINE formatted = ""
    FOR EACH obj IN objectivesList INDEX i {
        IF i > 0 { formatted += ", " }
        formatted += obj
    }
    RETURN formatted
}

// Example output:
// PSG:uid=INVESTIGATION_HUB_2;nam="Investigation Hub";tag=INVESTIGATION_HUB|MAIN;CNT;BOT:lin="[SEE: Investigation board with evidence and leads] [DO: Select your next investigative focus] [LEARN: Victim found dead in recording studio. Time of death: between 9-11 PM. Key evidence: bloodied microphone, studio access logs...]";brn=BRN:bds="Investigation Options";brp=re-playable;bpr=block-panel;bit=ada;ops=BOP:onm="Crime Scene";ods="Return to the studio";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_COLLECTION_3|BOP:onm="Interview Witnesses";ods="Speak with people present that night";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=SUSPECT_LIST_4|BOP:onm="Forensic Analysis";ods="Check lab results";cnd=CND:typ=checkAspect;asp=forensic_samples_collected;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_VERIFICATION_8|BOP:onm="Review Evidence";ods="Examine collected evidence";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=EVIDENCE;
{# END_PHENOTYPE: INVESTIGATION_HUB #}

{# PHENOTYPE: EVIDENCE_COLLECTION #}
PROCEDURE GenerateEvidenceCollection(stepIDPrefix, entry_point_id, locationScenes, returnPassage) {
    // Primary goal: Create multiple passages, one for each scene/area within a broader location, for discovering evidence.
    // Structure: Generates N passages, where N is the number of items in locationScenes list.
    // Input: locationScenes is a list of objects, each with { id, name, description, evidenceItems (list of {id, name, type, examineStepID}) }

    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // Loop through each scene defined for this location
    FOR EACH scene IN locationScenes INDEX i {
        // Create a unique ID for this specific scene passage
        // The FIRST scene passage (i=0) uses the entry_point_id
        DEFINE sceneUID = IF i == 0 THEN entry_point_id ELSE stepIDPrefix + "_" + scene.id
        DEFINE sceneName = scene.name

        // Step 1: Create descriptive scene content
        PROCEDURE CreateSceneDescription(description) {
            DEFINE see = "[SEE: " + description + "]"
            DEFINE do = "[DO: Examine the area for evidence]"
            DEFINE learn = "[LEARN: Look for anything that seems out of place]"
            RETURN see + " " + do + " " + learn
        }
        DEFINE sceneContent = CreateSceneDescription(scene.description)

        // Step 2: Create evidence examination options for this scene
        PROCEDURE CreateEvidenceOptionsForScene(evidenceItems, returnPassage) {
            DEFINE options = ""
            FOR EACH item IN evidenceItems INDEX j {
                IF j > 0 { options += "|" }
                // Each evidence item gets its own option
                options += "BOP:onm=\\\"" + item.name + "\\\";img=\\\"evidence_" + item.id + "\\\";" +
                          "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + item.examineStepID
            }
            // Add return option
            IF evidenceItems.length > 0 { options += "|" }
            options += "BOP:onm=\\\"Return\\\";img=\\\"return_to_location\\\";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
            RETURN options
        }
        DEFINE sceneOptions = CreateEvidenceOptionsForScene(scene.evidenceItems, returnPassage)

        // Step 3: Format the SLPN for this specific scene passage
        DEFINE slpnScenePassage = "PSG:uid=" + sceneUID + ";nam=\\\"" + sceneName + "\\";tag=EVIDENCE_COLLECTION|SCENE;CNT;BOT:lin=\\\"" + 
                                 sceneContent + "\\";brn=BRN:bds=\\"Examine " + sceneName + "\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + 
                                 sceneOptions + ";"
        
        
        IF i > 0 { allPassages += "\n\n" }
        allPassages += slpnScenePassage
        passageCounter++
    }
    
    // Validation check
    PROCEDURE ValidateEvidenceCollection(passageCounter, locationScenes) {
        VALIDATE passageCounter == locationScenes.length
        // Check that each scene passage has appropriate options
        FOR EACH scene IN locationScenes {
            VALIDATE scene.evidenceItems.length > 0
            // Validate that each evidence item has required fields
            FOR EACH item IN scene.evidenceItems {
                VALIDATE item.id AND item.name AND item.type AND item.examineStepID
            }
        }
    }
    
    ValidateEvidenceCollection(passageCounter, locationScenes)
    
    RETURN allPassages
}
{# END_PHENOTYPE: EVIDENCE_COLLECTION #}

{# PHENOTYPE: EVIDENCE_EXAMINATION #}
PROCEDURE GenerateEvidenceExamination(stepIDPrefix, entry_point_id, evidenceID, evidenceName, evidenceDetails, relevance, nextPassage) {
    // Primary goal: Create a streamlined evidence viewing experience
    // Structure: 1. Mention -> 2. View -> 3. React/Comment

    // Define UIDs for the 2 passages
    DEFINE mentionUID = entry_point_id
    DEFINE reactUID = stepIDPrefix + "_react"

    DEFINE mentionName = "Discover " + evidenceName
    DEFINE reactName = "Thoughts on " + evidenceName

    DEFINE allPassages = ""

    // == Passage 1: Mention/Reveal ==
    PROCEDURE CreateMentionPassage(uid, name, evidenceID, evidenceName, reactUID) {
        DEFINE content = "[SEE: You notice " + evidenceName + "] [DO: Examine this potential evidence]"
        // First reveal the evidence to make it available
        // Also set up the FIRST_VIEW trigger to route to the reaction passage
        DEFINE options = "BOP:onm=\\\"View " + evidenceName + "\\\";ods=\\\"Examine this evidence closely\\\";" +
                       "act=ACT:aty=REVEAL;aet=" + evidenceID + "|" +
                       "TRG:uid=" + evidenceID + "_first_view;trg=FIRST_VIEW;tar=" + evidenceID + ";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + reactUID + "|" +
                       "ACT:aty=MOVE;amt=AMT:typ=evidence;tgt=" + evidenceID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Discover Evidence\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateMentionPassage(mentionUID, mentionName, evidenceID, evidenceName, reactUID)
    slpnPassage1 = slpnPassage1.replace("PSG:uid=", "PSG:uid=" + mentionUID + ";tag=EVIDENCE_EXAMINATION|MENTION;")
    allPassages += slpnPassage1

    // == Passage 2: React/Comment ==
    PROCEDURE CreateReactPassage(uid, name, evidenceID, evidenceName, evidenceDetails, relevance, nextPassage) {
        DEFINE content = "[LEARN: '" + FormatClue(evidenceDetails) + "'] [DO: Consider how this relates to your case] [LEARN: Relevance: '" + FormatRelevance(relevance) + "']"
        // Option to proceed with investigation
        DEFINE options = "BOP:onm=\\\"Continue Investigation\\\";ods=\\\"Proceed with your investigation\\\";" +
                       "act=UAS:asp=" + evidenceID + "_examined;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassage
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Evidence Analysis\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateReactPassage(reactUID, reactName, evidenceID, evidenceName, evidenceDetails, relevance, nextPassage)
    slpnPassage2 = slpnPassage2.replace("PSG:uid=", "PSG:uid=" + reactUID + ";tag=EVIDENCE_EXAMINATION|REACT;")
    allPassages += "\n\n" + slpnPassage2
    
    RETURN allPassages
}

// Example output for a bloody knife evidence item:
/*
PSG:uid=EVIDENCE_EXAM_01_START;nam="Discover Bloody Knife";CNT;BOT:lin="[SEE: You notice Bloody Knife] [DO: Examine this potential evidence]";brn=BRN:bds="Discover Evidence";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="View Bloody Knife";ods="Examine this evidence closely";act=ACT:aty=REVEAL;aet=bloody_knife|TRG:uid=bloody_knife_first_view;trg=FIRST_VIEW;tar=bloody_knife;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_EXAM_01_react|ACT:aty=MOVE;amt=AMT:typ=evidence;tgt=bloody_knife;

PSG:uid=EVIDENCE_EXAM_01_react;nam="Thoughts on Bloody Knife";CNT;BOT:lin="[LEARN: 'Kitchen knife with blood residue on the blade. Partial fingerprint visible on handle.'] [DO: Consider how this relates to your case] [LEARN: Relevance: 'Potential murder weapon - matches wound pattern on victim.']";brn=BRN:bds="Evidence Analysis";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Continue Investigation";ods="Proceed with your investigation";act=UAS:asp=bloody_knife_examined;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CRIME_SCENE_02;
*/
{# END_PHENOTYPE: EVIDENCE_EXAMINATION #}

{# PHENOTYPE: SUSPECT_LIST #}
PROCEDURE GenerateSuspectList(stepIDPrefix, entry_point_id, suspects, returnPassage) {
    // Primary goal: Create overview of suspects, revealing brief details upon selection.
    // Structure: 1. Intro/List Passage -> 2..N+1. Brief Detail Passages (one per suspect)
    // Generates 1 + N passages, where N is the number of suspects.
    // Input: suspects is a list of objects, each with { id, name, role, briefDescription, profileID, profileStepID }

    DEFINE listUID = entry_point_id
    DEFINE listName = "Suspects Overview"
    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // == Passage 1: Suspect List Introduction ==
    PROCEDURE CreateListIntroPassage(uid, name, suspects, returnPassage) {
        DEFINE overviewContent = "[SEE: Gallery of suspect portraits] [DO: Select a suspect for initial details] [LEARN: Review the key individuals involved in the case]"
        DEFINE options = ""
        
        // Create options linking to the brief detail passage for each suspect
        FOR EACH suspect IN suspects INDEX i {
            IF i > 0 { options += "|" }
            DEFINE detailTargetUID = stepIDPrefix + "_detail_" + suspect.id
            options += "BOP:onm=\\\"" + suspect.name + "\\\";img=\\\"suspect_" + suspect.id + "_portrait\\\";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + detailTargetUID
        }
        
        // Add return option
        options += "|BOP:onm=\\\"Return to Investigation\\\";img=\\\"return_to_hub\\\";" +
                  "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
        
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + overviewContent + "\\\";brn=BRN:bds=\\\"Suspects\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnListPassage = CreateListIntroPassage(listUID, listName, suspects, returnPassage)
    slpnListPassage = slpnListPassage.replace("PSG:uid=", "PSG:uid=" + listUID + ";tag=SUSPECT_LIST|OVERVIEW;")
    allPassages += slpnListPassage
    passageCounter++
    
    // == Passages 2 to N+1: Brief Detail Passages (one per suspect) ==
    FOR EACH suspect IN suspects INDEX i {
        DEFINE detailUID = stepIDPrefix + "_detail_" + suspect.id
        DEFINE detailName = suspect.name + " - " + suspect.role
        
        PROCEDURE CreateDetailPassage(uid, name, suspect, listUID) {
            DEFINE content = "[SEE: Close-up of " + suspect.name + "] [LEARN: Role: " + suspect.role + ". " + suspect.briefDescription + "] [DO: Decide whether to learn more]"
            
            // Options: View full profile (links to external profileStepID) or return to list
            DEFINE options = "BOP:onm=\\\"Full Profile\\\";img=\\\"suspect_" + suspect.id + "_profile\\\";" +
                           "act=ACT:aty=REVEAL;aet=character;cid=" + suspect.id + "|" +
                           "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspect.profileStepID + "|" +
                           "BOP:onm=\\\"Back to List\\\";img=\\\"back_to_list\\\";" +
                           "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + listUID
                           
            RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Suspect Details\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";"
        }
        
        DEFINE slpnDetailPassage = CreateDetailPassage(detailUID, detailName, suspect, listUID)
        slpnDetailPassage = slpnDetailPassage.replace("PSG:uid=", "PSG:uid=" + detailUID + ";tag=SUSPECT_LIST|DETAIL;")
        allPassages += "\n\n" + slpnDetailPassage
        passageCounter++
    }
    
    // Validation check
    PROCEDURE ValidateSuspectList(passageCounter, suspects, returnPassage) {
        VALIDATE passageCounter == suspects.length + 1
        
        // Check that the list passage links to all detail passages and the return passage
        // Check that each detail passage links back to the list and to the correct profile
        FOR EACH suspect IN suspects {
            VALIDATE suspect.id AND suspect.name AND suspect.role AND suspect.profileStepID
        }
    }
    
    ValidateSuspectList(passageCounter, suspects, returnPassage)
    
    RETURN allPassages
}
{# END_PHENOTYPE: SUSPECT_LIST #}

{# PHENOTYPE: SUSPECT_PROFILE #}
PROCEDURE GenerateSuspectProfile(stepIDPrefix, entry_point_id, suspectID, suspectName, suspectRole, backgroundInfo, knownMotives, alibi, suspectOptions, returnPassage) {
    // Primary goal: Create detailed profile view with various action options.
    // Structure: Single passage with multiple possible paths (interview, confront, etc.)
    // Input: suspectOptions is an object with optional fields { interviewStepID, confrontStepID, etc. }
    
    DEFINE profileUID = entry_point_id
    DEFINE profileName = suspectName + " - Full Profile"
    
    // Create detailed content for the profile
    PROCEDURE CreateProfileContent(suspectName, suspectRole, backgroundInfo, knownMotives, alibi) {
        DEFINE seeComponent = "[SEE: Full dossier on " + suspectName + "]"
        DEFINE learnComponent = "[LEARN: Background: " + backgroundInfo + ". Role: " + suspectRole + ". Motives: " + knownMotives + ". Alibi: " + alibi + "]"
        DEFINE doComponent = "[DO: Determine your next action with this suspect]"
        RETURN seeComponent + " " + learnComponent + " " + doComponent
    }
    
    DEFINE profileContent = CreateProfileContent(suspectName, suspectRole, backgroundInfo, knownMotives, alibi)
    
    // Create dynamic options based on available actions for this suspect
    PROCEDURE CreateProfileOptions(suspectID, suspectOptions, returnPassage) {
        DEFINE options = ""
        DEFINE optionCount = 0
        
        // Interview option
        IF suspectOptions.interviewStepID {
            options += "BOP:onm=\\\"Interview\\\";img=\\\"interview_" + suspectID + "\\\";" +
                      "cnd=CND:typ=checkAspect;asp=" + suspectID + "_interview_complete;cmp=EQ;val=false;" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspectOptions.interviewStepID
            optionCount++
        }
        
        // Confrontation option
        IF suspectOptions.confrontStepID {
            IF optionCount > 0 { options += "|" }
            options += "BOP:onm=\\\"Confront\\\";img=\\\"confront_" + suspectID + "\\\";" +
                      "cnd=CND:typ=checkAspect;asp=" + suspectID + "_can_confront;cmp=EQ;val=true;" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspectOptions.confrontStepID
            optionCount++
        }
        
        // Deduction puzzle option
        IF suspectOptions.deductionStepID {
            IF optionCount > 0 { options += "|" }
            options += "BOP:onm=\\\"Analyze Statements\\\";img=\\\"analyze_" + suspectID + "\\\";" +
                      "cnd=CND:typ=checkAspect;asp=" + suspectID + "_statements_collected;cmp=EQ;val=true;" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + suspectOptions.deductionStepID
            optionCount++
        }
        
        // Always add return option
        IF optionCount > 0 { options += "|" }
        options += "BOP:onm=\\\"Return\\\";img=\\\"return_to_suspects\\\";" +
                  "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
        
        RETURN options
    }
    
    DEFINE profileOptions = CreateProfileOptions(suspectID, suspectOptions, returnPassage)
    
    // Format the SLPN
    DEFINE slpnProfilePassage = "PSG:uid=" + profileUID + ";nam=\\\"" + profileName + "\\\";CNT;BOT:lin=\\\"" + 
                             profileContent + "\\\";tag=SUSPECT_PROFILE|PROFILE;CNT;BOT:lin=\\\"" +
                             profileOptions + ";"
    
    // Validation check
    PROCEDURE ValidateSuspectProfile(slpnProfilePassage, suspectID, returnPassage) {
        VALIDATE slpnProfilePassage CONTAINS profileUID
        VALIDATE slpnProfilePassage CONTAINS suspectName AND suspectRole
        VALIDATE slpnProfilePassage CONTAINS returnPassage
        
        // Validate conditional options
        IF suspectOptions.interviewStepID {
            VALIDATE slpnProfilePassage CONTAINS suspectID + "_interview_complete" AND suspectOptions.interviewStepID
        }
        IF suspectOptions.confrontStepID {
            VALIDATE slpnProfilePassage CONTAINS suspectID + "_can_confront" AND suspectOptions.confrontStepID
        }
        IF suspectOptions.deductionStepID {
            VALIDATE slpnProfilePassage CONTAINS suspectID + "_statements_collected" AND suspectOptions.deductionStepID
        }
    }
    
    ValidateSuspectProfile(slpnProfilePassage, suspectID, returnPassage)
    
    RETURN slpnProfilePassage
}
{# END_PHENOTYPE: SUSPECT_PROFILE #}


{# PHENOTYPE: DEDUCTION_PUZZLE #}
PROCEDURE GenerateDeductionPuzzle(stepIDPrefix, entry_point_id, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, correctAnswer, successStepID, failureStepID, lockoutStepID) { // Modified Inputs
    // Primary goal: Create interactive puzzle (e.g., passcode, sequence) with attempt tracking and conditional outcomes.
    // Structure: 1. Entry/Choice -> 2. Check Outcome -> 3. Success/Retry/Lockout paths
    // Generates: Entry passage, Check Outcome passage. Success/Failure/Lockout are usually external targets.
    // Input: optionsList is list of { name: "Display Name", value: "value_to_set_in_lastAttemptAspect" }

    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Entry["_ENTRY (Choice)"] -- "Try Option A (attempts < max)" --> CheckOutcome{"_CHECK_OUTCOME"}
        Entry -- "Try Option B (attempts < max)" --> CheckOutcome
        Entry -- "Try Option N (attempts < max)" --> CheckOutcome
        Entry -- "Locked Out (attempts >= max)" --> Lockout[lockoutStepID (External)]
        
        CheckOutcome -- "Correct Answer" --> Success[successStepID (External)]
        CheckOutcome -- "Incorrect + Attempts Left" --> Entry
        CheckOutcome -- "Incorrect + No Attempts Left" --> Lockout
    ```
    */

    DEFINE entryUID = entry_point_id
    DEFINE checkOutcomeUID = stepIDPrefix + "_CHECK_OUTCOME"
    DEFINE entryName = puzzleDescription + " - Attempt"
    DEFINE checkOutcomeName = puzzleDescription + " - Check Outcome"

    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // == Passage 1: Entry / Choice ==
    PROCEDURE CreatePuzzleEntryPassage(uid, name, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, checkOutcomeUID, lockoutStepID) {
        DEFINE content = "[SEE: Puzzle Interface] [DO: " + puzzleDescription + "] [LEARN: Attempts remaining: {maxAttempts - $attemptAspect}]" // Dynamic attempt display hint
        DEFINE options = ""

        // Create options for each possible answer
        FOR EACH option IN optionsList INDEX i {
            IF i > 0 { options += "|" }
            options += "BOP:onm=\\\"" + option.name + "\\\";ods=\\\"Attempt with " + option.value + "\\\";" +
                       "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=LT;val=" + maxAttempts + ";" + // Check if attempts remain
                       "act=UAS:asp=" + attemptAspect + ";uty=INC;val=1|" + // Increment attempts
                       "UAS:asp=" + lastAttemptAspect + ";uty=SET;val=\\\"" + option.value + "\\\"|" + // Set last attempt value
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkOutcomeUID // Move to check outcome
        }

        // Add fallback option for lockout
        IF optionsList.length > 0 { options += "|" }
        options += "BOP:onm=\\\"No Attempts Left\\\";ods=\\\"The puzzle is locked.\\\";" +
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=GE;val=" + maxAttempts + ";" + // Check if locked out
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + lockoutStepID // Move directly to lockout

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_PUZZLE|ENTRY;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Make Your Choice\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";" // Re-playable until locked
    }
    DEFINE slpnPassageEntry = CreatePuzzleEntryPassage(entryUID, entryName, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, checkOutcomeUID, lockoutStepID)
    allPassages += slpnPassageEntry
    passageCounter++

    // == Passage 2: Check Outcome ==
    PROCEDURE CreateCheckOutcomePassage(uid, name, attemptAspect, maxAttempts, lastAttemptAspect, correctAnswer, successStepID, entryUID, lockoutStepID) {
        DEFINE content = "[SEE: Processing screen] [LEARN: Verifying attempt...] [DO: Wait] [FEEL: Anticipation]"
        DEFINE options = ""

        // Option 1: Correct Answer
        options += "BOP:onm=\\\"Correct Path\\\";ods=\\\"Hidden option for correct answer.\\\";" +
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=EQ;val=\\\"" + correctAnswer + "\\\";" + // Check if last attempt was correct
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successStepID // Move to success step

        // Option 2: Incorrect, Attempts Remaining
        options += "|BOP:onm=\\\"Incorrect Path (Retry)\\\";ods=\\\"Hidden option for incorrect answer with retries left.\\\";" +
                   "cnd=CAD:typ=checkAspect;lop=AND;" + // Compound AND condition
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=NE;val=\\\"" + correctAnswer + "\\\";" + // Incorrect answer
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=LT;val=" + maxAttempts + ";" + // Attempts remaining
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + entryUID // Move back to entry for another try

        // Option 3: Incorrect, No Attempts Remaining
        options += "|BOP:onm=\\\"Incorrect Path (Lockout)\\\";ods=\\\"Hidden option for incorrect answer with no retries left.\\\";" +
                   "cnd=CAD:typ=checkAspect;lop=AND;" + // Compound AND condition
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=NE;val=\\\"" + correctAnswer + "\\\";" + // Incorrect answer
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=GE;val=" + maxAttempts + ";" + // No attempts remaining
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + lockoutStepID // Move to lockout step

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_PUZZLE|CHECK_OUTCOME;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Processing\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";" // Not re-playable, it's a routing passage
    }
    // Note: The failureStepID input isn't directly used here, as failure means returning to the entryUID for another attempt. Lockout handles the final failure state.
    DEFINE slpnPassageCheckOutcome = CreateCheckOutcomePassage(checkOutcomeUID, checkOutcomeName, attemptAspect, maxAttempts, lastAttemptAspect, correctAnswer, successStepID, entryUID, lockoutStepID)
    allPassages += "\\n\\n" + slpnPassageCheckOutcome
    passageCounter++

    // Validation check
    PROCEDURE ValidateDeductionPuzzleSequence(passageCounter, attemptAspect, maxAttempts, lastAttemptAspect, successStepID, lockoutStepID) {
        VALIDATE passageCounter == 2 // Should generate Entry and CheckOutcome passages
        // Check Entry passage links correctly
        VALIDATE slpnPassageEntry CONTAINS attemptAspect AND maxAttempts AND lastAttemptAspect
        VALIDATE slpnPassageEntry CONTAINS checkOutcomeUID
        VALIDATE slpnPassageEntry CONTAINS lockoutStepID
        // Check CheckOutcome passage links correctly
        VALIDATE slpnPassageCheckOutcome CONTAINS lastAttemptAspect AND correctAnswer
        VALIDATE slpnPassageCheckOutcome CONTAINS successStepID
        VALIDATE slpnPassageCheckOutcome CONTAINS entryUID // Link back for retry
        VALIDATE slpnPassageCheckOutcome CONTAINS lockoutStepID
        VALIDATE slpnPassageCheckOutcome CONTAINS "cnd=CAD:" // Check for compound condition usage
    }
    
    ValidateDeductionPuzzleSequence(passageCounter, attemptAspect, maxAttempts, lastAttemptAspect, successStepID, lockoutStepID) // Updated validation call
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix DEDUCTION_PUZZLE_9, entry_point_id DEDUCTION_PUZZLE_9_entry, puzzleDescription "Enter Phone Passcode",
// attemptAspect "phone_attempts", maxAttempts 3, lastAttemptAspect "phone_last_code", correctAnswer "1987",
// optionsList [{name: "Code 1987", value: "1987"}, {name: "Code 0712", value: "0712"}],
// successStepID BREAKTHROUGH_10, lockoutStepID PHONE_LOCKOUT_11.
// Output includes:
// PSG:uid=DEDUCTION_PUZZLE_9_entry;nam="Enter Phone Passcode - Attempt";CNT;BOT:lin="...";brn=BRN:bds="Make Your Choice";...ops=BOP:onm="Code 1987";...cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=UAS:asp=phone_attempts;uty=INC;val=1|UAS:asp=phone_last_code;uty=SET;val="1987"|ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_CHECK_OUTCOME|BOP:onm="Code 0712";...cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=UAS:asp=phone_attempts;uty=INC;val=1|UAS:asp=phone_last_code;uty=SET;val="0712"|ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_CHECK_OUTCOME|BOP:onm="No Attempts Left";...cnd=CND:asp=phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;...;tgt=PHONE_LOCKOUT_11;
// PSG:uid=DEDUCTION_PUZZLE_9_CHECK_OUTCOME;nam="Enter Phone Passcode - Check Outcome";CNT;BOT:lin="...";brn=BRN:bds="Processing";...ops=BOP:onm="Correct Path";...cnd=CND:asp=phone_last_code;cmp=EQ;val="1987";act=ACT:aty=MOVE;...;tgt=BREAKTHROUGH_10|BOP:onm="Incorrect Path (Retry)";...cnd=CAD:...;cnd=CND:asp=phone_last_code;cmp=NE;val="1987";cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_entry|BOP:onm="Incorrect Path (Lockout)";...cnd=CAD:...;cnd=CND:asp=phone_last_code;cmp=NE;val="1987";cnd=CND:asp=phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;...;tgt=PHONE_LOCKOUT_11;
{# END_PHENOTYPE: DEDUCTION_PUZZLE #}

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

{# PHENOTYPE: BREAKTHROUGH_MOMENT #}
PROCEDURE GenerateBreakthroughMoment(stepIDPrefix, entry_point_id, breakthroughID, breakthroughName, connectedEvidence, revelation, newPathPassage, newEvidenceID) {
    // Primary goal: Create a dramatic 5-passage sequence for a critical revelation.
    // Structure: 1. Hint -> 2. Evidence A -> 3. Evidence B -> 4. Revelation -> 5. New Path
    // Input: connectedEvidence is an object like { items: ["Evidence A Name", "Evidence B Name"], newEvidenceID: "optional_new_evidence_id" }
    
    // Define UIDs
    DEFINE hintUID = entry_point_id
    DEFINE evidenceAUID = stepIDPrefix + "_EVID_A"
    DEFINE evidenceBUID = stepIDPrefix + "_EVID_B" // Assuming 2 pieces of connected evidence for simplicity
    DEFINE revealUID = stepIDPrefix + "_REVEAL"
    DEFINE newPathUID = stepIDPrefix + "_NEWPATH"

    DEFINE hintName = breakthroughName + " - Hint"
    DEFINE evidenceAName = breakthroughName + " - Connection 1"
    DEFINE evidenceBName = breakthroughName + " - Connection 2"
    DEFINE revealName = breakthroughName + " - Revelation!"
    DEFINE newPathName = "New Lead: " + breakthroughName

    DEFINE allPassages = ""

    // == Passage 1: Hint ==
    PROCEDURE CreateHintPassage(uid, name, breakthroughName, nextPassageUID) {
        DEFINE content = "[FEEL: Mounting tension...] [LEARN: Something isn't adding up regarding " + breakthroughName + ". Let's look closer.]"
        DEFINE options = "BOP:onm=\\\"Examine Connection\\\";ods=\\\"Review the first piece of related evidence\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=BREAKTHROUGH_MOMENT|HINT;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Developing Lead\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateHintPassage(hintUID, hintName, breakthroughName, evidenceAUID)
    allPassages += slpnPassage1

    // == Passage 2: Evidence A Connection ==
    PROCEDURE CreateEvidenceAPassage(uid, name, evidenceAName, nextPassageUID) {
        DEFINE content = "[SEE: Focus on " + evidenceAName + "] [LEARN: Considering this piece of evidence...] [DO: Recall its significance.]"
        DEFINE options = "BOP:onm=\\\"Connect Second Piece\\\";ods=\\\"Bring in the related evidence\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=BREAKTHROUGH_MOMENT|EVIDENCE_A;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Connecting Evidence\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateEvidenceAPassage(evidenceAUID, evidenceAName, connectedEvidence.items[0], evidenceBUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Evidence B Connection ==
    PROCEDURE CreateEvidenceBPassage(uid, name, evidenceBName, nextPassageUID) {
        DEFINE content = "[SEE: Focus on " + evidenceBName + "] [LEARN: And when combined with this piece...] [DO: What does this reveal?]"
        DEFINE options = "BOP:onm=\\\"The Revelation!\\\";ods=\\\"See the critical connection\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=BREAKTHROUGH_MOMENT|EVIDENCE_B;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Connecting Evidence\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateEvidenceBPassage(evidenceBUID, evidenceBName, connectedEvidence.items[1], revealUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Revelation ==
    PROCEDURE CreateRevelationPassage(uid, name, connectedEvidence, revelation, nextPassageUID) {
        DEFINE formattedEvidence = FormatConnectedEvidence(connectedEvidence.items) // Reuse existing helper if available, else simple join
        DEFINE content = "[SEE: Dramatic visualization of connection!] [FEEL: Breakthrough!] [LEARN: Critical connection between " + formattedEvidence + " reveals: '" + revelation + "']"
        DEFINE options = "BOP:onm=\\\"Follow This Lead\\\";ods=\\\"Pursue the new direction\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=BREAKTHROUGH_MOMENT|REVELATION;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Breakthrough!\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage4 = CreateRevelationPassage(revealUID, revealName, connectedEvidence, revelation, newPathUID)
    allPassages += "\n\n" + slpnPassage4

    // == Passage 5: New Path Opened ==
    PROCEDURE CreateNewPathPassage(uid, name, breakthroughID, newPathPassage, newEvidenceID) {
        DEFINE content = "[INFO: A new path in the investigation has opened based on this breakthrough.]"
        
        DEFINE actions = "UAS:asp=breakthrough_" + breakthroughID + "_found;uty=SET;val=true"
        IF newEvidenceID { // Check if newEvidenceID was provided in connectedEvidence
            actions += "|ACT:aty=REVEAL;aet=" + newEvidenceID
        }
        actions += "|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + newPathPassage

        DEFINE options = "BOP:onm=\\\"Proceed\\\";ods=\\\"Enter the next stage of investigation\\\";act=" + actions
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"New Lead\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage5 = CreateNewPathPassage(newPathUID, newPathName, breakthroughID, newPathPassage, connectedEvidence.newEvidenceID)
    allPassages += "\n\n" + slpnPassage5

    // Validation check
    PROCEDURE ValidateBreakthroughMomentSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, slpnPassage5, breakthroughID, newPathPassage) {
        VALIDATE slpnPassage1 CONTAINS hintUID AND evidenceAUID
        VALIDATE slpnPassage2 CONTAINS evidenceAUID AND evidenceBUID
        VALIDATE slpnPassage3 CONTAINS evidenceBUID AND revealUID
        VALIDATE slpnPassage4 CONTAINS revealUID AND newPathUID AND revelation
        VALIDATE slpnPassage5 CONTAINS newPathUID AND "breakthrough_" + breakthroughID + "_found" AND newPathPassage
    }
    
    ValidateBreakthroughMomentSequence(slpnPassage1, slpnPassage2, slpnPassage3, slpnPassage4, slpnPassage5, breakthroughID, newPathPassage)
    
    RETURN allPassages
}

// Helper functions
FUNCTION FormatConnectedEvidence(evidenceItemsList) { // Assuming this helper exists or is simple
    IF evidenceItemsList.length == 2 { RETURN evidenceItemsList[0] + " and " + evidenceItemsList[1] }
    // Add more robust formatting if needed
    RETURN String.join(evidenceItemsList, ", ")
}

// Example output:
// Assume stepIDPrefix is BREAKTHROUGH_MOMENT_13, breakthroughID is 'timeline', breakthroughName is "Timeline Discrepancy", 
// connectedEvidence = { items: ["Security Footage", "Suspect Statements"], newEvidenceID: "timeline_contradiction" },
// revelation = "The victim left the studio at 9:30 PM, contradicting Marcus's claim.", newPathPassage is SUSPECT_CONFRONTATION_14.
// Output includes 5 passages: _HINT, _EVID_A, _EVID_B, _REVEAL, _NEWPATH, linked sequentially.
// _NEWPATH passage sets aspect 'breakthrough_timeline_found', reveals 'timeline_contradiction', and moves to SUSPECT_CONFRONTATION_14.
{# END_PHENOTYPE: BREAKTHROUGH_MOMENT #}
// ... existing code ...

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
        DEFINE options = "BOP:onm=\\\"Confront " + suspectName + "\\\";ods=\\\"Present the evidence directly\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Initiate Confrontation\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateApproachPassage(approachUID, approachName, suspectName, presentUID)
    allPassages += slpnPassage1

    // == Passage 2: Present Evidence ==
    PROCEDURE CreatePresentPassage(uid, name, evidencePresentedName, suspectName, nextPassageUID) {
        DEFINE content = "[LEARN: You present the \'" + evidencePresentedName + "\' to " + suspectName + ".] [DO: Observe their reaction closely.]"
        DEFINE options = "BOP:onm=\\\"See Reaction\\\";ods=\\\"How do they respond? \\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Evidence Presented\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreatePresentPassage(presentUID, presentName, evidencePresentedName, suspectName, reactionUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Reaction ==
    PROCEDURE CreateReactionPassage(uid, name, suspectReaction, nextPassageUID) {
        DEFINE content = "[SEE: " + suspectName + " reacts.] [LEARN: Reaction: '" + suspectReaction + "'] [FEEL: Assess their response - truth, deflection, anger?]"
        DEFINE options = "BOP:onm=\\\"Decide Next Move\\\";ods=\\\"Consider your options\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Suspect Reaction\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateReactionPassage(reactionUID, reactionName, suspectReaction, optionsUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Options ==
    PROCEDURE CreateOptionsPassage(uid, name, suspectID, nextStepPassage, additionalEvidenceID, finalConfrontationStepID) {
        DEFINE content = "[DO: How do you proceed? Press further or step back?]"
        DEFINE options = ""
        
        // Conditional option to press further if additional evidence exists
        IF additionalEvidenceID AND finalConfrontationStepID {
            options += "BOP:onm=\\\"Press Further\\\";ods=\\\"Present additional evidence\\\";" +
                      "cnd=CND:typ=checkAspect;asp=" + additionalEvidenceID + "_found;cmp=EQ;val=true;" + // Check if the addtl evidence is found/unlocked
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + finalConfrontationStepID
        }

        // Option to return to investigation hub/next step
        IF options != "" { options += "|" }
        options += "BOP:onm=\\\"Step Back\\\";ods=\\\"Return to investigation, consider implications\\\";" +
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextStepPassage // Target the main hub or next logical step

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Confrontation Options\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";"
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
// ... existing code ...

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

//PRAGMA MARK: NARRATIVE
# Narrative Delivery Phenotype Dictionary

This dictionary defines the composable building blocks for presenting narrative information (derived from Story Phenotypes: Definitions, Propositions, Axioms) to the player within the gameplay flow. These phenotypes describe *how* story elements are delivered, integrating with the Gameplay Phenotypes and functioning as connectable sub-graphs within the overall gameplay journey. **Core Principle: Show, Don't Tell - Reveal evidence, guide player interpretation.**

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
    //     speakerImage: (String) Optional image alias for character portrait,
    //     dialogue: (String) The spoken text,
    //     backgroundImage: (String) Image for the slide background,
    //     backgroundDescription: (String) Description of the scene,
    //     emotion: (String) Optional emotional tone for context,
    //     isThought: (Boolean) Optional flag for internal thoughts vs spoken dialogue
    //   }
    // nextPassageID: (String) The passage to transition to after the dialogue sequence.

    // --- Logic ---
    // 1. Convert dialogue exchanges to intro slides format
    DEFINE introSlides = []
    
    FOR EACH exchange IN dialogueExchanges INDEX i {
        DEFINE slide = {}
        
        // Generate a unique ID for this dialogue slide
        slide.id = "dialogue_" + i
        
        // Use speaker name for slide name
        slide.name = exchange.speakerName
        
        // Use provided background image
        slide.backgroundImage = exchange.backgroundImage
        slide.imageDescription = exchange.backgroundDescription
        
        // Format dialogue content with appropriate tags
        DEFINE dialoguePrefix = IF exchange.isThought THEN "[THINK: " ELSE "[HEAR: "
        DEFINE formattedDialogue = dialoguePrefix + exchange.speakerName + ": \"" + exchange.dialogue + "\"]"
        
        // Add visual and emotional context
        DEFINE visualContext = "[SEE: " + (exchange.speakerImage ? exchange.speakerName + " " + exchange.speakerImage : slide.backgroundDescription) + "]"
        DEFINE emotionalContext = exchange.emotion ? "[FEEL: " + exchange.emotion + "]" : ""
        
        // Combine all content elements
        slide.content = formattedDialogue + " " + visualContext + " " + emotionalContext
        
        // Add target passage ID to last slide only
        IF i == dialogueExchanges.length - 1 {
            slide.targetPassageID = nextPassageID
        }
        
        // Add to slides collection
        introSlides[i] = slide
    }
    
    // 2. Use the standard intro sequence generator
    RETURN GenerateIntroSequence(stepIDPrefix, entry_point_id, sequenceTitle, introSlides, null)
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

GenerateDialogueSequence("CASE_01_INTERROGATION", "ENTRY_POINT_3", "First Interrogation", detectiveDialogue, "SUSPECT_PROFILE_4")
*/
{# END_PHENOTYPE: NARRATIVE_DIALOGUE_SEQUENCE #}


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
    // 1. Convert cutscene shots to intro slides format
    DEFINE introSlides = []
    
    FOR EACH shot IN cutsceneShots INDEX i {
        DEFINE slide = {}
        
        // Generate a unique ID for this cutscene shot
        slide.id = "cutscene_" + i
        
        // Use shot name for slide name
        slide.name = shot.shotName
        
        // Use provided background image
        slide.backgroundImage = shot.backgroundImage
        slide.imageDescription = shot.imageDescription
        
        // Format content with appropriate tags
        DEFINE narrativeContext = "[LEARN: " + shot.narration + "]"
        DEFINE visualContext = "[SEE: " + shot.imageDescription + "]"
        DEFINE emotionalContext = shot.emotionalTone ? "[FEEL: " + shot.emotionalTone + "]" : ""
        DEFINE temporalContext = shot.timeContext ? "[TIME: " + shot.timeContext + "]" : ""
        
        // Combine all content elements
        slide.content = narrativeContext + " " + visualContext + " " + emotionalContext + " " + temporalContext
        
        // Create a dramatic button text for transitions between shots
        DEFINE buttonText = ""
        IF i == cutsceneShots.length - 1 {
            // Last shot
            buttonText = "Continue"
        } ELSE {
            // Choose a dramatic transition based on emotional tone
            buttonText = ChooseDramaticTransition(shot.emotionalTone)
        }
        slide.buttonText = buttonText
        
        // Add target passage ID to last slide only
        IF i == cutsceneShots.length - 1 {
            slide.targetPassageID = nextPassageID
        }
        
        // Add to slides collection
        introSlides[i] = slide
    }
    
    // 2. Use the standard intro sequence generator
    RETURN GenerateIntroSequence(stepIDPrefix, entry_point_id, sequenceTitle, introSlides, null)
}

// Helper function for choosing dramatic transition text based on emotional tone
FUNCTION ChooseDramaticTransition(emotionalTone) {
    IF emotionalTone == "suspense" OR emotionalTone == "tension" OR emotionalTone == "mystery" {
        RETURN "And then..."
    } ELSE IF emotionalTone == "dread" OR emotionalTone == "fear" OR emotionalTone == "horror" {
        RETURN "Suddenly..."
    } ELSE IF emotionalTone == "revelation" OR emotionalTone == "realization" {
        RETURN "It becomes clear..."
    } ELSE IF emotionalTone == "sadness" OR emotionalTone == "grief" {
        RETURN "Meanwhile..."
    } ELSE IF emotionalTone == "hope" OR emotionalTone == "triumph" {
        RETURN "But then..."
    } ELSE {
        RETURN "Next"
    }
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

GenerateCutsceneSequence("CASE_01_INTRO", "ENTRY_POINT_1", "The Night Of", crimeMontage, "INVESTIGATION_HUB_1")
*/
{# END_PHENOTYPE: NARRATIVE_CUTSCENE_SEQUENCE #}


{# PHENOTYPE: NARRATIVE_EVIDENCE_SNIPPET (Revised from INFO_SNIPPET) #}

PROCEDURE DeliverEvidenceSnippet(stepIDPrefix, representingEvidenceID, contextText_Optional, nextTargetID, triggeringContext) {
    // Primary Goal: Make the player aware of and grant access to a specific piece of pre-defined evidence containing a narrative detail.
    // Integration: Triggered after Gameplay Phenotypes like EVIDENCE_EXAMINATION, SUSPECT_PROFILE updates, DEDUCTION_SUCCESS, or discovery events. Guides player to examine the new evidence.

    // --- Generation Context ---
    // Entry Point Construction: The primary (and only) passage generated will use the UID: stepIDPrefix + "_evidenceSnippet_" + representingEvidenceID. Targetable entry point.
    // Targeting Requirements: The 'nextTargetID' MUST be a valid subsequent UID ('next_steps'), the EVIDENCE application target, or a relevant DEDUCTION_PUZZLE UID. Ensures correct outward connection for interpretation.
    // Graph Structure: Single node sub-graph. Reveals evidence, then moves player towards examination/deduction.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating the unique passage UID.
    // representingEvidenceID: (String) REQUIRED. The unique ID (aet) of the pre-defined evidence item containing the narrative snippet.
    // contextText_Optional: (String, Optional) Brief text displayed via BOT *before* the reveal action (e.g., "You notice something relevant...", "A new report is available.").
    // nextTargetID: (String) The passage UID or application target (usually EVIDENCE) to navigate to after revealing the evidence.
    // triggeringContext: (String) Description of what gameplay event triggered this.

    // --- Logic ---
    // 1. Prepare optional context text.
    DEFINE escapedContextText = ""
    IF contextText_Optional IS NOT NULL {
        escapedContextText = EscapeStringForSLPN(contextText_Optional)
    }
    // 2. Construct SLPN commands.
    DEFINE passageUID = stepIDPrefix + "_evidenceSnippet_" + representingEvidenceID // Construct entry point UID.
    DEFINE passageName = "Evidence Found: " + representingEvidenceID
    DEFINE passageTag = "NARRATIVE|REVEAL|EVIDENCE|INFO"
    DEFINE commandSequence = ""
    // Command 1 (Optional): Display context text.
    IF escapedContextText != "" {
        commandSequence += "BOT:lin=\"" + escapedContextText + "\";"
    }
    // Command 2: Reveal the evidence item.
    commandSequence += "ACT:aty=REVEAL;aet=" + representingEvidenceID + ";"
    // Command 3: Navigate towards interpretation.
    commandSequence += "ACT:aty=MOVE;amt=AMT:typ=" + GetTargetType(nextTargetID) + ";tgt=" + nextTargetID + ";"
    // 3. Combine into the full SLPN passage definition.
    DEFINE fullPassageSLPN = "PSG:uid=" + passageUID + ";nam=\"" + passageName + "\";tag=" + passageTag + ";" + commandSequence

    RETURN fullPassageSLPN
}
{# END_PHENOTYPE: NARRATIVE_EVIDENCE_SNIPPET (Revised from INFO_SNIPPET) #}

{# PHENOTYPE: NARRATIVE_EVIDENCE_FOR_RELATIONSHIP (Revised for Show, Don't Tell) #}

PROCEDURE DeliverRelationshipEvidence(stepIDPrefix, relationshipID, sourceEvidenceID, contextText_Optional, nextTargetID, triggeringContext) {
    // Primary Goal: Make the player aware of and grant access to a specific piece of pre-defined evidence that reveals information about a relationship. Focuses on revealing the evidence item itself.
    // Integration: Triggered after deductions, examining related items, or key dialogue, leading the player to examine the evidence.

    // --- Generation Context ---
    // Entry Point Construction: The primary passage generated will use the UID: stepIDPrefix + "_relEvidence_" + sourceEvidenceID. This is the targetable entry point.
    // Targeting Requirements: The 'nextTargetID' MUST correspond to a valid subsequent UID ('next_steps'), a relevant DEDUCTION_PUZZLE UID, or the EVIDENCE application target. Ensures correct outward connection for player interpretation.
    // Graph Structure: Generates a single node sub-graph. Reveals evidence and directs the player towards interpretation (via examining evidence or deduction).

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating the unique passage UID.
    // relationshipID: (String) The Relationship_Definition this evidence pertains to (for context/naming).
    // sourceEvidenceID: (String) REQUIRED. The unique ID (aet) of the pre-defined evidence item containing the relationship information.
    // contextText_Optional: (String, Optional) Brief text displayed via BOT *before* the reveal action (e.g., "You found messages discussing their connection.").
    // nextTargetID: (String) The passage UID or application target (usually EVIDENCE or a DEDUCTION_PUZZLE UID) to navigate to after the reveal.
    // triggeringContext: (String) Description of what gameplay event triggered this.

    // --- Logic ---
    // 1. Prepare optional context text.
    DEFINE escapedContextText = ""
    IF contextText_Optional IS NOT NULL {
        escapedContextText = EscapeStringForSLPN(contextText_Optional)
    }
    // 2. Generate SLPN for the passage.
    DEFINE passageUID = stepIDPrefix + "_relEvidence_" + sourceEvidenceID // Construct entry point UID.
    DEFINE passageName = "Evidence Found: Relationship " + relationshipID
    DEFINE passageTag = "NARRATIVE|REVEAL|EVIDENCE|RELATIONSHIP"
    DEFINE commandSequence = ""
    // Command 1 (Optional): Display context text.
    IF escapedContextText != "" {
        commandSequence += "BOT:lin=\"" + escapedContextText + "\";"
    }
    // Command 2: Reveal the actual evidence item.
    commandSequence += "ACT:aty=REVEAL;aet=" + sourceEvidenceID + ";"
    // Command 3: Navigate player towards interpretation.
    commandSequence += "ACT:aty=MOVE;amt=AMT:typ=" + GetTargetType(nextTargetID) + ";tgt=" + nextTargetID + ";"
    // 4. Combine into the full SLPN passage definition.
    DEFINE fullPassageSLPN = "PSG:uid=" + passageUID + ";nam=\"" + passageName + "\";tag=" + passageTag + ";" + commandSequence

    RETURN fullPassageSLPN
}
{# END_PHENOTYPE: NARRATIVE_EVIDENCE_FOR_RELATIONSHIP (Revised for Show, Don't Tell) #}

{# PHENOTYPE: NARRATIVE_EVIDENCE_FOR_MOTIVE (Revised from MOTIVE_HINT) #}

PROCEDURE DeliverMotiveEvidence(stepIDPrefix, motiveID, sourceEvidenceID, contextText_Optional, nextTargetID, triggeringContext) {
    // Primary Goal: Reveal a specific piece of pre-defined evidence that suggests or confirms a character's motive.
    // Integration: Triggered by analyzing related evidence, suspect profiles, or dialogue. Guides player to examine the revealed evidence.

    // --- Generation Context ---
    // Entry Point Construction: The passage UID will be: stepIDPrefix + "_motiveEvidence_" + sourceEvidenceID. Targetable entry point.
    // Targeting Requirements: 'nextTargetID' MUST be a valid subsequent UID ('next_steps'), the EVIDENCE application target, or a relevant DEDUCTION_PUZZLE UID.
    // Graph Structure: Single node sub-graph. Reveals motive-related evidence, moves player towards interpretation.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating the unique passage UID.
    // motiveID: (String) The Motive_Definition this evidence pertains to (for context/naming).
    // sourceEvidenceID: (String) REQUIRED. The unique ID (aet) of the pre-defined evidence item implying/stating the motive.
    // contextText_Optional: (String, Optional) Brief BOT text displayed before the reveal (e.g., "Financial records indicate...", "A witness statement mentions...").
    // nextTargetID: (String) Passage UID or application target (usually EVIDENCE or DEDUCTION_PUZZLE) to navigate to.
    // triggeringContext: (String) Description of what gameplay event triggered this.

    // --- Logic ---
    // 1. Prepare optional context text.
    DEFINE escapedContextText = ""
    IF contextText_Optional IS NOT NULL {
        escapedContextText = EscapeStringForSLPN(contextText_Optional)
    }
    // 2. Generate SLPN.
    DEFINE passageUID = stepIDPrefix + "_motiveEvidence_" + sourceEvidenceID // Construct entry point UID.
    DEFINE passageName = "Evidence Found: Motive " + motiveID
    DEFINE passageTag = "NARRATIVE|REVEAL|EVIDENCE|MOTIVE"
    DEFINE commandSequence = ""
    // Command 1 (Optional): Display context.
    IF escapedContextText != "" {
        commandSequence += "BOT:lin=\"" + escapedContextText + "\";"
    }
    // Command 2: Reveal the evidence.
    commandSequence += "ACT:aty=REVEAL;aet=" + sourceEvidenceID + ";"
    // Command 3: Navigate towards interpretation.
    commandSequence += "ACT:aty=MOVE;amt=AMT:typ=" + GetTargetType(nextTargetID) + ";tgt=" + nextTargetID + ";"
    // 3. Combine.
    DEFINE fullPassageSLPN = "PSG:uid=" + passageUID + ";nam=\"" + passageName + "\";tag=" + passageTag + ";" + commandSequence

    RETURN fullPassageSLPN
}
{# END_PHENOTYPE: NARRATIVE_EVIDENCE_FOR_MOTIVE (Revised from MOTIVE_HINT) #}

{# PHENOTYPE: NARRATIVE_EVIDENCE_FOR_FLASHBACK (Revised from FLASHBACK_FRAGMENT) #}

PROCEDURE DeliverFlashbackEvidence(stepIDPrefix, interactionID, flashbackEvidenceID, contextText_Optional, nextTargetID, triggeringContext) {
    // Primary Goal: Reveal a pre-defined evidence item (diary, log, testimony) that represents a past event (Interaction_Proposition).
    // Integration: Triggered by examining relevant objects, locations, or dialogue. Guides player to examine the evidence representing the flashback.

    // --- Generation Context ---
    // Entry Point Construction: The passage UID: stepIDPrefix + "_flashbackEvidence_" + flashbackEvidenceID. Targetable entry point.
    // Targeting Requirements: 'nextTargetID' MUST be a valid subsequent UID ('next_steps') or the EVIDENCE application target.
    // Graph Structure: Single node sub-graph. Reveals flashback-related evidence, moves player towards examination.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating the unique passage UID.
    // interactionID: (String) The Interaction_Proposition this evidence describes (for context/naming).
    // flashbackEvidenceID: (String) REQUIRED. The `aet` ID of the pre-defined evidence item containing the flashback details (e.g., a diary page, a security log entry).
    // contextText_Optional: (String, Optional) Brief BOT text displayed before reveal (e.g., "You found an old diary entry...", "Security logs show...").
    // nextTargetID: (String) Passage UID or application target (usually EVIDENCE) to navigate to.
    // triggeringContext: (String) Description of what gameplay event triggered this.

    // --- Logic ---
    // 1. Prepare optional context text.
    DEFINE escapedContextText = ""
    IF contextText_Optional IS NOT NULL {
        escapedContextText = EscapeStringForSLPN(contextText_Optional)
    }
    // 2. Generate SLPN.
    DEFINE passageUID = stepIDPrefix + "_flashbackEvidence_" + flashbackEvidenceID // Construct entry point UID.
    DEFINE passageName = "Evidence Found: Flashback " + interactionID
    DEFINE passageTag = "NARRATIVE|REVEAL|EVIDENCE|FLASHBACK"
    DEFINE commandSequence = ""
    // Command 1 (Optional): Display context.
    IF escapedContextText != "" {
        commandSequence += "BOT:lin=\"" + escapedContextText + "\";"
    }
    // Command 2: Reveal the evidence.
    commandSequence += "ACT:aty=REVEAL;aet=" + flashbackEvidenceID + ";"
    // Command 3: Navigate towards examination.
    commandSequence += "ACT:aty=MOVE;amt=AMT:typ=" + GetTargetType(nextTargetID) + ";tgt=" + nextTargetID + ";"
    // 3. Combine.
    DEFINE fullPassageSLPN = "PSG:uid=" + passageUID + ";nam=\"" + passageName + "\";tag=" + passageTag + ";" + commandSequence

    RETURN fullPassageSLPN
}
{# END_PHENOTYPE: NARRATIVE_EVIDENCE_FOR_FLASHBACK (Revised from FLASHBACK_FRAGMENT) #}

{# PHENOTYPE: NARRATIVE_EVIDENCE_FOR_REFLECTION (Revised from CHARACTER_REFLECTION) #}

PROCEDURE DeliverReflectionEvidence(stepIDPrefix, characterID, observationEvidenceID, contextText_Optional, nextTargetID, triggeringContext) {
    // Primary Goal: Reveal a pre-defined "observation" evidence item describing a character's likely internal state or reaction, based on events.
    // Integration: Triggered after confrontations, viewing profiles, or significant events. Guides player to examine the observation evidence.

    // --- Generation Context ---
    // Entry Point Construction: The passage UID: stepIDPrefix + "_reflectionEvidence_" + observationEvidenceID. Targetable entry point.
    // Targeting Requirements: 'nextTargetID' MUST be a valid subsequent UID ('next_steps'), the EVIDENCE application target, or a relevant DEDUCTION_PUZZLE UID.
    // Graph Structure: Single node sub-graph. Reveals observation evidence, moves player towards examination or deduction.

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating the unique passage UID.
    // characterID: (String) The Character_Definition this observation pertains to (for context/naming).
    // observationEvidenceID: (String) REQUIRED. The `aet` ID of the pre-defined evidence item containing the observation text (e.g., "Observation: James seemed nervous").
    // contextText_Optional: (String, Optional) Brief BOT text displayed before reveal (e.g., "You recall James' reaction...", "Your observations suggest...").
    // nextTargetID: (String) Passage UID or application target (usually EVIDENCE or DEDUCTION_PUZZLE) to navigate to.
    // triggeringContext: (String) Description of what gameplay event triggered this.

    // --- Logic ---
    // 1. Prepare optional context text.
    DEFINE escapedContextText = ""
    IF contextText_Optional IS NOT NULL {
        escapedContextText = EscapeStringForSLPN(contextText_Optional)
    }
    // 2. Generate SLPN.
    DEFINE passageUID = stepIDPrefix + "_reflectionEvidence_" + observationEvidenceID // Construct entry point UID.
    DEFINE passageName = "Evidence Found: Reflection " + characterID
    DEFINE passageTag = "NARRATIVE|REVEAL|EVIDENCE|REFLECTION"
    DEFINE commandSequence = ""
    // Command 1 (Optional): Display context.
    IF escapedContextText != "" {
        commandSequence += "BOT:lin=\"" + escapedContextText + "\";"
    }
    // Command 2: Reveal the observation evidence.
    commandSequence += "ACT:aty=REVEAL;aet=" + observationEvidenceID + ";"
    // Command 3: Navigate towards interpretation/deduction.
    commandSequence += "ACT:aty=MOVE;amt=AMT:typ=" + GetTargetType(nextTargetID) + ";tgt=" + nextTargetID + ";"
    // 3. Combine.
    DEFINE fullPassageSLPN = "PSG:uid=" + passageUID + ";nam=\"" + passageName + "\";tag=" + passageTag + ";" + commandSequence

    RETURN fullPassageSLPN
}
{# END_PHENOTYPE: NARRATIVE_EVIDENCE_FOR_REFLECTION (Revised from CHARACTER_REFLECTION) #} 

// PRAGMA MARK: DIAGNOSTIC

{# PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}

PROCEDURE GenerateDiagnosticEntryPoint(stepIDPrefix, entry_point_id, testCaseID, testDescription, initialState, nextPassageID) {
    // Primary goal: Create the entry point for a test sequence that initializes the testing environment
    // Structure: Single passage that sets up initial conditions and directs to the first test passage

    // Define UID for this passage
    DEFINE entryUID = entry_point_id // Use the provided entry_point_id
    DEFINE entryName = "Test Case " + testCaseID + ": Entry Point"
    
    // Create descriptive text for the test initialization
    PROCEDURE CreateEntryContent(testDescription) {
        RETURN "Diagnostic Test Case " + testCaseID + ": " + testDescription
    }
    
    // Create state initialization commands
    PROCEDURE CreateInitialStateCommands(initialState) {
        DEFINE stateCommands = ""
        
        // Loop through all initial state variables and create SET commands
        FOR EACH key, value IN initialState {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                stateCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                stateCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        RETURN stateCommands
    }
    
    // Generate SLPN for this passage
    DEFINE entryContent = CreateEntryContent(testDescription)
    DEFINE stateCommands = CreateInitialStateCommands(initialState)
    
    DEFINE slpnPassage = "BOT:lin=\"" + entryContent + "\";\n" +
                        stateCommands + "\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateEntryPoint(slpnPassage, initialState, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Diagnostic Test Case"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all initial state variables are set
        FOR EACH key IN initialState {
            VALIDATE slpnPassage CONTAINS key
        }
    }
    
    ValidateEntryPoint(slpnPassage, initialState, nextPassageID)
    
    RETURN slpnPassage
}

// Helper function to determine data type for setting state variables correctly
FUNCTION GetDataType(value) {
    IF typeof(value) == "boolean" {
        RETURN "boolean"
    } ELSE IF typeof(value) == "number" {
        RETURN "number"
    } ELSE {
        RETURN "string"
    }
}

{# END_PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}

{# PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}

PROCEDURE GenerateDiagnosticLinearTest(stepIDPrefix, entry_point_id, testCaseID, stepNumber, totalSteps, stateChanges, nextPassageID) {
    // Primary goal: Create a straightforward test passage that modifies state and proceeds linearly
    // Structure: Single passage that tests simple progression and state modification

    // Define UID for this passage
    DEFINE linearUID = entry_point_id // Use the provided entry_point_id
    DEFINE linearName = "Test Case " + testCaseID + ": Linear Test Step " + stepNumber
    
    // Create descriptive text for the test step
    PROCEDURE CreateLinearContent(stepNumber, totalSteps) {
        RETURN "Testing linear progression (Step " + stepNumber + " of " + totalSteps + ")"
    }
    
    // Create state change commands
    PROCEDURE CreateStateChangeCommands(stateChanges, stepNumber) {
        DEFINE changeCommands = ""
        
        // Loop through all state changes and create SET commands
        FOR EACH key, value IN stateChanges {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                changeCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                changeCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        // Add a completed flag for this step
        changeCommands += "SET:evt=TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE;val=true;"
        
        RETURN changeCommands
    }
    
    // Generate SLPN for this passage
    DEFINE linearContent = CreateLinearContent(stepNumber, totalSteps)
    DEFINE changeCommands = CreateStateChangeCommands(stateChanges, stepNumber)
    
    DEFINE slpnPassage = "BOT:lin=\"" + linearContent + "\";\n" +
                         changeCommands + "\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing linear progression"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all state changes are set
        FOR EACH key IN stateChanges {
            VALIDATE slpnPassage CONTAINS key
        }
        
        // Verify step completion flag
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE"
    }
    
    ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}

{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}

PROCEDURE GenerateDiagnosticBranchTestBinary(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditionValue, pathAPassageID, pathBPassageID) {
    // Primary goal: Create a passage that tests binary branching based on a condition
    // Structure: Single passage with condition-based branching to two different paths

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Binary Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateBranchContent() {
        RETURN "Testing binary branching condition"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateBranchContent()
    
    // Create two branch options for true and false conditions
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=ada;" +
                        "ops=BOP:onm=\"If " + conditionVar + " = " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathAPassageID + ";" +
                        "ops=BOP:onm=\"If " + conditionVar + " ≠ " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=ne;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathBPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing binary branching condition"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS pathAPassageID
        VALIDATE slpnPassage CONTAINS pathBPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        VALIDATE slpnPassage CONTAINS "ops=BOP"
    }
    
    ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}

{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}

PROCEDURE GenerateDiagnosticBranchTestMulti(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditions, defaultPassageID) {
    // Primary goal: Create a passage that tests multi-way branching based on different values of a condition
    // Structure: Single passage with multi-way branching based on variable value
    // Input: conditions is a list of objects { value: valueToCheck, targetPassageID: passageIDForThisValue }

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Multi-way Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateMultiBranchContent() {
        RETURN "Testing multi-way branching conditions"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateMultiBranchContent()
    
    // Start with the branch header and bot line
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=ada;"
    
    // Loop through conditions to create branch options
    FOR EACH condition IN conditions {
        slpnPassage += "ops=BOP:onm=\"If " + conditionVar + " = " + condition.value + "\";" +
                      "chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + condition.value + ";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + condition.targetPassageID + ";"
    }
    
    // Add the default case (fallback option)
    slpnPassage += "ops=BOP:onm=\"Default Case\";act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + defaultPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing multi-way branching conditions"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS defaultPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        
        // Verify all target passages are included
        FOR EACH condition IN conditions {
            VALIDATE slpnPassage CONTAINS condition.targetPassageID
        }
    }
    
    ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}

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

{# PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}

PROCEDURE GenerateDiagnosticEvidenceExamination(stepIDPrefix, entry_point_id, testCaseID, evidenceID, attributeData, successPassageID, failPassageID) {
    // Primary goal: Create a passage that tests evidence examination and attribute discovery
    // Structure: Series of passages that sets evidence attributes and branches based on examination state
    // Input: attributeData is an object mapping attribute names to values

    // Define UIDs for the passage sequence
    DEFINE examineUID = entry_point_id
    DEFINE examineName = "Test Case " + testCaseID + ": Evidence Examination Test"
    DEFINE setStateUID = "diag_exam_" + testCaseID + "_set_state"
    DEFINE checkStateUID = "diag_exam_" + testCaseID + "_check_state"
    DEFINE successUID = "diag_exam_" + testCaseID + "_success"
    DEFINE failUID = "diag_exam_" + testCaseID + "_fail"
    
    // Create descriptive text for each passage
    PROCEDURE CreateStartContent() {
        RETURN "Testing evidence examination and attribute discovery for " + evidenceID + "."
    }
    
    PROCEDURE CreateSetStateContent() {
        RETURN "Setting state for " + evidenceID + "."
    }
    
    PROCEDURE CreateCheckContent() {
        RETURN "Checking state..."
    }
    
    PROCEDURE CreateSuccessContent() {
        RETURN "Attributes and examined status were set correctly."
    }
    
    PROCEDURE CreateFailContent() {
        RETURN "Attributes and examined status were NOT set correctly."
    }
    
    // Create attribute commands for setting state
    PROCEDURE CreateAttributeSettings(evidenceID, attributeData) {
        DEFINE attributeCommands = ""
        
        // Set the main examined flag
        attributeCommands += "SET:evt=" + evidenceID + "_EXAMINED;val=true;"
        
        // Set each attribute value
        FOR EACH attrName, attrValue IN attributeData {
            attributeCommands += "UAS:asp=" + attrName + ";uty=SET;val=\"" + attrValue + "\";"
        }
        
        RETURN attributeCommands
    }
    
    // 1. Create the start passage with branch to set state
    DEFINE startContent = CreateStartContent()
    DEFINE startPassage = "PSG:uid=" + examineUID + ";nam=\"" + examineName + "\";\n" +
                         "BOT:lin=\"" + startContent + "\";\n" +
                         "brn=BRN:bds=\"Start Test Step\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Begin Examination Test\";ods=\"Proceed to the next step in the diagnostic sequence\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + setStateUID + ";"
    
    // 2. Create the set state passage
    DEFINE setStateContent = CreateSetStateContent()
    DEFINE attributeCommands = CreateAttributeSettings(evidenceID, attributeData)
    DEFINE setStatePassage = "PSG:uid=" + setStateUID + ";nam=\"Set Evidence Attributes\";\n" +
                            "BOT:lin=\"" + setStateContent + "\";\n" +
                            attributeCommands + "\n" +
                            "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkStateUID + ";"
    
    // 3. Create the check state passage with branch
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkStatePassage = "PSG:uid=" + checkStateUID + ";nam=\"Verify Evidence State\";\n" +
                              "BOT:lin=\"" + checkContent + "\";\n" +
                              "brn=BRN:bds=\"Verify State\";brp=once;bpr=option-list;bit=ada;" +
                              "ops=BOP:onm=\"Success Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=eq;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successUID + ";" +
                              "ops=BOP:onm=\"Failure Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=ne;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failUID + ";"
    
    // 4. Create success passage
    DEFINE successContent = CreateSuccessContent()
    DEFINE successPassage = "PSG:uid=" + successUID + ";nam=\"Examination Test Success\";\n" +
                           "BOT:lin=\"" + successContent + "\";\n" +
                           "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successPassageID + ";"
    
    // 5. Create fail passage
    DEFINE failContent = CreateFailContent()
    DEFINE failPassage = "PSG:uid=" + failUID + ";nam=\"Examination Test Failure\";\n" +
                        "BOT:lin=\"" + failContent + "\";\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failPassageID + ";"
    
    // Combine all passages
    DEFINE allPassages = startPassage + "\n\n" + 
                        setStatePassage + "\n\n" + 
                        checkStatePassage + "\n\n" + 
                        successPassage + "\n\n" + 
                        failPassage
    
    // Validation check
    PROCEDURE ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID) {
        // Verify that required elements are present
        VALIDATE allPassages CONTAINS "Testing evidence examination"
        VALIDATE allPassages CONTAINS evidenceID + "_EXAMINED;val=true"
        VALIDATE allPassages CONTAINS successPassageID
        VALIDATE allPassages CONTAINS failPassageID
        VALIDATE allPassages CONTAINS "brn=BRN"
        
        // Verify all attributes are set
        FOR EACH attrName IN attributeData {
            VALIDATE allPassages CONTAINS attrName
        }
        
        // Verify all passage IDs are included
        VALIDATE allPassages CONTAINS successUID
        VALIDATE allPassages CONTAINS failUID
        VALIDATE allPassages CONTAINS setStateUID
        VALIDATE allPassages CONTAINS checkStateUID
    }
    
    ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}

{# PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}

PROCEDURE GenerateDiagnosticMergePoint(stepIDPrefix, entry_point_id, testCaseID, trackOriginPath, nextPassageID) {
    // Primary goal: Create a passage that tests the convergence of multiple paths into a single outcome
    // Structure: Single passage that can be targeted from multiple sources and tracks arrival path

    // Define UID for this passage
    DEFINE mergeUID = entry_point_id
    DEFINE mergeName = "Test Case " + testCaseID + ": Merge Point Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateMergeContent() {
        RETURN "Testing path merge functionality (arrival from multiple sources)"
    }
    
    // Generate SLPN for this passage
    DEFINE mergeContent = CreateMergeContent()
    DEFINE originTracking = ""
    
    // Add optional origin path tracking - use $source_path as a literal, not template syntax
    IF trackOriginPath {
        originTracking = "UAS:asp=arrival_path;uty=SET;val=\"$source_path\";\n"
    }
    
    DEFINE slpnPassage = "BOT:lin=\"" + mergeContent + "\";\n" +
                         originTracking +
                         "UAS:asp=MERGE_POINT_REACHED;uty=SET;val=true;\n" +
                         "brn=BRN:bds=\"Proceed to Next Test\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Continue\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing path merge functionality"
        VALIDATE slpnPassage CONTAINS "MERGE_POINT_REACHED"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify origin tracking if enabled
        IF trackOriginPath {
            VALIDATE slpnPassage CONTAINS "arrival_path"
        }
    }
    
    ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}

{# PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}

PROCEDURE GenerateDiagnosticLoopTest(stepIDPrefix, entry_point_id, testCaseID, loopVarName, maxIterations, exitPassageID) {
    // Primary goal: Create a passage that tests cyclical progression with iteration counter and exit condition
    // Structure: Single self-referencing passage with counter that exits after a certain number of iterations

    // Define UID for this passage
    DEFINE loopUID = entry_point_id
    DEFINE loopName = "Test Case " + testCaseID + ": Loop Test"
    
    // Create descriptive text for the test that includes the dynamic counter
    PROCEDURE CreateLoopContent(loopVarName) {
        RETURN "Testing loop functionality (iteration $" + loopVarName + ")"
    }
    
    // Generate SLPN for this passage
    DEFINE loopContent = CreateLoopContent(loopVarName)
    
    // Create a separate check passage to handle the conditional logic
    DEFINE checkPassageUID = entry_point_id + "_check"
    DEFINE loopPassages = ""
    
    // First passage - increment the counter
    DEFINE slpnPassage = "BOT:lin=\"" + loopContent + "\";\n" +
                         "UAS:asp=" + loopVarName + ";uty=SET;val=$" + loopVarName + " + 1;\n" +
                         "brn=BRN:bds=\"Loop Control\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Proceed\";ods=\"Continue to next step\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkPassageUID + ";"
    
    // Check passage - evaluate and branch
    DEFINE checkPassage = "PSG:uid=" + checkPassageUID + ";nam=\"" + loopName + " - Check\";\n" +
                         "BOT:lin=\"Evaluating loop condition...\";\n" +
                         "brn=BRN:bds=\"Loop Evaluation\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Exit Loop\";chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations + ";" +
                         "UAS:asp=LOOP_TEST_COMPLETE;uty=SET;val=true;" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + exitPassageID + ";" +
                         "ops=BOP:onm=\"Continue Loop\";chk=CHK:asp=" + loopVarName + ";cty=lt;vlu=" + maxIterations + ";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + entry_point_id + ";"
    
    // Combine the passages
    loopPassages = slpnPassage + "\n\n" + checkPassage
    
    // Validation check
    PROCEDURE ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID) {
        // Verify that required elements are present
        VALIDATE loopPassages CONTAINS "Testing loop functionality"
        VALIDATE loopPassages CONTAINS loopVarName + ";uty=SET;val=$" + loopVarName + " + 1"
        VALIDATE loopPassages CONTAINS "chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations
        VALIDATE loopPassages CONTAINS "LOOP_TEST_COMPLETE;uty=SET;val=true"
        VALIDATE loopPassages CONTAINS exitPassageID
        VALIDATE loopPassages CONTAINS "tgt=" + entry_point_id
        VALIDATE loopPassages CONTAINS "brn=BRN"
        VALIDATE loopPassages CONTAINS checkPassageUID
    }
    
    ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID)
    
    RETURN loopPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}

{# PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}

PROCEDURE GenerateDiagnosticAppNavigation(stepIDPrefix, entry_point_id, testCaseID, targetApp, returnPassageID) {
    // Primary goal: Create a passage that tests navigation between different application interfaces
    // Structure: Single passage that navigates to a specific application and sets state

    // Define UID for this passage
    DEFINE navUID = entry_point_id
    DEFINE navName = "Test Case " + testCaseID + ": Application Navigation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateNavContent(targetApp) {
        RETURN "Testing application navigation to " + targetApp
    }
    
    // Generate SLPN for this passage
    DEFINE navContent = CreateNavContent(targetApp)
    
    DEFINE appTypeMap = {
        "EVIDENCE": "EVIDENCE",
        "DEDUCTION": "DEDUCTION",
        "NOTES": "NOTES",
        "MAP": "MAP",
        "CASE_FILE": "CASE_FILE"
    }
    
    // Lookup the app type or default to the provided value
    DEFINE appType = appTypeMap[targetApp] ? appTypeMap[targetApp] : targetApp
    
    DEFINE slpnPassage = "BOT:lin=\"" + navContent + "\";\n" +
                         "SET:evt=NAV_TO_" + appType + "_APP;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=" + appType + ";tgt=" + targetApp.toLowerCase() + "_app;\n" +
                         "SET:evt=RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\";"
    
    // Validation check
    PROCEDURE ValidateAppNavigation(slpnPassage, targetApp, returnPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing application navigation"
        VALIDATE slpnPassage CONTAINS "NAV_TO_" + appType + "_APP;val=true"
        VALIDATE slpnPassage CONTAINS "ACT:aty=MOVE;amt=AMT:typ=" + appType
        VALIDATE slpnPassage CONTAINS "RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\""
    }
    
    ValidateAppNavigation(slpnPassage, targetApp, returnPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}

{# PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}

PROCEDURE GenerateDiagnosticExitPoint(stepIDPrefix, entry_point_id, testCaseID, testOutcome, resultData) {
    // Primary goal: Create a passage that tests proper system termination and outcome recording
    // Structure: Single passage that records final state and signals test completion
    // Input: resultData is an object of key-value pairs to record as test results

    // Define UID for this passage
    DEFINE exitUID = entry_point_id
    DEFINE exitName = "Test Case " + testCaseID + ": Exit Point"
    
    // Create descriptive text for the test
    PROCEDURE CreateExitContent(testOutcome) {
        RETURN "Test case complete. Validating final state. Outcome: " + testOutcome
    }
    
    // Create result data recording
    PROCEDURE CreateResultRecording(testCaseID, resultData) {
        DEFINE resultCommands = ""
        
        // Record overall test completion
        resultCommands += "SET:evt=TC" + testCaseID + "_COMPLETE;val=true;\n"
        resultCommands += "SET:var=test_outcome;val=\"" + testOutcome + "\";\n"
        
        // Record each result data point
        FOR EACH key, value IN resultData {
            DEFINE dataType = GetDataType(value)
            
            IF dataType == "boolean" {
                resultCommands += "SET:evt=TC" + testCaseID + "_RESULT_" + key + ";val=" + value + ";\n"
            } ELSE {
                resultCommands += "SET:var=TC" + testCaseID + "_RESULT_" + key + ";val=" + (typeof(value) == "string" ? "\"" + value + "\"" : value) + ";\n"
            }
        }
        
        RETURN resultCommands
    }
    
    // Generate SLPN for this passage
    DEFINE exitContent = CreateExitContent(testOutcome)
    DEFINE resultCommands = CreateResultRecording(testCaseID, resultData)
    
    DEFINE slpnPassage = "BOT:lin=\"" + exitContent + "\";\n" +
                         resultCommands + "\n" +
                         "brn=BRN:bds=\"Test Complete\";brp=once;bpr=option-list;bit=ada;ops=BOP:onm=\"Finalize Test\";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME;"
    
    // Validation check
    PROCEDURE ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Test case complete"
        VALIDATE slpnPassage CONTAINS "Outcome: " + testOutcome
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_COMPLETE;val=true"
        VALIDATE slpnPassage CONTAINS "test_outcome;val=\"" + testOutcome + "\""
        VALIDATE slpnPassage CONTAINS "brn=BRN:bds=\"Test Complete\""
        VALIDATE slpnPassage CONTAINS "act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME"
        
        // Verify result data points are recorded
        FOR EACH key IN resultData {
            VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_RESULT_" + key
        }
    }
    
    ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}

{# PHENOTYPE: DIAGNOSTIC_COMPOUND_CONDITION #}

PROCEDURE GenerateDiagnosticCompoundCondition(stepIDPrefix, entry_point_id, testCaseID, logicalOperator, conditions, truePassageID, falsePassageID) {
    // Primary goal: Create a passage that tests complex condition combinations using logical operators
    // Structure: Single passage with a compound condition (AND/OR/NOT) that branches based on evaluation
    // Input: logicalOperator is "AND", "OR", or "NOT"
    // Input: conditions is a list of condition objects { variable: name, operator: "EQUALS"|"NOT_EQUALS"|etc, value: checkValue }

    // Define UID for this passage
    DEFINE compoundUID = entry_point_id
    DEFINE compoundName = "Test Case " + testCaseID + ": Compound Condition Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateCompoundContent(logicalOperator) {
        RETURN "Testing compound condition with " + logicalOperator + " operator"
    }
    
    // Create compound condition CHK string for branch option
    PROCEDURE CreateCompoundConditionCheck(logicalOperator, conditions) {
        DEFINE checkString = ""
        
        // Special case for NOT (single condition)
        IF logicalOperator == "NOT" {
            DEFINE condition = conditions[0]
            checkString = "chk=CHK:cty=not;chk=CHK:asp=" + condition.variable + ";cty=" + MapOperator(condition.operator) + ";vlu=" + condition.value + ";"
            RETURN checkString
        }
        
        // For AND/OR compound conditions
        checkString = "chk=CHK:cty=" + logicalOperator.toLowerCase() + ";"
        
        // Add each individual condition
        FOR EACH condition IN conditions {
            checkString += "chk=CHK:asp=" + condition.variable + ";cty=" + MapOperator(condition.operator) + ";vlu=" + condition.value + ";"
        }
        
        RETURN checkString
    }
    
    // Helper function to map SLPN operators to CHK format
    FUNCTION MapOperator(operator) {
        DEFINE opMap = {
            "EQUALS": "eq",
            "NOT_EQUALS": "ne", 
            "GREATER_THAN": "gt",
            "LESS_THAN": "lt",
            "GREATER_OR_EQUAL": "gte",
            "LESS_OR_EQUAL": "lte"
        }
        
        RETURN opMap[operator] || "eq" // Default to eq if not found
    }
    
    // Generate SLPN for this passage
    DEFINE compoundContent = CreateCompoundContent(logicalOperator)
    DEFINE conditionCheck = CreateCompoundConditionCheck(logicalOperator, conditions)
    
    DEFINE slpnPassage = "BOT:lin=\"" + compoundContent + "\";\n" +
                        "brn=BRN:bds=\"Compound Condition Evaluation\";brp=once;bpr=option-list;bit=ada;" +
                        "ops=BOP:onm=\"True Path\";" + conditionCheck +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + truePassageID + ";" +
                        "ops=BOP:onm=\"False Path\";act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + falsePassageID + ";"
    
    // Validation check
    PROCEDURE ValidateCompoundCondition(slpnPassage, logicalOperator, conditions, truePassageID, falsePassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing compound condition with " + logicalOperator
        VALIDATE slpnPassage CONTAINS truePassageID
        VALIDATE slpnPassage CONTAINS falsePassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        
        // Verify each condition variable is included
        FOR EACH condition IN conditions {
            VALIDATE slpnPassage CONTAINS condition.variable
        }
        
        // Verify logical operator (in lowercase as used in CHK)
        IF logicalOperator == "NOT" {
            VALIDATE slpnPassage CONTAINS "cty=not"
        } ELSE {
            VALIDATE slpnPassage CONTAINS "cty=" + logicalOperator.toLowerCase()
        }
    }
    
    ValidateCompoundCondition(slpnPassage, logicalOperator, conditions, truePassageID, falsePassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_COMPOUND_CONDITION #}

{# PHENOTYPE: DIAGNOSTIC_TEST_SEQUENCE #}

PROCEDURE GenerateDiagnosticTestSequence(stepIDPrefix, rootID, testCaseID, sequenceConfig) {
    // Primary goal: Create a complete sequence of connected test passages for full test case verification
    // Structure: Generates all required passages for a complete test following the provided configuration
    // Input: sequenceConfig defines the test sequence - array of passage configs in order
    
    // Validate sequence config
    PROCEDURE ValidateSequenceConfig(sequenceConfig) {
        VALIDATE sequenceConfig.length >= 2 // Must have at least entry and exit
        VALIDATE sequenceConfig[0].type == "ENTRY_POINT" // First must be entry
        VALIDATE sequenceConfig[sequenceConfig.length - 1].type == "EXIT_POINT" // Last must be exit
    }
    
    ValidateSequenceConfig(sequenceConfig)
    
    DEFINE allPassages = ""
    DEFINE passageCounter = 0
    
    // Create unique IDs for each passage
    DEFINE passageIDs = []
    FOR EACH config IN sequenceConfig INDEX i {
        IF i == 0 {
            // Entry point uses the rootID
            passageIDs.push(rootID)
        } ELSE {
            passageIDs.push(stepIDPrefix + "_" + config.type + "_" + i)
        }
    }
    
    // Generate each passage in the sequence
    FOR EACH config IN sequenceConfig INDEX i {
        DEFINE currentID = passageIDs[i]
        DEFINE nextID = i < sequenceConfig.length - 1 ? passageIDs[i + 1] : null
        DEFINE slpnPassage = ""
        
        // For the purposes of the passageCount increment, used in multiple SWITCH branches
        IF true {
            passageCounter++
        }
        
        SWITCH config.type {
            CASE "ENTRY_POINT":
                slpnPassage = GenerateDiagnosticEntryPoint(
                    stepIDPrefix, 
                    currentID, 
                    testCaseID, 
                    config.description, 
                    config.initialState, 
                    nextID
                )
                BREAK
                
            CASE "LINEAR_TEST":
                slpnPassage = GenerateDiagnosticLinearTest(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.stepNumber,
                    config.totalSteps,
                    config.stateChanges,
                    nextID
                )
                BREAK
                
            CASE "BRANCH_TEST_BINARY":
                slpnPassage = GenerateDiagnosticBranchTestBinary(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.conditionVar,
                    config.conditionValue,
                    config.pathAPassageID || nextID, // Use next sequential ID if not specified
                    config.pathBPassageID || nextID
                )
                BREAK
                
            CASE "BRANCH_TEST_MULTI":
                slpnPassage = GenerateDiagnosticBranchTestMulti(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.conditionVar,
                    config.conditions,
                    config.defaultPassageID || nextID
                )
                BREAK
                
            CASE "EVIDENCE_REVEAL":
                slpnPassage = GenerateDiagnosticEvidenceReveal(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.evidenceID,
                    nextID
                )
                BREAK
                
            CASE "EVIDENCE_EXAMINATION":
                slpnPassage = GenerateDiagnosticEvidenceExamination(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.evidenceID,
                    config.attributeData,
                    config.successPassageID || nextID,
                    config.failPassageID || nextID
                )
                BREAK
                
            CASE "MERGE_POINT":
                slpnPassage = GenerateDiagnosticMergePoint(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.trackOriginPath,
                    nextID
                )
                BREAK
                
            CASE "LOOP_TEST":
                slpnPassage = GenerateDiagnosticLoopTest(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.loopVarName,
                    config.maxIterations,
                    config.exitPassageID || nextID
                )
                BREAK
                
            CASE "APP_NAVIGATION":
                slpnPassage = GenerateDiagnosticAppNavigation(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.targetApp,
                    config.returnPassageID || nextID
                )
                BREAK
                
            CASE "COMPOUND_CONDITION":
                slpnPassage = GenerateDiagnosticCompoundCondition(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.logicalOperator,
                    config.conditions,
                    config.truePassageID || nextID,
                    config.falsePassageID || nextID
                )
                BREAK
                
            CASE "EXIT_POINT":
                slpnPassage = GenerateDiagnosticExitPoint(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.testOutcome,
                    config.resultData
                )
                BREAK
                
            DEFAULT:
                THROW "Unsupported passage type: " + config.type
        }
        
        // Add to the complete sequence
        IF i > 0 {
            allPassages += "\n\n"
        }
        allPassages += "PSG:uid=" + currentID + ";nam=\"Test Case " + testCaseID + ": " + config.type + "\";" + 
                      "tag=DIAGNOSTIC|TEST_CASE_" + testCaseID + ";" +
                      "cmd=CMD:typ=diagnostic;\n" + slpnPassage
    }
    
    // Validation check
    PROCEDURE ValidateTestSequence(allPassages, passageCounter, sequenceConfig) {
        VALIDATE passageCounter == sequenceConfig.length
        
        // Verify entry and exit markers
        VALIDATE allPassages CONTAINS "Test case complete" // Exit marker
        VALIDATE allPassages CONTAINS sequenceConfig[0].description // Entry description
    }
    
    ValidateTestSequence(allPassages, passageCounter, sequenceConfig)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_TEST_SEQUENCE #}

{# PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}

PROCEDURE GenerateDiagnosticSLPNConversionTest(stepIDPrefix, entry_point_id, testCaseID, journeyFormat, expectedSLPN, nextPassageID) {
    // Primary goal: Create a passage that tests conversion from journey format to SLPN notation
    // Structure: Single passage that displays both journey input and expected SLPN output for verification

    // Define UID for this passage
    DEFINE conversionUID = entry_point_id
    DEFINE conversionName = "Test Case " + testCaseID + ": SLPN Conversion Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateConversionContent() {
        RETURN "Testing journey to SLPN conversion"
    }
    
    // Format journey and SLPN for display
    PROCEDURE FormatJourneyAndSLPN(journeyFormat, expectedSLPN) {
        DEFINE journeyString = JSON.stringify(journeyFormat, null, 2)
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = expectedSLPN.replace(/"/g, '\\"')
        
        RETURN "Journey Format: '" + journeyString + "', Expected SLPN: '" + escapedSLPN + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE conversionContent = CreateConversionContent()
    DEFINE formattedData = FormatJourneyAndSLPN(journeyFormat, expectedSLPN)
    
    DEFINE slpnPassage = "BOT:lin=\"" + conversionContent + "\";\n" +
                         "SET:var=conversion_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=CONVERSION_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing journey to SLPN conversion"
        VALIDATE slpnPassage CONTAINS "conversion_test_data"
        VALIDATE slpnPassage CONTAINS "CONVERSION_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}

{# PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}

PROCEDURE GenerateDiagnosticJSONGenerationTest(stepIDPrefix, entry_point_id, testCaseID, slpnInput, expectedJSON, nextPassageID) {
    // Primary goal: Create a passage that tests SLPN-to-JSON transformation
    // Structure: Single passage that displays both SLPN input and expected JSON output for verification

    // Define UID for this passage
    DEFINE jsonGenUID = entry_point_id
    DEFINE jsonGenName = "Test Case " + testCaseID + ": JSON Generation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateJSONGenContent() {
        RETURN "Testing SLPN to JSON conversion"
    }
    
    // Format SLPN and JSON for display
    PROCEDURE FormatSLPNAndJSON(slpnInput, expectedJSON) {
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = slpnInput.replace(/"/g, '\\"')
        DEFINE jsonString = JSON.stringify(expectedJSON, null, 2)
        
        RETURN "SLPN Input: '" + escapedSLPN + "', Expected JSON: '" + jsonString + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE jsonGenContent = CreateJSONGenContent()
    DEFINE formattedData = FormatSLPNAndJSON(slpnInput, expectedJSON)
    
    DEFINE slpnPassage = "BOT:lin=\"" + jsonGenContent + "\";\n" +
                         "SET:var=json_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=JSON_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing SLPN to JSON conversion"
        VALIDATE slpnPassage CONTAINS "json_test_data"
        VALIDATE slpnPassage CONTAINS "JSON_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}

{# PHENOTYPE: DIAGNOSTIC_COMPLEX_CONDITION #}

PROCEDURE GenerateDiagnosticComplexCondition(stepIDPrefix, entry_point_id, testCaseID, logicalOperator, conditionVars, truePassageID, falsePassageID) {
    // Primary goal: Create a passage structure that tests complex conditions (AND/OR) across multiple variables
    // Structure: Multiple passages for setting variables and direct branch validation with aspect checks
    // Input: logicalOperator is "AND" or "OR"
    // Input: conditionVars is a list of variable names to check in the complex condition

    // Define UIDs for the passage sequence
    DEFINE startUID = entry_point_id
    DEFINE checkUID = entry_point_id + "_check"
    DEFINE trueResultUID = entry_point_id + "_true_result"
    DEFINE falseResultUID = entry_point_id + "_false_result"
    
    // Create variable setting UIDs for each condition var
    DEFINE varSetUIDs = {}
    FOR EACH varName IN conditionVars {
        varSetUIDs[varName + "_true"] = "diag_set_" + varName + "_true_" + testCaseID
        varSetUIDs[varName + "_false"] = "diag_set_" + varName + "_false_" + testCaseID
    }
    
    // Create descriptive text for each passage
    PROCEDURE CreateStartContent() {
        RETURN "Testing complex " + logicalOperator + " condition with multiple variables"
    }
    
    PROCEDURE CreateVariableSetContent(varName, value) {
        RETURN "Setting " + varName + " to " + value
    }
    
    PROCEDURE CreateCheckContent() {
        RETURN "Evaluating complex " + logicalOperator + " condition"
    }
    
    PROCEDURE CreateResultContent(result) {
        RETURN "Complex condition evaluated to " + result + "!"
    }
    
    // 1. Create the start passage with variable setting options
    DEFINE startContent = CreateStartContent()
    DEFINE startPassage = "PSG:uid=" + startUID + ";nam=\"Complex Condition Test\";\n" +
                         "BOT:lin=\"" + startContent + "\";\n" +
                         "brn=BRN:bds=\"Set Variables or Check\";brp=re-playable;bpr=option-list;bit=ada;"
    
    // Add options for setting each variable true/false
    FOR EACH varName IN conditionVars {
        startPassage += "ops=BOP:onm=\"Set " + varName + " True\";ods=\"Set " + varName + " to true\";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + varSetUIDs[varName + "_true"] + "|"
        
        startPassage += "ops=BOP:onm=\"Set " + varName + " False\";ods=\"Set " + varName + " to false\";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + varSetUIDs[varName + "_false"] + "|"
    }
    
    // Add option to perform the check
    startPassage += "ops=BOP:onm=\"Perform " + logicalOperator + " Check\";ods=\"Test the complex condition\";" +
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkUID + ";"
    
    // 2. Create variable setting passages
    DEFINE varSetPassages = ""
    FOR EACH varName IN conditionVars {
        // True setting passage
        DEFINE trueContent = CreateVariableSetContent(varName, "TRUE")
        DEFINE trueSetPassage = "PSG:uid=" + varSetUIDs[varName + "_true"] + ";nam=\"Set " + varName + " True\";\n" +
                                "BOT:lin=\"" + trueContent + "\";\n" +
                                "UAS:asp=" + varName + ";uty=SET;val=true;\n" +
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=ada;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        // False setting passage
        DEFINE falseContent = CreateVariableSetContent(varName, "FALSE")
        DEFINE falseSetPassage = "PSG:uid=" + varSetUIDs[varName + "_false"] + ";nam=\"Set " + varName + " False\";\n" +
                                "BOT:lin=\"" + falseContent + "\";\n" +
                                "UAS:asp=" + varName + ";uty=SET;val=false;\n" +
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=ada;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        varSetPassages += trueSetPassage + "\n\n" + falseSetPassage + "\n\n"
    }
    
    // 3. Create check passage with branch options for complex condition
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkPassage = "PSG:uid=" + checkUID + ";nam=\"Evaluate " + logicalOperator + " Condition\";\n" +
                         "BOT:lin=\"" + checkContent + "\";\n" +
                         "brn=BRN:bds=\"Condition Check\";brp=once;bpr=option-list;bit=ada;"
    
    // Add success branch with complex condition check
    checkPassage += "ops=BOP:onm=\"True Path\";"
    
    // Add the appropriate check based on logicalOperator
    IF logicalOperator == "AND" {
        checkPassage += "chk=CHK:cty=and;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    } ELSE { // OR case
        checkPassage += "chk=CHK:cty=or;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    }
    
    checkPassage += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + trueResultUID + ";"
    
    // Add failure branch 
    checkPassage += "ops=BOP:onm=\"False Path\";"
    
    // Add the opposite check based on logicalOperator
    IF logicalOperator == "AND" {
        checkPassage += "chk=CHK:cty=not;chk=CHK:cty=and;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    } ELSE { // OR case
        checkPassage += "chk=CHK:cty=not;chk=CHK:cty=or;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    }
    
    checkPassage += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + falseResultUID + ";"
    
    // 4. Create result passages
    DEFINE trueContent = CreateResultContent("TRUE")
    DEFINE trueResultPassage = "PSG:uid=" + trueResultUID + ";nam=\"Complex Check: TRUE\";\n" +
                              "BOT:lin=\"" + trueContent + "\";\n" +
                              "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=ada;" +
                              "ops=BOP:onm=\"Proceed\";ods=\"Continue to next test\";" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + truePassageID + ";"
    
    DEFINE falseContent = CreateResultContent("FALSE")
    DEFINE falseResultPassage = "PSG:uid=" + falseResultUID + ";nam=\"Complex Check: FALSE\";\n" +
                               "BOT:lin=\"" + falseContent + "\";\n" +
                               "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=ada;" +
                               "ops=BOP:onm=\"Proceed\";ods=\"Continue to next test\";" +
                               "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + falsePassageID + ";"
    
    // Combine all passages
    DEFINE allPassages = startPassage + "\n\n" + 
                        varSetPassages +
                        checkPassage + "\n\n" +
                        trueResultPassage + "\n\n" +
                        falseResultPassage
    
    // Validation check
    PROCEDURE ValidateComplexCondition(allPassages, logicalOperator, conditionVars, truePassageID, falsePassageID) {
        // Verify that required elements are present
        VALIDATE allPassages CONTAINS "Testing complex " + logicalOperator + " condition"
        VALIDATE allPassages CONTAINS truePassageID
        VALIDATE allPassages CONTAINS falsePassageID
        
        // Verify each condition variable is included
        FOR EACH varName IN conditionVars {
            VALIDATE allPassages CONTAINS varName
            VALIDATE allPassages CONTAINS varSetUIDs[varName + "_true"]
            VALIDATE allPassages CONTAINS varSetUIDs[varName + "_false"]
        }
        
        // Verify logical operator
        VALIDATE allPassages CONTAINS "cty=" + logicalOperator.toLowerCase()
        
        // Verify result passages
        VALIDATE allPassages CONTAINS trueResultUID
        VALIDATE allPassages CONTAINS falseResultUID
    }
    
    ValidateComplexCondition(allPassages, logicalOperator, conditionVars, truePassageID, falsePassageID)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_COMPLEX_CONDITION #} 

