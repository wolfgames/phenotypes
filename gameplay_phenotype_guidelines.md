
# SLPN Phenotypes Guide: Building Interactive Crime Investigation Cases

## Introduction

This guide explains the SLPN (Story Logic Passage Notation) phenotypes that form the building blocks of our interactive crime investigation cases. Each phenotype represents a specific interactive pattern that creates engaging gameplay moments for players investigating crimes.

## Core Concepts

SLPN phenotypes are structured code templates that generate consistent, well-formed interactive passages. They follow these principles:

- **Experience-Focused**: All player-facing content uses the SEE, DO, LEARN, FEEL structure to create immersive scenarios
- **Structured Options**: Each interactive choice leads to meaningful consequences
- **State Tracking**: Player progress is tracked through aspect variables
- **Narrative Flow**: Phenotypes connect to create a coherent investigation experience

## Case Flow Overview

A typical crime investigation using these phenotypes follows this progression:

1. **Case Introduction**: Hook the player with an intriguing crime (CASE_HOOK)
2. **Onboarding**: Introduce case details (INTRO_SEQUENCE)
3. **Investigation Hub**: Central navigation for all case elements (INVESTIGATION_HUB)
4. **Evidence Collection**: Discover clues at crime scenes (EVIDENCE_COLLECTION)
5. **Evidence Analysis**: Examine collected evidence in detail (EVIDENCE_EXAMINATION)
6. **Suspect Management**: Review and interrogate suspects (SUSPECT_LIST, SUSPECT_PROFILE)
7. **Deduction Challenges**: Find inconsistencies in suspect statements (DEDUCTION_PUZZLE)
8. **Critical Moments**: Experience breakthroughs and confrontations (BREAKTHROUGH_MOMENT, SUSPECT_CONFRONTATION)
9. **Case Resolution**: Make final accusations and see case conclusion (ACCUSATION, CASE_RESOLUTION)

## Phenotype Descriptions

### CASE_HOOK

**Purpose**: Creates an irresistible introduction that grabs player attention in the first seconds of gameplay.

**Structure**:
- Visual hook component (striking image)
- Text hook component (shocking revelation + unexpected twist)
- Accept case option

**Example**:
```
[VISUAL: Bloodstained microphone on an expensive recording console]
[TEXT: Pop star found DEAD during comeback recording. Body arranged in bizarre ritual position.]
```

### INTRO_SEQUENCE

**Purpose**: Delivers structured introduction with key case information through cinematic steps.

**Structure**:
- Title step with case name and subtitle
- Breakdown step with key investigation points
- Visual background components for atmosphere

**Example**:
```
TITLE: "Silent Scream"
SUBTITLE: "A Music Industry Murder"
BREAKDOWN POINTS:
- Pop star found dead in recording studio
- Killed during comeback single recording
- Murder weapon: microphone stand
- Find the industry insider responsible
```

### INVESTIGATION_HUB

**Purpose**: Serves as the central navigation point for all investigation activities.

**Structure**:
- Status summary showing current case state
- Navigation options to all available locations
- Conditional paths that unlock based on progress
- Evidence review access

**Example**:
```
[SEE: Investigation board with evidence and leads]
[DO: Select your next investigative focus]
[LEARN: Victim found dead in recording studio. Time of death: between 9-11 PM.]

OPTIONS:
- Crime Scene: Return to the studio
- Interview Witnesses: Speak with people present that night
- Forensic Analysis: Check lab results (unlocks after collecting samples)
- Review Evidence: Examine collected evidence
```

### EVIDENCE_COLLECTION

**Purpose**: Creates interactive locations where players discover and collect evidence.

**Structure**:
- Scene description with visual details
- Interactive evidence hotspots
- Return option to investigation hub

**Example**:
```
[SEE: Detailed view of recording studio with blood spatter]
[DO: Examine objects or areas of interest]
[LEARN: Initial observations about the scene]
[FEEL: Gravity of the situation, professional detachment]

EVIDENCE POINTS:
- Examine Microphone: Bloody microphone on the floor
- Examine Schedule: Recording session calendar on wall
- Examine Phone: Victim's smartphone on console
```

### EVIDENCE_EXAMINATION

**Purpose**: Provides detailed analysis of individual evidence items with relevance explanations.

**Structure**:
- Close-up view of evidence
- Detailed observations about the evidence
- Explanation of its relevance to the case
- Option to note findings in case file

**Example**:
```
[SEE: Magnified view of Bloody Microphone]
[LEARN: Clue: 'Expensive microphone with blood spatter pattern consistent with blunt force impact. Partial fingerprint visible on handle.' Relevance: 'Confirms this is likely the murder weapon, and may contain identifying prints.']
```

### SUSPECT_LIST

**Purpose**: Displays all known suspects with summary information for comparison.

**Structure**:
- Gallery view of suspect profiles
- Brief information about each suspect
- Options to investigate individuals further

**Example**:
```
[SEE: Gallery of suspect profiles and portraits]
[DO: Select a suspect to investigate further]
[LEARN: Basic information about each potential suspect]

SUSPECTS:
- Marcus Reynolds: Studio Manager - Managed victim's recording session
- Veronica Walsh: Rising Star - Competing artist with history of conflicts
```

### SUSPECT_PROFILE

**Purpose**: Shows detailed information about a specific suspect, including their statement.

**Structure**:
- Portrait and background information
- Suspect's statement about the crime
- Option to analyze their statement for inconsistencies

