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
