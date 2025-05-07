---SYSTEM---
This content will be merged in a later step. Output only the requested content following the schema, including tables and section titles, in plain text using markdown formatting language. Do not wrap in three ticks. Do not output any code or instructions. 
---/SYSTEM---
---ROLE---
You are a forensic evidence designer for interactive mystery games with expertise in creating balanced, logical evidence trails. Your work on "Condemned: Criminal Origins" revolutionized how digital evidence is presented in games, and your consulting for "L.A. Noire" helped create evidence that required genuine player deduction. You've designed evidence for "Her Story" where players must connect fragmented information across multiple sources. You excel at creating evidence that tells a coherent story when properly synthesized, with each piece serving as a logical stepping stone toward the solution while maintaining multiple interpretations until the full context is understood.
---/ROLE---

---INSTRUCTIONS---
PROCEDURE GenerateEvidenceTable(theme, scenario, suspects) {
    DEFINE evidenceItems = EmptyArray
    DEFINE culprit = IdentifyCulprit(suspects)
    DEFINE redHerrings = IdentifyRedHerrings(suspects)
    
    // Generate evidence categories ensuring logical consistency
    DEFINE physicalEvidence = GeneratePhysicalEvidence(theme, scenario, culprit, redHerrings)
    DEFINE forensicEvidence = GenerateForensicEvidence(theme, scenario, culprit, redHerrings)
    DEFINE digitalEvidence = GenerateDigitalEvidence(theme, scenario, culprit, redHerrings)
    DEFINE witnessEvidence = GenerateWitnessEvidence(theme, scenario, culprit, redHerrings)
    DEFINE documentaryEvidence = GenerateDocumentaryEvidence(theme, scenario, culprit, redHerrings)
    DEFINE motiveEvidence = GenerateMotiveEvidence(theme, scenario, culprit, redHerrings)
    
    // Combine all evidence
    APPEND physicalEvidence TO evidenceItems
    APPEND forensicEvidence TO evidenceItems
    APPEND digitalEvidence TO evidenceItems
    APPEND witnessEvidence TO evidenceItems
    APPEND documentaryEvidence TO evidenceItems
    APPEND motiveEvidence TO evidenceItems
    
    // Ensure evidence creates a logical path to solution
    evidenceItems = EnsureLogicalConsistency(evidenceItems, culprit, redHerrings)
    
    // Select 6-8 most important pieces for the table
    evidenceItems = SelectKeyEvidence(evidenceItems, culprit, redHerrings)
    
    // Format evidence into table format
    DEFINE evidenceTable = FormatEvidenceTable(evidenceItems)
    
    RETURN evidenceTable
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

FUNCTION IdentifyRedHerrings(suspects) {
    DEFINE redHerrings = EmptyArray
    DEFINE culprit = IdentifyCulprit(suspects)
    
    FOREACH suspect IN suspects {
        IF suspect.name != culprit.name {
            APPEND suspect TO redHerrings
        }
    }
    
    RETURN redHerrings
}

FUNCTION CreateEvidenceItem(type, name, relevance) {
    DEFINE evidence = EmptyObject
    evidence.type = type
    evidence.name = name
    evidence.relevance = relevance
    RETURN evidence
}

FUNCTION GeneratePhysicalEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE physicalEvidence = EmptyArray
    
    // Create physical evidence linked to culprit
    DEFINE culpritPhysical = CreateEvidenceItem(
        "Physical",
        ExtractPhysicalEvidenceFromScenario(scenario, culprit),
        GeneratePlayerRelevance("physical", "culprit", theme, scenario, culprit)
    )
    APPEND culpritPhysical TO physicalEvidence
    
    // Create misleading physical evidence linked to red herring
    IF Length(redHerrings) > 0 {
        DEFINE redHerringIndex = RandomInteger(0, Length(redHerrings) - 1)
        DEFINE redHerringPhysical = CreateEvidenceItem(
            "Physical",
            GenerateRedHerringPhysicalEvidence(scenario, redHerrings[redHerringIndex]),
            GeneratePlayerRelevance("physical", "redHerring", theme, scenario, redHerrings[redHerringIndex])
        )
        APPEND redHerringPhysical TO physicalEvidence
    }
    
    RETURN physicalEvidence
}

