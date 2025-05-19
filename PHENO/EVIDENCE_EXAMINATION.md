{# PHENOTYPE: EVIDENCE_EXAMINATION #}

PROCEDURE GenerateEvidenceExaminationSequence(stepIDPrefix, entry_point_id, evidenceID, evidenceName, initialNarrativeText, evidenceContextText, followUpNarrativeText, nextPassage) {
    // Primary goal: Create a structured three-passage evidence examination flow.
    // Structure: 1. Initial Narrative (Discovery) -> 2. Action-Only Reveal -> 3. Follow-up Commentary (Reaction/Analysis)

    // --- Input Parameters ---
    // stepIDPrefix: (String) Base prefix for generating unique passage UIDs for the action and follow-up passages.
    // entry_point_id: (String) UID for the first (initial narrative) passage.
    // evidenceID: (String) The unique ID (aet) of the evidence item.
    // evidenceName: (String) The display name of the evidence.
    // initialNarrativeText: (String) Text for the first passage, describing the discovery context (e.g., "You notice a strange device under the victim's desk.").
    // evidenceContextText: (String) Descriptive text for the evidence item itself, used during the REVEAL action (e.g., "A small, metallic device with unfamiliar symbols etched on its surface.").
    // followUpNarrativeText: (String) Text for the third passage, providing commentary, analysis, or relevance of the evidence (e.g., "This device doesn't look like standard Earth technology. Its symbols are unlike anything you've seen. This could be a key clue to the perpetrators' origins.").
    // nextPassage: (String) The UID of the passage to transition to after the follow-up commentary.

    // --- UIDs ---
    DEFINE initialPassageUID = entry_point_id
    DEFINE actionRevealUID = stepIDPrefix + "_actionReveal_" + evidenceID
    DEFINE followUpPassageUID = stepIDPrefix + "_followUp_" + evidenceID

    DEFINE allPassages = ""

    // --- Passage 1: Initial Narrative (Discovery) ---
    DEFINE passage1Name = "Discovery: " + evidenceName
    DEFINE passage1Tags = "EVIDENCE_EXAMINATION|INITIAL_NARRATIVE"
    DEFINE passage1BranchDesc = "What you've found"
    DEFINE passage1ButtonText = "Examine the " + evidenceName
    DEFINE passage1ButtonDesc = "Take a closer look at this item."
    
    DEFINE slpnPassage1 = "PSG:uid=" + initialPassageUID + ";nam=\"" + passage1Name + "\";tag=" + passage1Tags + ";CNT;" +
                          "BOT:lin=\"" + initialNarrativeText + "\";" +
                          "brn=BRN:bds=\"" + passage1BranchDesc + "\";brp=once;bpr=option-list;bit=ada;" +
                          "ops=BOP:onm=\"" + passage1ButtonText + "\";ods=\"" + passage1ButtonDesc + "\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + actionRevealUID + ";"
    allPassages += slpnPassage1

    // --- Passage 2: Action-Only Evidence Reveal ---
    DEFINE passage2Name = "Revealing: " + evidenceName
    DEFINE passage2Tags = "EVIDENCE_EXAMINATION|ACTION_REVEAL"
    // No BOT for this passage.
    
    DEFINE slpnPassage2 = "PSG:uid=" + actionRevealUID + ";nam=\"" + passage2Name + "\";tag=" + passage2Tags + ";CNT;" + // Added CNT based on original example, though unusual for action-only
                          "ACT:aty=REVEAL;aet=" + evidenceID + ";axt=\"" + evidenceContextText + "\";" +
                          "ACT:aty=MOVE;amt=AMT:typ=evidence;tgt=" + evidenceID + ";" +
                          "TRG:uid=" + evidenceID + "_first_view;trg=FIRST_VIEW;tar=" + evidenceID + ";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + followUpPassageUID + ";"
    allPassages += "\n\n" + slpnPassage2
    
    // --- Passage 3: Follow-up Commentary (Reaction/Analysis) ---
    DEFINE passage3Name = "Thoughts on: " + evidenceName
    DEFINE passage3Tags = "EVIDENCE_EXAMINATION|FOLLOWUP_COMMENTARY"
    DEFINE passage3BranchDesc = "Evidence Analysis"
    DEFINE passage3ButtonText = "Continue Investigation"
    DEFINE passage3ButtonDesc = "Proceed with your investigation."

    DEFINE slpnPassage3 = "PSG:uid=" + followUpPassageUID + ";nam=\"" + passage3Name + "\";tag=" + passage3Tags + ";CNT;" +
                          "BOT:lin=\"" + followUpNarrativeText + "\";" +
                          "brn=BRN:bds=\"" + passage3BranchDesc + "\";brp=once;bpr=option-list;bit=ada;" +
                          "ops=BOP:onm=\"" + passage3ButtonText + "\";ods=\"" + passage3ButtonDesc + "\";" +
                                "act=UAS:asp=" + evidenceID + "_examined;uty=SET;val=true|" +
                                "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassage + ";"
    allPassages += "\n\n" + slpnPassage3
    
    RETURN allPassages
}

// Example usage based on the original phenotype's example:
/*
CALL GenerateEvidenceExaminationSequence(
    stepIDPrefix = "EVIDENCE_EXAM_01", 
    entry_point_id = "EVIDENCE_EXAM_01_START", 
    evidenceID = "bloody_knife", 
    evidenceName = "Bloody Knife", 
    initialNarrativeText = "[SEE: You notice a Bloody Knife on the floor.] [DO: Investigate further?]",
    evidenceContextText = "Kitchen knife with blood residue on the blade. Partial fingerprint visible on handle.", 
    followUpNarrativeText = "[THINK: This kitchen knife has blood on it and a partial print. It's a potential murder weapon, especially since it matches the victim's wound pattern. This is a critical find.]",
    nextPassage = "CRIME_SCENE_02"
)
*/

// --- Sample SLPN Output (Based on the example usage above) ---
/*
PSG:uid=EVIDENCE_EXAM_01_START;nam="Discovery: Bloody Knife";tag=EVIDENCE_EXAMINATION|INITIAL_NARRATIVE;CNT;BOT:lin="[SEE: You notice a Bloody Knife on the floor.] [DO: Investigate further?]";brn=BRN:bds="What you've found";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Examine the Bloody Knife";ods="Take a closer look at this item.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_EXAM_01_actionReveal_bloody_knife;

PSG:uid=EVIDENCE_EXAM_01_actionReveal_bloody_knife;nam="Revealing: Bloody Knife";tag=EVIDENCE_EXAMINATION|ACTION_REVEAL;CNT;ACT:aty=REVEAL;aet=bloody_knife;axt="Kitchen knife with blood residue on the blade. Partial fingerprint visible on handle.";ACT:aty=MOVE;amt=AMT:typ=evidence;tgt=bloody_knife;TRG:uid=bloody_knife_first_view;trg=FIRST_VIEW;tar=bloody_knife;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_EXAM_01_followUp_bloody_knife;

PSG:uid=EVIDENCE_EXAM_01_followUp_bloody_knife;nam="Thoughts on: Bloody Knife";tag=EVIDENCE_EXAMINATION|FOLLOWUP_COMMENTARY;CNT;BOT:lin="[THINK: This kitchen knife has blood on it and a partial print. It's a potential murder weapon, especially since it matches the victim's wound pattern. This is a critical find.]";brn=BRN:bds="Evidence Analysis";brp=once;bpr=option-list;bit=ada;ops=BOP:onm="Continue Investigation";ods="Proceed with your investigation.";act=UAS:asp=bloody_knife_examined;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=CRIME_SCENE_02;
*/

{# END_PHENOTYPE: EVIDENCE_EXAMINATION #}
