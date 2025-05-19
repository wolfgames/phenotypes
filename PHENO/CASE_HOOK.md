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
    choicePromptText,               // Text for the accept/review decision point (e.g., "This is a complex case. Are you ready to uncover the truth?")
    
    acceptActionConfig,             // REQUIRED: { targetID: "UID_OR_APPTARGET", targetType: "passage" | "application", setAspects_Optional: [{ name: "aspectName", value: "aspectValue", type: "boolean" | "string" | "number" }] }
    rejectActionConfig,             // MAINTAINED FOR COMPATIBILITY: No longer used for rejection, but kept for backward compatibility
    
    acceptMessage_Optional,         // Optional: Custom text for the accept confirmation screen
    declineMessage_Optional         // MAINTAINED FOR COMPATIBILITY: No longer used for decline messaging, but kept for backward compatibility
) {
    // Primary goal: Create an irresistible hook sequence with review option instead of decline
    // Structure: 1. Intro sequence with multiple steps -> 2. Accept/Review Choice -> 3. Confirmation (Accept) 
    // The player can either accept the case or review details again (cycling back to intro sequence)
    // Uses multi-step CMD:typ=intro for richer initial presentation, all within a single passage.

    // --- Define UIDs for the passages ---
    DEFINE introPassageUID = entry_point_id // Single intro passage containing all intro steps
    DEFINE choicePassageUID = stepIDPrefix + "_choice"
    DEFINE confirmAcceptUID = stepIDPrefix + "_confirm_ACCEPT"
    DEFINE confirmDeclineUID = stepIDPrefix + "_confirm_DECLINE" // Kept for backward compatibility but not used in current flow

    // --- Define Passage Names ---
    DEFINE introName = caseTitle + " - Introduction"
    DEFINE choiceName = caseTitle + " - Your Decision"
    DEFINE confirmAcceptName = caseTitle + " - Case Accepted"
    DEFINE confirmDeclineName = caseTitle + " - Case Declined" // Kept for backward compatibility but not used in current flow

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

    // == Intro Passage with multiple steps ==
    // Step 1: Visual Hook & Victim Introduction
    DEFINE hook_step_title = caseTitle + ": A Life Cut Short"
    DEFINE hook_step_subtitle = EscapeStringForSLPN(hookIntroText + " The victim: " + victimName + ", " + victimDescription_Brief + ".")
    DEFINE hookVisualDescPG13 = EscapeStringForSLPN("Dark atmospheric shot of a university ID badge lying on a desk next to an overturned coffee cup, dramatic lighting creates long shadows, suggesting something has gone wrong. No faces visible.")
    
    // Step 2: Crime Scene Details
    DEFINE details_step1_header = "CRIME SCENE:"
    DEFINE details_step1_body = "The incident occurred at " + crimeScene_LocationName + ", " + crimeScene_BriefDescription + "."
    DEFINE details_step1_body2 = apparentMurderMode
    
    // Create properly formatted array of quoted strings for step 2
    DEFINE details_step1_lines_array = [details_step1_header, details_step1_body, details_step1_body2]
    DEFINE details_step1_lines = "["
    FOR i = 0; i < details_step1_lines_array.length; i++ {
        IF i > 0 { details_step1_lines += "," }
        details_step1_lines += "\"" + EscapeStringForSLPN(details_step1_lines_array[i]) + "\""
    }
    details_step1_lines += "]"

    // Step 3: Context & Stakes
    DEFINE details_step2_header = "CASE OVERVIEW:"
    DEFINE details_step2_lines_array = [details_step2_header, contextSummary]
    IF characterStakes_Optional { details_step2_lines_array.push("The ramifications are significant: " + characterStakes_Optional) }
    IF moralQuestion_Optional { details_step2_lines_array.push("This case forces us to ask: " + moralQuestion_Optional) }
    
    // Create properly formatted array of quoted strings for step 3
    DEFINE details_step2_lines = "["
    FOR i = 0; i < details_step2_lines_array.length; i++ {
        IF i > 0 { details_step2_lines += "," }
        details_step2_lines += "\"" + EscapeStringForSLPN(details_step2_lines_array[i]) + "\""
    }
    details_step2_lines += "]"

    DEFINE details_bg_image = contextImageAlias_Optional || "default_context_image"
    DEFINE details_bg_imagedesc = EscapeStringForSLPN(contextImageDesc_Optional || "A case file open on a detective's desk, illuminated by a single desk lamp, with crime scene photos and police reports visible.")

    // Assemble the complete intro passage with all three steps
    DEFINE slpnIntroPassage = "PSG:uid=" + introPassageUID + ";nam=\"" + introName + "\";tag=CASE_HOOK|INTRO;" +
                           "cmd=CMD:typ=intro;" +
                               "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + choicePassageUID + ";" +
                               // Step 1: Hook & Victim Introduction
                               "STP:typ=introStep;" + 
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + hookVisual_ImageAlias + ";imd=\"" + hookVisualDescPG13 + "\";" +
                                   "cmp=CMP:typ=introStepText;txt=TITLE;mnt=\"" + EscapeStringForSLPN(hook_step_title) + "\";sbt=\"" + hook_step_subtitle + "\";" +
                                   "cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=PRIMARY;tex=\"Open Case\";" +
                               // Step 2: Crime Scene Details
                               "STP:typ=introStep;" + 
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + (crimeScene_ImageAlias_Optional || "default_scene_image") + ";imd=\"" + EscapeStringForSLPN("An empty academic office with police tape across the doorway. A desk with scattered papers and a knocked-over chair. Yellow evidence markers visible on surfaces. Dramatic shadows from venetian blinds create a noir atmosphere.") + "\";" +
                                   "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=" + details_step1_lines + ";" +
                                   "cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=PRIMARY;tex=\"What's the situation?\";" +
                               // Step 3: Context & Stakes - uses FINISH_INTRO_BUTTON since it's the last step
                               "STP:typ=introStep;" + 
                                   "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + details_bg_image + ";imd=\"" + EscapeStringForSLPN("A detective's desk illuminated by a single lamp in a dark room. Case files, photographs, and evidence reports spread across the surface. A coffee cup and magnifying glass sit nearby. No faces visible in any photos.") + "\";" +
                                   "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=" + details_step2_lines + ";" +
                                   "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Consider the Case\";"
    allPassages += slpnIntroPassage

    // == Passage 2: Accept/Review Choice ==
    DEFINE slpnPassage3 = "PSG:uid=" + choicePassageUID + ";nam=\"" + choiceName + "\";tag=CASE_HOOK|INTRO|CHOICE;" +
                           "cmd=CMD:typ=branch;bds=\"" + EscapeStringForSLPN(choicePromptText) + "\";brp=once;bpr=option-list;bit=ada;" +
                               "ops=BOP:onm=\"Accept Case\";img=\"accept_case_icon\";imd=\"Take on the investigation.\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + confirmAcceptUID + "|" +
                               "BOP:onm=\"REVIEW DETAILS\";img=\"review_details_icon\";imd=\"Review the case information again.\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + introPassageUID + ";"
    allPassages += "\n\n" + slpnPassage3

    // == Passage 3: Confirmation / Transition (Accept) ==
    DEFINE acceptActionsString = BuildActionString(acceptActionConfig)
    DEFINE acceptConfirmText = "[\"CONGRATULATIONS:\",\"" + EscapeStringForSLPN(acceptMessage_Optional || "Case accepted. We're counting on you. Preparing your full briefing now.") + "\"]"

    DEFINE slpnPassage4_Accept = "PSG:uid=" + confirmAcceptUID + ";nam=\"" + confirmAcceptName + "\";tag=CASE_HOOK|INTRO;" +
                                "cmd=CMD:typ=intro;" +
                                    "act=" + acceptActionsString + ";" +
                                    "STP:typ=introStep;" +
                                        "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_accepted_graphic;imd=\"Close-up of a hand placing a red 'ACCEPTED' stamp on official case documents. The desk is illuminated by a single desk lamp, creating dramatic shadows. A police badge visible out of focus in the background.\";" +
                                        "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=" + acceptConfirmText + ";" +
                                        "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Begin Investigation\";"
    allPassages += "\n\n" + slpnPassage4_Accept

    // === Note: We're keeping the decline passage structure for backward compatibility, but it's not used with the new REVIEW DETAILS option ===
    DEFINE rejectActionsString = BuildActionString(rejectActionConfig)
    DEFINE declineConfirmText = "[\"NOTICE:\",\"" + EscapeStringForSLPN(declineMessage_Optional || "Understood. Some cases are best left to others. Returning to main menu.") + "\"]"

    DEFINE slpnPassage4_Decline = "PSG:uid=" + confirmDeclineUID + ";nam=\"" + confirmDeclineName + "\";tag=CASE_HOOK|INTRO;" +
                                 "cmd=CMD:typ=intro;" +
                                     "act=" + rejectActionsString + ";" +
                                     "STP:typ=introStep;" +
                                         "cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_declined_graphic;imd=\"A gloved hand placing a manila folder into a filing cabinet labeled 'PENDING'. The office is dimly lit with blue-tinted lighting. A clock on the wall shows it's late in the evening.\";" +
                                         "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=" + declineConfirmText + ";" +
                                         "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Okay\";"
    allPassages += "\n\n" + slpnPassage4_Decline

    // --- Validation (Conceptual) ---
    PROCEDURE ValidateRevisedHookSequence(slpnIntro, slpnChoice, slpnAccept, slpnDecline, inputs) {
        VALIDATE slpnIntro CONTAINS inputs.hookVisual_ImageAlias AND inputs.hookIntroText AND inputs.victimName
        VALIDATE slpnIntro CONTAINS inputs.crimeScene_LocationName AND inputs.apparentMurderMode AND inputs.contextSummary
        VALIDATE slpnIntro CONTAINS "NEXT_STEP_BUTTON" AND "FINISH_INTRO_BUTTON" // Verify proper button types
        IF inputs.characterStakes_Optional { VALIDATE slpnIntro CONTAINS inputs.characterStakes_Optional }
        VALIDATE slpnChoice CONTAINS inputs.choicePromptText AND confirmAcceptUID AND introPassageUID
        VALIDATE slpnAccept CONTAINS BuildActionString(inputs.acceptActionConfig)
        IF inputs.acceptActionConfig.setAspects_Optional {
            FOR EACH aspect IN inputs.acceptActionConfig.setAspects_Optional {
                VALIDATE slpnAccept CONTAINS aspect.name
            }
        }
    }
    // Pass a structure containing all inputs to the validation function for thorough checking.
    // ValidateRevisedHookSequence(slpnIntroPassage, slpnPassage3, slpnPassage4_Accept, slpnPassage4_Decline, {input parameters...})

    RETURN allPassages
}
//example output:
//PSG:uid=CH_SF_ENTRY;nam="The Shepherd's Flock - Introduction";tag=CASE_HOOK|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_choice;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=ethan_thompson_split;imd="Dark atmospheric shot of a university ID badge lying on a desk next to an overturned coffee cup, dramatic lighting creates long shadows, suggesting something has gone wrong. No faces visible.";cmp=CMP:typ=introStepText;txt=TITLE;mnt="The Shepherd's Flock: A Life Cut Short";sbt="Professor Ethan Thompson, pillar of the community, found dead in his office. The victim: Professor Ethan Thompson, a beloved university professor known for his kindness.";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=PRIMARY;tex="Open Case";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=office_chalk_outline;imd="An empty academic office with police tape across the doorway. A desk with scattered papers and a knocked-over chair. Yellow evidence markers visible on surfaces. Dramatic shadows from venetian blinds create a noir atmosphere.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=["CRIME SCENE:","The incident occurred at his university office, a place of learning, now stained by tragedy.","Initial signs pointed to natural causes, but toxicology reports scream murder. The method: a potent pesticide."];cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=PRIMARY;tex="What's the situation?";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_file_shepherds_flock;imd="A detective's desk illuminated by a single lamp in a dark room. Case files, photographs, and evidence reports spread across the surface. A coffee cup and magnifying glass sit nearby. No faces visible in any photos.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=["CASE OVERVIEW:","A respected professor's life cut short. Early reports were misleading, but advanced toxicology confirms foul play. A thermos, potentially crucial, was recovered from the scene.","The ramifications are significant: The university community is shaken, a family is devastated, and unsettling secrets are beginning to surface.","This case forces us to ask: What could drive someone to commit such a calculated act against a man like him?"];cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Consider the Case";

