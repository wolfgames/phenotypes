# Analysis of Existing Gameplay Phenotypes

The codebase defines various gameplay phenotypes using a Single-Line Passage Notation (SLPN), designed for machine parsing and conciseness. These phenotypes represent interactive patterns focused on the player's experience (SEE, DO, LEARN, FEEL) and track progress through aspect variables. The `player_gameplay_graph.txt` illustrates the typical flow and relationships between these phenotypes in a case.

Key Gameplay Phenotypes identified include:

1.  **CASE_HOOK:** Introduces the case with a striking visual and text to grab attention. Connects to `INTRO_SEQUENCE`.
2.  **INTRO_SEQUENCE:** Delivers initial case information and theories. Can lead to various starting points like `IntroEvidenceReveal`.
3.  **INVESTIGATION_HUB:** Acts as a central navigation point to different investigation activities (Crime Scene, Interviews, Evidence Review).
4.  **EVIDENCE_COLLECTION:** Represents locations where players find evidence hotspots. Connects back to the `INVESTIGATION_HUB`.
5.  **EVIDENCE_EXAMINATION:** Allows detailed analysis of collected evidence, often revealing clues.
6.  **SUSPECT_LIST:** Displays available suspects. Leads to `SUSPECT_PROFILE`.
7.  **SUSPECT_PROFILE:** Provides detailed suspect information and statements, allowing for analysis. Can lead to `DEDUCTION_PUZZLE`.
8.  **DEDUCTION_PUZZLE:** Challenges players to find inconsistencies in statements using evidence. Success leads to `DEDUCTION_SUCCESS`, failure to `DEDUCTION_FAILURE`.
9.  **DEDUCTION_SUCCESS/FAILURE:** Provide feedback on deduction outcomes, potentially unlocking new information (`DEDUCTION_SUCCESS`).
10. **EVIDENCE_VERIFICATION:** Represents expert analysis of evidence (e.g., forensics).
11. **BREAKTHROUGH_MOMENT:** Occurs when key evidence connections reveal significant insights, opening new paths.
12. **SUSPECT_CONFRONTATION:** Likely a phenotype for confronting suspects with evidence, implied by the flow but details less explicit in the guidelines excerpt.
13. **ACCUSATION:** The final phase where the player accuses a suspect. Leads to various `Suspect Result` phenotypes based on correctness.
14. **Suspect Result (e.g., Suspect1Result, CulpritResult):** Provides the outcome of the accusation (correct or incorrect). Incorrect outcomes may allow retrying the accusation.

Relationships are managed through explicit connections in the graph and likely implicit state changes (aspect variables) that gate access to different phenotypes or paths (`GATEIntroEvidenceCheck`, `GATEDossierCheck`, `GATEInterviewCheck`). The `guidelines-long.md` provides principles on how these phenotypes should be used to create an engaging, clear, and rewarding player experience, emphasizing strong hooks, gated information, active investigation, clear deductions, and unambiguous resolutions.

# Plan for Complementary Story Phenotypes (Byrne's Approach)

To enrich the game with character lives, loves, and motivations, we will develop a set of complementary Story Phenotypes, following the structure of Byrne's Euclid:

## 1. Definitions:

Story Definitions will define the fundamental narrative elements and their properties. These will provide the raw material for building character backstories, relationships, and internal states.

*   **Character_Definition:** Defines a character's core traits, background history (family, education, career), personality quirks, hidden secrets, and initial emotional state regarding the case/victim.
*   **Relationship_Definition:** Defines the nature and history of a relationship between two or more characters (e.g., spouse, business partner, rival, secret lover), including key events or dynamics within that relationship.
*   **Motive_Definition:** Defines a character's potential reasons for committing the crime or obstructing justice, linking back to their background, relationships, or secrets. Includes the type of motive (e.g., financial, emotional, revenge).
*   **Location_Definition:** Defines the narrative significance and history of a location beyond its function as a crime scene or interview spot, including who has access and why.
*   **Object_Definition:** Defines the backstory or narrative significance of a key object beyond its function as physical evidence, including its ownership history or symbolic meaning.

## 2. Propositions:

