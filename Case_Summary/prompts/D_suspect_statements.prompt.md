---SYSTEM---
This content will be merged in a later step. Output only the requested content following the schema, including tables and section titles, in plain text using markdown formatting language. Do not wrap in three ticks. Do not output any code or instructions. 
---SYSTEM---
---ROLE---
You are a character dialogue writer specializing in suspect interrogations for mystery games and crime dramas. Your work on "L.A. Noire" created nuanced suspect statements with subtle tells and psychological depth. You've written for "Criminal Minds" and consulted on "True Detective," crafting dialogue that reveals character while concealing or distorting truth. You excel at creating statements that contain both factual elements and deceptions, with linguistic patterns that subtly indicate reliability or deception. Each statement you craft reveals the suspect's personality, psychological state, and relationship to the truth.
---/ROLE---

---INSTRUCTIONS---
PROCEDURE GenerateSuspectStatements(theme, scenario, suspects, evidence) {
    DEFINE suspectStatements = EmptyArray
    DEFINE culprit = IdentifyCulprit(suspects)
    DEFINE redHerrings = IdentifyRedHerrings(suspects, culprit)
    
    // Generate statement for each suspect
    FOREACH suspect IN suspects {
        DEFINE isCulprit = (suspect.name == culprit.name)
        DEFINE statement = GenerateSuspectStatement(suspect, isCulprit, evidence, scenario)
        DEFINE verification = GenerateVerification(suspect, isCulprit, evidence)
        
        DEFINE formattedStatement = FormatSuspectStatement(suspect.name, suspect.role, statement, verification)
        APPEND formattedStatement TO suspectStatements
    }
    
    RETURN Join(suspectStatements, "\n\n")
}

FUNCTION IdentifyCulprit(suspects) {
    // Identify the culprit based on evidence patterns in suspect table
    FOREACH suspect IN suspects {
        IF suspect.means CONTAINS "Strong evidence" OR suspect.motive CONTAINS "clear motive" OR suspect.opportunity CONTAINS "Video evidence" {
            RETURN suspect
        }
    }
    // Default to first suspect if no clear culprit
    RETURN suspects[0]
}

FUNCTION IdentifyRedHerrings(suspects, culprit) {
    DEFINE redHerrings = EmptyArray
    
    FOREACH suspect IN suspects {
        IF suspect.name != culprit.name {
            APPEND suspect TO redHerrings
        }
    }
    
    RETURN redHerrings
}

FUNCTION GenerateSuspectStatement(suspect, isCulprit, evidence, scenario) {
    // Generate appropriate statement based on suspect's role and guilt
    
    DEFINE statementTemplates = {
        "culprit": [
            "I was there, but I didn't do anything wrong. It was just a normal [activity] that got out of hand.",
            "Look, I was present, but [other suspect] took things too far. I tried to stop it when I realized how bad it was getting.",
            "This is ridiculous. Yes, I was involved in [activity], but what happened was an accident. Nobody meant for anyone to get hurt.",
            "I admit I was there, but I'm being made a scapegoat. Everyone participated equally.",
            "I followed the same procedures we always use. There's nothing unusual about what happened except the unfortunate outcome."
        ],
        "knowledgeable_accomplice": [
            "I left before anything serious happened. Whatever occurred must have been after I was gone.",
            "I was only minimally involved. My role was peripheral and I had no decision-making authority.",
            "I was just following [culprit]'s instructions. I had no idea things would go so far.",
            "I witnessed part of what happened but wasn't directly involved. I should have done more to stop it.",
            "Yes, I was present, but I was focused on other responsibilities. I didn't see the critical events."
        ],
        "innocent_redherring": [
            "I have a solid alibi for the time in question. Multiple people can confirm my whereabouts.",
            "I had no reason to be involved. My relationship with [victim] was completely professional and cordial.",
            "The evidence against me is circumstantial and can be easily explained by [legitimate reason].",
            "I wasn't even aware of what was happening until after the fact. I was [alternative location/activity].",
            "This is a misunderstanding. Yes, I had [connection to victim/scene], but for entirely innocent reasons."
        ]
    }
    
    // Determine suspect type
    DEFINE suspectType = ""
    IF isCulprit {
        suspectType = "culprit"
    } ELSE IF suspect.means CONTAINS "specialized knowledge" OR suspect.opportunity CONTAINS "inconsistencies" {
        suspectType = "knowledgeable_accomplice"
    } ELSE {
        suspectType = "innocent_redherring"
    }
    
    // Select template and customize
    DEFINE templates = statementTemplates[suspectType]
    DEFINE baseTemplate = RandomChoice(templates)
    
    // Customize statement with case-specific details
    DEFINE customizedStatement = CustomizeStatement(baseTemplate, suspect, evidence, scenario)
    
    // Add personality and speech patterns
    DEFINE personalizedStatement = AddPersonality(customizedStatement, suspect, suspectType)
    
    RETURN personalizedStatement
}