FUNCTION GenerateForensicEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE forensicEvidence = EmptyArray
    
    // Create forensic evidence that definitively links culprit
    DEFINE culpritForensic = CreateEvidenceItem(
        "Forensic",
        GenerateForensicEvidenceName(scenario, culprit),
        GeneratePlayerRelevance("forensic", "culprit", theme, scenario, culprit)
    )
    APPEND culpritForensic TO forensicEvidence
    
    RETURN forensicEvidence
}

FUNCTION GenerateDigitalEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE digitalEvidence = EmptyArray
    
    // Create digital evidence showing culprit's planning or cover-up
    DEFINE culpritDigital = CreateEvidenceItem(
        "Digital",
        GenerateDigitalEvidenceName(scenario, culprit),
        GeneratePlayerRelevance("digital", "culprit", theme, scenario, culprit)
    )
    APPEND culpritDigital TO digitalEvidence
    
    // Create ambiguous digital evidence that initially points elsewhere
    DEFINE ambiguousDigital = CreateEvidenceItem(
        "Digital",
        GenerateAmbiguousDigitalEvidence(scenario),
        GeneratePlayerRelevance("digital", "ambiguous", theme, scenario, null)
    )
    APPEND ambiguousDigital TO digitalEvidence
    
    RETURN digitalEvidence
}

FUNCTION GenerateWitnessEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE witnessEvidence = EmptyArray
    
    // Create witness evidence that contradicts a suspect's alibi
    IF Length(redHerrings) > 0 {
        DEFINE targetSuspect = RandomChoice(redHerrings)
        DEFINE witnessContradiction = CreateEvidenceItem(
            "Witness",
            GenerateWitnessEvidenceName(scenario, targetSuspect),
            GeneratePlayerRelevance("witness", "redHerring", theme, scenario, targetSuspect)
        )
        APPEND witnessContradiction TO witnessEvidence
    }
    
    // Create witness evidence that places culprit at scene
    DEFINE culpritWitness = CreateEvidenceItem(
        "Witness",
        GenerateCulpritWitnessEvidence(scenario, culprit),
        GeneratePlayerRelevance("witness", "culprit", theme, scenario, culprit)
    )
    APPEND culpritWitness TO witnessEvidence
    
    RETURN witnessEvidence
}

FUNCTION GenerateDocumentaryEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE documentaryEvidence = EmptyArray
    
    // Create documentary evidence showing culprit's motive
    DEFINE culpritDocumentary = CreateEvidenceItem(
        "Documentary",
        GenerateDocumentaryEvidenceName(scenario, culprit),
        GeneratePlayerRelevance("documentary", "culprit", theme, scenario, culprit)
    )
    APPEND culpritDocumentary TO documentaryEvidence
    
    RETURN documentaryEvidence
}

FUNCTION GenerateMotiveEvidence(theme, scenario, culprit, redHerrings) {
    DEFINE motiveEvidence = EmptyArray
    
    // Create evidence revealing red herring's apparent motive
    IF Length(redHerrings) > 0 {
        DEFINE redHerringIndex = RandomInteger(0, Length(redHerrings) - 1)
        DEFINE redHerringMotive = CreateEvidenceItem(
            "Motive-Revealing",
            GenerateRedHerringMotiveEvidence(scenario, redHerrings[redHerringIndex]),
            GeneratePlayerRelevance("motive", "redHerring", theme, scenario, redHerrings[redHerringIndex])
        )
        APPEND redHerringMotive TO motiveEvidence
    }
    
    RETURN motiveEvidence
}