Story Propositions will describe narrative sequences, character interactions, or state changes that occur, often triggered by player actions or the reveal of new information via Gameplay Phenotypes. These show the relationships *between* narrative elements or how they change.

*   **Interaction_Proposition:** Describes a specific past interaction between characters relevant to the case (e.g., an argument, a secret meeting, an act of kindness). Can be revealed through interviews or evidence.
*   **Revelation_Proposition:** Describes the narrative impact of a specific piece of evidence or a successful deduction on a character's known story (e.g., this evidence proves a character lied about their alibi, this deduction reveals a hidden relationship).
*   **Emotional_Shift_Proposition:** Describes how a character's emotional state changes based on player actions or new revelations (e.g., a character becomes nervous when confronted, a character shows grief when a secret is revealed).
*   **Backstory_Unfold_Proposition:** A sequence of narrative reveals that piece together a significant part of a character's past or a key event leading up to the crime, triggered by collecting related `Character_Definition` fragments or `Interaction_Proposition`s.

## 3. Axioms:

Story Axioms are the foundational, immutable truths of the narrative world and the specific case. They are facts that exist regardless of player action and provide essential context and constraints.

*   **Case_Axiom:** A fundamental, undeniable fact about the crime or the victim that sets the stage (e.g., "The victim was last seen alive at 9 PM," "The murder weapon belonged to the victim's spouse"). Revealed early, often in the `INTRO_SEQUENCE`.
*   **World_Axiom:** A fundamental rule or fact about the game's setting or the society the characters inhabit that impacts the story (e.g., "In this city, police corruption is rampant," "Advanced surveillance technology is commonplace"). Provides context for character actions or motivations.
*   **Character_Axiom:** An unchangeable, core truth about a character's nature or past that is crucial to the plot, even if initially hidden (e.g., "Despite appearances, Character X was deeply in debt," "Character Y had a history of violence years ago").

# Work Plan

We will proceed with the following steps to develop the Story Phenotypes:

1.  **Phase 1: Synthesize Gameplay Phenotypes (Completed):** Document the existing gameplay phenotypes, their purpose, structure, and relationships based on the codebase analysis.
2.  **Phase 2: Brainstorm Core Story Elements:** Based on common crime narrative tropes and the need to complement gameplay, brainstorm a comprehensive list of story elements (character types, relationship types, motive types, key event types) relevant to our game.
3.  **Phase 3: Define Story Phenotype Definitions:** Formalize the brainstormed elements into `Character_Definition`, `Relationship_Definition`, `Motive_Definition`, etc. Define the key parameters and properties for each type, ensuring they align with information potentially revealed through gameplay.
4.  **Phase 4: Define Story Phenotype Propositions:** Design the `Interaction_Proposition`, `Revelation_Proposition`, `Emotional_Shift_Proposition`, and `Backstory_Unfold_Proposition` structures. Define their parameters, focusing on how they link to `Definition` elements and how they would be triggered by or reveal information relevant to Gameplay Phenotypes (e.g., link a `Revelation_Proposition` to a `DEDUCTION_SUCCESS`).
5.  **Phase 5: Define Story Phenotype Axioms:** Identify core, unchangeable narrative truths that would serve as `Case_Axiom`, `World_Axiom`, and `Character_Axiom`. Define how these would be incorporated or revealed within the game flow (e.g., via `INTRO_SEQUENCE` or initial `EVIDENCE_EXAMINATION`).
6.  **Phase 6: Develop Story Phenotype Guidelines:** Write detailed guidelines for using the Story Phenotypes when creating case narratives, explaining how to combine Definitions, Propositions, and Axioms to build compelling character arcs, subplots, and overall case narratives that seamlessly integrate with the Gameplay Phenotypes.
7.  **Phase 7: Draft Story Phenotype Notation (Optional but Recommended):** Consider developing a notation (possibly extending SLPN or a new format) for representing Story Phenotypes to facilitate their integration with the game's technical systems.
8.  **Phase 8: Pilot Case Development:** Apply the developed Story Phenotypes and guidelines to create the narrative for a pilot case, testing their effectiveness and refining the definitions and structures based on the experience. 

# Story Phenotype Definitions

