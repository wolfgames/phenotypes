# Story Phenotype Guidelines: Building Rich Narrative Layers

## Introduction

This guide explains the Story Phenotypes, a structured system for designing the narrative elements of our interactive crime investigation cases. Complementing the Gameplay Phenotypes (which focus on player interaction and investigation mechanics), Story Phenotypes provide the framework for crafting compelling character backstories, relationships, motivations, and the overall plot. They ensure narrative depth and consistency, enriching the player's understanding of the "why" behind the crime.

## Core Concepts

Story Phenotypes are based on Byrne's adaptation of Euclid's Elements, breaking down narrative into fundamental components:

-   **Definitions**: Establish the static elements of the story world – the characters, relationships, motives, locations, and objects that form the foundation.
-   **Propositions**: Describe the dynamic events, interactions, and discoveries that drive the plot forward and reveal information over time.
-   **Axioms**: Define the unchangeable truths of the case, the world, and the characters, providing essential context and constraints.

**Key Principles:**

-   **Narrative Depth**: Move beyond simple clue-gathering to explore the human element – lives, loves, secrets, and motivations.
-   **Integration with Gameplay**: Story Phenotypes are designed to be revealed *through* gameplay. Discoveries made via `EVIDENCE_EXAMINATION` or `DEDUCTION_PUZZLE` should trigger `Revelation_Proposition`s, unfolding the narrative.
-   **Structured Design**: Provides a systematic way to build complex narratives, ensuring all necessary components are considered.
-   **Consistency**: Ensures a coherent narrative logic across different cases.

## Narrative Design Flow

A recommended workflow for using Story Phenotypes when designing a case:

1.  **Establish Foundations (Axioms)**: Define the core `Case_Axiom`s (what fundamentally happened?) and relevant `World_Axiom`s (what are the rules of this setting?).
2.  **Define Key Players (Character Definitions & Axioms)**: Create `Character_Definition`s for the victim, culprit, key suspects, and important witnesses. Define any critical `Character_Axiom`s (unchangeable truths like addictions, hidden histories).
3.  **Map Relationships (Relationship Definitions)**: Define the key `Relationship_Definition`s connecting the characters. Outline their history, current state, and dynamics.
4.  **Set the Stage (Location & Object Definitions)**: Define important `Location_Definition`s and `Object_Definition`s, considering their narrative significance beyond just being places or clues.
5.  **Outline the Plot (Interaction Propositions)**: Map out the key events leading up to and following the crime using `Interaction_Proposition`s. Create a timeline.
6.  **Determine Motivations (Motive Definitions)**: Define the primary `Motive_Definition`s for the culprit and plausible alternative motives for key suspects, linking them to character traits, relationships, or events.
7.  **Plan the Reveal (Revelation Propositions)**: Strategically decide which key pieces of information will be revealed when. Define `Revelation_Proposition`s and link their `source_of_revelation` and `triggering_condition` to specific Gameplay Phenotypes (e.g., finding a specific clue via `EVIDENCE_EXAMINATION`, succeeding at a `DEDUCTION_PUZZLE`).
8.  **Deepen Characters (Backstory Unfold Propositions)**: Structure any significant backstory reveals using `Backstory_Unfold_Proposition`s, linking constituent events and planning the triggering mechanisms.
9.  **Refine Emotional Arcs**: Review the `emotional_impact` defined within `Interaction_Proposition`s to ensure character reactions feel consistent and contribute to the narrative.
10. **Integrate & Verify**: Ensure the narrative built with Story Phenotypes logically supports the gameplay flow defined by Gameplay Phenotypes. Check that evidence required for deductions exists and that revelations meaningfully impact the player's understanding. Ensure misleading information (`false_positive`/`false_negative` clues or statements) is intentionally placed and derivable from the defined story elements.

## Phenotype Descriptions

### Definitions

#### Character_Definition

*   **Purpose**: To create a detailed, multi-faceted profile for each significant character.
*   **Structure**: Captures unique ID, name, role, status, basic demographics, physical/behavioral/vocal details, background history, internal state (goals, fears, secrets, vices), and initial connection to the case.
*   **Example Use**: Populating this fully for the victim (Iryna), culprit (James), and key suspects (Emma, Qasim, Jordan) using details like those in `sample_styorecore.json`, including James's gambling vice (`internal_state.vices`) and Iryna's discovery of the affair (`background.key_life_events`).

#### Relationship_Definition

*   **Purpose**: To define the nature, history, and current state of connections between characters.
*   **Structure**: Includes unique ID, involved characters, type (marital, business, affair, etc.), history, current state, key dynamics (power, resentment), key events shaping it, and its relevance to the case.
*   **Example Use**: Defining the `james_iryna_marriage` relationship, noting its history (`history_summary`), current state ("Strained due to gambling and infidelity"), key dynamics ("Financial dependency," "Hidden resentment"), and relevance ("Forms the core motive for the crime"). Define the `iryna_emma_friendship` relationship, noting its evolution to `Romantic_Affair`.

