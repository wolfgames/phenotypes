{# PHENOTYPE: CASE_HOOK #}

PROCEDURE GenerateIntroductionHook(stepIDPrefix, entry_point_id, caseTitle, crimeDetails, victimDetails, sceneDetails, briefContext, acceptTarget, rejectTarget) {
    // Primary goal: Create an irresistible hook sequence (4 passages) that grabs player attention
    // Structure: 1. Visual/Text Hook -> 2. Brief Context -> 3. Accept/Reject Choice -> 4. Confirmation/Transition
    // Corrected Structure: Uses CMD:typ=intro for steps 1, 2, 4 and CMD:typ=branch for step 3 (choice).

    // Define UIDs for the 4 passages
    DEFINE hookPassageUID = entry_point_id // Use entry_point_id for the first passage
    DEFINE contextPassageUID = stepIDPrefix + "_context" // Internal passages can use derived IDs
    DEFINE choicePassageUID = stepIDPrefix + "_choice"
    DEFINE confirmPassageUID_Base = stepIDPrefix + "_confirm" // Base for accept/decline variations

    DEFINE hookName = caseTitle + " - The Hook"
    DEFINE contextName = caseTitle + " - Initial Context"
    DEFINE choiceName = caseTitle + " - Take the Case?"
    DEFINE confirmName_Base = caseTitle + " - Decision Made"

    // == Passage 1: The Hook ==
    PROCEDURE CreateVisualHook(crimeDetails, sceneDetails) {
        // Select a single striking image element
        DEFINE visualOptions = [
            ExtractUnusualEvidence(crimeDetails),
            CreateJuxtaposition(victimDetails, sceneDetails),
            CaptureDramaticMoment(crimeDetails)
        ]

        // Assume SelectMostImpactful returns an object { imageAlias: "...", imageDescription: "..." }
        DEFINE selectedVisualInfo = SelectMostImpactful(visualOptions)
        DEFINE selectedVisualAlias = selectedVisualInfo.imageAlias
        DEFINE selectedVisualDesc = selectedVisualInfo.imageDescription

        // Visual hook must:
        // - Focus on a single striking detail
        // - Be specific to this case (not generic)
        // - Create immediate mental image

        RETURN selectedVisualInfo // Return the whole info object
    }

    // Step 2: Generate text hook component
    PROCEDURE CreateTextHook(crimeDetails, victimDetails) {
        DEFINE shockingRevelation = ExtractMostShocking(crimeDetails)
        DEFINE unexpectedTwist = FindContradiction(crimeDetails, victimDetails)

        // Add emphasis with CAPITALIZATION on 1-2 key terms
        DEFINE capitalizedRevelation = AddEmphasis(shockingRevelation)

        // Format as punchy, present-tense statements
        DEFINE textHook = capitalizedRevelation + " " + unexpectedTwist

        // Text hook must:
        // - Include shocking revelation AND unexpected twist
        // - Use present tense for immediacy
        // - Keep sentences short (5-10 words)
        // - Include concrete details that create questions

        RETURN textHook
    }

    // Step 3: Format the complete hook in SLPN (Corrected)
    DEFINE visualInfo = CreateVisualHook(crimeDetails, sceneDetails)
    DEFINE textComponent = CreateTextHook(crimeDetails, victimDetails)

    // Create the single step for the intro command
    DEFINE hookStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=" + visualInfo.imageAlias + ";imd=\"" + visualInfo.imageDescription + "\";" +
                      "cmp=CMP:typ=introStepText;txt=TITLE;mnt=\"" + caseTitle + "\";sbt=\"" + textComponent + "\";" +
                      "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Continue...\";" // No ops/brn here

    // Define the move action at the command level
    DEFINE hookAction = "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + contextPassageUID

    // Combine into the intro command
    DEFINE slpnPassage1 = "PSG:uid=" + hookPassageUID + ";nam=\"" + hookName + "\";tag=NARRATIVE|INTRO;" +
                           "cmd=CMD:typ=intro;" + hookAction + ";" + hookStep

    // == Passage 2: Brief Context ==
    PROCEDURE CreateContextContent(briefContext) {
        // Add SEE/DO/LEARN structure
        DEFINE seeComponent = "[SEE: Case file summary]"
        DEFINE learnComponent = "[LEARN: " + briefContext + "]"
        DEFINE doComponent = "[DO: Consider if you want to take this case]"
        RETURN seeComponent + " | " + learnComponent + " | " + doComponent // Use pipe delimiter for breakdown lines
    }
    DEFINE contextContent = CreateContextContent(briefContext)

    // Create the single step for the intro command
    DEFINE contextStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_file_summary;imd=\"Case file with initial details\";" +
                         "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + contextContent + "\";" +
                         "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Proceed\";" // No ops/brn here

    // Define the move action at the command level
    DEFINE contextAction = "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + choicePassageUID

    // Combine into the intro command
    DEFINE slpnPassage2 = "PSG:uid=" + contextPassageUID + ";nam=\"" + contextName + "\";tag=NARRATIVE|INTRO;" +
                           "cmd=CMD:typ=intro;" + contextAction + ";" + contextStep

    // == Passage 3: Accept/Reject Choice (Corrected to use Branch Command) ==
    DEFINE choiceDescription = "[DO: Accept the challenge or decline?]" // More like a prompt for the branch
    // Define branch options directly
    DEFINE choiceOptions = "ops=BOP:onm=\"Accept Case\";img=\"accept_case\";imd=\"Accept the case and investigate\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + confirmPassageUID_Base + "_ACCEPT|" +
                         "BOP:onm=\"Decline Case\";img=\"decline_case\";imd=\"Decline the case and return to HQ\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + confirmPassageUID_Base + "_DECLINE"

    // Format the SLPN using CMD:typ=branch
    DEFINE slpnPassage3 = "PSG:uid=" + choicePassageUID + ";nam=\"" + choiceName + "\";tag=NARRATIVE|INTRO|CHOICE;" +
                           "cmd=CMD:typ=branch;bds=\"" + choiceDescription + "\";brp=once;bpr=option-list;bit=blocking;" + choiceOptions // Use option-list for explicit choices

    // == Passage 4: Confirmation / Transition ==
    // Two versions of this passage: one for accept, one for decline.

    // 4a: Accept Confirmation (Corrected)
    DEFINE acceptConfirmUID = confirmPassageUID_Base + "_ACCEPT"
    DEFINE acceptConfirmName = confirmName_Base + " (Accepted)"
    DEFINE acceptConfirmContent = "[LEARN: Case accepted. Preparing evidence drive...]"
    // Create the single step
    DEFINE acceptConfirmStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_accepted;imd=\"Evidence drive preparation\";" +
                             "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + acceptConfirmContent + "\";" +
                             "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Start Investigation\";" // No ops/brn here
    // Define the move action at the command level
    DEFINE acceptConfirmAction = "act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=" + acceptTarget // e.g., EVIDENCE or specific intro sequence start
    // Combine into the intro command
    DEFINE slpnPassage4_Accept = "PSG:uid=" + acceptConfirmUID + ";nam=\"" + acceptConfirmName + "\";tag=NARRATIVE|INTRO;" +
                                "cmd=CMD:typ=intro;" + acceptConfirmAction + ";" + acceptConfirmStep

    // 4b: Decline Confirmation (Corrected)
    DEFINE declineConfirmUID = confirmPassageUID_Base + "_DECLINE"
    DEFINE declineConfirmName = confirmName_Base + " (Declined)"
    DEFINE declineConfirmContent = "[LEARN: Case declined. Returning to main menu...]"
    // Create the single step
    DEFINE declineConfirmStep = "STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=case_declined;imd=\"Return to main menu\";" +
                              "cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin=\"" + declineConfirmContent + "\";" +
                              "cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex=\"Okay\";" // No ops/brn here
    // Define the move action at the command level
    DEFINE declineConfirmAction = "act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=" + rejectTarget // e.g., HOME or case selection screen
    // Combine into the intro command
    DEFINE slpnPassage4_Decline = "PSG:uid=" + declineConfirmUID + ";nam=\"" + declineConfirmName + "\";tag=NARRATIVE|INTRO;" +
                                 "cmd=CMD:typ=intro;" + declineConfirmAction + ";" + declineConfirmStep

    // Validation check (Checks content, structure change doesn't affect this)
    PROCEDURE ValidateHookSequence(visualInfo, textComponent, contextContent, choiceDescription, acceptConfirmContent, declineConfirmContent) {
        // Adjusted visual check slightly if CreateVisualHook returns an object
        VALIDATE visualInfo.imageAlias CONTAINS specific_case_detail_indicator // Assuming alias contains something specific
        VALIDATE textComponent CONTAINS both_shock_AND_twist
        VALIDATE LENGTH(textComponent) IS_APPROPRIATE // Check text length, not combined content
        VALIDATE contextContent CONTAINS "[LEARN:"
        VALIDATE choiceDescription CONTAINS "[DO:" // Check the branch description/prompt
        VALIDATE acceptConfirmContent CONTAINS "accepted"
        VALIDATE declineConfirmContent CONTAINS "declined"
    }

    // Pass the correct variables to validation
    ValidateHookSequence(visualInfo, textComponent, contextContent, choiceDescription, acceptConfirmContent, declineConfirmContent)

    // Combine all generated passages into a single multi-line string or structured format
    DEFINE allPassages = slpnPassage1 + "

" + slpnPassage2 + "

" + slpnPassage3 + "

" + slpnPassage4_Accept + "

" + slpnPassage4_Decline

    RETURN allPassages
}
{# END_PHENOTYPE: CASE_HOOK #}

{# PHENOTYPE: INTRO_SEQUENCE (REVISED FOR THEORIES) #}
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
        RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=NARRATIVE|INTRO;" +
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
            RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=NARRATIVE|INTRO|THEORY;" +
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
        RETURN "PSG:uid=" + uid + ";nam=\"" + name + "\";tag=NARRATIVE|INTRO|CHOICE;" +
               "cmd=CMD:typ=branch;bds=\"" + choicePrompt + "\";brp=once;bpr=option-list;bit=blocking;ops=" + branchOptions
    }

    DEFINE slpnChoicePassage = CreateTheoryChoicePassage(finalChoiceUID, choiceName, theories, choicePrompt)
    allPassages += "
\n" + slpnChoicePassage
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
                           statusSummary + "\\\";brn=BRN:bds=\\\"Investigation Options\\\";brp=re-playable;bpr=block-panel;bit=blocking;ops=" + 
                           navigationOptions + ";"
    allPassages += slpnHubPassage

    // == Passage 2: Case Briefing ==
    PROCEDURE CreateBriefingPassage(uid, name, fullCaseStatus, returnHubUID) { // Use returnHubUID param name
        DEFINE see = "[SEE: Detailed case file and evidence board connections]"
        DEFINE learn = "[LEARN: Full Case Details: " + fullCaseStatus + "]"
        DEFINE content = see + " " + learn
        DEFINE options = "BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Briefing\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnBriefingPassage = CreateBriefingPassage(briefingUID, briefingName, caseStatus, hubUID) // Use full caseStatus here
    allPassages += "\n\n" + slpnBriefingPassage

    // == Passage 3: Current Objectives ==
    PROCEDURE CreateObjectivesPassage(uid, name, objectivesList, returnHubUID) { // Use returnHubUID param name
        DEFINE see = "[SEE: List of current tasks and leads]"
        DEFINE learn = "[LEARN: Objectives: " + FormatObjectives(objectivesList) + "]" // Needs FormatObjectives helper
        DEFINE content = see + " " + learn
        DEFINE options = "BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Current Objectives\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnObjectivesPassage = CreateObjectivesPassage(objectivesUID, objectivesName, currentObjectives, hubUID)
    allPassages += "\n\n" + slpnObjectivesPassage

    // == Passage 4: Investigator Notes ==
    PROCEDURE CreateNotesPassage(uid, name, returnHubUID) { // Use returnHubUID param name
        // This passage might dynamically load notes via application logic rather than static content.
        DEFINE see = "[SEE: Your personal notebook interface]"
        DEFINE do = "[DO: Review, add, or organize your notes]"
        DEFINE content = see + " " + do + " [INFO: Notes are managed by the application]"
        DEFINE options = "BOP:onm=\"Return to Hub\";ods=\"Close notebook and return to hub\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnHubUID // Ensure target is the main hub UID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Investigator Notes\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";"
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
// PSG:uid=INVESTIGATION_HUB_2;nam="Investigation Hub";CNT;BOT:lin="[SEE: Investigation board with evidence and leads] [DO: Select your next investigative focus] [LEARN: Victim found dead in recording studio. Time of death: between 9-11 PM. Key evidence: bloodied microphone, studio access logs...]";brn=BRN:bds="Investigation Options";brp=re-playable;bpr=block-panel;bit=blocking;ops=BOP:onm="Crime Scene";ods="Return to the studio";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_COLLECTION_3|BOP:onm="Interview Witnesses";ods="Speak with people present that night";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=SUSPECT_LIST_4|BOP:onm="Forensic Analysis";ods="Check lab results";cnd=CND:typ=checkAspect;asp=forensic_samples_collected;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_VERIFICATION_8|BOP:onm="Review Evidence";ods="Examine collected evidence";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=EVIDENCE;
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
        DEFINE slpnScenePassage = "PSG:uid=" + sceneUID + ";nam=\\\"" + sceneName + "\\\";CNT;BOT:lin=\\\"" + 
                                 sceneContent + "\\\";brn=BRN:bds=\\\"Examine " + sceneName + "\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + 
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
PROCEDURE GenerateEvidenceExamination(stepIDPrefix, entry_point_id, evidenceID, evidenceName, evidenceDetails, relevance, returnPassage) {
    // Primary goal: Create a 4-passage sequence for detailed evidence examination.
    // Structure: 1. Observe -> 2. Analyze -> 3. Relevance -> 4. Confirm/Note
    
    // Define UIDs for the 4 passages
    DEFINE observeUID = entry_point_id
    DEFINE analyzeUID = stepIDPrefix + "_analyze"
    DEFINE relevanceUID = stepIDPrefix + "_relevance"
    DEFINE confirmUID = stepIDPrefix + "_confirm"

    DEFINE observeName = "Observe " + evidenceName
    DEFINE analyzeName = "Analyze " + evidenceName
    DEFINE relevanceName = "Relevance of " + evidenceName
    DEFINE confirmName = "Noting " + evidenceName

    DEFINE allPassages = ""

    // == Passage 1: Observe ==
    PROCEDURE CreateObservePassage(uid, name, evidenceName, nextPassageUID) {
        DEFINE content = "[SEE: Close-up view of " + evidenceName + "] [DO: Look for details] [LEARN: Initial observations]"
        DEFINE options = "BOP:onm=\\\"Examine Further\\\";img=\\\"evidence_" + evidenceID + "_closeup\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Initial Observation\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateObservePassage(observeUID, observeName, evidenceName, analyzeUID)
    allPassages += slpnPassage1

    // == Passage 2: Analyze ==
    PROCEDURE CreateAnalyzePassage(uid, name, evidenceDetails, nextPassageUID) {
        DEFINE content = "[LEARN: Findings: '" + FormatClue(evidenceDetails) + "'] [DO: Consider the implications] [SEE: Detailed analysis results]"
        DEFINE options = "BOP:onm=\\\"Determine Relevance\\\";img=\\\"evidence_" + evidenceID + "_analysis\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Analysis Results\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateAnalyzePassage(analyzeUID, analyzeName, evidenceDetails, relevanceUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Relevance ==
    PROCEDURE CreateRelevancePassage(uid, name, relevance, nextPassageUID) {
        DEFINE content = "[LEARN: Relevance: '" + FormatRelevance(relevance) + "'] [DO: Decide whether to note this]"
        DEFINE options = "BOP:onm=\\\"Make Note\\\";ods=\\\"Add this clue to your case file\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Relevance\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    // Use relevanceUID (derived) here, target confirmUID (derived)
    DEFINE slpnPassage3 = CreateRelevancePassage(relevanceUID, relevanceName, relevance, confirmUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Confirm/Note ==
    PROCEDURE CreateConfirmPassage(uid, name, evidenceID, returnPassage) {
        DEFINE content = "[INFO: Clue noted. This information is now available in your evidence review.]"
        // Option to return to the previous location/hub
        DEFINE options = "BOP:onm=\\\"Return\\\";ods=\\\"Go back\\\";" +
                       "act=UAS:asp=" + evidenceID + "_examined;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Clue Recorded\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    // Use confirmUID (derived) here
    DEFINE slpnPassage4 = CreateConfirmPassage(confirmUID, confirmName, evidenceID, returnPassage)
    allPassages += "\n\n" + slpnPassage4
    

    
    RETURN allPassages
}
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
        
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + overviewContent + "\\\";brn=BRN:bds=\\\"Suspects\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnListPassage = CreateListIntroPassage(listUID, listName, suspects, returnPassage)
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
                           
            RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Suspect Details\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";"
        }
        
        DEFINE slpnDetailPassage = CreateDetailPassage(detailUID, detailName, suspect, listUID)
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
                             profileContent + "\\\";brn=BRN:bds=\\\"Suspect Profile\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + 
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
// ... existing code ...

{# PHENOTYPE: DEDUCTION_PUZZLE #}
PROCEDURE GenerateDeductionPuzzle(stepIDPrefix, entry_point_id, suspectID, suspectName, statementsAndEvidence, lieIndex, successStepID, failureStepID) {
    // Primary goal: Create interactive challenge comparing statements to evidence snippets.
    // Structure: 1. Intro -> 2..N+1. Statement/Evidence Comparison -> N+2. Final Choice
    // Generates N + 2 passages where N is the number of statement/evidence pairs.
    // Input: statementsAndEvidence is a list of { statement: "text", evidenceSnippet: "text" }
    // Input: lieIndex indicates the index of the statement that is the lie.
    // Output: Sets aspect deduction_attempt_X_choice = index (0-based) of selected lie on final choice.

    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Intro["_INTRO"] --> Compare0["_COMPARE_0"]
        Compare0 --> Compare1["_COMPARE_1"]
        Compare1 --> CompareN["..."]
        CompareN --> FinalChoice["_FINAL_CHOICE"]
        
        FinalChoice --"Select Lie (Correct)"--> Success[successStepID (External)]
        FinalChoice --"Select Truth (Incorrect)"--> Failure[failureStepID (External)]
    ```
    */

    DEFINE introUID = entry_point_id
    DEFINE finalChoiceUID = stepIDPrefix + "_FINAL_CHOICE"
    DEFINE introName = "Analyze " + suspectName + " - Intro"
    DEFINE finalChoiceName = "Analyze " + suspectName + " - Final Choice"
    
    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // == Passage 1: Introduction ==
    PROCEDURE CreatePuzzleIntro(uid, name, suspectName, firstStatementUID) {
        DEFINE content = "[SEE: Deduction interface] [DO: Compare each part of " + suspectName + "'s statement with relevant evidence.] [LEARN: Identify the inconsistency.]"
        DEFINE options = "BOP:onm=\\\"Begin Analysis\\\";img=\\\"deduction_interface\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + firstStatementUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Statement Analysis\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE firstStatementUID = stepIDPrefix + "_COMPARE_0"
    DEFINE slpnPassageIntro = CreatePuzzleIntro(introUID, introName, suspectName, firstStatementUID)
    allPassages += slpnPassageIntro
    passageCounter++

    // == Passages 2 to N+1: Statement/Evidence Comparison ==
    FOR EACH item IN statementsAndEvidence INDEX i {
        DEFINE compareUID = stepIDPrefix + "_COMPARE_" + i
        DEFINE compareName = suspectName + " - Compare Statement " + (i + 1)
        DEFINE nextPassageUID = IF i == statementsAndEvidence.length - 1 THEN finalChoiceUID ELSE stepIDPrefix + "_COMPARE_" + (i + 1)

        PROCEDURE CreateComparePassage(uid, name, statement, evidenceSnippet, nextPassageUID) {
            DEFINE content = "[LEARN: Statement: '" + statement + "' | Evidence: '" + evidenceSnippet + "'] [DO: Does the evidence support this statement?]"
            // Simple progression, actual deduction happens in the final choice passage.
            DEFINE options = "BOP:onm=\\\"Next Statement\\\";img=\\\"compare_evidence\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
            RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Compare Evidence\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
        }
        DEFINE slpnPassageCompare = CreateComparePassage(compareUID, compareName, item.statement, item.evidenceSnippet, nextPassageUID)
        allPassages += "\n\n" + slpnPassageCompare
        passageCounter++
    }

    // == Passage N+2: Final Choice ==
    PROCEDURE CreateFinalChoicePassage(uid, name, suspectID, statementsAndEvidence, lieIndex, successStepID, failureStepID) {
        DEFINE content = "[DO: Based on the comparisons, select the statement you believe is the lie.]"
        DEFINE options = ""
        FOR EACH item IN statementsAndEvidence INDEX i {
            IF i > 0 { options += "|" }
            DEFINE targetStepID = IF i == lieIndex THEN successStepID ELSE failureStepID
            // Set an aspect indicating the player's choice for potential feedback later
            DEFINE aspectSetAction = "UAS:asp=deduction_attempt_" + suspectID + "_choice;uty=SET;val=" + i
            options += "BOP:onm=\\\"'" + item.statement + "'\\\";img=\\\"statement_" + i + "\\\";" +
                       "cnd=CND:typ=checkAspect;asp=deduction_attempt_" + suspectID + "_made;cmp=EQ;val=false;" + // Prevent multiple attempts here
                       "act=" + aspectSetAction + "|UAS:asp=deduction_attempt_" + suspectID + "_made;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + targetStepID
        }
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Make Your Deduction\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassageFinalChoice = CreateFinalChoicePassage(finalChoiceUID, finalChoiceName, suspectID, statementsAndEvidence, lieIndex, successStepID, failureStepID)
    allPassages += "\n\n" + slpnPassageFinalChoice
    passageCounter++

    // Validation check
    PROCEDURE ValidateDeductionPuzzleSequence(passageCounter, statementsAndEvidence, successStepID, failureStepID) {
        VALIDATE passageCounter == statementsAndEvidence.length + 2
        // Check links: Intro -> Compare0, Compare_i -> Compare_i+1, Compare_N-1 -> FinalChoice
        // Check FinalChoice options link to success/failure
    }
    
    ValidateDeductionPuzzleSequence(passageCounter, statementsAndEvidence, successStepID, failureStepID)
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix is DEDUCTION_PUZZLE_9, suspectID is 'marcus', successStepID is DEDUCTION_SUCCESS_10, failureStepID is DEDUCTION_FAILURE_11.
// statementsAndEvidence: [ {statement: "S1", evidenceSnippet: "E1"}, {statement: "S2", evidenceSnippet: "E2"}, {statement: "S3 (Lie)", evidenceSnippet: "E3"} ] , lieIndex: 2
// Output includes:
// PSG:uid=DEDUCTION_PUZZLE_9_INTRO;...;ops=BOP:...;tgt=DEDUCTION_PUZZLE_9_COMPARE_0;
// PSG:uid=DEDUCTION_PUZZLE_9_COMPARE_0;...;ops=BOP:...;tgt=DEDUCTION_PUZZLE_9_COMPARE_1;
// PSG:uid=DEDUCTION_PUZZLE_9_COMPARE_1;...;ops=BOP:...;tgt=DEDUCTION_PUZZLE_9_COMPARE_2;
// PSG:uid=DEDUCTION_PUZZLE_9_COMPARE_2;...;ops=BOP:...;tgt=DEDUCTION_PUZZLE_9_FINAL_CHOICE;
// PSG:uid=DEDUCTION_PUZZLE_9_FINAL_CHOICE;...;ops=BOP:onm="'S1'";...;tgt=DEDUCTION_FAILURE_11|BOP:onm="'S2'";...;tgt=DEDUCTION_FAILURE_11|BOP:onm="'S3 (Lie)'";...;tgt=DEDUCTION_SUCCESS_10;
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Correct\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateMsgPassage(msgUID, msgName, explainUID)
    allPassages += slpnPassage1

    // == Passage 2: Explanation ==
    PROCEDURE CreateExplainPassage(uid, name, suspectName, nextPassageUID) {
        DEFINE content = "[LEARN: " + suspectName + " lied about their involvement in the crime.] [DO: Understand the implications.]"
        DEFINE options = "BOP:onm=\\\"Reveal New Evidence\\\";ods=\\\"Discover the evidence that exposes the lie\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Lie Exposed\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"New Evidence\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Next Step\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Incorrect\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateFailMsgPassage(failUID, failName, attemptedStatement, hintUID)
    allPassages += slpnPassage1

    // == Passage 2: Hint/Suggestion ==
    PROCEDURE CreateHintPassage(uid, name, hintText, nextPassageUID) {
        DEFINE content = "[LEARN: Hint: '" + hintText + "'] [DO: Re-evaluate the statements and evidence based on this hint.]"
        DEFINE options = "BOP:onm=\\\"Try Again\\\";ods=\\\"Re-attempt the deduction puzzle\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Hint Provided\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Retry\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Start\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateStartPassage(startUID, startName, evidenceName, verificationType, processUID)
    allPassages += slpnPassage1

    // == Passage 2: Process Details ==
    PROCEDURE CreateProcessPassage(uid, name, analysisDetails, nextPassageUID) {
        DEFINE content = "[LEARN: Analysis Process: '" + analysisDetails + "'] [DO: Await results] [SEE: Analysis in progress]"
        DEFINE options = "BOP:onm=\\\"View Findings\\\";img=\\\"verification_" + evidenceID + "_process\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Analysis Details\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateProcessPassage(processUID, processName, analysisDetails, resultsUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Results/Findings ==
    PROCEDURE CreateResultsPassage(uid, name, findings, verificationType, nextPassageUID) {
        DEFINE formattedFindings = FormatFindings(verificationType, findings)
        DEFINE content = "[SEE: Analysis results visualization] [LEARN: Findings: '" + formattedFindings + "'] [DO: Confirm and note results]"
        DEFINE options = "BOP:onm=\\\"Confirm Results\\\";img=\\\"verification_" + evidenceID + "_results\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Results\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateResultsPassage(resultsUID, resultsName, findings, verificationType, confirmUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Confirmation/Return ==
    PROCEDURE CreateConfirmPassage(uid, name, evidenceID, returnPassage) {
        DEFINE content = "[INFO: Verification complete. Findings logged.] [SEE: Evidence marked as verified]"
        DEFINE options = "BOP:onm=\\\"Return to Investigation\\\";img=\\\"verification_" + evidenceID + "_complete\\\";" +
                       "act=UAS:asp=" + evidenceID + "_verified;uty=SET;val=true|" +
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verification Complete\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Developing Lead\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateHintPassage(hintUID, hintName, breakthroughName, evidenceAUID)
    allPassages += slpnPassage1

    // == Passage 2: Evidence A Connection ==
    PROCEDURE CreateEvidenceAPassage(uid, name, evidenceAName, nextPassageUID) {
        DEFINE content = "[SEE: Focus on " + evidenceAName + "] [LEARN: Considering this piece of evidence...] [DO: Recall its significance.]"
        DEFINE options = "BOP:onm=\\\"Connect Second Piece\\\";ods=\\\"Bring in the related evidence\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Connecting Evidence\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateEvidenceAPassage(evidenceAUID, evidenceAName, connectedEvidence.items[0], evidenceBUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Evidence B Connection ==
    PROCEDURE CreateEvidenceBPassage(uid, name, evidenceBName, nextPassageUID) {
        DEFINE content = "[SEE: Focus on " + evidenceBName + "] [LEARN: And when combined with this piece...] [DO: What does this reveal?]"
        DEFINE options = "BOP:onm=\\\"The Revelation!\\\";ods=\\\"See the critical connection\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Connecting Evidence\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage3 = CreateEvidenceBPassage(evidenceBUID, evidenceBName, connectedEvidence.items[1], revealUID)
    allPassages += "\n\n" + slpnPassage3

    // == Passage 4: Revelation ==
    PROCEDURE CreateRevelationPassage(uid, name, connectedEvidence, revelation, nextPassageUID) {
        DEFINE formattedEvidence = FormatConnectedEvidence(connectedEvidence.items) // Reuse existing helper if available, else simple join
        DEFINE content = "[SEE: Dramatic visualization of connection!] [FEEL: Breakthrough!] [LEARN: Critical connection between " + formattedEvidence + " reveals: '" + revelation + "']"
        DEFINE options = "BOP:onm=\\\"Follow This Lead\\\";ods=\\\"Pursue the new direction\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Breakthrough!\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"New Lead\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Initiate Confrontation\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateApproachPassage(approachUID, approachName, suspectName, presentUID)
    allPassages += slpnPassage1

    // == Passage 2: Present Evidence ==
    PROCEDURE CreatePresentPassage(uid, name, evidencePresentedName, suspectName, nextPassageUID) {
        DEFINE content = "[LEARN: You present the \'" + evidencePresentedName + "\' to " + suspectName + ".] [DO: Observe their reaction closely.]"
        DEFINE options = "BOP:onm=\\\"See Reaction\\\";ods=\\\"How do they respond? \\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Evidence Presented\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreatePresentPassage(presentUID, presentName, evidencePresentedName, suspectName, reactionUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Reaction ==
    PROCEDURE CreateReactionPassage(uid, name, suspectReaction, nextPassageUID) {
        DEFINE content = "[SEE: " + suspectName + " reacts.] [LEARN: Reaction: '" + suspectReaction + "'] [FEEL: Assess their response - truth, deflection, anger?]"
        DEFINE options = "BOP:onm=\\\"Decide Next Move\\\";ods=\\\"Consider your options\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Suspect Reaction\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Confrontation Options\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Point of Accusation\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
            
            RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Final Review: " + suspectName + "\\\";brp=re-playable;bpr=option-list;bit=blocking;ops=" + options + ";" // Re-playable to allow revisiting
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
        
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Who Is Guilty?\\\";brp=once;bpr=option-list;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Verdict Delivered\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage1 = CreateVerdictPassage(verdictUID, verdictName, culpritName, explainUID)
    allPassages += slpnPassage1

    // == Passage 2: Full Explanation ==
    PROCEDURE CreateExplanationPassage(uid, name, caseExplanation, nextPassageUID) {
        DEFINE formattedExplanation = FormatLongText(caseExplanation, 240) 
        DEFINE content = "[LEARN: The Full Story: '" + formattedExplanation + "'] [DO: Review the evidence that sealed the case] [SEE: Timeline of the crime]"
        DEFINE options = "BOP:onm=\\\"Review Key Evidence\\\";img=\\\"explanation_" + culpritID + "\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Full Explanation\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
    }
    DEFINE slpnPassage2 = CreateExplanationPassage(explainUID, explainName, caseExplanation, recapUID)
    allPassages += "\n\n" + slpnPassage2

    // == Passage 3: Evidence Recap ==
    PROCEDURE CreateRecapPassage(uid, name, evidenceConnections, nextPassageUID) {
        DEFINE formattedConnections = String.join(evidenceConnections, ", ")
        DEFINE content = "[SEE: Visualization of connected evidence] [LEARN: Key Evidence: '" + formattedConnections + "'] [DO: Conclude the investigation]"
        DEFINE options = "BOP:onm=\\\"Case Closed\\\";img=\\\"evidence_recap_" + culpritID + "\\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageUID
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Evidence Recap\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
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
        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Case Closed\\\";brp=once;bpr=block-panel;bit=blocking;ops=" + options + ";"
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

