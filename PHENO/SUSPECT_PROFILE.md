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
