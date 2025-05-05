# Narrative Delivery Phenotype Dictionary

This dictionary defines the composable building blocks for presenting narrative information (derived from Story Phenotypes: Definitions, Propositions, Axioms) to the player within the gameplay flow. These phenotypes describe *how* story elements are delivered, integrating with the Gameplay Phenotypes and functioning as connectable sub-graphs within the overall gameplay journey. **Core Principle: Show, Don't Tell - Reveal evidence, guide player interpretation.**

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