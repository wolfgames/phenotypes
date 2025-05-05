
# SLPN Narrative Phenotypes Guide: Delivering Rich Narrative in Crime Investigation Cases

## Introduction

This guide explains the Narrative Delivery Phenotypes in SLPN (Story Logic Passage Notation) that form the building blocks for presenting story elements to players. These phenotypes focus on *how* narrative information is delivered, emphasizing the core principle: "Show, Don't Tell - Reveal evidence, guide player interpretation."

## Core Concepts

Narrative Phenotypes are based on these foundational principles:

- **Evidence-Based Delivery**: Narrative is revealed through discoverable evidence rather than direct exposition
- **Player Interpretation**: Players construct the story by examining and connecting evidence pieces
- **Integration with Gameplay**: Narrative elements trigger from and enhance gameplay interactions
- **Structured Revelation**: Information unfolds through carefully designed evidence discovery

## Narrative Flow Overview

The narrative in a crime investigation case is delivered through this progression:

1. **Evidence Snippets**: Initial clues containing basic narrative information
2. **Relationship Evidence**: Items revealing connections between characters
3. **Motive Evidence**: Clues suggesting or confirming character motivations
4. **Flashback Evidence**: Items representing past events critical to the case
5. **Reflection Evidence**: Observations about characters' internal states

## Phenotype Descriptions

### NARRATIVE_EVIDENCE_SNIPPET

**Purpose**: Makes the player aware of and grants access to a specific piece of evidence containing a narrative detail.

**Structure**:
- Optional context text before reveal (via BOT)
- Evidence reveal command (REVEAL action)
- Navigation command to guide player toward examination

**Example**:
```
BOT:lin="You notice something relevant in the victim's belongings...";
ACT:aty=REVEAL;aet=victim_notebook;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### NARRATIVE_EVIDENCE_FOR_RELATIONSHIP

**Purpose**: Reveals evidence that contains information about a relationship between characters.

**Structure**:
- Optional context text before reveal (via BOT)
- Evidence reveal command for relationship information
- Navigation command to guide interpretation

**Example**:
```
BOT:lin="You found messages discussing their connection.";
ACT:aty=REVEAL;aet=private_messages;
ACT:aty=MOVE;amt=AMT:typ=DEDUCTION;tgt=relationship_puzzle_01;
```

### NARRATIVE_EVIDENCE_FOR_MOTIVE

**Purpose**: Reveals evidence that suggests or confirms a character's motive.

**Structure**:
- Optional context text before reveal (via BOT)
- Evidence reveal command for motive-related item
- Navigation toward interpretation

**Example**:
```
BOT:lin="Financial records indicate a desperate situation.";
ACT:aty=REVEAL;aet=bank_statements;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### NARRATIVE_EVIDENCE_FOR_FLASHBACK

**Purpose**: Reveals evidence that represents a past event (Interaction_Proposition).

**Structure**:
- Optional context text before reveal (via BOT)
- Evidence reveal command for flashback item
- Navigation toward examination

**Example**:
```
BOT:lin="You found an old diary entry describing the confrontation.";
ACT:aty=REVEAL;aet=victim_diary_page;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### NARRATIVE_EVIDENCE_FOR_REFLECTION

**Purpose**: Reveals an "observation" evidence item describing a character's likely internal state or reaction.

**Structure**:
- Optional context text before reveal (via BOT)
- Evidence reveal command for observation
- Navigation toward interpretation/deduction

**Example**:
```
BOT:lin="You recall the suspect's reaction during questioning.";
ACT:aty=REVEAL;aet=detective_observations;
ACT:aty=MOVE;amt=AMT:typ=DEDUCTION;tgt=character_analysis_puzzle;
```

## Implementation Guidelines

### Best Practices

1. **Focus on Discovery**: Let players discover narrative through evidence rather than being told
2. **Contextual Relevance**: Ensure evidence appears at logical moments in the investigation
3. **Gradual Revelation**: Strategically pace reveals to build tension and understanding
4. **Meaningful Connections**: Design evidence items that connect to multiple narrative elements
5. **Interpretative Space**: Allow room for player interpretation between evidence pieces

### Integration with Story Phenotypes

Narrative Delivery Phenotypes should connect directly to the underlying Story Phenotypes:

- Connect `NARRATIVE_EVIDENCE_SNIPPET` to basic information about Characters and Locations
- Use `NARRATIVE_EVIDENCE_FOR_RELATIONSHIP` to reveal details from Relationship_Definition
- Link `NARRATIVE_EVIDENCE_FOR_MOTIVE` to specific Motive_Definition elements
- Tie `NARRATIVE_EVIDENCE_FOR_FLASHBACK` to key Interaction_Proposition events
- Use `NARRATIVE_EVIDENCE_FOR_REFLECTION` to hint at Character_Axiom traits

### Customization Tips

- Vary the depth of evidence - some items may reveal complete information while others only hint
- Create layered evidence where initial examination reveals basic details, but deeper analysis uncovers more
- Consider multiple evidence items that reveal different perspectives on the same event
- Use contextual text to subtly guide player interpretation without directly stating conclusions

## Technical Requirements

- Evidence IDs must correspond to pre-defined evidence items in the game
- Context text should be brief and suggestive rather than explanatory
- Target IDs must be valid subsequent points in the gameplay flow
- Passage UIDs should follow consistent naming patterns for easy reference

By following this guide, you can create rich narrative experiences where players actively discover and interpret the story through evidence rather than passive exposition.
