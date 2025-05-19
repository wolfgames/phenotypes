{# PHENOTYPE: DIAGNOSTIC_TEST_SEQUENCE #}

PROCEDURE GenerateDiagnosticTestSequence(stepIDPrefix, rootID, testCaseID, sequenceConfig) {
    // Primary goal: Create a complete sequence of connected test passages for full test case verification
    // Structure: Generates all required passages for a complete test following the provided configuration
    // Input: sequenceConfig defines the test sequence - array of passage configs in order
    
    // Validate sequence config
    PROCEDURE ValidateSequenceConfig(sequenceConfig) {
        VALIDATE sequenceConfig.length >= 2 // Must have at least entry and exit
        VALIDATE sequenceConfig[0].type == "ENTRY_POINT" // First must be entry
        VALIDATE sequenceConfig[sequenceConfig.length - 1].type == "EXIT_POINT" // Last must be exit
    }
    
    ValidateSequenceConfig(sequenceConfig)
    
    DEFINE allPassages = ""
    DEFINE passageCounter = 0
    
    // Create unique IDs for each passage
    DEFINE passageIDs = []
    FOR EACH config IN sequenceConfig INDEX i {
        IF i == 0 {
            // Entry point uses the rootID
            passageIDs.push(rootID)
        } ELSE {
            passageIDs.push(stepIDPrefix + "_" + config.type + "_" + i)
        }
    }
    
    // Generate each passage in the sequence
    FOR EACH config IN sequenceConfig INDEX i {
        DEFINE currentID = passageIDs[i]
        DEFINE nextID = i < sequenceConfig.length - 1 ? passageIDs[i + 1] : null
        DEFINE slpnPassage = ""
        
        // For the purposes of the passageCount increment, used in multiple SWITCH branches
        IF true {
            passageCounter++
        }
        
        SWITCH config.type {
            CASE "ENTRY_POINT":
                slpnPassage = GenerateDiagnosticEntryPoint(
                    stepIDPrefix, 
                    currentID, 
                    testCaseID, 
                    config.description, 
                    config.initialState, 
                    nextID
                )
                BREAK
                
            CASE "LINEAR_TEST":
                slpnPassage = GenerateDiagnosticLinearTest(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.stepNumber,
                    config.totalSteps,
                    config.stateChanges,
                    nextID
                )
                BREAK
                
            CASE "BRANCH_TEST_BINARY":
                slpnPassage = GenerateDiagnosticBranchTestBinary(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.conditionVar,
                    config.conditionValue,
                    config.pathAPassageID || nextID, // Use next sequential ID if not specified
                    config.pathBPassageID || nextID
                )
                BREAK
                
            CASE "BRANCH_TEST_MULTI":
                slpnPassage = GenerateDiagnosticBranchTestMulti(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.conditionVar,
                    config.conditions,
                    config.defaultPassageID || nextID
                )
                BREAK
                
            CASE "EVIDENCE_REVEAL":
                slpnPassage = GenerateDiagnosticEvidenceReveal(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.evidenceID,
                    nextID
                )
                BREAK
                
            CASE "EVIDENCE_EXAMINATION":
                slpnPassage = GenerateDiagnosticEvidenceExamination(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.evidenceID,
                    config.attributeData,
                    config.successPassageID || nextID,
                    config.failPassageID || nextID
                )
                BREAK
                
            CASE "MERGE_POINT":
                slpnPassage = GenerateDiagnosticMergePoint(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.trackOriginPath,
                    nextID
                )
                BREAK
                
            CASE "LOOP_TEST":
                slpnPassage = GenerateDiagnosticLoopTest(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.loopVarName,
                    config.maxIterations,
                    config.exitPassageID || nextID
                )
                BREAK
                
            CASE "APP_NAVIGATION":
                slpnPassage = GenerateDiagnosticAppNavigation(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.targetApp,
                    config.returnPassageID || nextID
                )
                BREAK
                
            CASE "COMPOUND_CONDITION":
                slpnPassage = GenerateDiagnosticCompoundCondition(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.logicalOperator,
                    config.conditions,
                    config.truePassageID || nextID,
                    config.falsePassageID || nextID
                )
                BREAK
                
            CASE "EXIT_POINT":
                slpnPassage = GenerateDiagnosticExitPoint(
                    stepIDPrefix,
                    currentID,
                    testCaseID,
                    config.testOutcome,
                    config.resultData
                )
                BREAK
                
            DEFAULT:
                THROW "Unsupported passage type: " + config.type
        }
        
        // Add to the complete sequence
        IF i > 0 {
            allPassages += "\n\n"
        }
        allPassages += "PSG:uid=" + currentID + ";nam=\"Test Case " + testCaseID + ": " + config.type + "\";" + 
                      "tag=DIAGNOSTIC|TEST_CASE_" + testCaseID + ";" +
                      "cmd=CMD:typ=diagnostic;\n" + slpnPassage
    }
    
    // Validation check
    PROCEDURE ValidateTestSequence(allPassages, passageCounter, sequenceConfig) {
        VALIDATE passageCounter == sequenceConfig.length
        
        // Verify entry and exit markers
        VALIDATE allPassages CONTAINS "Test case complete" // Exit marker
        VALIDATE allPassages CONTAINS sequenceConfig[0].description // Entry description
    }
    
    ValidateTestSequence(allPassages, passageCounter, sequenceConfig)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_TEST_SEQUENCE #}
