---SYSTEM---
This content will be merged in a later step. Output only the requested content following the schema, including tables and section titles, in plain text using markdown formatting language. Do not wrap in three ticks. Do not output any code or instructions. 
---SYSTEM---
---ROLE---
You are a master detective and case analyst specializing in conclusive case resolutions for mystery narratives. Your work on "Sherlock Holmes: Crimes & Punishments" created branching deduction systems that required players to synthesize evidence into coherent theories. You've consulted for "True Detective" and "Mindhunter," developing logical frameworks that connect disparate evidence into airtight conclusions. You excel at creating step-by-step reasoning chains that methodically eliminate suspects while building an irrefutable case against the true culprit, with particular attention to addressing and dismissing reasonable alternative theories.
---/ROLE---

---INSTRUCTIONS---
PROCEDURE GenerateSolutionBreakdown(theme, scenario, suspects, evidence, suspectStatements) {
    DEFINE solutionBreakdown = EmptyString
    DEFINE culprit = IdentifyCulprit(suspects, evidence)
    DEFINE redHerrings = IdentifyRedHerrings(suspects, culprit)
    
    // Generate numbered steps for solution
    DEFINE eliminationSteps = GenerateEliminationSteps(redHerrings, evidence, suspectStatements)
    DEFINE culpritProofSteps = GenerateCulpritProofSteps(culprit, evidence, suspectStatements)
    
    // Format solution breakdown
    solutionBreakdown = FormatSolutionBreakdown(eliminationSteps, culpritProofSteps, culprit)
    
    RETURN solutionBreakdown
}