## 1. Character_Definition

Defines a character participating in the story, including their inherent traits, background, and psychological makeup.

*   **`character_id`**: (String) Unique identifier for the character (e.g., "james_chen").
*   **`full_name`**: (String) Full name of the character (e.g., "James Chen").
*   **`role`**: (Enum) Role in the story (e.g., `Victim`, `Culprit`, `Suspect`, `Witness`, `Detective`, `Peripheral`).
*   **`status`**: (Enum) Current status (e.g., `Alive`, `Deceased`, `In_Custody`, `At_Large`, `Unknown`).
*   **`basic_info`**: (Object)
    *   `age`: (Integer) Character's age.
    *   `ethnicity`: (String, Optional) Character's ethnicity.
    *   `occupation`: (String) Character's job or primary activity.
    *   `sex`: (String, Optional) Character's sex (e.g., "male", "female", "other").
*   **`physical_profile`**: (Object)
    *   `description`: (String) General physical appearance.
    *   `distinguishing_features`: (List<String>) Notable physical traits (e.g., scars, tattoos, limp).
*   **`behavioral_profile`**: (Object)
    *   `personality_summary`: (String) Overview of their personality.
    *   `behavioral_tells`: (List<String>) Actions indicating stress, deception, etc. (e.g., "Tugs tie when lying").
    *   `mannerisms`: (List<String>) Habitual gestures or actions (e.g., "Adjusts cufflinks").
*   **`voice_signature`**: (Object, Optional)
    *   `base_tone`: (String) Underlying quality of their voice.
    *   `speech_pattern`: (String) Rhythm, speed, vocabulary patterns.
    *   `vocal_quirks`: (List<String>) Unique vocal habits (e.g., stammer, accent).
    *   `stress_indicators`: (List<String>) How their voice changes under pressure.
*   **`background`**: (Object)
    *   `history_summary`: (String) Brief narrative of their life story relevant to the case.
    *   `key_life_events`: (List<String>) IDs of relevant `Interaction_Proposition` or event descriptions.
    *   `education`: (String, Optional) Educational background.
    *   `family`: (String, Optional) Key family relationships (can also link to `Relationship_Definition` IDs).
*   **`internal_state`**: (Object)
    *   `goals_ambitions`: (List<String>) What drives them.
    *   `fears_insecurities`: (List<String>) What they want to hide or avoid.
    *   `secrets`: (List<String>) Hidden facts about them.
    *   `vices`: (List<String>, Optional) Addictions, flaws (e.g., gambling, drinking).
    *   `moral_compass`: (String, Optional) Description of their ethics.
*   **`initial_case_relevance`**: (String) Brief description of how they are initially connected to the case.

## 2. Relationship_Definition

Defines the connection between two or more characters.

*   **`relationship_id`**: (String) Unique identifier for the relationship (e.g., "james_iryna_marriage").
*   **`involved_characters`**: (List<String>) `character_id`s of the characters involved.
*   **`relationship_type`**: (Enum) Nature of the relationship (e.g., `Marital`, `Familial_ParentChild`, `Familial_Sibling`, `Romantic_Affair`, `Friendship`, `Business_Partnership`, `Professional_Rivalry`, `Professional_Associate`, `Confidante`, `Antagonistic`).
*   **`history_summary`**: (String) Narrative overview of the relationship's development and key phases.
*   **`current_state`**: (String) Description of the relationship's status at the time the case begins (e.g., "Strained," "Supportive," "Secretive," "Terminated").
*   **`key_dynamics`**: (List<String>) Core elements defining the interaction (e.g., "Power imbalance," "Mutual respect," "Hidden resentment," "Financial dependency").
*   **`key_events`**: (List<String>) IDs of relevant `Interaction_Proposition`s that shaped the relationship.
*   **`case_relevance`**: (String) How this relationship impacts the motives, opportunities, or events of the case.

## 3. Motive_Definition

Defines a potential reason for a character's actions related to the crime.

