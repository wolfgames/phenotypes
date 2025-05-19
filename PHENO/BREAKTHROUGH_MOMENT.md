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
