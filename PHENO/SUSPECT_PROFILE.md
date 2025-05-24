{# PHENOTYPE: SUSPECT_PROFILE #}

// This procedure generates:
// - 1 vignette (profile) passage
// - 1 passage per interpretation option (typically 2-3)
// - 1 update passage for correct interpretation
// - 1 dossier reveal branch (optional, if not already revealed)
// For 3 interpretation options, this yields 5-6 passages per suspect profile step.

PROCEDURE GenerateSuspectProfile(
    stepIDPrefix,
    entry_point_id,
    suspectID,
    suspectName,
    vignetteText, // Cinematic, third-person context
    interpretationOptions, // array of { summary, adaResponse, isCorrect }
    dossierAssetID, // asset to reveal
    nextStepID // UID to move to after correct interpretation
) {
    // 1. Cinematic vignette passage
    DEFINE profileUID = entry_point_id
    DEFINE profileName = suspectName + " - Profile"

    PROCEDURE CreateInterpretationOptions(interpretationOptions, profileUID, suspectID) {
        DEFINE options = ""
        FOR i = 0 TO interpretationOptions.length - 1 {
            IF i > 0 { options += "|" }
            options += "BOP:onm=\\"" + interpretationOptions[i].summary + "\\";"
            options += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + profileUID + "_interpret_" + i
        }
        // Dossier reveal option (if not already revealed)
        options += "|BOP:onm=\\"Review Dossier\\";cnd=CND:typ=checkAspect;asp=" + suspectID + "_dossier_revealed;cmp=EQ;val=false;"
        options += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + profileUID + "_dossier_reveal"
        RETURN options
    }

    DEFINE interpretationOptionsStr = CreateInterpretationOptions(interpretationOptions, profileUID, suspectID)

    DEFINE slpnProfilePassage = "PSG:uid=" + profileUID + ";nam=\\"" + profileName + "\\";CNT;BOT:lin=\\"" + vignetteText + "\\";tag=SUSPECT_PROFILE|VIGNETTE;"
    slpnProfilePassage += "brn=BRN:bds=\\"What stands out to you?\\";brp=once;bpr=option-list;bit=ada;ops=" + interpretationOptionsStr + ";"

    // 2. Interpretation option passages (one per option)
    FOR i = 0 TO interpretationOptions.length - 1 {
        DEFINE passageUID = profileUID + "_interpret_" + i
        DEFINE passageName = "Your Insight: " + interpretationOptions[i].summary
        DEFINE botText = interpretationOptions[i].adaResponse
        IF interpretationOptions[i].isCorrect {
            DEFINE tgt = profileUID + "_update_success"
        } ELSE {
            DEFINE tgt = profileUID // loop back to vignette
        }
        slpnProfilePassage += "\nPSG:uid=" + passageUID + ";nam=\\"" + passageName + "\\";CNT;BOT:lin=\\"" + botText + "\\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + tgt + ";"
    }

    // 3. Update passage for correct interpretation
    DEFINE updateSuccessUID = profileUID + "_update_success"
    slpnProfilePassage += "\nPSG:uid=" + updateSuccessUID + ";nam=\\"Update Interpretation Success\\";CNT;BOT:lin=\\"\\";act=UAS:asp=" + suspectID + "_profile_interpreted;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextStepID + ";"

    // 4. Dossier reveal branch (optional)
    DEFINE dossierRevealUID = profileUID + "_dossier_reveal"
    slpnProfilePassage += "\nPSG:uid=" + dossierRevealUID + ";nam=\\"Reveal Dossier\\";CNT;BOT:lin=\\"\\";act=UAS:asp=" + suspectID + "_dossier_revealed;uty=SET;val=true|ACT:aty=REVEAL;aet=" + dossierAssetID + "|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + profileUID + ";"

    RETURN slpnProfilePassage
}

// --- Example: Alan Park Suspect Profile ---
/*
GenerateSuspectProfile(
    stepIDPrefix = "ALAN_PARK_PROFILE",
    entry_point_id = "ALAN_PARK_PROFILE_4",
    suspectID = "alan_park",
    suspectName = "Alan Park",
    vignetteText = "Alan Park stands by the window, sunlight glinting off his silver hair. His suit is immaculate, but his hands fidget with a folded piece of paper. He glances at the empty chair across from him, jaw tight, eyes distant. The office is silent except for the faint hum of a computer left on.",
    interpretationOptions = [
        { summary: "Park's composure is a mask; the way he clutches that paper hints at something weighing on him.", adaResponse: "Good eye. People hide their stress, but their hands always give them away.", isCorrect: true },
        { summary: "He's just lost in thought, probably replaying the accident in his mind.", adaResponse: "Maybe. But there's more to that tension than just grief.", isCorrect: false },
        { summary: "He's perfectly calm, nothing seems out of place.", adaResponse: "You sure? Sometimes the quietest rooms have the loudest secrets.", isCorrect: false }
    ],
    dossierAssetID = "alan_park_dossier",
    nextStepID = "INVESTIGATION_HUB_1"
)
*/

// --- Sample SLPN Block for Alan Park ---
/*
PSG:uid=ALAN_PARK_PROFILE_4;nam="Profile";CNT;BOT:lin="Alan Park stands by the window, sunlight glinting off his silver hair. His suit is immaculate, but his hands fidget with a folded piece of paper. He glances at the empty chair across from him, jaw tight, eyes distant. The office is silent except for the faint hum of a computer left on.";brn=BRN:bds="What stands out to you?";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Park's composure is a mask; the way he clutches that paper hints at something weighing on him.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4_interpret_0|BOP:onm="He's just lost in thought, probably replaying the accident in his mind.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4_interpret_1|BOP:onm="He's perfectly calm, nothing seems out of place.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4_interpret_2|BOP:onm="Review Dossier";cnd=CND:typ=checkAspect;asp=alan_park_dossier_revealed;cmp=EQ;val=false;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4_dossier_reveal;

PSG:uid=ALAN_PARK_PROFILE_4_interpret_0;nam="Insight: Mask";CNT;BOT:lin="Good eye. People hide their stress, but their hands always give them away.";brn=BRN:bds="";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Continue";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4_update_success;

PSG:uid=ALAN_PARK_PROFILE_4_interpret_1;nam="Insight: Thought";CNT;BOT:lin="Maybe. But there's more to that tension than just grief.";brn=BRN:bds="";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Try Again";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4;

PSG:uid=ALAN_PARK_PROFILE_4_interpret_2;nam="Insight: Calm";CNT;BOT:lin="You sure? Sometimes the quietest rooms have the loudest secrets.";brn=BRN:bds="";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Try Again";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4;

PSG:uid=ALAN_PARK_PROFILE_4_update_success;nam="Update Success";CNT;ACT:aty=UAS;asp=alan_park_profile_interpreted;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_1;

PSG:uid=ALAN_PARK_PROFILE_4_dossier_reveal;nam="Dossier Reveal";CNT;ACT:aty=UAS;asp=alan_park_dossier_revealed;uty=SET;val=true|ACT:aty=REVEAL;aet=alan_park_dossier|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=ALAN_PARK_PROFILE_4;
*/

{# END_PHENOTYPE: SUSPECT_PROFILE #}