*   **`motive_id`**: (String) Unique identifier for the motive (e.g., "james_financial_desperation").
*   **`character_id`**: (String) The `character_id` possessing this motive.
*   **`motive_category`**: (Enum) Type of motive (e.g., `Financial`, `Emotional_Revenge`, `Emotional_Jealousy`, `Emotional_Passion`, `Emotional_Protection`, `Professional_Advancement`, `Cover_up`, `Ideological`, `Accident_Related`, `Self_Defense_Related`).
*   **`description`**: (String) Specific description of the motive (e.g., "Avoid public humiliation and loss of company due to gambling debts").
*   **`underlying_cause`**: (String) Link to the root cause (e.g., Can reference `Character_Definition` secrets/vices, `Relationship_Definition` conflicts, or specific `Interaction_Proposition` IDs).
*   **`target`**: (String, Optional) The target of the motive, if applicable (e.g., a specific character_id, an organization).
*   **`strength_evidence`**: (Enum) How strongly supported this motive is by potential evidence (e.g., `Speculative`, `Circumstantial`, `Supported`, `Confirmed`).
*   **`linked_evidence_ids`**: (List<String>, Optional) IDs of specific pieces of evidence (from Gameplay Phenotypes or Object Definitions) that support this motive.

## 4. Location_Definition

Defines a significant place within the narrative.

*   **`location_id`**: (String) Unique identifier for the location (e.g., "pacific_heights_mansion").
*   **`name`**: (String) Common name of the location (e.g., "Pacific Heights Mansion", "Chen Tech Office").
*   **`location_type`**: (Enum) Type of place (e.g., `Residence`, `Office`, `Public_Space`, `Vehicle`, `Outdoor_Area`).
*   **`description`**: (String) Physical and atmospheric description of the location.
*   **`narrative_significance`**: (String) Why this location is important to the story beyond its basic function (e.g., "Symbol of wealth and hidden decay," "Site of secret meetings").
*   **`access_control`**: (String) Who can typically access this location and how (e.g., "Private residence, key access," "Public park," "Secure office floor").
*   **`associated_characters`**: (List<String>) `character_id`s strongly linked to this location.
*   **`key_events_here`**: (List<String>) IDs of `Interaction_Proposition`s or other key events that occurred here.
*   **`discoverable_elements`**: (List<Object>, Optional) Things players can find/interact with here (could link to `Object_Definition` IDs or specific clues).
    *   `element_id`: (String) ID for the discoverable element.
    *   `description`: (String) What the element is.
    *   `linked_clue_id`: (String, Optional) ID of a specific gameplay clue.

## 5. Object_Definition

Defines a significant physical object within the narrative.

*   **`object_id`**: (String) Unique identifier for the object (e.g., "irynas_iphone", "hidden_camera_office").
*   **`name`**: (String) Common name of the object (e.g., "Iryna's iPhone", "Bloody Microphone").
*   **`object_type`**: (Enum) Type of object (e.g., `Digital_Device`, `Weapon`, `Document`, `Personal_Item`, `Vehicle`, `Forensic_Material`).
*   **`description`**: (String) Physical description of the object.
*   **`ownership_history`**: (String) Who owned/possessed the object and when.
*   **`narrative_significance`**: (String) Why this object is important to the story (e.g., "Contained incriminating evidence," "Used in the crime," "Symbolic of the relationship").
*   **`current_location_id`**: (String, Optional) `location_id` where the object is currently found (if static) or last known location.
*   **`associated_characters`**: (List<String>) `character_id`s strongly linked to this object.
*   **`key_events_involved`**: (List<String>) IDs of `Interaction_Proposition`s or other key events involving this object.
*   **`discoverable_clues`**: (List<Object>, Optional) Specific pieces of information (gameplay clues) that can be derived from examining this object.
    *   `clue_id`: (String) ID for the clue.
    *   `description`: (String) The clue itself.
    *   `relevance`: (String) How the clue impacts the case.
    *   `unlock_condition`: (String, Optional) Any conditions required to find this clue (e.g., "Requires Forensic Analysis").

# Story Phenotype Propositions

## 1. Interaction_Proposition

Describes a specific event, action, or interaction involving one or more characters at a particular time and place. This covers the granular events seen in the `sample_styorecore.json`.

