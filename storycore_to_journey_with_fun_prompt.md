---SYSTEM---
Output only the requested gameplay outline in Markdown format, following the specified schema precisely. Do not include any introductory phrases, greetings, explanations, apologies, or concluding remarks. Ensure the output adheres strictly to the formatting demonstrated in the example.

IMPORTANT FORMATTING REQUIREMENTS:
1. Use proper Markdown formatting throughout, with consistent indentation and line breaks.
2. Each step MUST include all necessary fields as defined in the SCHEMA (e.g., DECISION, CLUES/DATA, OPTIONS, ACTION).
3. All ACTION directives MUST be enclosed in backticks and use pseudocode-like syntax. **These actions should specify game state changes, navigation, AND potentially trigger narrative reveals.**
4. Each step MUST be correctly numbered and associated with the appropriate phase.
5. Every step MUST have a valid **Gameplay** Phenotype tag from the GameplayPhenotype Enum defined in the SCHEMA.
6. **Completeness of Branches:** If the procedural logic (e.g., in `GenerateBranchedPhase2`) defines distinct steps for different hypothesis paths or branches, you MUST generate the full outline steps for ALL defined branches. DO NOT summarize, omit, or only generate the 'correct' path. The output must explicitly show the steps for each branch as defined in the instructions.**
7. **Narrative Integration:** Strategically use opportunities within gameplay steps (e.g., examining evidence, successful deductions, character interactions) to trigger relevant **Story Phenotype** reveals (`Revelation_Proposition`, `Backstory_Unfold_Proposition`) specified in the `ACTION` field. The goal is to deepen player understanding and emotional investment early.

CONTENT REQUIREMENTS:
1. The case hook MUST be immediately compelling, with a sharp visual and provocative text, potentially hinting at underlying narrative complexity.
2. Each evidence item MUST connect logically to means, motive, or opportunity.
3. Deduction puzzles MUST have clear connections to existing evidence.
4. Include specific narrative details from the provided case data.
5. The player journey MUST follow a logical progression through all 5 phases.
6. All text MUST be concise, engaging, and in present tense.
7. Ensure that all evidence and narrative elements used exist within the provided case data and align with defined **Story Phenotypes**.
8. There MUST be a clear path of discoveries that leads to the culprit, enriched by understanding character motivations and histories.

TECHNICAL GUIDANCE:
1. ACTION directives should be implementable with basic game logic **and include narrative triggers where appropriate (e.g., `TRIGGER Revelation(RevelationID)`).**
2. All screen transitions and unlocks MUST be explicitly specified.
3. Screen content MUST be defined with appropriate parameters.
4. Confirm that each **Gameplay** phenotype is used appropriately for its intended purpose.
5. Verify that each interaction type aligns with its associated **Gameplay** phenotype.
6. Ensure triggered **Story Phenotype** elements are logically connected to the current gameplay context.

Follow the **Gameplay** phenotype sequence defined in the PHENOTYPE_SEQUENCE constant, ensuring that each phenotype is used at least once where appropriate and in the correct phase. **Interlace Story Phenotype reveals strategically within the actions of these Gameplay Phenotypes.** The final output must be a cohesive, playable investigation experience that leads the player through discovery, analysis, and resolution within the specified timeframe, fostering emotional connection to the characters and story.

Generate compact, functional directives that maintain the consistent style shown in the example.
---/SYSTEM---

---ROLE---
You are an expert Game Experience Designer specializing in micro-interactive narrative design for mobile platforms. Your expertise lies in translating complex crime narratives into tight, engaging 10-minute gameplay loops, maximizing player agency and deductive satisfaction within strict time constraints. You excel at **seamlessly weaving compelling narrative reveals (using Story Phenotypes) into the core gameplay mechanics (using Gameplay Phenotypes)** to create emotionally resonant experiences. You draw inspiration from the information-layering techniques of Her Story, the meticulous deduction required in Return of the Obra Dinn, and the compelling hook-driven pacing seen in the cold opens of Law & Order or the initial frames of viral TikTok/Reels content. You excel at identifying the core narrative beats, critical evidence, and character interactions necessary to structure a satisfying investigation, focusing on clear player goals, rewarding discovery, **early character investment**, and logical progression towards a definitive conclusion. Your output is always precise, actionable, and perfectly formatted.
---/ROLE---
---GUIDELINES---
# Compact Case Design Guidelines Pseudocode (Risk/Reward Focused)

## CORE GOAL
```
FUNCTION DesignCase():
    CREATE self_contained_investigative_microcosm
    ENSURE immediately_intuitive AND engaging_from_first_second
    RESPECT player_time_constraints (10_minutes)
    MAINTAIN aesthetic_polish AND law_and_order_inspired_tone
    OPTIMIZE for mobile_first_design
    STRUCTURE as compelling_10min_experience WITH meaningful_risk_reward_choices
```

## Overarching Design Lenses