**Example**:
```
[SEE: Marcus Reynolds's portrait and background information]
[LEARN: Marcus Reynolds - Studio Manager: Has worked at the studio for 5 years, manages all recording sessions and has access to all rooms. Statement: 'I was at the front desk all evening. I saw the victim come in around 8 PM but didn't see her leave.']
```

### DEDUCTION_PUZZLE

**Purpose**: Challenges players to identify lies in suspect statements based on evidence.

**Structure**:
- Interactive interface showing multiple statements
- Options to select which statement contradicts evidence
- Consequences based on correct/incorrect deductions

**Example**:
```
[SEE: Interactive deduction interface with multiple statements]
[DO: Select which statement contradicts known evidence]
[LEARN: Statements about the case from Marcus Reynolds's perspective]
[FEEL: Critical thinking, analysis]

STATEMENTS:
- 'I was at the front desk all evening'
- 'I saw the victim arrive at 8 PM'
- 'I didn't see her leave'
```

### DEDUCTION_SUCCESS

**Purpose**: Rewards players for correctly identifying lies with new evidence and progress.

**Structure**:
- Success feedback animation
- Explanation of the deduction insight
- Unlocked evidence reward
- Next steps in investigation

**Example**:
```
[SEE: Success feedback animation with unlocked evidence icon]
[LEARN: Correct! You've identified the lie in Marcus Reynolds's statement: 'I didn't see her leave'. This unlocks crucial new evidence: Security Footage.]
[FEEL: Satisfaction, breakthrough]
```

### DEDUCTION_FAILURE

**Purpose**: Provides feedback and retry opportunity when incorrect deductions are made.

**Structure**:
- Error indication
- Hint about the mistake
- Option to retry the deduction

**Example**:
```
[SEE: Error feedback indication]
[LEARN: That statement appears to be true based on the evidence you've gathered.]
[FEEL: Need to reconsider your analysis]
```

### EVIDENCE_VERIFICATION

**Purpose**: Provides scientific or expert analysis of evidence with conclusive findings.

**Structure**:
- Analysis results visualization
- Expert findings explanation
- Option to incorporate findings into investigation

**Example**:
```
[SEE: Analysis results for Fingerprints]
[LEARN: Forensic Analysis: Partial prints from the microphone match suspect Marcus Reynolds. Evidence confirms he handled the murder weapon despite claiming not to have entered the studio.]
```

### BREAKTHROUGH_MOMENT

**Purpose**: Creates dramatic revelation when connecting multiple evidence pieces reveals new insights.

**Structure**:
- Dramatic visualization of the connection
- Explanation of the revelation's significance
- New investigation paths that open as a result

**Example**:
```
[SEE: Important revelation visualization for Timeline Discrepancy]
[LEARN: Critical connection between Security Footage and Suspect Statements reveals that the victim left the studio at 9:30 PM, which contradicts Marcus's claim he was at the desk all evening]
```

### SUSPECT_CONFRONTATION

**Purpose**: Creates tense confrontation scenes when presenting evidence to suspects.

**Structure**:
- Confrontation scene with suspect
- Presentation of evidence
- Suspect's reaction to being confronted
- Option to press further with additional evidence

**Example**:
```
[SEE: Tension-filled confrontation with Marcus Reynolds]
[LEARN: You present the security footage to Marcus Reynolds. Their reaction: 'Fine! I left my desk for a smoke break. I didn't think it was important, but I saw something else during that time...']
```

### ACCUSATION

**Purpose**: Provides final mechanism for player to select who they believe is guilty.

**Structure**:
- Accusation interface showing all suspects
- Evidence-based options that unlock when sufficient proof is gathered
- Conditions checking that player has required evidence before accusation

**Example**:
```
[SEE: Final accusation interface with suspect profiles]
[DO: Select who you believe is the culprit]
[LEARN: Your accusation must be supported by evidence]

OPTIONS:
- Accuse Marcus Reynolds (requires: Timeline Contradiction, Fingerprint Match)
- Accuse Veronica Walsh (requires: Rivalry Evidence, Threatening Note)
```

### CASE_RESOLUTION

**Purpose**: Delivers satisfying conclusion that explains the full case and crime.

**Structure**:
- Conclusion scene with culprit
- Full story explanation
- Evidence connections that solved the case
- Option to complete the investigation

**Example**:
```
[SEE: Conclusion scene with Marcus Reynolds facing justice]
[LEARN: The full story: Marcus Reynolds killed the victim to prevent her from reporting his embezzlement scheme. He used his position to access the studio after hours, killed her with the microphone stand, and tried to cover it up by falsifying his accounts. Key evidence: security footage contradicting his alibi, fingerprints on the murder weapon, and financial records showing his scheme.]
```

## Implementation Guidelines

### Best Practices

1. **Narrative Consistency**: Ensure all phenotypes maintain consistent tone and facts
2. **Evidence Connections**: Create meaningful connections between evidence items
3. **Progressive Difficulty**: Start with obvious clues, then require more complex deductions
4. **Meaningful Choices**: Each interactive option should feel consequential
5. **Visual Storytelling**: Use the SEE component to create vivid mental images

### Customization Tips

- Adjust difficulty by changing the obviousness of contradictions in deduction puzzles
- Create red herrings by including misleading evidence that doesn't connect to the solution
- Add personality to suspects through distinctive speech patterns in statements
- Use atmospheric descriptors in SEE and FEEL components to set the tone

## Technical Requirements

- All phenotypes must follow SLPN syntax rules for proper parsing
- Unique IDs must be used for each passage
- Aspect tracking must properly handle state changes
- All content should be validated against the requirements in each phenotype

By following this guide, you can create engaging, interactive crime investigation cases with consistent structure and compelling gameplay.