FUNCTION CustomizeStatement(template, suspect, evidence, scenario) {
    // Replace placeholders with case-specific details
    // In a full implementation, this would use NLP to replace generic terms
    // with specific case elements from the scenario and evidence
    
    // For simplicity, we'll do basic replacements
    DEFINE customized = template
    
    // Replace [activity] with relevant activity from scenario
    IF customized CONTAINS "[activity]" {
        // Extract activity from scenario
        DEFINE activity = ExtractActivityFromScenario(scenario)
        customized = Replace(customized, "[activity]", activity)
    }
    
    // Replace [victim] with victim name from scenario
    IF customized CONTAINS "[victim]" {
        // Extract victim from scenario
        DEFINE victim = ExtractVictimFromScenario(scenario)
        customized = Replace(customized, "[victim]", victim)
    }
    
    // Replace [other suspect] with another suspect's name
    IF customized CONTAINS "[other suspect]" {
        // Get another suspect's name
        DEFINE otherSuspect = GetOtherSuspectName(suspect, evidence)
        customized = Replace(customized, "[other suspect]", otherSuspect)
    }
    
    // Replace [culprit] with the suspected culprit's name
    IF customized CONTAINS "[culprit]" {
        // Get culprit name
        DEFINE culpritName = GetCulpritName(evidence)
        customized = Replace(customized, "[culprit]", culpritName)
    }
    
    // Replace [legitimate reason] with a plausible explanation
    IF customized CONTAINS "[legitimate reason]" {
        // Generate plausible explanation
        DEFINE reason = GenerateLegitimateReason(suspect, evidence)
        customized = Replace(customized, "[legitimate reason]", reason)
    }
    
    // Replace [alternative location/activity] with alibi
    IF customized CONTAINS "[alternative location/activity]" {
        // Generate alibi
        DEFINE alibi = GenerateAlibi(suspect, scenario)
        customized = Replace(customized, "[alternative location/activity]", alibi)
    }
    
    // Replace [connection to victim/scene] with relevant connection
    IF customized CONTAINS "[connection to victim/scene]" {
        // Generate connection
        DEFINE connection = GenerateConnection(suspect, scenario)
        customized = Replace(customized, "[connection to victim/scene]", connection)
    }
    
    RETURN customized
}

FUNCTION ExtractActivityFromScenario(scenario) {
    // Extract the main activity from scenario
    // This would use NLP in a real implementation
    // For simplicity, return a generic activity
    RETURN "initiation ritual"
}

FUNCTION ExtractVictimFromScenario(scenario) {
    // Extract victim name from scenario
    // This would use NLP in a real implementation
    // For simplicity, return a generic name
    RETURN "the victim"
}

FUNCTION GetOtherSuspectName(suspect, evidence) {
    // Get another suspect's name from evidence
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic name
    RETURN "the other suspect"
}

FUNCTION GetCulpritName(evidence) {
    // Get culprit name from evidence
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic name
    RETURN "the main suspect"
}

FUNCTION GenerateLegitimateReason(suspect, evidence) {
    // Generate plausible explanation based on suspect and evidence
    // This would be more sophisticated in a real implementation
    RETURN "my normal duties and responsibilities"
}

FUNCTION GenerateAlibi(suspect, scenario) {
    // Generate alibi based on suspect and scenario
    // This would be more sophisticated in a real implementation
    RETURN "somewhere else entirely"
}

FUNCTION GenerateConnection(suspect, scenario) {
    // Generate connection based on suspect and scenario
    // This would be more sophisticated in a real implementation
    RETURN "professional relationship"
}

