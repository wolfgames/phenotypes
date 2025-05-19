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