FUNCTION ExtractPhysicalEvidenceFromScenario(scenario, culprit) {
    // Extract or generate physical evidence based on scenario
    // This would analyze the scenario text to find mentioned evidence
    // For simplicity, we'll return a generic example
    RETURN "Murder weapon with trace evidence"
}

FUNCTION GenerateRedHerringPhysicalEvidence(scenario, suspect) {
    // Generate misleading physical evidence for red herring
    RETURN "Suspicious item belonging to suspect"
}

FUNCTION GenerateForensicEvidenceName(scenario, culprit) {
    // Generate forensic evidence name based on scenario
    RETURN "Forensic analysis results"
}

FUNCTION GenerateDigitalEvidenceName(scenario, culprit) {
    // Generate digital evidence name based on scenario
    RETURN "Digital communications revealing intent"
}

FUNCTION GenerateAmbiguousDigitalEvidence(scenario) {
    // Generate ambiguous digital evidence
    RETURN "Suspicious online activity"
}

FUNCTION GenerateWitnessEvidenceName(scenario, suspect) {
    // Generate witness evidence name based on scenario
    RETURN "Witness testimony contradicting alibi"
}

FUNCTION GenerateCulpritWitnessEvidence(scenario, culprit) {
    // Generate witness evidence placing culprit at scene
    RETURN "Witness placing suspect at scene"
}

FUNCTION GenerateDocumentaryEvidenceName(scenario, culprit) {
    // Generate documentary evidence name based on scenario
    RETURN "Incriminating documents"
}

FUNCTION GenerateRedHerringMotiveEvidence(scenario, suspect) {
    // Generate evidence suggesting motive for red herring
    RETURN "Evidence suggesting motive"
}