#### Motive_Definition

*   **Purpose**: To articulate specific reasons why a character might have committed the crime or acted in a certain way.
*   **Structure**: Captures unique ID, the character involved, category (financial, emotional), specific description, underlying cause (linking to character traits, relationships, events), target, evidence strength, and links to supporting evidence.
*   **Example Use**: Defining `james_financial_desperation` motive for James, linking its `underlying_cause` to his `Character_Definition` vice (gambling) and `Relationship_Definition` conflict (impending divorce). Defining a speculative `emma_jealousy` motive for Emma, noting its `strength_evidence` as `Circumstantial`.

#### Location_Definition

*   **Purpose**: To define significant settings, giving them narrative weight beyond physical description.
*   **Structure**: Includes unique ID, name, type, description, narrative significance (e.g., symbol of status), access control, associated characters, key events that occurred there, and discoverable elements/clues.
*   **Example Use**: Defining the `pacific_heights_mansion`, noting its significance ("Symbol of wealth and hidden decay"), who has access, key events (arguments, murder), and discoverable elements (crime scene clues, hidden camera `Object_Definition`).

#### Object_Definition

*   **Purpose**: To define key physical items, detailing their history, significance, and the clues they hold.
*   **Structure**: Includes unique ID, name, type (digital device, weapon), description, ownership history, narrative significance (contains proof, symbolic), current location, associated characters, key events involving it, and discoverable clues (linking to gameplay relevance).
*   **Example Use**: Defining `irynas_iphone`, noting its ownership, significance ("Contained proof of motive and affair"), location (initially hidden in safe deposit box), and discoverable clues (text messages, video recording) with their relevance and unlock conditions (`Requires tech specialist analysis`).

### Propositions

#### Interaction_Proposition

*   **Purpose**: To describe specific, discrete events or actions that occur within the narrative timeline.
*   **Structure**: Captures unique ID, name, description, participants, location, objects involved, timestamp, type (argument, meeting), outcome, emotional impact on characters, narrative significance, and how the player can discover it.
*   **Example Use**: Defining the `james_iryna_final_argument` interaction, including participants, location (`Location_Definition: home_office`), timestamp, type (`Argument`), outcome ("Divorce finalized as intent"), emotional impact (James: "Desperate Anger", Iryna: "Resolute"), significance ("Final trigger for murder"), and discoverability (`Evidence_Examination [hidden_camera_object_id]`).

#### Revelation_Proposition

*   **Purpose**: To explicitly link the discovery of information (often via gameplay) to changes in narrative understanding.
*   **Structure**: Includes unique ID, the information revealed, the source (gameplay deduction, evidence analysis, witness), impact on the story, which Definitions are affected and how, and the triggering condition (gameplay state).
*   **Example Use**: Defining `discovery_james_gambling_debt`, noting the `information_revealed`, the `source_of_revelation` (e.g., `Evidence_Analysis` of `Object_Definition: financial_records`), `impact_on_elements` (confirming `Motive_Definition: james_financial_desperation`), and `triggering_condition` (`Examination of financial_records`).

#### Backstory_Unfold_Proposition

*   **Purpose**: To structure the gradual reveal of a significant piece of character or relationship history.
*   **Structure**: Includes unique ID, name, the subject (character/relationship), summary, an ordered list of constituent `Interaction_Proposition`s or `Revelation_Proposition`s, the triggering mechanism (collecting items, dialogue path), and completion reward.
*   **Example Use**: Defining `james_gambling_history` backstory, linking constituent interactions (losing game, borrowing money, arguments) and revelations (discovery of debt by Iryna), triggered by finding specific evidence items or successful interview paths, rewarding the player with a deeper understanding of James's desperation.

### Axioms

#### Case_Axiom

*   **Purpose**: To establish fundamental, indisputable facts about the crime itself.
*   **Structure**: Includes unique ID, the factual statement, type (cause of death, time), related elements (victim, location), and typical reveal timing.
*   **Example Use**: Defining `axiom_victim_drowned` stating Iryna died by drowning, related to `Character_Definition: iryna_anderson-chen`, revealed via `Autopsy_Report`.

#### World_Axiom

*   **Purpose**: To define background truths about the game setting that provide context.
*   **Structure**: Includes unique ID, the statement about the world (tech level, social norms), category, scope, and narrative implication.
*   **Example Use**: Defining `axiom_sfpd_resources` stating advanced digital forensics are available, influencing how digital evidence (`Object_Definition: irynas_iphone`) can be processed.

#### Character_Axiom

*   **Purpose**: To define core, unchangeable truths about a character critical to the plot.
*   **Structure**: Includes unique ID, the character affected, the statement (hidden history, core trait), type, initial discoverability, narrative impact, and links to propositions it explains.
*   **Example Use**: Defining `axiom_james_gambling_addiction` for James, noting its type (`Inherent_Flaw`), discoverability (`Deeply_Hidden_Secret` initially), narrative impact (drives financial motive), and linking to related interactions (arguments, borrowing money). 