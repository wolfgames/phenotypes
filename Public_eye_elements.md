
# Public Eye: Elements

## Definitions

1.  **Case**: A self-contained crime scenario presented to the player, requiring investigation and resolution.
2.  **Evidence**: Factual data points (objects, documents, statements, digital records) that exist within the case and serve as the raw material for investigation.
3.  **Clue**: An insight or conclusion derived by the player through the analysis and connection of one or more pieces of evidence.
4.  **Suspect**: An individual within a case identified as potentially having the Means, Motive, or Opportunity (MMO) to commit the crime.
5.  **ADA**: The AI chatbot interface (Associate District Attorney) that facilitates the player's journey by delivering case information and evidence in a structured, conversational manner.
6.  **Pillar**: One of four core components (Story, Facts, Flow, Puzzle) that are integrated to construct a complete and playable case.
7.  **Phenotype**: A standardized, reusable template defining a specific pattern of player interaction or narrative presentation within the game flow.
8.  **Archetype**: A classification pattern applied to Evidence or Suspects to define their behavioral role and expected interaction within the case structure.

## Fundamental Principles

1.  All cases are built upon the essential integration of the Story, Facts, Flow, and Puzzle pillars.
2.  Evidence is pre-existing; players gain access to it through progression, they do not discover new evidence.
3.  Clues are solely the product of player analysis and logical deduction based on available evidence.
4.  ADA acts strictly as an assistant and information provider; it cannot analyze evidence or make accusations.
5.  The truth of a case is revealed by establishing clear chains of evidence that define a suspect's Means, Motive, and Opportunity.
6.  Every interactive element (evidence, suspect statement, location) is designed with a specific purpose, guiding or challenging the player's investigation.

## Case Structure

**I. Foundation**

1.  Each case initiates with a captivating hook (visual + text) and a structured introduction that sets the scene and introduces key parameters.
2.  Global case parameters (e.g., number of suspects, difficulty, length) define the overall scope and influence all pillars.
3.  The Story Pillar provides the narrative context, characters, and initial events that frame the crime.
4.  The Facts Pillar defines the evidence ecosystem, including evidence types, their relationships, and their inherent reliability and purpose.

**II. Systems**

1.  Evidence is systematically categorized and assigned Archetypes based on its properties and function (e.g., Smoking Gun, Red Herring, Alibi Breaker). This system informs how evidence is presented and analyzed.
2.  Suspects are defined by their relationship to the case, their MMO factors, and their interaction behavior, categorized into Archetypes (e.g., Primary Suspect, Secretive Insider, Opportunist).
3.  The case narrative flow follows defined patterns (FlowTypes) that shape how the player progresses through the investigation (e.g., Gauntlet, Branch and Bottleneck).
4.  Gameplay elements are designed as Puzzles that require the player to connect evidence and draw conclusions (e.g., Deduction Puzzles, Accusation).

## Interaction Patterns

**I. Core Loop**

1.  Player investigation is managed through an Investigation Hub, providing a central point for status updates and navigation.
2.  Players explore locations and evidence through dedicated interfaces (Phenotypes) that provide immersive prompts ([SEE, DO, LEARN, FEEL]) and allow for detailed examination.
3.  Evidence examination reveals specific clues, prompts analysis, and tracks player interaction.

**II. Suspect Interaction**

1.  Players access suspect information via profiles that summarize background, role, and provide initial statements.
2.  Deduction Puzzles challenge players to identify contradictions or falsehoods within suspect statements based on collected evidence.
3.  Successful deductions and evidence analysis may unlock Confrontation sequences where players present evidence to suspects to elicit reactions or further information.

**III. Resolution**

1.  ADA guides the player through the process of making a final Accusation, requiring sufficient supporting evidence chains linking Means, Motive, and Opportunity to the chosen culprit.
2.  Case Resolution provides a complete explanation of the crime, detailing how the evidence supports the true outcome and clarifying previous misdirections.
3.  Player performance is evaluated based on the accuracy of the accusation and the thoroughness of the investigation that led to it.

## ADA's Role

1.  ADA is the primary interface for case information delivery, maintaining a consistent tone (professional yet conversational) and interaction style (short sentences, inclusive language).
2.  ADA acts as an evidence gatekeeper, pacing the release of information and ensuring players "earn" access to sensitive details.
3.  ADA manages the flow between interactive elements and phenotypes, guiding the player through the structured investigation process.
4.  ADA facilitates the final accusation process and delivers the case resolution and player evaluation.