*   **`interaction_id`**: (String) Unique identifier for the interaction (e.g., "james_iryna_final_argument").
*   **`name`**: (String) Short descriptive name for the event (e.g., "James and Iryna Argue About Divorce").
*   **`description`**: (String) Narrative description of what happened during the interaction.
*   **`involved_characters`**: (List<String>) `character_id`s of participants.
*   **`location_id`**: (String, Optional) `location_id` where the interaction occurred.
*   **`involved_object_ids`**: (List<String>, Optional) `object_id`s relevant to the interaction (e.g., a weapon used, a document signed).
*   **`timestamp`**: (String/DateTime) When the interaction occurred (can be specific or approximate).
*   **`interaction_type`**: (Enum) Category of interaction (e.g., `Argument`, `Conversation`, `Physical_Altercation`, `Meeting`, `Transaction`, `Observation`, `Action_Taken`).
*   **`outcome_summary`**: (String) Brief description of the immediate result or consequence of the interaction.
*   **`emotional_impact`**: (List<Object>, Optional) Describes the emotional effect on involved characters. This integrates the core idea of `Emotional_Shift_Proposition`.
    *   `character_id`: (String) Character affected.
    *   `emotion_before`: (String, Optional) Emotional state before the interaction.
    *   `emotion_after`: (String) Emotional state after the interaction (e.g., "Angry," "Fearful," "Relieved," "Suspicious").
    *   `intensity`: (Enum, Optional) `Low`, `Medium`, `High`.
*   **`narrative_significance`**: (String) Why this interaction is important to the overall story or character arcs.
*   **`discoverable_through`**: (List<String>) How the player might learn about this interaction (e.g., `Witness_Testimony`, `Evidence_Examination [object_id]`, `Suspect_Interview`, `Flashback_Sequence`). Links to Gameplay Phenotypes or reveal mechanics.

## 2. Revelation_Proposition

Describes the narrative impact when a specific piece of information (often derived from gameplay) becomes known, changing the understanding of the story, characters, or relationships.

*   **`revelation_id`**: (String) Unique identifier for the revelation (e.g., "discovery_hidden_camera").
*   **`information_revealed`**: (String) The core piece of information that was discovered (e.g., "James Chen was heavily in debt," "Iryna and Emma were having an affair," "The alibi provided by Qasim is false").
*   **`source_of_revelation`**: (Object) How this information came to light.
    *   `source_type`: (Enum) `Gameplay_Deduction`, `Evidence_Analysis`, `Witness_Statement`, `Suspect_Confession`, `Character_Observation`.
    *   `source_id`: (String, Optional) ID linking to the specific gameplay element (e.g., `DEDUCTION_PUZZLE` ID, `object_id` of evidence, `character_id` of witness/suspect).
*   **`impact_on_story`**: (String) How this revelation changes the narrative direction or understanding of past events.
*   **`impact_on_elements`**: (List<Object>) Specifies which Definitions are affected by this revelation.
    *   `element_type`: (Enum) `Character_Definition`, `Relationship_Definition`, `Motive_Definition`, `Location_Definition`, `Object_Definition`.
    *   `element_id`: (String) ID of the specific definition affected.
    *   `change_description`: (String) How the understanding of this element changes (e.g., "Character X's alibi is now known to be false," "Relationship Y is revealed to be antagonistic," "Motive Z is confirmed").
*   **`triggering_condition`**: (String, Optional) The specific gameplay state or player action that triggers this revelation (e.g., "Successful completion of deduction_puzzle_1", "Examination of object_iphone").

## 3. Backstory_Unfold_Proposition

Represents a larger narrative sequence composed of multiple related interactions or revelations that collectively build a significant piece of backstory for a character or relationship.

*   **`backstory_id`**: (String) Unique identifier for this backstory element (e.g., "james_gambling_history").
*   **`name`**: (String) Descriptive name for the backstory element (e.g., "James Chen's Descent into Gambling Debt").
*   **`subject_element`**: (Object) The primary definition this backstory relates to.
    *   `element_type`: (Enum) `Character_Definition`, `Relationship_Definition`.
    *   `element_id`: (String) ID of the character or relationship.