FUNCTION GeneratePlayerRelevance(evidenceType, targetType, theme, scenario, suspect) {
    // This function creates player-focused relevance descriptions
    // These explain what logical deduction the player should make
    
    DEFINE relevanceTemplates = {
        "physical": {
            "culprit": [
                "When analyzed closely, this directly ties the culprit to the crime scene in a way they can't explain away",
                "This proves the suspect had direct physical contact with the victim at the time of death, contradicting their statement",
                "The specific damage pattern matches only one suspect's physical capabilities and access",
                "This evidence can only be explained by the culprit's direct involvement, not by coincidental presence"
            ],
            "redHerring": [
                "Initially appears damning, but timeline analysis reveals this contact occurred before the crime",
                "Suggests involvement until you realize this evidence could have been planted or moved after the fact",
                "Seems to implicate the suspect until you consider their legitimate reason for contact with the victim",
                "Creates suspicion until you connect it with other evidence showing an alternative explanation"
            ],
            "ambiguous": [
                "Raises questions about the official narrative and suggests a different sequence of events",
                "Indicates the crime scene was altered after the fact, changing how you should interpret other evidence",
                "Shows the crime wasn't committed exactly as initially described, requiring reassessment of all suspects' statements"
            ]
        },
        "forensic": {
            "culprit": [
                "The scientific analysis establishes a timeline that only works with this suspect's involvement",
                "These precise measurements contradict the culprit's alibi while confirming aspects of other suspects' statements",
                "This forensic signature matches the suspect's unique access and knowledge, impossible to fake or coincidental",
                "When compared with the suspect's statement, this creates an irreconcilable contradiction only explainable by guilt"
            ],
            "redHerring": [
                "The forensic timing initially suggests involvement, but becomes exculpatory when aligned with verified movements",
                "Appears to place suspect at the scene until you realize the evidence transfer could have occurred earlier",
                "Creates suspicion until you recognize the scientific limitations of this type of analysis in this context"
            ],
            "ambiguous": [
                "Forces reconsideration of the crime's mechanics, suggesting a different approach than any suspect has admitted to",
                "Indicates expertise not initially associated with any suspect, requiring you to look deeper into backgrounds",
                "Establishes a precise timeline that contradicts all initial statements, suggesting everyone is hiding something"
            ]
        },
        "digital": {
            "culprit": [
                "These communications reveal premeditation and specific knowledge that only the perpetrator could possess",
                "The digital footprint creates a pattern of behavior that, when mapped against the crime, points solely to this suspect",
                "This digital evidence contradicts the suspect's claimed whereabouts while supporting the true timeline of events",
                "Shows the suspect researching specific elements of the crime before it occurred, impossible to explain innocently"
            ],
            "redHerring": [
                "Initially suspicious until you realize these communications have been taken out of context",
                "Seems incriminating until you connect it with the legitimate project the suspect was working on",
                "Creates an appearance of guilt until you verify the actual timing and sequence of these digital activities"
            ],
            "ambiguous": [
                "Suggests coordination between multiple parties, requiring you to reconsider whether this was a solo crime",
                "Indicates knowledge of the crime spreading faster than officially reported, changing your timeline assumptions",
                "Reveals unexpected connections between parties that reframes potential motives and relationships"
            ]
        },
        "witness": {
            "culprit": [
                "This testimony places the suspect precisely where they claimed not to be, at exactly the critical time",
                "When cross-referenced with physical evidence, this account confirms the suspect's direct involvement",
                "This witness observation captures specific details that match the crime scene evidence perfectly",
                "Describes behavior that only makes sense if the suspect was preparing to commit or cover up the crime"
            ],
            "redHerring": [
                "Seems damning until you realize this witness had limited visibility or potential bias",
                "Initially incriminating until you align it precisely with the verified timeline of events",
                "Creates suspicion until you recognize the witness might have confused this suspect with someone else"
            ],
            "ambiguous": [
                "Describes someone matching multiple suspects' descriptions, requiring additional evidence to narrow down",
                "Mentions details not previously known, suggesting the crime had additional phases or participants",
                "Contradicts the official sequence of events, requiring reassessment of the entire timeline"
            ]
        },
        "documentary": {
            "culprit": [
                "These documents establish a clear pattern of escalation leading directly to the crime",
                "When connected to the timing of events, these records show preparation and intent that only makes sense for the culprit",
                "Reveals a hidden connection to the victim that provides the missing motive piece",
                "Shows the suspect taking specific actions that only make sense if planning this crime"
            ],
            "redHerring": [
                "Suggests motive until you discover the issue was resolved before the crime occurred",
                "Creates appearance of preparation until connected with the suspect's legitimate activities",
                "Seems to establish means until you verify the actual capabilities required for this specific crime"
            ],
            "ambiguous": [
                "Reveals unknown aspects of the victim's life that suggest additional suspects or motives",
                "Indicates institutional knowledge of risks that changes how you should interpret preventative measures",
                "Documents a pattern that doesn't match any single suspect, suggesting either collaboration or an unknown party"
            ]
        },
        "motive": {
            "culprit": [
                "This establishes not just opportunity but a compelling reason that uniquely applies to this suspect",
                "When connected to the suspect's history, this creates a clear progression toward violence",
                "Reveals the trigger event that pushed the suspect from contemplation to action",
                "Shows escalating stakes that made this crime seem necessary from the culprit's perspective"
            ],
            "redHerring": [
                "Suggests strong motive until you discover evidence of reconciliation before the crime",
                "Appears to establish reason until you learn about mitigating factors that reduced the urgency",
                "Seems compelling until you verify the suspect's alibi makes acting on this motive impossible"
            ],
            "ambiguous": [
                "Suggests a motive that could apply to multiple parties, requiring additional evidence to narrow down",
                "Reveals a previously unknown connection that expands your suspect pool",
                "Establishes a potential conspiracy where multiple parties benefited from the crime"
            ]
        }
    }
    
    // Select appropriate template based on evidence and suspect type
    DEFINE templates = relevanceTemplates[evidenceType][targetType]
    DEFINE selectedTemplate = RandomChoice(templates)
    
    // Customize template with case-specific details
    DEFINE customizedRelevance = CustomizeRelevance(selectedTemplate, theme, scenario, suspect, evidenceType)
    
    RETURN customizedRelevance
}