PSG:uid=CH_SF_choice;nam="The Shepherd's Flock - Your Decision";tag=CASE_HOOK|INTRO|CHOICE;cmd=CMD:typ=branch;bds="This case, 'The Shepherd's Flock,' promises to be challenging. Are you prepared to delve into its depths?";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Accept Case";img="accept_case_icon";imd="Take on the investigation.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_confirm_ACCEPT|BOP:onm="REVIEW DETAILS";img="review_details_icon";imd="Review the case information again.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CH_SF_ENTRY;

PSG:uid=CH_SF_confirm_ACCEPT;nam="The Shepherd's Flock - Case Accepted";tag=CASE_HOOK|INTRO;cmd=CMD:typ=intro;act=UAS:asp=CaseIntroduced_ShepherdsFlock;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=SUSPECT_INTRODUCTION_THROUGH_DIALOGUE_1;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_accepted_graphic;imd="Close-up of a hand placing a red 'ACCEPTED' stamp on official case documents. The desk is illuminated by a single desk lamp, creating dramatic shadows. A police badge visible out of focus in the background.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=["CONGRATULATIONS:","Case accepted. 'The Shepherd's Flock' needs your expertise. Preparing your investigation dashboard now."];cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Begin Investigation";

PSG:uid=CH_SF_confirm_DECLINE;nam="The Shepherd's Flock - Case Declined";tag=CASE_HOOK|INTRO;cmd=CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_declined_graphic;imd="A gloved hand placing a manila folder into a filing cabinet labeled 'PENDING'. The office is dimly lit with blue-tinted lighting. A clock on the wall shows it's late in the evening.";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=["NOTICE:","Understood. We'll assign 'The Shepherd's Flock' to another team. Returning you to case selection."];cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Okay";

{# END_PHENOTYPE: CASE_HOOK #}