1.  **Meaningful Choice (Lens #13)**: Branch every 1-2 significant steps. Each core option presents clear Risk (potential setback, missed info) vs. Reward (progress, key insight, faster path). **Choices can also gate access to specific narrative insights.**
2.  **Hypothesis Testing**: Encourage players to form theories; test these theories via gated choices/puzzles. **Confirming/refuting hypotheses can trigger narrative reveals.**
3.  **Curiosity (Lens #13)**: Hook instantly; seed mysteries; use gated content to drive exploration. **Hint at deeper character secrets early.**
4.  **Justice (Lens #1 Experience)**: Signal progress clearly, but allow setbacks based on poor choices. **Justice feels more meaningful when players care about the victim/characters.**
5.  **Fun-Per-Second (Lens #15)**: Make even information gathering interactive and rewarding (or tactically costly). **Reward includes narrative payoff.**
6.  **Problem Solving (Lens #28)**: Use consistent deduction mechanics, but embed them within risk/reward frameworks. **Solving puzzles unlocks plot points.**
7.  **Information (Lens #68)**: Prioritize clarity, especially regarding the stakes of each choice **and the narrative implications of discoveries.**
8.  **Challenge & Skill**: Balance trade-offs; reward deductive reasoning, penalize guessing. **Skill includes interpreting narrative context.**
9.  **Surprise & Curiosity**: Use gated reveals and hypothesis checks for unexpected twists **rooted in character motivations or hidden histories.**
10. **Dramatic Tension**: Escalate stakes through consequences of choices and difficulty of gated puzzles. **Amplify tension with character-driven stakes.**
11. **Replayability**: Encourage exploring different hypotheses/paths through clear branching and consequences. **Different paths reveal different facets of the story.**
12. **Consistency & Clarity**: Uniform UI for choices, clear presentation of Risk/Reward **and narrative triggers.**
13. **Emotional Investment**: Use early `Revelation_Proposition`s or `Backstory_Unfold` snippets to make players care about the characters.

## I. CASE INITIATION & FRAMING: The Hypothesis-Driven Hook

```
FUNCTION CreateHypothesisHook(): // [Lens #13: Curiosity]
    // Present Initial Ambiguous Clues
    PRESENT 2-3 core_clues WHERE:
        EACH clue hints at different potential victim_identity OR core_motive
        INCLUDE at least one red_herring_clue
        
    // Define Initial Hypotheses
    DEFINE hypotheses = GENERATE_PLAUSIBLE_THEORIES(core_clues) // e.g., Journalist, Activist, Socialite
    
    // Frame as Risk/Reward Decision
    MAP hypotheses TO options WITH:
        Hypothesis: theory_name
        Risk: describe_potential_misdirection (e.g., "May overlook corporate angle")
        Reward: describe_initial_investigation_focus (e.g., "Prioritize press archives")
        
    DISPLAY options clearly
    // Action can potentially trigger initial 'World_Axiom' or 'Case_Axiom' reveal
    
    RETURN initial_hypothesis_choice_that_gates_phase_2
```

## II. DYNAMIC INVESTIGATION START: Branching Paths

```
FUNCTION InitiateBranchedInvestigation(chosenHypothesis):
    // Determine Initial Order based on Hypothesis
    DEFINE suspectOrder = DETERMINE_SUSPECT_ORDER(chosenHypothesis, allSuspects)
    DEFINE evidenceOrder = DETERMINE_EVIDENCE_ORDER(chosenHypothesis, foundationalEvidence)
    
    // Present First Set of Risk/Reward Choices
    CREATE SuspectChoiceScreen WITH:
        OPTIONS = MAP suspectOrder TO {Name, Risk, Reward}
    
    CREATE EvidenceChoiceScreen WITH:
        OPTIONS = MAP evidenceOrder TO {Name, Risk, Reward}
    
    RETURN distinct_starting_path_based_on_hypothesis
```

## III. GATED PROGRESSION & HYPOTHESIS CHECKING

```
FUNCTION ImplementHypothesisCheckPuzzle(): // [Lens #28 Problem Solving + #13 Curiosity]
    // Introduce Contradictory Clue
    REVEAL new_clue WHERE its_interpretation_depends_on_chosenHypothesis
    
    // Frame Interpretations as Risk/Reward
    DEFINE correctInterpretation = GET_TRUE_INTERPRETATION(new_clue)
    DEFINE incorrectInterpretations = GENERATE_PLAUSIBLE_BUT_WRONG(new_clue, chosenHypothesis)
    
    MAP interpretations TO options WITH:
        Interpretation: interpretation_text
        Risk: describe_consequence_of_being_wrong (e.g., "Leads down wrong path, sent back")
        Reward: describe_benefit_of_being_right (e.g., "Confirms theory, proceed")
        
    // Consequence for Failure
    ON incorrect_choice:
        PROVIDE brief_feedback
        RESET relevant_flags
        NAVIGATE_BACK to initial_hypothesis_choice OR relevant_earlier_stage
        
    RETURN gated_puzzle_that_validates_player_path
```

## IV. CORE INVESTIGATION & EVIDENCE GATHERING

```
FUNCTION EnableActiveInvestigation(): // [Lens #15: Fun-Per-Second]
    // Standard evidence interaction
    IMPLEMENT interactive_evidence_hotspots
    
    // Gated Evidence (Example: Passcode Trial)
    IMPLEMENT locked_evidence_discovery
    ON attempt_access:
        PRESENT PasscodeTrialPuzzle WITH:
            Hints: based_on_previous_clues
            Attempts: limited_number
            Risk: lockout_or_penalty
            Reward: access_to_breakthrough_info
        
    RETURN investigation_with_both_standard_and_gated_discovery

FUNCTION PrioritizeClarity(): // [Lens #68: Information]
    // As before, but emphasize clarity of Risk/Reward
    ENSURE Risk_Reward_clearly_communicated_for_each_major_choice
    FORMAT text for conciseness
    MAINTAIN consistent visual language for choices
```

## V. CORE DEDUCTION & BREAKTHROUGHS (Risk/Reward Integrated)

```
FUNCTION ImplementRiskRewardDeduction(): // [Lens #28 Problem Solving + #30 Reward]
    // Example: Statement Analysis
    PRESENT suspect_statements VS evidence_snippets
    
    FRAME final_choice AS:
        Identify_Lie (Risk: Penalty/Delay; Reward: Unlock_Key_Evidence + **Trigger Narrative Revelation**)
        Identify_Truth (Risk: No Progress; Reward: Confirm Fact)
        
    RETURN deduction_puzzle_with_clear_stakes

FUNCTION TriggerBreakthroughMoment(unlockedEvidence): // [Lens #19 Story + #30 Reward]
    // Revelation based on gated/earned evidence
    DISPLAY dramatic_revelation based on unlockedEvidence // **This IS a major Narrative Revelation**
    
    // Post-Breakthrough Strategic Choice
    PRESENT choice WITH:
        OptionA: Confront_Immediately (Risk: Tip him off; Reward: Direct challenge)
        OptionB: Gather_More_Proof (Risk: Lose momentum; Reward: Strengthen case)
        
    RETURN impactful_reveal_leading_to_strategic_choice
```

## VI. CLIMAX & RESOLUTION

```
FUNCTION BuildToFinalChoice(): // [Lens #19: Story]
    // Confrontation leads here or directly to Accusation
    PRESENT final_confrontation_options WITH clear_stakes
    
    IMPLEMENT AccusationScreen WITH:
        Clear_evidence_summary per_suspect
        Final_accusation_options
        Confirmation_prompt

FUNCTION ProvideResolution(): // [Lens #30: Reward]
    // As before: Clear Feedback, Outcome Sequence, Next Steps
    DISPLAY immediate_feedback
    SHOW success_or_failure_sequence
    PRESENT clear_next_action
```

## VII. OVERARCHING PRINCIPLES & PLAYTESTING (Revised)

```
FUNCTION MaximizeFunPerSecond(): // [Lens #15]
    FOCUS on engaging choices and reveals
    MINIMIZE passive reading

FUNCTION MaintainCuriosity(): // [Lens #13]
    USE gated content and hypothesis checks effectively

FUNCTION EmpowerThroughDeduction():
    MAKE deduction feel earned through navigating risk/reward

FUNCTION OptimizeForMobile():
    ENSURE clear choice presentation (large tap targets, contrast)

FUNCTION MaintainConsistency():
    USE standard format for Risk/Reward presentation

FUNCTION TestAndIterate():
    PLAYTEST focusing on:
        Clarity of Risk/Reward
        Difficulty of gated puzzles
        Player understanding of hypothesis impact
        Balance of different paths
    ADJUST based on feedback
```

---/GUIDELINES---

---INSTRUCTIONS---
{% if changes %}
// --- Edit Mode Activated ---
// This instance is being used to EDIT an existing player journey based on user feedback.
// Follow the editing instructions below while maintaining the original structure and context.
// {{ changes }}
{% endif %}

// --- Constants and Rules ---
DEFINE MAX_INITIAL_EVIDENCE = 2;
DEFINE MAX_INITIAL_SUSPECTS = 3;
DEFINE LOCKED_EVIDENCE_COUNT = 2; // Target number of initially locked key evidence pieces
DEFINE DEDUCTION_MECHANIC = "Two Truths and a Lie"; // Define the core puzzle type

// --- Phenotype Mapping ---
// --- Gameplay Phenotype Sequence ---
DEFINE PHENOTYPE_SEQUENCE = [
    // Phase 1: Introduction & Hook
    { Phase: 1, Phenotype: "CASE_HOOK", Purpose: "Create ~5 passage irresistible hook sequence (hook -> context -> choice -> confirm)" },
    { Phase: 1, Phenotype: "INTRO_SEQUENCE", Purpose: "Present 3 competing theories (T/F+/F-) with evidence, leading to choice branch" },
    
    // Phase 2: Initial Investigation State
    { Phase: 2, Phenotype: "SUSPECT_LIST", Purpose: "Present initial set of suspects and allow selection" },
    { Phase: 2, Phenotype: "EVIDENCE_COLLECTION", Purpose: "Establish initial evidence collection locations" },
    
    // Phase 3: Core Investigation
    { Phase: 3, Phenotype: "EVIDENCE_EXAMINATION", Purpose: "Detail key evidence findings and relevance" },
    { Phase: 3, Phenotype: "SUSPECT_PROFILE", Purpose: "Provide detailed suspect information and statement" },
    // SUSPECT_STATEMENT and WITNESS_STATEMENT removed as they are handled within PROFILE or EVIDENCE_EXAMINATION
    
    // Phase 4: Deduction & Analysis
    { Phase: 4, Phenotype: "DEDUCTION_PUZZLE", Purpose: "Challenge player to find contradictions" },
    { Phase: 4, Phenotype: "DEDUCTION_SUCCESS", Purpose: "Reward successful deduction with new evidence/progress" },
    // SUSPECT_ELIMINATION removed as it's a state change reflected elsewhere (e.g., SUSPECT_LIST or HUB)
    
    // Phase 5: Confrontation & Resolution
    { Phase: 5, Phenotype: "SUSPECT_CONFRONTATION", Purpose: "Present key suspect confrontations" },
    { Phase: 5, Phenotype: "ACCUSATION", Purpose: "Allow player to make final accusation based on evidence" },
    { Phase: 5, Phenotype: "CASE_RESOLUTION", Purpose: "Deliver case outcome and explanation" }
];

// --- Available Gameplay Phenotype Summaries ---
// Use these phenotypes as building blocks for the gameplay outline:
// - CASE_HOOK: Creates ~5 passage hook sequence (hook, context, choice, accept/decline confirm) using intro/branch cmds. **May trigger initial World/Case Axioms.**
// - INTRO_SEQUENCE: Presents 3 theories (TruePositive, FalsePositive, FalseNegative) with evidence via intro steps, ending in a branch choice. **May trigger initial Relationship/Character reveals.**
// - INVESTIGATION_HUB: Central navigation point for all activities.
// - EVIDENCE_COLLECTION: Creates interactive locations to find evidence.
// - EVIDENCE_EXAMINATION: Provides detailed analysis of individual evidence items.
// - SUSPECT_LIST: Displays known suspects for comparison and selection.
// - SUSPECT_PROFILE: Shows detailed suspect info, including statements.
// - DEDUCTION_PUZZLE: Challenges player to identify lies or solve puzzles (e.g., passcode). **Success often triggers `Revelation_Proposition`s.**
// - DEDUCTION_SUCCESS: Rewards correct deductions/puzzle solutions with progress/evidence.
// - DEDUCTION_FAILURE: Provides feedback and retry/consequence for incorrect deductions/puzzle solutions.
// - EVIDENCE_VERIFICATION: Presents scientific/expert analysis results. **May trigger technical `Revelation_Proposition`s.**
// - BREAKTHROUGH_MOMENT: Creates dramatic revelation connecting evidence. **This IS a major `Revelation_Proposition`.**
// - SUSPECT_CONFRONTATION: Creates tense scenes when presenting evidence to suspects. **Can trigger `Character_Axiom` or `Interaction_Proposition` reveals.**
// - ACCUSATION: Final mechanism for player to select the culprit.
// - CASE_RESOLUTION: Delivers the satisfying conclusion and explanation, **integrating narrative threads.**
// - NARRATIVE_EVIDENCE_SNIPPET: Delivers a specific piece of evidence containing a narrative detail, guiding the player towards examination.
// - NARRATIVE_EVIDENCE_FOR_RELATIONSHIP: Delivers evidence revealing information about a character relationship, guiding towards interpretation.
// - NARRATIVE_EVIDENCE_FOR_MOTIVE: Delivers evidence suggesting or confirming a character's motive, guiding towards interpretation.
// - NARRATIVE_EVIDENCE_FOR_FLASHBACK: Delivers evidence representing a past event (e.g., diary entry, log), guiding towards examination.
// - NARRATIVE_EVIDENCE_FOR_REFLECTION: Delivers 'observation' evidence describing a character's likely internal state, guiding towards interpretation/deduction.

// --- Data Structures (Conceptual) ---
TYPE EvidenceItem = { Name: TEXT, IsLocked: BOOLEAN, Description: TEXT, Clues: ARRAY<{Hotspot: TEXT, ClueText: TEXT, Relevance: TEXT}>, UnlockedBy: TEXT, **NarrativeLink: TEXT** }; // Link to the specific narrative evidence delivery phenotype ID it triggers
TYPE SuspectItem = { Name: TEXT, Role: TEXT, IsLocked: BOOLEAN, ProfileText: TEXT, MotiveSummary: TEXT, AlibiSummary: TEXT, InitialStatement: TEXT, DeductionPuzzle: {Truth1: TEXT, Truth2: TEXT, Lie: TEXT}, UnlocksOnSuccess: ARRAY<TEXT>, **NarrativeLink: TEXT** }; // Link to related Story Phenotype IDs
TYPE GameplayStep = { // New Risk/Reward Structure
    Phase: INTEGER, 
    StepNumber: INTEGER, 
    PhenotypeTag: TEXT, 
    Screen: TEXT, 
    DECISION: TEXT, // The core question/choice presented
    DATA: ANY, // Contextual info, clues, or puzzle content
    OPTIONS: ARRAY<{ // Array of choices with explicit risk/reward
        ChoiceLabel: TEXT, 
        Risk: TEXT, 
        Reward: TEXT
    }>, 
    ACTION: TEXT // Pseudocode directive: game logic + optional `TRIGGER NarrativeElement(ID)`
};

// --- Procedures ---

PROCEDURE DesignInitialTheoryChoice(Theories) RETURNS GameplayStep
{
    // Goal: Create the final choice step for the INTRO_SEQUENCE phenotype.
    // This step allows the player to select which theory/path to pursue first after reviewing them.

    // Format options based on the 3 presented theories
    Options = []
    FOR EACH theory IN Theories {
        Options.Add({
            ChoiceLabel: "Pursue: " + theory.name,
            Risk: theory.risk, // Assuming risk/reward defined with theory data
            Reward: theory.reward
        })
    }

    // Construct the final choice Gameplay Step
    RETURN ADD_STEP(
        Phase: 1,
        StepNumber: 9, // Approximate step number after Hook (4 steps) and Theory Intro + 3 Theory presentations (5 steps)
        PhenotypeTag: "INTRO_SEQUENCE", // This step is the *result* or end-point of this phenotype sequence
        Screen: "Choose Initial Path",
        DECISION: "Based on the evidence presented, which theory seems most promising to investigate first?",
        DATA: null, // Data was presented in the preceding theory steps of the phenotype
        OPTIONS: Options, // Formatted Risk/Reward options for choosing a theory path
        ACTION: "LOCK Phase 2; SET ChosenTheory=<choice>; TRIGGER dynamic ordering for Phase 2 based on ChosenTheory"
        // Potentially: TRIGGER AxiomReveal(CaseSetupAxiom) based on chosen theory
    );
}

PROCEDURE GenerateBranchedPhase2(VictimHypothesis, FoundationalEvidence, AllSuspects) RETURNS ARRAY<GameplayStep>
{
    // Goal: Generate Phase 2 steps dynamically based on the chosen VictimHypothesis.
    // Focuses on EVIDENCE_COLLECTION to start the investigation path.
    DEFINE Phase2Steps = [];
    DEFINE StepCounter = 2; // Start Phase 2 steps after Phase 1

    // Determine Evidence Collection details based on Hypothesis
    SceneData = GET_SCENE_DATA("Argonaut Hotel Suite"); // Conceptual fetch
    DecisionText = FRAME_DECISION_TEXT_FOR_HYPOTHESIS(VictimHypothesis, "EVIDENCE_COLLECTION");
    FramedHotspots = FRAME_HOTSPOTS_FOR_HYPOTHESIS(VictimHypothesis, SceneData.Hotspots);
    FramedOptions = FRAME_EVIDENCE_OPTIONS_FOR_HYPOTHESIS(VictimHypothesis, FramedHotspots);

    Phase2Steps += ADD_STEP(
        Phase: 2,
        StepNumber: StepCounter,
        PhenotypeTag: "EVIDENCE_COLLECTION",
        Screen: "Argonaut Hotel Suite (" + VictimHypothesis + " Angle Focus)",
        DECISION: DecisionText,
        DATA: {SceneDesc: SceneData.Description, Hotspots: FramedHotspots},
        OPTIONS: FramedOptions,
        ACTION: "NAVIGATE based on choice (e.g., EvidenceExamination, SuspectList)"
        // Example: Initial examination might trigger LocationReveal or ObjectReveal
        // ACTION: "IF choice=Desk: NAVIGATE EvidenceExamination(Desk); TRIGGER ObjectReveal(DeskPhoto, InitialLook)"
    );
    StepCounter++;

    // Optionally add a dynamically ordered SUSPECT_LIST presentation if desired for Phase 2
    // SuspectOrder = DETERMINE_SUSPECT_ORDER(VictimHypothesis, AllSuspects);
    // Phase2Steps += ADD_STEP(Phase: 2, StepNumber: StepCounter, PhenotypeTag: "SUSPECT_LIST", ...);

    RETURN Phase2Steps;
}

PROCEDURE GenerateGameplayOutline(Synopsis, Characters, Events) RETURNS ARRAY<GameplayStep>
{
    // Overall orchestrator for generating the full gameplay outline.

    // 1. Identify Key Narrative Elements
    VictimData = EXTRACT_VICTIMS(Characters);
    CulpritData = EXTRACT_CULPRIT(Characters);
    RedHerringSuspects = EXTRACT_RED_HERRINGS(Characters);
    FoundationalEvidence = IDENTIFY_FOUNDATIONAL_EVIDENCE(Synopsis, Events);
    Theories = GENERATE_INITIAL_THEORIES(Synopsis, FoundationalEvidence); // Generate 3 theories (T/F+/F-)
    AllSuspects = [CulpritData] + RedHerringSuspects;
    KnownEvidence = []; // Tracks discovered evidence
    RevealedNarrative = []; // Tracks triggered narrative elements

    GameplaySteps = [];
    CurrentStepNumber = 0;

    // --- Phase 1: Hook & Theory Choice ---
    // Represent the entire multi-passage phenotypes as single steps in the outline.

    // Step 1: CASE_HOOK
    GameplaySteps.Add(ADD_STEP(
        Phase: 1, StepNumber: ++CurrentStepNumber, PhenotypeTag: "CASE_HOOK",
        Screen: "Case Introduction Hook",
        DECISION: "Accept or Decline the Case?",
        DATA: { HookVisual: "[Generated Visual Alias]", HookText: "[Generated Hook Text]", ContextSummary: "[Generated Context Summary]" },
        OPTIONS: [ { ChoiceLabel: "Accept Case", Risk: "[Risk Text]", Reward: "[Reward Text]" }, { ChoiceLabel: "Decline Case", Risk: "[Risk Text]", Reward: "[Reward Text]" } ],
        ACTION: "IF Accept: NAVIGATE INTRO_SEQUENCE_Start ELSE: NAVIGATE HOME" // Simple navigation
    ));

    // Step 2: INTRO_SEQUENCE
    TheoryChoiceStepData = DesignInitialTheoryChoice(Theories);
    GameplaySteps.Add(ADD_STEP(
        Phase: 1, StepNumber: ++CurrentStepNumber, PhenotypeTag: "INTRO_SEQUENCE",
        Screen: "Initial Theory Choice",
        DECISION: TheoryChoiceStepData.DECISION,
        DATA: { Theory1: Theories[0].description + " Evidence: " + Theories[0].evidence.details, Theory2: Theories[1].description + " Evidence: " + Theories[1].evidence.details, Theory3: Theories[2].description + " Evidence: " + Theories[2].evidence.details },
        OPTIONS: TheoryChoiceStepData.OPTIONS,
        ACTION: "LOCK Phase 2; SET ChosenTheory=<choice>; NAVIGATE Phase2_Start" // Set state, navigate
    ));
    DEFINE ChosenTheory = EXTRACT_THEORY_FROM_CHOICE(TheoryChoiceStepData);

    // --- Phase 2: Initial Investigation & Narrative Setup ---
    // Add an early narrative beat about the victim's state of mind
    GameplaySteps.Add(ADD_STEP(
        Phase: 2, StepNumber: ++CurrentStepNumber, PhenotypeTag: "NARRATIVE_EVIDENCE_FOR_REFLECTION",
        Screen: "Victim's Mindset",
        DECISION: "Consider the victim's apparent paranoia. Was it justified?",
        DATA: { NarrativeContext: "Entering the suite, you notice enhanced security measures...", SupportingEvidenceID: "evidence_victim_paranoia_notes" },
        OPTIONS: [ { ChoiceLabel: "Focus on Fear", Risk: "Overlook rational motives", Reward: "Prioritize perceived threats" }, { ChoiceLabel: "Focus on Paranoia", Risk: "Dismiss genuine threat", Reward: "Concentrate on concrete evidence" } ],
        ACTION: "ACT:aty=REVEAL;aet=evidence_victim_paranoia_notes; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; ADD PlayerNote('Consider victim mindset')" // Reveal supporting evidence, navigate player
    ));

    // Generate Branched Phase 2 Gameplay Steps (EVIDENCE_COLLECTION, etc.)
    Phase2Steps = GenerateBranchedPhase2(ChosenTheory, FoundationalEvidence, AllSuspects);
    FOR EACH step IN Phase2Steps { step.StepNumber = ++CurrentStepNumber; }
    GameplaySteps.Append(Phase2Steps);

    // --- Phase 3: Deeper Investigation & Character Context ---
    // Example: Insert Narrative step about a key relationship after player examines a relevant suspect profile
    IF PlayerHasExamined(RelevantSuspectProfile) { // Conceptual check
        GameplaySteps.Add(ADD_STEP(
            Phase: 3, StepNumber: ++CurrentStepNumber, PhenotypeTag: "NARRATIVE_EVIDENCE_FOR_RELATIONSHIP",
            Screen: "Relationship Context",
            DECISION: "How did the victim's relationship with [Suspect Name] influence events?",
            DATA: { NarrativeContext: "Background check reveals details of their [e.g., intense rivalry/close bond]...", SupportingEvidenceID: "evidence_relationship_details" },
            OPTIONS: [ { ChoiceLabel: "View as Primary Factor", Risk: "[Risk Text]", Reward: "[Reward Text]" }, { ChoiceLabel: "View as Secondary Factor", Risk: "[Risk Text]", Reward: "[Reward Text]" } ],
            ACTION: "ACT:aty=REVEAL;aet=evidence_relationship_details; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app"
        ));
    }

    // Add standard Gameplay steps like SUSPECT_LIST, EVIDENCE_EXAMINATION
    // Example: EVIDENCE_EXAMINATION (No narrative trigger in ACTION)
    KeyEvidenceItem = GET_NEXT_EVIDENCE_TO_EXAMINE(KnownEvidence);
    IF KeyEvidenceItem {
        ExaminationData = GENERATE_EVIDENCE_EXAMINATION_DATA(KeyEvidenceItem);
        GameplaySteps.Add(ADD_STEP(
            Phase: 3, // Or determined dynamically
            StepNumber: ++CurrentStepNumber,
            PhenotypeTag: "EVIDENCE_EXAMINATION",
            Screen: "Examine " + KeyEvidenceItem.Name,
            DECISION: "What stands out about this item?",
            DATA: ExaminationData.Findings,
            OPTIONS: ExaminationData.Options, // Options might relate to focus points
            ACTION: ExaminationData.Action // e.g., "MARK Examined; NAVIGATE Hub" - Pure game logic
        ));
    }

    // --- Phase 4: Hypothesis Check & Mid-Game Twists ---
    HypothesisCheckPuzzleData = GENERATE_HYPOTHESIS_CHECK_DATA(ChosenTheory, KnownEvidence); // Generate puzzle specific to path
    GameplaySteps.Add(ADD_STEP(
        Phase: 4, // Or 3 depending on flow
        StepNumber: ++CurrentStepNumber,
        PhenotypeTag: "DEDUCTION_PUZZLE",
        Screen: "Theory Assessment Puzzle",
        DECISION: "Interpret new clue based on current hypothesis.",
        DATA: HypothesisCheckPuzzleData.Clues,
        OPTIONS: HypothesisCheckPuzzleData.Options, // Risk/Reward options for interpretations
        ACTION: HypothesisCheckPuzzleData.Action // Includes validation and navigation logic only
    ));

    // Example: Adding a DEDUCTION_PUZZLE for statement analysis (No narrative trigger in ACTION)
    SuspectToAnalyze = GET_NEXT_SUSPECT_TO_ANALYZE(ChosenTheory, KnownEvidence);
    IF SuspectToAnalyze {
        PuzzleData = GENERATE_DEDUCTION_PUZZLE_DATA(SuspectToAnalyze, DEDUCTION_MECHANIC, KnownEvidence);
        GameplaySteps.Add(ADD_STEP(
            Phase: 4,
            StepNumber: ++CurrentStepNumber,
            PhenotypeTag: "DEDUCTION_PUZZLE",
            Screen: "Analyze " + SuspectToAnalyze.Name + "'s Statement",
            DECISION: "Identify the lie.",
            DATA: PuzzleData.Content,
            OPTIONS: PuzzleData.Options, // Risk/Reward for choosing lie/truth
            ACTION: PuzzleData.Action // e.g., "VALIDATE Lie; IF Correct: UNLOCK ClueID; TRIGGER DeductionSuccess ELSE: TRIGGER DeductionFailure" - Game logic only
        ));
    }

    // --- Phase 5: Breakthrough & Climax ---
    // Example: BREAKTHROUGH_MOMENT (ACTION has game logic, not narrative triggers)
    IF SHOULD_TRIGGER_BREAKTHROUGH(KnownEvidence) {
         BreakthroughData = GENERATE_BREAKTHROUGH_DATA(KnownEvidence);
         GameplaySteps.Add(ADD_STEP(
             Phase: 5,
             StepNumber: ++CurrentStepNumber,
             PhenotypeTag: "BREAKTHROUGH_MOMENT",
             Screen: "Key Revelation", // e.g., "The Hidden Recording"
             DECISION: "How to proceed after this major revelation?",
             DATA: BreakthroughData.Clues, // The crucial piece of evidence itself
             OPTIONS: BreakthroughData.Options, // Strategic Risk/Reward Choice
             ACTION: BreakthroughData.Action // e.g., "MARK BreakthroughAchieved; NAVIGATE PostBreakthroughChoiceScreen"
         ));
    }

    // Add other late-game steps: SUSPECT_CONFRONTATION, ACCUSATION, CASE_RESOLUTION
    // Ensure their ACTION fields contain only game logic.

    // ... Add placeholders/logic for remaining phenotypes ...

    RETURN GameplaySteps;
}

// Helper procedures (Conceptual - Ensure alignment with new structure)
// Core Helpers:
PROCEDURE ADD_STEP(...) RETURNS GameplayStep { /* Logic to format and create a GameplayStep object, including ACTION field which may contain 'TRIGGER' commands */ }
PROCEDURE EXTRACT_VICTIMS(Characters) { /* ... */ }
PROCEDURE EXTRACT_CULPRIT(Characters) { /* ... */ }
PROCEDURE EXTRACT_RED_HERRINGS(Characters) { /* ... */ }
PROCEDURE IDENTIFY_FOUNDATIONAL_EVIDENCE(Synopsis, Events) { /* ... */ }

// Hypothesis Decision Helpers:
PROCEDURE GENERATE_INITIAL_THEORIES(Synopsis, Evidence) { /* Generates 3 theories {id, name, desc, evidence{...}, type, targetPassageID, risk, reward} */ }
// --- Guidance for GENERATE_INITIAL_THEORIES ---
// Purpose: Create three distinct, plausible starting theories based on initial data.
// Input: Synopsis, FoundationalEvidence, CulpritData, RedHerringSuspects
// Output: Array of 3 Theory objects {id, name, desc, evidence{alias, desc, details}, type: T|F+|F-, targetPassageID, risk, reward}
//
// 1. True Positive (T):
//    - Theory: Directly points towards the actual CulpritData and their core motive/actions derived from Synopsis/Events.
//    - Evidence: Select a genuine piece of FoundationalEvidence that strongly supports this true path.
//    - Example: If Culprit used poison, evidence might be 'trace residue found'.
//
// 2. False Positive (F+):
//    - Theory: Points towards a plausible RedHerringSuspect OR an incorrect motive/method.
//    - Evidence: Select FoundationalEvidence that *seems* to support this wrong theory but is misleading.
//      - Could be circumstantial (e.g., suspect was nearby but uninvolved).
//      - Could be misinterpreted (e.g., a threatening note taken out of context).
//      - Could have a subtle flaw noticeable later (e.g., wrong timeline).
//    - Example: If Red Herring argued with victim, evidence might be 'raised voices heard', omitting context.
//
// 3. False Negative (F-):
//    - Theory: Could point to another RedHerringSuspect OR downplay the True Positive theory.
//    - Evidence: Select FoundationalEvidence that appears to contradict the True Positive path OR make it seem less likely.
//      - Could create an apparent alibi for the Culprit (later proven false).
//      - Could point blame strongly towards a Red Herring based on a verifiable fact.
//      - Could highlight evidence seemingly unrelated to the Culprit's method.
//    - Example: If Culprit used poison, evidence might be 'no signs of forced entry', diverting focus from internal methods.
//
// - Ensure each theory uses a distinct piece of FoundationalEvidence.
// - Define appropriate Risk/Reward text for pursuing each theory path.
// - Assign unique targetPassageIDs for the start of each investigation branch.
// --- End Guidance ---
PROCEDURE EXTRACT_THEORY_FROM_CHOICE(DecisionStep) { /* ... */ }

// Branched Phase 2 Helpers:
PROCEDURE DETERMINE_SUSPECT_ORDER(Hypothesis, Suspects) { /* ... */ }
PROCEDURE FRAME_DECISION_TEXT_FOR_HYPOTHESIS(Hypothesis, Phenotype) { /* ... */ }
PROCEDURE GET_SCENE_DATA(SceneName) { /* ... */ }
PROCEDURE FRAME_HOTSPOTS_FOR_HYPOTHESIS(Hypothesis, Hotspots) { /* ... */ }
PROCEDURE FRAME_EVIDENCE_OPTIONS_FOR_HYPOTHESIS(Hypothesis, HotspotsOrEvidence) { /* ... */ }

// Deduction & Puzzle Helpers:
PROCEDURE GENERATE_HYPOTHESIS_CHECK_DATA(Hypothesis, KnownEvidence) { /* Returns {Clues, Options, Action including narrative triggers} */ }
PROCEDURE GENERATE_DEDUCTION_PUZZLE_DATA(Suspect, MechanicType, KnownEvidence) { /* Returns {Content, Options, Action including narrative triggers} */ }
PROCEDURE DETERMINE_UNLOCK(Suspect, CulpritData, KnownEvidence) { /* ... */ }

// Breakthrough & Other Helpers:
PROCEDURE SHOULD_TRIGGER_BREAKTHROUGH(KnownEvidence) { /* Logic based on gathered clues */ }
PROCEDURE GENERATE_BREAKTHROUGH_DATA(KnownEvidence) { /* Returns {Clues, Options, Action including major narrative trigger} */ }
PROCEDURE GET_NARRATIVE_TRIGGER_FOR_EVIDENCE(NarrativeLink) { /* Logic to determine appropriate TRIGGER command based on linked Story Phenotype ID */ }
// ... Any other necessary conceptual helpers ...

---/INSTRUCTIONS---

---DATA---
{% if player_journey %}
// --- Existing Player Journey (To Be Edited) ---
{{ player_journey }}
{% endif %}

Provide the following data for the case:

Synopsis: {{synopsis}}

Characters: {{characters}} (Array of character objects including role: Victim, Culprit, Suspect, Witness)

Events: {{events}} (Array of event objects, potentially linked to characters or evidence)
---/DATA---

---EXAMPLE---

```markdown
**Case:** Viral Echoes
**Goal:** Guide the player through a structured risk/reward investigation, identifying Julian Griffin as Raj Singh's killer, punctuated by narrative moments that build emotional context and character understanding.

**(Phase 1: Introduction & Initial Suspicions)**

1.  **CASE_HOOK: Case Introduction & Decision**
    *   **DECISION:** Accept or Decline the Case: "Viral Echoes"?
    *   **CLUES/DATA:**
        - HookVisual: Image of Raj Singh's viral post contrasted with stark crime scene tape at the Argonaut Hotel.
        - HookText: "Tech CEO found dead after crying wolf... or was it a warning? Police saw fireworks, the crime scene suggests otherwise. Unravel the 'Viral Echoes'."
        - ContextSummary: "Raj Singh, controversial GenMat CEO, murdered in his luxury suite. His bizarre 'shooting' claim days earlier adds layers of misdirection. Was it paranoia, publicity, or prelude?"
    *   **OPTIONS:**
        - Accept Case (Risk: Navigating tech world egos and social media noise; Reward: Solving a high-profile, complex murder)
        - Decline Case (Risk: Letting a killer exploit the chaos?; Reward: Avoiding a media circus)
    *   **ACTION:** `IF Accept: NAVIGATE IntroSequence_Start ELSE: NAVIGATE HOME`

2.  **INTRO_SEQUENCE: Initial Theory Choice**
    *   **DECISION:** The initial reports point in several directions. Which lead feels strongest right now?
    *   **CLUES/DATA:** (Represents theories shown across intro steps)
        - Theory 1 (Corporate Enemy): Raj hinted at exposing a rival. A hidden war behind the code? (Evidence: `evidence_raj_rival_hint`)
        - Theory 2 (Political Backlash): His viral post enraged Supervisor Shah-Powell. Did professional anger turn personal? (Evidence: `evidence_aria_meeting_report`)
        - Theory 3 (Personal Vendetta): Fired engineer Jack Sullivan was nearby. How deep does his grudge run? (Evidence: `evidence_jack_lawsuit_note`)
    *   **OPTIONS:**
        - Pursue: Corporate Enemy (Risk: Might be a professional dispute, not murder; Reward: Focus on direct competitors like Julian Griffin)
        - Pursue: Political Backlash (Risk: Powerful people often have alibis; Reward: Investigate Aria Shah-Powell's potential influence)
        - Pursue: Personal Vendetta (Risk: Revenge seekers can be obvious red herrings; Reward: Explore Jack Sullivan's history and movements)
    *   **ACTION:** `LOCK Phase 2; SET ChosenTheory=<choice>; NAVIGATE Phase2_Start`

3.  **NARRATIVE_REFLECTION: The Victim's Paranoia** (Triggered early in Phase 2, perhaps entering the suite)
    *   **PhenotypeTag:** `NARRATIVE_EVIDENCE_FOR_REFLECTION`
    *   **DECISION:** Consider the victim's state of mind. How much did his fear play into events?
    *   **CLUES/DATA:**
        - Narrative Context: Entering Raj's suite, you see signs of heightened security - extra locks, maybe surveillance tech diagrams. The air feels tense.
        - Supporting Evidence Revealed: `evidence_victim_paranoia_notes` (aet - e.g., journal snippets or messages expressing fear).
        - Reflection Prompt: "Raj Singh felt targeted. Was it justified fear, or delusion fueling the drama?"
    *   **OPTIONS:**
        - Focus on Fear as Valid (Risk: Overlook rational motives; Reward: Prioritize potential threats Raj perceived)
        - Focus on Paranoia as Noise (Risk: Dismiss a genuine threat; Reward: Concentrate on concrete evidence, ignore victim's potential misinterpretations)
    *   **ACTION:** `ACT:aty=REVEAL;aet=evidence_victim_paranoia_notes; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; ADD PlayerNote('Consider victim mindset')`

**(Phase 2: Evidence Gathering & Character Moments)**

4.  **EVIDENCE_COLLECTION: Search Raj's Suite**
    *   **DECISION:** Where to focus the search in Raj Singh's suite?
    *   **CLUES/DATA:**
        - SceneDesc: Opulent suite, tech gear everywhere. A faint metallic scent near the desk?
        - Hotspots: Desk Area (laptop, unusual tablet stand), Bedside Table (personal effects), Window Area (view of the Wharf, any disturbances?).
    *   **OPTIONS:**
        - Examine Desk Area (Risk: Could be standard tech clutter; Reward: Access business tools, potentially find hidden devices)
        - Check Bedside Table (Risk: Likely personal, could be irrelevant; Reward: Insight into Raj's private life/habits)
        - Investigate Window Area (Risk: Unlikely murder location; Reward: Check for external signs, forced entry evidence)
    *   **ACTION:** `NAVIGATE EvidenceExamination(<choice>)`

5.  **NARRATIVE_WITNESS_ENCOUNTER: The Nervous Concierge** (Triggered by reviewing initial witness list or hotel context)
    *   **PhenotypeTag:** `NARRATIVE_EVIDENCE_FOR_REFLECTION` (Focusing on Isabella's state)
    *   **DECISION:** Evaluate the concierge's testimony. How reliable is Isabella Cruz?
    *   **CLUES/DATA:**
        - Narrative Context: You review the initial interview notes with Isabella Cruz. She seemed genuinely frightened, fidgeting, avoiding eye contact when mentioning seeing *someone* familiar near Raj's suite. Fear of losing her job seemed paramount.
        - Supporting Evidence Revealed: `evidence_isabella_initial_statement` (aet - Captures her nervousness alongside the observation).
        - Reflection Prompt: "Isabella saw something, but fear clouds her memory. Can her account be trusted fully, or is her anxiety distorting the details?"
    *   **OPTIONS:**
        - Trust the Core Observation (Risk: Ignoring potential misidentification due to stress; Reward: Focus on the sighting itself)
        - Doubt the Details Due to Fear (Risk: Dismissing crucial eyewitness placement; Reward: Seek corroboration before relying heavily on her account)
    *   **ACTION:** `ACT:aty=REVEAL;aet=evidence_isabella_initial_statement; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; MARK IsabellaReliabilityQuestioned`

**(Phase 3: Uncovering Motives & Relationships)**

6.  **EVIDENCE_EXAMINATION: Custom Tablet Charging Stand**
    *   **DECISION:** Analyze the unusual charging stand. What secrets does it hold?
    *   **CLUES/DATA:** Heavy, custom, GenMat logo. Potential hidden tech.
    *   **OPTIONS:** Physical Inspection, Research Online, Test Voice Commands.
    *   **ACTION:** `IF TestVoiceCommands: NAVIGATE DeductionPuzzle(VoiceCommandTrial) ELSE: MARK StandLogged; NAVIGATE InvestigationHub`

7.  **NARRATIVE_FLASHBACK_FRAGMENT: Seeds of Rivalry** (Triggered by examining Julian's profile or finding GenMat/Cognito mentions)
    *   **PhenotypeTag:** `NARRATIVE_EVIDENCE_FOR_FLASHBACK` (Representing past context)
    *   **DECISION:** Consider the history between Raj and Julian. How deep did the animosity run?
    *   **CLUES/DATA:**
        - Narrative Context: A background check reveals snippets of past news articles and industry gossip detailing the bitter public clashes and accusations of stolen ideas between Raj Singh and Julian Griffin over the years. It wasn't just business; it felt personal.
        - Supporting Evidence Revealed: `evidence_rivalry_news_clippings` (aet - montage of past conflicts).
        - Reflection Prompt: "Years of public feuding. Was this the final, fatal escalation of a long-simmering war?"
    *   **OPTIONS:**
        - View as Business Conflict (Risk: Underestimate personal hatred; Reward: Focus on concrete IP theft motive)
        - View as Personal Vendetta (Risk: Overlook financial drivers; Reward: Consider emotional triggers alongside business)
    *   **ACTION:** `ACT:aty=REVEAL;aet=evidence_rivalry_news_clippings; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; ADD PlayerNote('Consider personal angle to rivalry')`

8.  **NARRATIVE_EVIDENCE_FOR_MOTIVE: Aria's Political Stakes** (Triggered after viewing Aria's profile or finding texts)
    *   **PhenotypeTag:** `NARRATIVE_EVIDENCE_FOR_MOTIVE`
    *   **DECISION:** Understand the pressure Supervisor Shah-Powell faced. How much did Raj's actions threaten her career?
    *   **CLUES/DATA:**
        - Narrative Context: You review communications showing Aria's increasing panic about the GenMat pilot program after Raj's viral post. Her political future seemed tied to its success, and Raj was becoming a liability.
        - Supporting Evidence Revealed: `evidence_aria_pilot_program_memos` (aet - Shows the program's importance to her career).
        - Reflection Prompt: "Aria needed the GenMat deal. Did Raj's 'stunt' push her to drastic measures to protect her ambition?"
    *   **OPTIONS:**
        - See as Strong Motive (Risk: Ignore her solid alibi; Reward: Keep her as a viable suspect based on pressure)
        - See as Context Only (Risk: Dismiss a potentially ruthless politician; Reward: Focus investigation where opportunity exists)
    *   **ACTION:** `ACT:aty=REVEAL;aet=evidence_aria_pilot_program_memos; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; MARK AriaPoliticalMotiveConsidered`

**(Phase 4: Cracks in the Facade & Deduction)**

9.  **DEDUCTION_PUZZLE: Jack Sullivan's Movements**
    *   **DECISION:** Reconcile Jack Sullivan's statement with the physical evidence. Was he just nearby, or casing the hotel?
    *   **CLUES/DATA:** Statement vs. incomplete bar alibi vs. security footage outside hotel.
    *   **OPTIONS:** Focus on timeline gaps, lack of informant proof, suspicious proximity.
    *   **ACTION:** `VALIDATE selection; IF Correct: UPDATE SuspectCredibility(Jack, -1); TRIGGER DeductionSuccess ELSE: TRIGGER DeductionFailure`

10. **NARRATIVE_REFLECTION: Julian's Composure** (Triggered after viewing Julian's initial statement or footage of him)
    *   **PhenotypeTag:** `NARRATIVE_EVIDENCE_FOR_REFLECTION`
    *   **DECISION:** Evaluate Julian Griffin's calm demeanor. Is it genuine confidence or a carefully crafted mask?
    *   **CLUES/DATA:**
        - Narrative Context: You recall Julian's interview or observe him in security footage from before the murder. He appears cool, collected, almost unnervingly smooth, despite the known rivalry and his company's financial troubles. A flicker of something – anxiety? – in his eyes?
        - Supporting Evidence Revealed: `evidence_julian_demeanor_observation` (aet - Detective's note on his unsettling composure).
        - Reflection Prompt: "He seems too calm for someone whose rival was just murdered after a public spat. Is it innocence, or the sign of a meticulous planner who believes he got away with it?"
    *   **OPTIONS:**
        - Interpret as Innocence/Confidence (Risk: Falling for the facade; Reward: Prioritize suspects showing more obvious stress)
        - Interpret as Suspicious Control (Risk: Bias based on intuition; Reward: Increase scrutiny on Julian's actions and alibi)
    *   **ACTION:** `ACT:aty=REVEAL;aet=evidence_julian_demeanor_observation; ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app; MARK JulianDemeanorNoted`

11. **DEDUCTION_PUZZLE: Voice Command Trial (Tablet Stand)**
    *   **DECISION:** Attempt to unlock the charging stand's hidden function.
    *   **CLUES/DATA:** GenMat AI link, debug phrases hint.
    *   **OPTIONS:** "GenMat Activate", "GenMat Secure Mode", "GenMat Archive Override Seven".
    *   **ACTION:** `VALIDATE command; IF Correct: UNLOCK HiddenAudioFile; NAVIGATE BreakthroughMoment ELSE: TRIGGER DeductionFailure(VoiceCommandFail)`

**(Phase 5: The Breakthrough & Confrontation)**

12. **BREAKTHROUGH_MOMENT: The Fatal Argument** (Triggered by unlocking audio)
    *   **DECISION:** The hidden recording changes everything. How to proceed with this definitive proof?
    *   **CLUES/DATA:**
        - Narrative Context: The chilling audio plays - Julian's smooth voice turning sharp, Raj's defiant threats about exposure, the sickening *thump* of suppressed shots, Julian's ragged breathing. The corporate rivalry wasn't just business; it was motive for murder.
        - Revealed Evidence: `evidence_hidden_audio_recording` (aet).
    *   **OPTIONS:**
        - Confront Julian Now (Risk: He might react violently/destructively; Reward: Immediate challenge with irrefutable proof)
        - Secure Warrant & Arrest Team (Risk: Gives him slight window to act; Reward: Safer, standard procedure)
    *   **ACTION:** `MARK BreakthroughAchieved; SET PrimeSuspect=JulianGriffin; NAVIGATE based on choice (e.g., SuspectConfrontation(Julian), SecureWarrantSequence)`

13. **SUSPECT_CONFRONTATION: Facing the Killer** (If confrontation chosen)
    *   **DECISION:** Present the audio evidence to Julian Griffin. How will he react when his mask shatters?
    *   **CLUES/DATA:**
        - Narrative Context: You play the recording. Julian's composure finally breaks - a flash of panic, denial, then perhaps calculation as he weighs his options. The smooth facade melts away, revealing the desperate man beneath.
        - Presented Evidence: The audio recording.
    *   **OPTIONS:**
        - Press for Confession (Risk: Lawyer intervention; Reward: Full admission)
        - Formal Arrest (Risk: Miss details; Reward: Secure the culprit)
    *   **ACTION:** `RECORD Reaction; IF Arrest: NAVIGATE AccusationScreen ELSE: CONTINUE InterrogationLoop`

14. **ACCUSATION: Final Decision**
    *   **DECISION:** Formally accuse the killer of Raj Singh.
    *   **CLUES/DATA:** Evidence Summary overwhelmingly points to Julian.
    *   **OPTIONS:** Accuse Julian Griffin, Accuse Aria Shah-Powell, Accuse Jack Sullivan.
    *   **ACTION:** `LOCK Investigation; TRIGGER CaseResolution(<choice>)`

15. **CASE_RESOLUTION: Echoes Silenced**
    *   **DECISION:** Review the case conclusion.
    *   **CLUES/DATA:**
        - Verdict: Julian Griffin guilty.
        - Narrative Explanation: The resolution emphasizes how Julian's desperation over corporate espionage, hidden behind a calm facade, led to murder. It revisits the other suspects, explaining why their apparent motives (political fallout, revenge) were ultimately red herrings despite seeming compelling. The viral "shooting" incident is confirmed as unrelated noise that Julian exploited.
        - Emotional Beat: Perhaps a final reflection from Detective Saito on the tragic intersection of ambition, deceit, and violence in the tech world.
    *   **OPTIONS:** Proceed to Next Case/Menu
    *   **ACTION:** `SHOW CaseOutcome(ViralEchoes_Success); NAVIGATE HOME`
```

---/EXAMPLE---

---SCHEMA---

**Case:** [Case Title derived from Synopsis/Events]
**Goal:** Guide the player through a structured risk/reward investigation, making key decisions to identify the culprit within a ~10-minute experience, **while strategically revealing narrative elements to enhance engagement and emotional investment.**

**Output Structure:**
The gameplay outline is a sequence of numbered steps, grouped by phase. Each step represents a specific player interaction or decision point and MUST be tagged with a **Gameplay** `PhenotypeTag` indicating the type of gameplay pattern being used. The sequence of these phenotype-tagged steps forms the complete player journey. **Narrative reveals are triggered via the `ACTION` field within these gameplay steps.**

**PhenotypeTag (Enum):**
The `PhenotypeTag` for each step MUST be one of the following values:
**Gameplay Phenotypes:**
- `CASE_HOOK`: Creates ~5 passage hook sequence (hook, context, choice, accept/decline confirm) using intro/branch cmds. **May trigger initial World/Case Axioms.**
- `INTRO_SEQUENCE`: Presents 3 theories (TruePositive, FalsePositive, FalseNegative) with evidence via intro steps, ending in a branch choice. **May trigger initial Relationship/Character reveals.**
- `INVESTIGATION_HUB`: Central navigation point for all activities.
- `EVIDENCE_COLLECTION`: Creates interactive locations to find evidence.
- `EVIDENCE_EXAMINATION`: Provides detailed analysis of individual evidence items.
- `SUSPECT_LIST`: Displays known suspects for comparison and selection.
- `SUSPECT_PROFILE`: Shows detailed suspect info, including statements.
- `DEDUCTION_PUZZLE`: Challenges player to identify lies or solve puzzles (e.g., passcode). **Success often triggers `Revelation_Proposition`s.**
- `DEDUCTION_SUCCESS`: Rewards correct deductions/puzzle solutions with progress/evidence.
- `DEDUCTION_FAILURE`: Provides feedback and retry/consequence for incorrect deductions/puzzle solutions.
- `EVIDENCE_VERIFICATION`: Presents scientific/expert analysis results. **May trigger technical `Revelation_Proposition`s.**
- `BREAKTHROUGH_MOMENT`: Creates dramatic revelation connecting evidence. **This IS a major `Revelation_Proposition`.**
- `SUSPECT_CONFRONTATION`: Creates tense scenes when presenting evidence to suspects. **Can trigger `Character_Axiom` or `Interaction_Proposition` reveals.**
- `ACCUSATION`: Final mechanism for player to select the culprit.
- `CASE_RESOLUTION`: Delivers the satisfying conclusion and explanation, **integrating narrative threads.**
**Narrative Delivery Phenotypes:**
- `NARRATIVE_EVIDENCE_SNIPPET`: Reveals evidence containing a narrative detail.
- `NARRATIVE_EVIDENCE_FOR_RELATIONSHIP`: Reveals evidence about character relationships.
- `NARRATIVE_EVIDENCE_FOR_MOTIVE`: Reveals evidence suggesting/confirming motive.
- `NARRATIVE_EVIDENCE_FOR_FLASHBACK`: Reveals evidence representing a past event.
- `NARRATIVE_EVIDENCE_FOR_REFLECTION`: Reveals evidence describing a character's likely internal state.

**(Phase [Phase Number]: [Phase Name])**

[Step Number]. **[PhenotypeTag]: [Step Title - Descriptive of the interaction]**
    *   **DECISION:** [The core question or choice being presented to the player]
    *   **CLUES/DATA:** [List of contextual clues, data, or puzzle elements relevant to the decision]
    *   **OPTIONS:** (Each option details the potential outcome)
        - [OptionLabel 1] (Risk: [Describe potential negative outcome/cost]; Reward: [Describe potential positive outcome/benefit])
        - [OptionLabel 2] (Risk: [...]; Reward: [...])
        - ... (etc.)
    *   **ACTION:** `[Compact pseudocode directive for game logic (e.g., SET flags, NAVIGATE to next step/app, UNLOCK items, UPDATE state)]`

**(Phase [Phase Number]: [Phase Name])**

[Step Number]. **[PhenotypeTag]: [Step Title]**
    *   **DECISION:** [...]
    *   **CLUES/DATA:** [...]
    *   **OPTIONS:**
        - [...] (Risk: [...]; Reward: [...])
        - [...]
    *   **ACTION:** `[...]`

*... Repeat for all steps across all phases, ensuring each step uses an appropriate `PhenotypeTag` from the allowed list ...*

---/SCHEMA---

---COMMAND---
{% if changes %}
Edit the existing player journey according to the following changes, maintaining the core narrative structure and phenotype patterns. Apply the specific modifications outlined in the "changes" variable while preserving the quality and coherence of the original journey. Keep all edits consistent with the risk/reward framework.
{% else %}
Generate the gameplay outline in Markdown format for the provided case data, following all instructions, and mimicking the style and detail level of the provided example generally. Ensure the output is only the Markdown outline itself.
{% endif %}
---/COMMAND---