*   **`summary`**: (String) Overview of the backstory being revealed.
*   **`constituent_propositions`**: (List<Object>) Ordered list of propositions that make up this backstory arc.
    *   `proposition_type`: (Enum) `Interaction_Proposition`, `Revelation_Proposition`.
    *   `proposition_id`: (String) ID of the specific proposition.
    *   `order`: (Integer) Sequence number within the unfold.
*   **`triggering_mechanism`**: (String) How this backstory sequence is initiated or progressed (e.g., "Collecting related journal entries," "Successful questioning path with Character Y," "Finding key objects Z and W").
*   **`completion_reward`**: (String, Optional) Narrative or gameplay reward for uncovering the full backstory (e.g., "Unlocks deeper understanding of motive," "Reveals hidden vulnerability," "Opens new dialogue options").

# Story Phenotype Axioms

## 1. Case_Axiom

Defines a fundamental, undeniable fact about the specific crime or the circumstances surrounding it, often established early in the investigation.

*   **`axiom_id`**: (String) Unique identifier for the axiom (e.g., "axiom_victim_drowned").
*   **`description`**: (String) The axiomatic statement (e.g., "Iryna Anderson-Chen died by drowning," "The time of death was between 9:00 PM and 10:00 PM on July 14th," "No forced entry was detected at the primary crime scene location").
*   **`axiom_type`**: (Enum) Category (e.g., `Cause_Of_Death`, `Time_Of_Death`, `Location_Fact`, `Victim_State`, `Initial_Scene_Condition`).
*   **`related_elements`**: (List<Object>, Optional) Links to specific definitions this axiom relates to.
    *   `element_type`: (Enum) `Character_Definition`, `Location_Definition`, `Object_Definition`.
    *   `element_id`: (String) ID of the related element (e.g., the victim's `character_id`).
*   **`reveal_timing`**: (Enum) When this axiom is typically established (e.g., `Initial_Briefing`, `Early_Investigation`, `Autopsy_Report`).

## 2. World_Axiom

Defines a fundamental rule, characteristic, or truth about the game's setting (city, society, technology level) that impacts the narrative context.

*   **`axiom_id`**: (String) Unique identifier for the axiom (e.g., "axiom_sfpd_resources").
*   **`description`**: (String) The axiomatic statement about the world (e.g., "Advanced digital forensics are readily available to SFPD," "Pacific Heights society values appearances above all else," "Organized crime has a significant presence in the city's waterfront district").
*   **`axiom_category`**: (Enum) Domain of the axiom (e.g., `Social_Norm`, `Technological_Level`, `Legal_System`, `Political_Climate`, `Economic_Condition`, `Environmental_Factor`).
*   **`scope`**: (Enum) Applicability (e.g., `City_Wide`, `Specific_District`, `Specific_Industry`, `Universal`).
*   **`narrative_implication`**: (String) How this axiom typically influences character behavior, available resources, or story possibilities.

## 3. Character_Axiom

Defines an unchangeable, core truth about a specific character's nature, history, or a fundamental condition affecting them, which is crucial to understanding their actions or the plot, even if initially hidden.

*   **`axiom_id`**: (String) Unique identifier for the axiom (e.g., "axiom_james_gambling_addiction").
*   **`character_id`**: (String) The `character_id` this axiom applies to.
*   **`description`**: (String) The axiomatic statement about the character (e.g., "James Chen has a severe, long-standing gambling addiction," "Emma Sullivan secretly inherited a large sum of money," "Detective Winslow has an eidetic memory").
*   **`axiom_type`**: (Enum) Category of the axiom (e.g., `Personality_Trait`, `Hidden_History`, `Medical_Condition`, `Secret_Skill`, `Core_Belief`, `Inherent_Flaw`).
*   **`discoverability`**: (Enum) How hidden this truth is initially (e.g., `Public_Knowledge`, `Known_To_Associates`, `Deeply_Hidden_Secret`, `Self_Deception`).
*   **`narrative_impact`**: (String) How this core truth fundamentally influences the character's motivations, decisions, or role in the story.
*   **`related_propositions`**: (List<String>, Optional) IDs of `Interaction_Proposition`s or `Revelation_Proposition`s that might reveal or be explained by this axiom. 