

{# PHENOTYPE: INVESTIGATION_HUB #}
### INVESTIGATION_HUB

**Purpose**: Serves as the central navigation point for all investigation activities.

**Structure**:
- Status summary showing current case state
- Navigation options to all available locations
- Conditional paths that unlock based on progress
- Evidence review access

**Example**:
```
[SEE: Investigation board with evidence and leads]
[DO: Select your next investigative focus]
[LEARN: Victim found dead in recording studio. Time of death: between 9-11 PM.]

OPTIONS:
- Crime Scene: Return to the studio
- Interview Witnesses: Speak with people present that night
- Forensic Analysis: Check lab results (unlocks after collecting samples)
- Review Evidence: Examine collected evidence
```

PROCEDURE GenerateInvestigationHub(stepIDPrefix, entry_point_id, caseStatus, currentObjectives, availableLocations, unlockedFeatures, conditionalPaths, suspectProfilesTarget) { // Added entry_point_id, suspectProfilesTarget
    // Primary goal: Create central investigation hub and related informational passages.
    // Structure: 1. Main Hub Passage -> Links to 2. Case Briefing, 3. Objectives. May also link to Suspect Profiles.
    // Generates 3 passages total (Hub, Briefing, Objectives).
    
    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Hub["_MAIN (Hub)"] --> Loc1["Location 1 (External)"]
        Hub --> LocN["... Locations (External)"]
        Hub --> Feat1["Feature 1 (External)"]
        Hub --> FeatN["... Features (External)"]
        Hub --> EvReview["EVIDENCE (Application)"]
        Hub --> Suspects["SUSPECT_PROFILES (Generated or External)"]
        Hub --> Briefing["_BRIEFING (Generated)"]
        Hub --> Objectives["_OBJECTIVES (Generated)"]
        Briefing --> Hub
        Objectives --> Hub
    ```
    */
    
    // Define UIDs
    DEFINE hubUID = entry_point_id // Use entry_point_id for the first passage
    DEFINE briefingUID = stepIDPrefix + "_briefing" // Derived IDs for internal passages
    DEFINE objectivesUID = stepIDPrefix + "_objectives"

    DEFINE hubName = "Investigation Hub"
    DEFINE briefingName = "Case Briefing"
    DEFINE objectivesName = "Current Objectives"

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
    
    PROCEDURE CreateNavigationOptions(availableLocations, unlockedFeatures, conditionalPaths, derivedBriefingUID, derivedObjectivesUID, hubUID, derivedSuspectProfilesTarget) { // Pass derived UIDs and suspect target
        // Modified to include links to briefing, objectives, and potentially suspect profiles
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

        // Add suspect profiles review option
        IF derivedSuspectProfilesTarget != "" && derivedSuspectProfilesTarget != null {
            IF optionIndex > 0 { options += "|" }
            options += "BOP:onm=\"Review Suspect Profiles\";ods=\"Examine profiles of individuals involved\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + derivedSuspectProfilesTarget // Assuming passage type for consistency
            optionIndex++
        }
        
        RETURN options
    }
    
    DEFINE statusSummary = CreateStatusSummary(SummarizeCase(caseStatus)) // Use summarized version for main hub
    DEFINE navigationOptions = CreateNavigationOptions(availableLocations, unlockedFeatures, conditionalPaths, briefingUID, objectivesUID, hubUID, suspectProfilesTarget) // Pass derived UIDs and suspect target
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

    // Validation check
    PROCEDURE ValidateInvestigationHub(slpnHubPassage, slpnBriefingPassage, slpnObjectivesPassage, suspectProfilesTarget) {
        VALIDATE slpnHubPassage CONTAINS "Review Evidence" AND briefingUID AND objectivesUID
        VALIDATE slpnBriefingPassage CONTAINS hubUID
        VALIDATE slpnObjectivesPassage CONTAINS hubUID
        IF suspectProfilesTarget != "" && suspectProfilesTarget != null {
            VALIDATE slpnHubPassage CONTAINS suspectProfilesTarget
        }
    }
    
    ValidateInvestigationHub(slpnHubPassage, slpnBriefingPassage, slpnObjectivesPassage, suspectProfilesTarget)
    
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
// PSG:uid=INVESTIGATION_HUB_EXAMPLE;nam="Investigation Hub";CNT;BOT:lin="[SEE: Investigation board with evidence and leads] [DO: Select your next investigative focus] [LEARN: A renowned scientist, Dr. Aris Thorne, was found murdered in his private observatory. Initial fin...]";brn=BRN:bds="Investigation Options";brp=re-playable;bpr=block-panel;bit=ada;ops=BOP:onm=\"Observatory Crime Scene\";ods=\"Return to Dr. Thorne's observatory\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=OBSERVATORY_CS_1|BOP:onm=\"University Campus\";ods=\"Explore the campus for clues or witnesses\";cnd=CND:typ=checkFlag;flg=observatory_secured;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=UNI_CAMPUS_MAIN|BOP:onm=\"Forensic Database\";ods=\"Access police forensic records\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=APP_FORENSICS|BOP:onm=\"Review Evidence\";ods=\"Examine collected evidence\";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=EVIDENCE|BOP:onm=\"View Case Briefing\";ods=\"Review the full case summary\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE_briefing|BOP:onm=\"Check Objectives\";ods=\"See current investigation goals\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE_objectives|BOP:onm=\"Review Suspect Profiles\";ods=\"Examine profiles of individuals involved\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE_suspects;
//
// PSG:uid=INVESTIGATION_HUB_EXAMPLE_briefing;nam="Case Briefing";CNT;BOT:lin="[SEE: Detailed case file and evidence board connections] [LEARN: Full Case Details: A renowned scientist, Dr. Aris Thorne, was found murdered in his private observatory. Initial findings suggest a struggle, and a rare celestial artifact is missing. The time of death is estimated to be between 10 PM and midnight.]";brn=BRN:bds="Case Briefing";brp=re-playable;bpr=option-list;bit=ada;ops=BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE;
//
// PSG:uid=INVESTIGATION_HUB_EXAMPLE_objectives;nam="Current Objectives";tag=INVESTIGATION_HUB|OBJECTIVES;CNT;BOT:lin="[SEE: List of current tasks and leads] [LEARN: Objectives: Secure Dr. Thorne's observatory, Identify any forced entry points, Question the research assistant who found the body]";brn=BRN:bds="Current Objectives";brp=re-playable;bpr=option-list;bit=ada;ops=BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE;
//
// PSG:uid=INVESTIGATION_HUB_EXAMPLE_suspects;nam="Suspect Profiles";tag=INVESTIGATION_HUB|SUSPECTS;CNT;BOT:lin="[SEE: Dossiers and interrogation notes for all persons of interest] [DO: Select a suspect to review their profile and evidence connections] [INFO: Suspect details are managed here.]";brn=BRN:bds="Suspect Profiles";brp=re-playable;bpr=option-list;bit=ada;ops=BOP:onm=\"Return to Hub\";ods=\"Go back to main investigation view\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_EXAMPLE;

{# END_PHENOTYPE: INVESTIGATION_HUB #}