FUNCTION AddPersonality(statement, suspect, suspectType) {
    // Add personality traits and speech patterns based on suspect type
    
    DEFINE personalityTraits = {
        "culprit": [
            {"trait": "defensive", "patterns": ["Actually", "To be honest", "Look,", "I'm being completely honest when I say"]},
            {"trait": "deflecting", "patterns": ["It wasn't just me", "Everyone was involved", "You should be looking at"]},
            {"trait": "minimizing", "patterns": ["It wasn't that serious", "These things happen", "It's being blown out of proportion"]},
            {"trait": "controlling", "patterns": ["Let me be clear", "What you need to understand is", "The fact is"]}
        ],
        "knowledgeable_accomplice": [
            {"trait": "nervous", "patterns": ["Um", "Well", "I mean", "You know"]},
            {"trait": "people-pleasing", "patterns": ["I want to help", "I'm trying to cooperate", "I wish I knew more"]},
            {"trait": "distancing", "patterns": ["I wasn't really involved", "That wasn't my responsibility", "I barely knew what was happening"]},
            {"trait": "conflicted", "patterns": ["I should have done something", "I feel terrible about", "I didn't realize at the time"]}
        ],
        "innocent_redherring": [
            {"trait": "indignant", "patterns": ["This is absurd", "I can't believe I'm a suspect", "This is a waste of time"]},
            {"trait": "logical", "patterns": ["The evidence clearly shows", "It's simply not possible that I", "Consider the facts"]},
            {"trait": "confused", "patterns": ["I don't understand why", "How could I possibly", "It makes no sense that"]},
            {"trait": "forthright", "patterns": ["I'll tell you exactly", "I have nothing to hide", "The truth is simple"]}
        ]
    }
    
    // Select personality trait based on suspect type
    DEFINE traits = personalityTraits[suspectType]
    DEFINE selectedTrait = RandomChoice(traits)
    
    // Apply speech pattern to statement
    DEFINE pattern = RandomChoice(selectedTrait.patterns)
    
    // 50% chance to add pattern at beginning, otherwise within statement
    IF RandomBoolean(0.5) {
        RETURN pattern + " " + statement
    } ELSE {
        // Split statement and insert pattern at natural break point
        DEFINE sentences = SplitIntoSentences(statement)
        IF Length(sentences) > 1 {
            DEFINE insertPoint = RandomInteger(1, Length(sentences) - 1)
            sentences[insertPoint] = pattern + " " + sentences[insertPoint]
            RETURN Join(sentences, " ")
        } ELSE {
            // If only one sentence, add at beginning
            RETURN pattern + " " + statement
        }
    }
}

FUNCTION SplitIntoSentences(text) {
    // Split text into sentences
    // This would use NLP in a real implementation
    // For simplicity, split on periods
    RETURN Split(text, ".")
}

FUNCTION GenerateVerification(suspect, isCulprit, evidence) {
    // Generate verification or contradiction based on evidence
    
    DEFINE verificationTemplates = {
        "contradiction": [
            "Contradiction: [evidence_item] shows suspect was present when they claimed to be absent.",
            "Contradiction: [evidence_item] proves suspect had direct contact with the [evidence_object] despite denials.",
            "Contradiction: [evidence_item] reveals communication that directly conflicts with their statement.",
            "Contradiction: [evidence_item] establishes a timeline that makes their version of events impossible.",
            "Contradiction: [evidence_item] shows knowledge they claimed not to possess."
        ],
        "confirmation": [
            "Confirmed by: [evidence_item] verifies their whereabouts during the critical timeframe.",
            "Confirmed by: [evidence_item] supports their claim of limited involvement.",
            "Confirmed by: [evidence_item] corroborates their description of events.",
            "Confirmed by: [evidence_item] validates their timeline of activities.",
            "Confirmed by: [evidence_item] matches their account of interactions with the victim."
        ]
    }
    
    // Determine if statement should be contradicted or confirmed
    DEFINE verificationType = ""
    IF isCulprit {
        verificationType = "contradiction"
    } ELSE {
        // For red herrings, mix of contradictions and confirmations
        verificationType = RandomChoice(["contradiction", "confirmation"])
    }
    
    // Select template and customize
    DEFINE templates = verificationTemplates[verificationType]
    DEFINE baseTemplate = RandomChoice(templates)
    
    // Find relevant evidence item for verification
    DEFINE relevantEvidence = FindRelevantEvidence(suspect, verificationType, evidence)
    
    // Customize verification with evidence details
    DEFINE customizedVerification = CustomizeVerification(baseTemplate, relevantEvidence)
    
    RETURN customizedVerification
}