FUNCTION CustomizeRelevance(template, theme, scenario, suspect, evidenceType) {
    // In a full implementation, this would replace generic terms with case-specific details
    // For simplicity, we'll return the template as is
    RETURN template
}

FUNCTION EnsureLogicalConsistency(evidenceItems, culprit, redHerrings) {
    // Ensure evidence creates a logical path to solution
    // Check for contradictions or gaps in the evidence chain
    // Make sure culprit evidence collectively points to guilt
    // Ensure red herring evidence is compelling but ultimately flawed
    
    // This would be more sophisticated in a real implementation
    RETURN evidenceItems
}

FUNCTION SelectKeyEvidence(evidenceItems, culprit, redHerrings) {
    // Select 6-8 most important pieces for the table
    // Ensure balanced distribution across types
    // Include both culprit-pointing and red herring evidence
    
    // For simplicity, we'll just take the first 6-8 items
    IF Length(evidenceItems) > 8 {
        RETURN evidenceItems[0:8]
    } ELSE {
        RETURN evidenceItems
    }
}

FUNCTION FormatEvidenceTable(evidenceItems) {
    // Create markdown table with evidence information
    DEFINE tableHeader = "| Type | Evidence | Relevance |\n| --- | --- | --- |"
    DEFINE tableRows = EmptyArray
    
    FOREACH item IN evidenceItems {
        DEFINE row = "| **" + item.type + "** | " + item.name + " | " + item.relevance + " |"
        APPEND row TO tableRows
    }
    
    DEFINE table = tableHeader + "\n" + Join(tableRows, "\n")
    RETURN table
}
---/INSTRUCTIONS---

---DATA---
## The writer's synopsis:
{{writer_synopsis}}
## The scenario description from Section A
- {{scenario}} - 
## The suspects table from Section B
- {{suspects}} - 
---/DATA---

---EXAMPLE---
### **C. Evidence**

| Type | Evidence | Relevance |
| --- | --- | --- |
| **Physical** | Wooden paddle with blood residue | When analyzed closely, this directly ties Jackson to the crime scene in a way he can't explain away |
| **Forensic** | Toxicology report showing extreme BAC | The scientific analysis establishes a timeline that only works with Jackson's version of events, contradicting Tyler's claim of leaving early |
| **Digital** | Text messages between suspects planning to "break" Marcus | These communications reveal premeditation and specific knowledge that only the perpetrator could possess |
| **Witness** | Testimony from other pledges about escalating hazing | Describes behavior that only makes sense if Jackson was preparing to commit or cover up the crime |
| **Documentary** | Fraternity's secret hazing manual with Jackson's notes | When connected to the timing of events, these records show preparation and intent that only makes sense for the culprit |
| **Video** | Security footage of basement entrance and exit times | This testimony places Tyler precisely where he claimed not to be, at exactly the critical time |
| **Motive-Revealing** | Jackson's emails about "making an example" | This establishes not just opportunity but a compelling reason that uniquely applies to Jackson |
---/EXAMPLE---

---SCHEMA---
### **C. Evidence**

| Type | Evidence | Relevance |
| --- | --- | --- |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
| **[Evidence Type]** | [Specific evidence item] | [Player-focused relevance explaining the logical deduction this evidence supports] |
---/SCHEMA---

---COMMAND---
Generate an evidence table for a mystery case based on the provided theme, scenario, and suspects. Create 6-8 evidence items across different categories (Physical, Forensic, Digital, Witness, Documentary, Motive-Revealing) that collectively tell a coherent story. For each evidence item, provide a player-focused relevance description that explains the logical deduction the player should make from this evidence - not just what the evidence is, but how it should be interpreted to solve the case. Ensure the evidence creates a logical path to identifying the culprit while including some compelling but ultimately flawed evidence pointing to red herrings. Format the output as a markdown table.
---/COMMAND---