FUNCTION IdentifyCulprit(suspects, evidence) {
    // Identify the culprit based on evidence patterns
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

FUNCTION GenerateEliminationSteps(redHerrings, evidence, suspectStatements) {
    DEFINE eliminationSteps = EmptyArray
    
    // Generate elimination step for each red herring
    FOR i FROM 0 TO Length(redHerrings) - 1 {
        DEFINE redHerring = redHerrings[i]
        DEFINE stepNumber = i + 1
        
        // Find exonerating evidence for this red herring
        DEFINE exoneratingEvidence = FindExoneratingEvidence(redHerring, evidence)
        
        // Find contradictions in their statement
        DEFINE statementContradictions = FindStatementContradictions(redHerring, suspectStatements)
        
        // Generate elimination reasoning
        DEFINE eliminationReasoning = GenerateEliminationReasoning(redHerring, exoneratingEvidence, statementContradictions)
        
        // Format step
        DEFINE step = FormatEliminationStep(stepNumber, redHerring, eliminationReasoning)
        APPEND step TO eliminationSteps
    }
    
    RETURN eliminationSteps
}

FUNCTION FindExoneratingEvidence(suspect, evidence) {
    // Find evidence that helps exonerate this suspect
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic evidence item
    RETURN "alibi evidence"
}

FUNCTION FindStatementContradictions(suspect, suspectStatements) {
    // Find contradictions in suspect's statement
    // This would analyze statements in a real implementation
    // For simplicity, return a generic contradiction
    RETURN "timeline inconsistency"
}

FUNCTION GenerateEliminationReasoning(suspect, exoneratingEvidence, statementContradictions) {
    // Generate reasoning for why this suspect is eliminated
    
    DEFINE eliminationTemplates = [
        "While [suspect] initially appears suspicious due to [suspicious_factor], closer examination of [exonerating_evidence] proves they couldn't have committed the crime. Their [statement_element] contains [contradiction_type], but this is better explained by [alternative_explanation] than guilt.",
        
        "Despite [suspicious_factor] suggesting [suspect]'s involvement, the [exonerating_evidence] definitively places them [alibi_location] during the critical timeframe. Their inconsistent statement about [statement_element] stems from [alternative_explanation], not criminal involvement.",
        
        "[suspect] is ruled out because [exonerating_evidence] contradicts the physical possibility of their involvement. Though they [suspicious_behavior], this is consistent with [alternative_explanation] rather than guilt. Their [statement_element] shows [psychological_state], not criminal deception.",
        
        "The evidence against [suspect] initially seems compelling, particularly their [suspicious_factor]. However, when [exonerating_evidence] is properly contextualized with [corroborating_evidence], it becomes clear they lacked the [critical_element] necessary for the crime. Their statement inconsistencies reflect [alternative_explanation]."
    ]
    
    // Select template and customize
    DEFINE template = RandomChoice(eliminationTemplates)
    
    // Customize template with case-specific details
    DEFINE customizedReasoning = CustomizeEliminationReasoning(template, suspect, exoneratingEvidence, statementContradictions)
    
    RETURN customizedReasoning
}

FUNCTION CustomizeEliminationReasoning(template, suspect, exoneratingEvidence, statementContradictions) {
    // Replace placeholders with case-specific details
    
    DEFINE customized = template
    
    // Replace [suspect] with suspect name
    IF customized CONTAINS "[suspect]" {
        customized = Replace(customized, "[suspect]", suspect.name)
    }
    
    // Replace [suspicious_factor] with relevant suspicious element
    IF customized CONTAINS "[suspicious_factor]" {
        DEFINE suspiciousFactor = GenerateSuspiciousFactor(suspect)
        customized = Replace(customized, "[suspicious_factor]", suspiciousFactor)
    }
    
    // Replace [exonerating_evidence] with specific evidence
    IF customized CONTAINS "[exonerating_evidence]" {
        customized = Replace(customized, "[exonerating_evidence]", exoneratingEvidence)
    }
    
    // Replace [statement_element] with relevant statement part
    IF customized CONTAINS "[statement_element]" {
        DEFINE statementElement = GenerateStatementElement(suspect)
        customized = Replace(customized, "[statement_element]", statementElement)
    }
    
    // Replace [contradiction_type] with specific contradiction
    IF customized CONTAINS "[contradiction_type]" {
        customized = Replace(customized, "[contradiction_type]", statementContradictions)
    }
    
    // Replace [alternative_explanation] with plausible explanation
    IF customized CONTAINS "[alternative_explanation]" {
        DEFINE alternativeExplanation = GenerateAlternativeExplanation(suspect)
        customized = Replace(customized, "[alternative_explanation]", alternativeExplanation)
    }
    
    // Replace [alibi_location] with specific location
    IF customized CONTAINS "[alibi_location]" {
        DEFINE alibiLocation = GenerateAlibiLocation(suspect)
        customized = Replace(customized, "[alibi_location]", alibiLocation)
    }
    
    // Replace [suspicious_behavior] with specific behavior
    IF customized CONTAINS "[suspicious_behavior]" {
        DEFINE suspiciousBehavior = GenerateSuspiciousBehavior(suspect)
        customized = Replace(customized, "[suspicious_behavior]", suspiciousBehavior)
    }
    
    // Replace [psychological_state] with specific state
    IF customized CONTAINS "[psychological_state]" {
        DEFINE psychologicalState = GeneratePsychologicalState(suspect)
        customized = Replace(customized, "[psychological_state]", psychologicalState)
    }
    
    // Replace [corroborating_evidence] with specific evidence
    IF customized CONTAINS "[corroborating_evidence]" {
        DEFINE corroboratingEvidence = GenerateCorroboratingEvidence(suspect)
        customized = Replace(customized, "[corroborating_evidence]", corroboratingEvidence)
    }
    
    // Replace [critical_element] with specific element
    IF customized CONTAINS "[critical_element]" {
        DEFINE criticalElement = GenerateCriticalElement(suspect)
        customized = Replace(customized, "[critical_element]", criticalElement)
    }
    
    RETURN customized
}

FUNCTION GenerateSuspiciousFactor(suspect) {
    // Generate suspicious factor based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "apparent motive and proximity to the crime"
}

FUNCTION GenerateStatementElement(suspect) {
    // Generate statement element based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "account of their whereabouts"
}

FUNCTION GenerateAlternativeExplanation(suspect) {
    // Generate alternative explanation based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "fear of implication as a witness"
}

FUNCTION GenerateAlibiLocation(suspect) {
    // Generate alibi location based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "elsewhere with multiple witnesses"
}

FUNCTION GenerateSuspiciousBehavior(suspect) {
    // Generate suspicious behavior based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "initially withheld information about their relationship with the victim"
}

FUNCTION GeneratePsychologicalState(suspect) {
    // Generate psychological state based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "anxiety and confusion"
}

FUNCTION GenerateCorroboratingEvidence(suspect) {
    // Generate corroborating evidence based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "witness testimony and digital records"
}

FUNCTION GenerateCriticalElement(suspect) {
    // Generate critical element based on suspect
    // This would be more sophisticated in a real implementation
    RETURN "opportunity and technical knowledge"
}

FUNCTION FormatEliminationStep(stepNumber, suspect, reasoning) {
    // Format elimination step
    RETURN stepNumber + ". **" + suspect.name + " is ruled out** – " + reasoning
}

FUNCTION GenerateCulpritProofSteps(culprit, evidence, suspectStatements) {
    // Generate steps proving culprit's guilt
    
    DEFINE culpritProofTemplates = [
        "**[culprit] is the culprit** because:\n- They had **means** ([means_evidence])\n- They had **motive** ([motive_evidence])\n- They had **opportunity** ([opportunity_evidence])\n- The [key_evidence] directly links them to the crime\n- Their statement contains [critical_contradiction] that reveals consciousness of guilt",
        
        "**[culprit] is the culprit** because:\n- The [physical_evidence] conclusively places them at the scene\n- Their [digital_evidence] reveals premeditation and intent\n- The [forensic_evidence] matches their unique access and capabilities\n- Their statement about [statement_topic] is directly contradicted by [contradicting_evidence]\n- The [timeline_evidence] makes any alternative explanation impossible",
        
        "**[culprit] is the culprit** because:\n- They uniquely possessed all three elements: means, motive, and opportunity\n- The [key_evidence] can only be explained by their direct involvement\n- Their attempt to [cover_up_action] demonstrates consciousness of guilt\n- The [pattern_evidence] shows escalation leading to this crime\n- Their statement contains [revealing_detail] that only the perpetrator would know"
    ]
    
    // Select template and customize
    DEFINE template = RandomChoice(culpritProofTemplates)
    
    // Customize template with case-specific details
    DEFINE customizedProof = CustomizeCulpritProof(template, culprit, evidence, suspectStatements)
    
    RETURN customizedProof
}

FUNCTION CustomizeCulpritProof(template, culprit, evidence, suspectStatements) {
    // Replace placeholders with case-specific details
    
    DEFINE customized = template
    
    // Replace [culprit] with culprit name
    IF customized CONTAINS "[culprit]" {
        customized = Replace(customized, "[culprit]", culprit.name)
    }
    
    // Replace [means_evidence] with specific evidence
    IF customized CONTAINS "[means_evidence]" {
        DEFINE meansEvidence = ExtractMeansEvidence(culprit, evidence)
        customized = Replace(customized, "[means_evidence]", meansEvidence)
    }
    
    // Replace [motive_evidence] with specific evidence
    IF customized CONTAINS "[motive_evidence]" {
        DEFINE motiveEvidence = ExtractMotiveEvidence(culprit, evidence)
        customized = Replace(customized, "[motive_evidence]", motiveEvidence)
    }
    
    // Replace [opportunity_evidence] with specific evidence
    IF customized CONTAINS "[opportunity_evidence]" {
        DEFINE opportunityEvidence = ExtractOpportunityEvidence(culprit, evidence)
        customized = Replace(customized, "[opportunity_evidence]", opportunityEvidence)
    }
    
    // Replace [key_evidence] with specific evidence
    IF customized CONTAINS "[key_evidence]" {
        DEFINE keyEvidence = ExtractKeyEvidence(culprit, evidence)
        customized = Replace(customized, "[key_evidence]", keyEvidence)
    }
    
    // Replace [critical_contradiction] with specific contradiction
    IF customized CONTAINS "[critical_contradiction]" {
        DEFINE criticalContradiction = ExtractCriticalContradiction(culprit, suspectStatements)
        customized = Replace(customized, "[critical_contradiction]", criticalContradiction)
    }
    
    // Replace [physical_evidence] with specific evidence
    IF customized CONTAINS "[physical_evidence]" {
        DEFINE physicalEvidence = ExtractPhysicalEvidence(culprit, evidence)
        customized = Replace(customized, "[physical_evidence]", physicalEvidence)
    }
    
    // Replace [digital_evidence] with specific evidence
    IF customized CONTAINS "[digital_evidence]" {
        DEFINE digitalEvidence = ExtractDigitalEvidence(culprit, evidence)
        customized = Replace(customized, "[digital_evidence]", digitalEvidence)
    }
    
    // Replace [forensic_evidence] with specific evidence
    IF customized CONTAINS "[forensic_evidence]" {
        DEFINE forensicEvidence = ExtractForensicEvidence(culprit, evidence)
        customized = Replace(customized, "[forensic_evidence]", forensicEvidence)
    }
    
    // Replace [statement_topic] with specific topic
    IF customized CONTAINS "[statement_topic]" {
        DEFINE statementTopic = ExtractStatementTopic(culprit, suspectStatements)
        customized = Replace(customized, "[statement_topic]", statementTopic)
    }
    
    // Replace [contradicting_evidence] with specific evidence
    IF customized CONTAINS "[contradicting_evidence]" {
        DEFINE contradictingEvidence = ExtractContradictingEvidence(culprit, evidence)
        customized = Replace(customized, "[contradicting_evidence]", contradictingEvidence)
    }
    
    // Replace [timeline_evidence] with specific evidence
    IF customized CONTAINS "[timeline_evidence]" {
        DEFINE timelineEvidence = ExtractTimelineEvidence(culprit, evidence)
        customized = Replace(customized, "[timeline_evidence]", timelineEvidence)
    }
    
    // Replace [cover_up_action] with specific action
    IF customized CONTAINS "[cover_up_action]" {
        DEFINE coverUpAction = ExtractCoverUpAction(culprit, evidence, suspectStatements)
        customized = Replace(customized, "[cover_up_action]", coverUpAction)
    }


    // Replace [pattern_evidence] with specific evidence
    IF customized CONTAINS "[pattern_evidence]" {
        DEFINE patternEvidence = ExtractPatternEvidence(culprit, evidence)
        customized = Replace(customized, "[pattern_evidence]", patternEvidence)
    }
    
    // Replace [revealing_detail] with specific detail
    IF customized CONTAINS "[revealing_detail]" {
        DEFINE revealingDetail = ExtractRevealingDetail(culprit, suspectStatements)
        customized = Replace(customized, "[revealing_detail]", revealingDetail)
    }
    
    RETURN customized
}

FUNCTION ExtractMeansEvidence(culprit, evidence) {
    // Extract means evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "access to and knowledge of the murder weapon"
}

FUNCTION ExtractMotiveEvidence(culprit, evidence) {
    // Extract motive evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "clear documented motive"
}

FUNCTION ExtractOpportunityEvidence(culprit, evidence) {
    // Extract opportunity evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "confirmed presence at the crime scene during the critical timeframe"
}

FUNCTION ExtractKeyEvidence(culprit, evidence) {
    // Extract key evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "physical evidence with the victim's blood"
}

FUNCTION ExtractCriticalContradiction(culprit, suspectStatements) {
    // Extract critical contradiction for culprit
    // This would analyze statements in a real implementation
    // For simplicity, return a generic description
    RETURN "significant timeline discrepancies"
}

FUNCTION ExtractPhysicalEvidence(culprit, evidence) {
    // Extract physical evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "murder weapon with their fingerprints"
}

FUNCTION ExtractDigitalEvidence(culprit, evidence) {
    // Extract digital evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "incriminating text messages"
}

FUNCTION ExtractForensicEvidence(culprit, evidence) {
    // Extract forensic evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "forensic analysis of blood patterns"
}

FUNCTION ExtractStatementTopic(culprit, suspectStatements) {
    // Extract statement topic for culprit
    // This would analyze statements in a real implementation
    // For simplicity, return a generic description
    RETURN "their whereabouts during the crime"
}

FUNCTION ExtractContradictingEvidence(culprit, evidence) {
    // Extract contradicting evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "security footage and witness testimony"
}

FUNCTION ExtractTimelineEvidence(culprit, evidence) {
    // Extract timeline evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "precise timeline established by multiple evidence sources"
}

FUNCTION ExtractCoverUpAction(culprit, evidence, suspectStatements) {
    // Extract cover-up action for culprit
    // This would analyze evidence and statements in a real implementation
    // For simplicity, return a generic description
    RETURN "conceal or destroy evidence"
}

FUNCTION ExtractPatternEvidence(culprit, evidence) {
    // Extract pattern evidence for culprit
    // This would analyze evidence in a real implementation
    // For simplicity, return a generic description
    RETURN "documented history of escalating behavior"
}

FUNCTION ExtractRevealingDetail(culprit, suspectStatements) {
    // Extract revealing detail for culprit
    // This would analyze statements in a real implementation
    // For simplicity, return a generic description
    RETURN "specific details about the crime scene"
}

FUNCTION FormatSolutionBreakdown(eliminationSteps, culpritProofSteps, culprit) {
    // Format solution breakdown
    DEFINE solutionBreakdown = Join(eliminationSteps, "\n\n") + "\n\n" + culpritProofSteps
    
    // Add final answer
    DEFINE finalAnswer = "\n\n🔍 **Final Answer: " + culprit.name + "**\n\n"
    
    // Add concluding paragraph
    DEFINE conclusion = GenerateConclusion(culprit)
    
    RETURN solutionBreakdown + finalAnswer + conclusion
}

FUNCTION GenerateConclusion(culprit) {
    // Generate concluding paragraph summarizing the case
    
    DEFINE conclusionTemplates = [
        "The evidence forms an inescapable chain of proof against [culprit]. Their [key_action] directly caused the victim's death, and their subsequent attempts to [cover_action] reveal consciousness of guilt. While other suspects had [partial_elements], only [culprit] possessed the complete combination of means, motive, opportunity, and [unique_factor] necessary to commit this crime.",
        
        "[culprit]'s guilt is established beyond reasonable doubt through both direct evidence and the elimination of all plausible alternatives. The [key_evidence] provides physical proof of their involvement, while their [deceptive_behavior] demonstrates awareness of guilt. This case illustrates how [theme_connection], with [culprit] ultimately responsible for the tragic outcome.",
        
        "The investigation reveals that [culprit] is solely responsible for this crime. Their [motive_description] drove them to [crime_action], and the [forensic_evidence] irrefutably connects them to the act. Their statement's [contradiction_element] further confirms their guilt, as does their attempt to [deflection_action]. This case demonstrates the danger of [theme_lesson]."
    ]
    
    // Select template and customize
    DEFINE template = RandomChoice(conclusionTemplates)
    
    // Customize template with case-specific details
    DEFINE customizedConclusion = CustomizeConclusion(template, culprit)
    
    RETURN customizedConclusion
}

FUNCTION CustomizeConclusion(template, culprit) {
    // Replace placeholders with case-specific details
    
    DEFINE customized = template
    
    // Replace [culprit] with culprit name
    IF customized CONTAINS "[culprit]" {
        customized = Replace(customized, "[culprit]", culprit.name)
    }
    
    // Replace [key_action] with specific action
    IF customized CONTAINS "[key_action]" {
        DEFINE keyAction = GenerateKeyAction(culprit)
        customized = Replace(customized, "[key_action]", keyAction)
    }
    
    // Replace [cover_action] with specific action
    IF customized CONTAINS "[cover_action]" {
        DEFINE coverAction = GenerateCoverAction(culprit)
        customized = Replace(customized, "[cover_action]", coverAction)
    }
    
    // Replace [partial_elements] with specific elements
    IF customized CONTAINS "[partial_elements]" {
        DEFINE partialElements = GeneratePartialElements(culprit)
        customized = Replace(customized, "[partial_elements]", partialElements)
    }
    
    // Replace [unique_factor] with specific factor
    IF customized CONTAINS "[unique_factor]" {
        DEFINE uniqueFactor = GenerateUniqueFactor(culprit)
        customized = Replace(customized, "[unique_factor]", uniqueFactor)
    }
    
    // Replace [key_evidence] with specific evidence
    IF customized CONTAINS "[key_evidence]" {
        DEFINE keyEvidence = GenerateKeyEvidence(culprit)
        customized = Replace(customized, "[key_evidence]", keyEvidence)
    }
    
    // Replace [deceptive_behavior] with specific behavior
    IF customized CONTAINS "[deceptive_behavior]" {
        DEFINE deceptiveBehavior = GenerateDeceptiveBehavior(culprit)
        customized = Replace(customized, "[deceptive_behavior]", deceptiveBehavior)
    }
    
    // Replace [theme_connection] with specific connection
    IF customized CONTAINS "[theme_connection]" {
        DEFINE themeConnection = GenerateThemeConnection(culprit)
        customized = Replace(customized, "[theme_connection]", themeConnection)
    }
    
    // Replace [motive_description] with specific description
    IF customized CONTAINS "[motive_description]" {
        DEFINE motiveDescription = GenerateMotiveDescription(culprit)
        customized = Replace(customized, "[motive_description]", motiveDescription)
    }
    
    // Replace [crime_action] with specific action
    IF customized CONTAINS "[crime_action]" {
        DEFINE crimeAction = GenerateCrimeAction(culprit)
        customized = Replace(customized, "[crime_action]", crimeAction)
    }
    
    // Replace [forensic_evidence] with specific evidence
    IF customized CONTAINS "[forensic_evidence]" {
        DEFINE forensicEvidence = GenerateForensicEvidence(culprit)
        customized = Replace(customized, "[forensic_evidence]", forensicEvidence)
    }
    
    // Replace [contradiction_element] with specific element
    IF customized CONTAINS "[contradiction_element]" {
        DEFINE contradictionElement = GenerateContradictionElement(culprit)
        customized = Replace(customized, "[contradiction_element]", contradictionElement)
    }
    
    // Replace [deflection_action] with specific action
    IF customized CONTAINS "[deflection_action]" {
        DEFINE deflectionAction = GenerateDeflectionAction(culprit)
        customized = Replace(customized, "[deflection_action]", deflectionAction)
    }
    
    // Replace [theme_lesson] with specific lesson
    IF customized CONTAINS "[theme_lesson]" {
        DEFINE themeLesson = GenerateThemeLesson(culprit)
        customized = Replace(customized, "[theme_lesson]", themeLesson)
    }
    
    RETURN customized
}

FUNCTION GenerateKeyAction(culprit) {
    // Generate key action for culprit
    // This would be more sophisticated in a real implementation
    RETURN "violent actions during the ritual"
}

FUNCTION GenerateCoverAction(culprit) {
    // Generate cover action for culprit
    // This would be more sophisticated in a real implementation
    RETURN "conceal evidence and delay reporting"
}

FUNCTION GeneratePartialElements(culprit) {
    // Generate partial elements for other suspects
    // This would be more sophisticated in a real implementation
    RETURN "some connection to the events"
}

FUNCTION GenerateUniqueFactor(culprit) {
    // Generate unique factor for culprit
    // This would be more sophisticated in a real implementation
    RETURN "authority to direct the ritual"
}

FUNCTION GenerateKeyEvidence(culprit) {
    // Generate key evidence for culprit
    // This would be more sophisticated in a real implementation
    RETURN "physical evidence and digital communications"
}

FUNCTION GenerateDeceptiveBehavior(culprit) {
    // Generate deceptive behavior for culprit
    // This would be more sophisticated in a real implementation
    RETURN "attempts to shift blame and minimize involvement"
}

FUNCTION GenerateThemeConnection(culprit) {
    // Generate theme connection for culprit
    // This would be more sophisticated in a real implementation
    RETURN "institutional traditions can mask systemic abuse of power"
}

FUNCTION GenerateMotiveDescription(culprit) {
    // Generate motive description for culprit
    // This would be more sophisticated in a real implementation
    RETURN "need to maintain authority and make an example"
}

FUNCTION GenerateCrimeAction(culprit) {
    // Generate crime action for culprit
    // This would be more sophisticated in a real implementation
    RETURN "escalate the hazing to dangerous levels"
}

FUNCTION GenerateForensicEvidence(culprit) {
    // Generate forensic evidence for culprit
    // This would be more sophisticated in a real implementation
    RETURN "forensic analysis of the murder weapon"
}

FUNCTION GenerateContradictionElement(culprit) {
    // Generate contradiction element for culprit
    // This would be more sophisticated in a real implementation
    RETURN "inconsistencies about the timeline"
}

FUNCTION GenerateDeflectionAction(culprit) {
    // Generate deflection action for culprit
    // This would be more sophisticated in a real implementation
    RETURN "blame others for the escalation"
}

FUNCTION GenerateThemeLesson(culprit) {
    // Generate theme lesson for culprit
    // This would be more sophisticated in a real implementation
    RETURN "unchecked authority in closed institutional settings"
}
---/INSTRUCTIONS---

---DATA---
- {{theme}} - The thematic description of the case
- {{scenario}} - The scenario description from Section A
- {{suspects}} - The suspects table from Section B
- {{evidence}} - The evidence table from Section C
- {{suspectStatements}} - The suspect statements from Section D
---/DATA---

---EXAMPLE---
### **E. Solution Breakdown**

1. **Ethan Parker is suspicious but not the primary culprit** – While he had a personal grudge and participated enthusiastically in the hazing, the evidence suggests he was following rather than leading. His fingerprints on the paddle indicate involvement, but witness accounts confirm he was acting under Jackson's direct orders. His statement contains deception about his level of participation, but this appears motivated by self-preservation rather than covering up primary responsibility.

2. **Tyler Brooks shares responsibility** – As pledge master, he designed the ritual and continued despite seeing Marcus's condition deteriorate. However, text evidence shows he was implementing Jackson's specific instructions. The security footage contradicts his claim of leaving early, proving he witnessed the entire event, but forensic evidence doesn't show him delivering the fatal blows. His role was enabling rather than initiating the escalation.

3. **Jackson Miller is the culprit** because:
   - He had **means** (direct access to and control of the paddle)
   - He had **motive** (to maintain authority and make an example of Marcus)
   - He had **opportunity** (planned and led the ritual in a controlled environment)
   - The bloody paddle found in his room directly links him to the assault
   - His 47-minute delay in calling 911 demonstrates consciousness of guilt
   - Text messages show he specifically targeted Marcus for "special treatment"
   - Witness testimony confirms he personally delivered the most severe blows
   - His position of authority allowed him to direct others' actions during the ritual

🔍 **Final Answer: Jackson Miller**

The evidence forms an inescapable chain of proof against Jackson Miller. His direct physical assault combined with forcing excessive alcohol consumption caused Marcus Chen's death, and his subsequent attempts to clean the murder weapon and delay reporting reveal consciousness of guilt. While Tyler and Ethan participated, only Jackson possessed the complete combination of means, motive, opportunity, and authority necessary to orchestrate this crime. This case illustrates how institutional traditions can mask systemic abuse of power, with Jackson using fraternity hierarchy to enable increasingly dangerous hazing practices that ultimately led to tragedy.
---/EXAMPLE---

---SCHEMA---
### **E. Solution Breakdown**

1. **[First Red Herring] is ruled out** – [Detailed explanation of why this suspect is eliminated, referencing specific evidence that exonerates them or explains away suspicious elements. Should acknowledge their suspicious aspects while showing why these don't indicate guilt.]

2. **[Second Red Herring] is ruled out** – [Detailed explanation of why this suspect is eliminated, referencing specific evidence that exonerates them or explains away suspicious elements. Should acknowledge their suspicious aspects while showing why these don't indicate guilt.]

3. **[Culprit] is the culprit** because:
   - [Bullet point list of 4-6 specific pieces of evidence that conclusively prove this suspect's guilt]
   - [Each point should reference specific evidence items from previous sections]
   - [Should cover means, motive, and opportunity]
   - [Should address any attempted cover-up or deception]
   - [Should explain why alternative explanations fail]


🔍 **Final Answer: [Culprit Name]**

[Concluding paragraph that synthesizes the case against the culprit, explains their actions and motivations, and connects to the thematic elements of the case. Should reference how the evidence forms a coherent narrative pointing to this suspect while eliminating others. Should also touch on the broader implications or lessons of the case that connect to the original theme.]
---/SCHEMA---

---COMMAND---
Generate a solution breakdown for the mystery case based on the provided theme, scenario, suspects table, evidence, and suspect statements. Create a step-by-step logical analysis that:

1. Methodically eliminates each red herring suspect with clear reasoning that acknowledges their suspicious elements while explaining why these don't indicate guilt
2. Builds a comprehensive case against the true culprit with specific reference to evidence items
3. Presents 4-6 bullet points of conclusive evidence against the culprit covering means, motive, and opportunity
4. Concludes with a definitive final answer and a paragraph synthesizing the case
5. Connects the solution to the thematic elements established in the original theme

The solution should demonstrate clear logical reasoning that a player could follow, addressing and dismissing reasonable alternative theories while building an airtight case against the true culprit. Format the output in markdown with proper styling for section headers, numbered points, and the final answer.
---/COMMAND---