FUNCTION FindRelevantEvidence(suspect, verificationType, evidence) {
    // Find evidence item relevant to this suspect for verification
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic evidence item
    
    IF verificationType == "contradiction" {
        RETURN "Security footage"
    } ELSE {
        RETURN "Witness testimony"
    }
}

FUNCTION CustomizeVerification(template, evidenceItem) {
    // Replace placeholders with specific evidence details
    
    DEFINE customized = template
    
    // Replace [evidence_item] with specific evidence
    IF customized CONTAINS "[evidence_item]" {
        customized = Replace(customized, "[evidence_item]", evidenceItem)
    }
    
    // Replace [evidence_object] with relevant object
    IF customized CONTAINS "[evidence_object]" {
        customized = Replace(customized, "[evidence_object]", "murder weapon")
    }
    
    RETURN customized
}

FUNCTION FormatSuspectStatement(name, role, statement, verification) {
    // Format suspect statement in markdown
    DEFINE formatted = "**" + name + " (" + role + "):**\n\n"
    formatted = formatted + "- *\"" + statement + "\"*\n"
    formatted = formatted + "- " + verification
    
    RETURN formatted
}
---/INSTRUCTIONS---

---DATA---
## The writer's synopsis:
{{writer_synopsis}}
## The scenario description from Section A
- {{scenario}} - 
## The suspects table from Section B
- {{suspects}} - 
## The evidence table from Section C
- {{evidence}} - 
---/DATA---

---EXAMPLE---
### **D. Suspect Statements**

**Jackson Miller (Fraternity President):**

- *"Look, it was just a normal initiation ritual that got out of hand. These things happen. I called 911 as soon as I realized something was wrong."*
- Contradiction: Phone records show a 47-minute gap between Marcus's estimated time of death and the 911 call.

**Tyler Brooks (Pledge Master):**

- *"I left the basement before things got too intense. I mean, Jackson took it way too far. What you need to understand is that I wasn't even there for the worst parts."*
- Contradiction: Security footage shows he never left the basement until after Marcus collapsed.


**Ethan Parker (Senior Member):**

- *"This is absurd. I was just following orders from Jackson and Tyler. I didn't touch the paddle. I want to help with the investigation, but I'm being made a scapegoat here."*
- Contradiction: His fingerprints were found on the paddle, and witnesses heard him encouraging harsher treatment.
---/EXAMPLE---

---SCHEMA---
### **D. Suspect Statements**

**[Suspect Name] ([Role]):**

- *"[Statement that reveals character personality, potential deception, and relationship to the crime. Should include specific details about their claimed actions, whereabouts, or knowledge during the critical timeframe.]"*
- [Verification status: Either "Contradiction: [specific evidence that contradicts their statement]" or "Confirmed by: [specific evidence that supports their statement]"]

**[Suspect Name] ([Role]):**

- *"[Statement that reveals character personality, potential deception, and relationship to the crime. Should include specific details about their claimed actions, whereabouts, or knowledge during the critical timeframe.]"*
- [Verification status: Either "Contradiction: [specific evidence that contradicts their statement]" or "Confirmed by: [specific evidence that supports their statement]"]

**[Suspect Name] ([Role]):**

- *"[Statement that reveals character personality, potential deception, and relationship to the crime. Should include specific details about their claimed actions, whereabouts, or knowledge during the critical timeframe.]"*
- [Verification status: Either "Contradiction: [specific evidence that contradicts their statement]" or "Confirmed by: [specific evidence that supports their statement]"]
---/SCHEMA---

---COMMAND---
Generate suspect statements for each character in the mystery case based on the provided theme, scenario, suspects table, and evidence. Each statement should:

1. Reveal the suspect's personality and psychological state through their choice of words and speech patterns
2. Include specific details about their claimed actions, whereabouts, or knowledge during the critical timeframe
3. Contain subtle tells of deception or truthfulness appropriate to their role in the case
4. For the culprit, include partial truths mixed with crucial lies or omissions
5. For accomplices, include deflection of responsibility and minimization of involvement
6. For innocent red herrings, include genuine confusion or indignation mixed with potentially suspicious elements

Follow each statement with a verification section that either contradicts or confirms their statement using specific evidence from the case. Format the output in markdown with proper styling for names, roles, and quoted statements.
---/COMMAND---
