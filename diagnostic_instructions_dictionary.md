{# PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}

PROCEDURE GenerateDiagnosticEntryPoint(stepIDPrefix, entry_point_id, testCaseID, testDescription, initialState, nextPassageID) {
    // Primary goal: Create the entry point for a test sequence that initializes the testing environment
    // Structure: Single passage that sets up initial conditions and directs to the first test passage

    // Define UID for this passage
    DEFINE entryUID = entry_point_id // Use the provided entry_point_id
    DEFINE entryName = "Test Case " + testCaseID + ": Entry Point"
    
    // Create descriptive text for the test initialization
    PROCEDURE CreateEntryContent(testDescription) {
        RETURN "Diagnostic Test Case " + testCaseID + ": " + testDescription
    }
    
    // Create state initialization commands
    PROCEDURE CreateInitialStateCommands(initialState) {
        DEFINE stateCommands = ""
        
        // Loop through all initial state variables and create SET commands
        FOR EACH key, value IN initialState {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                stateCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                stateCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        RETURN stateCommands
    }
    
    // Generate SLPN for this passage
    DEFINE entryContent = CreateEntryContent(testDescription)
    DEFINE stateCommands = CreateInitialStateCommands(initialState)
    
    DEFINE slpnPassage = "BOT:lin=\"" + entryContent + "\";\n" +
                        stateCommands + "\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateEntryPoint(slpnPassage, initialState, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Diagnostic Test Case"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all initial state variables are set
        FOR EACH key IN initialState {
            VALIDATE slpnPassage CONTAINS key
        }
    }
    
    ValidateEntryPoint(slpnPassage, initialState, nextPassageID)
    
    RETURN slpnPassage
}

// Helper function to determine data type for setting state variables correctly
FUNCTION GetDataType(value) {
    IF typeof(value) == "boolean" {
        RETURN "boolean"
    } ELSE IF typeof(value) == "number" {
        RETURN "number"
    } ELSE {
        RETURN "string"
    }
}

{# END_PHENOTYPE: DIAGNOSTIC_ENTRY_POINT #}

{# PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}

PROCEDURE GenerateDiagnosticLinearTest(stepIDPrefix, entry_point_id, testCaseID, stepNumber, totalSteps, stateChanges, nextPassageID) {
    // Primary goal: Create a straightforward test passage that modifies state and proceeds linearly
    // Structure: Single passage that tests simple progression and state modification

    // Define UID for this passage
    DEFINE linearUID = entry_point_id // Use the provided entry_point_id
    DEFINE linearName = "Test Case " + testCaseID + ": Linear Test Step " + stepNumber
    
    // Create descriptive text for the test step
    PROCEDURE CreateLinearContent(stepNumber, totalSteps) {
        RETURN "Testing linear progression (Step " + stepNumber + " of " + totalSteps + ")"
    }
    
    // Create state change commands
    PROCEDURE CreateStateChangeCommands(stateChanges, stepNumber) {
        DEFINE changeCommands = ""
        
        // Loop through all state changes and create SET commands
        FOR EACH key, value IN stateChanges {
            DEFINE dataType = GetDataType(value)
            
            // Check if it's an event flag or variable
            IF dataType == "boolean" {
                changeCommands += "SET:evt=" + key + ";val=" + value + ";"
            } ELSE {
                changeCommands += "SET:var=" + key + ";val=" + value + ";"
            }
        }
        
        // Add a completed flag for this step
        changeCommands += "SET:evt=TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE;val=true;"
        
        RETURN changeCommands
    }
    
    // Generate SLPN for this passage
    DEFINE linearContent = CreateLinearContent(stepNumber, totalSteps)
    DEFINE changeCommands = CreateStateChangeCommands(stateChanges, stepNumber)
    
    DEFINE slpnPassage = "BOT:lin=\"" + linearContent + "\";\n" +
                         changeCommands + "\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing linear progression"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify that all state changes are set
        FOR EACH key IN stateChanges {
            VALIDATE slpnPassage CONTAINS key
        }
        
        // Verify step completion flag
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_STEP" + stepNumber + "_COMPLETE"
    }
    
    ValidateLinearTest(slpnPassage, stateChanges, nextPassageID, stepNumber)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_LINEAR_TEST #}

{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}

PROCEDURE GenerateDiagnosticBranchTestBinary(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditionValue, pathAPassageID, pathBPassageID) {
    // Primary goal: Create a passage that tests binary branching based on a condition
    // Structure: Single passage with condition-based branching to two different paths

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Binary Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateBranchContent() {
        RETURN "Testing binary branching condition"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateBranchContent()
    
    // Create two branch options for true and false conditions
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=blocking;" +
                        "ops=BOP:onm=\"If " + conditionVar + " = " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathAPassageID + ";" +
                        "ops=BOP:onm=\"If " + conditionVar + " ≠ " + conditionValue + "\";chk=CHK:asp=" + conditionVar + ";cty=ne;vlu=" + conditionValue + ";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + pathBPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing binary branching condition"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS pathAPassageID
        VALIDATE slpnPassage CONTAINS pathBPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        VALIDATE slpnPassage CONTAINS "ops=BOP"
    }
    
    ValidateBinaryBranchTest(slpnPassage, conditionVar, pathAPassageID, pathBPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_BINARY #}

{# PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}

PROCEDURE GenerateDiagnosticBranchTestMulti(stepIDPrefix, entry_point_id, testCaseID, conditionVar, conditions, defaultPassageID) {
    // Primary goal: Create a passage that tests multi-way branching based on different values of a condition
    // Structure: Single passage with multi-way branching based on variable value
    // Input: conditions is a list of objects { value: valueToCheck, targetPassageID: passageIDForThisValue }

    // Define UID for this passage
    DEFINE branchUID = entry_point_id
    DEFINE branchName = "Test Case " + testCaseID + ": Multi-way Branch Test"
    
    // Create descriptive text for the test branching
    PROCEDURE CreateMultiBranchContent() {
        RETURN "Testing multi-way branching conditions"
    }
    
    // Generate SLPN for this passage
    DEFINE branchContent = CreateMultiBranchContent()
    
    // Start with the branch header and bot line
    DEFINE slpnPassage = "BOT:lin=\"" + branchContent + "\";\n" +
                        "brn=BRN:bds=\"Condition Evaluation\";brp=once;bpr=option-list;bit=blocking;"
    
    // Loop through conditions to create branch options
    FOR EACH condition IN conditions {
        slpnPassage += "ops=BOP:onm=\"If " + conditionVar + " = " + condition.value + "\";" +
                      "chk=CHK:asp=" + conditionVar + ";cty=eq;vlu=" + condition.value + ";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + condition.targetPassageID + ";"
    }
    
    // Add the default case (fallback option)
    slpnPassage += "ops=BOP:onm=\"Default Case\";act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + defaultPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing multi-way branching conditions"
        VALIDATE slpnPassage CONTAINS conditionVar
        VALIDATE slpnPassage CONTAINS defaultPassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        
        // Verify all target passages are included
        FOR EACH condition IN conditions {
            VALIDATE slpnPassage CONTAINS condition.targetPassageID
        }
    }
    
    ValidateMultiBranchTest(slpnPassage, conditionVar, conditions, defaultPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_BRANCH_TEST_MULTI #}

{# PHENOTYPE: DIAGNOSTIC_EVIDENCE_REVEAL #}

PROCEDURE GenerateDiagnosticEvidenceReveal(stepIDPrefix, entry_point_id, testCaseID, evidenceID, nextPassageID) {
    // Primary goal: Create a passage that tests the evidence reveal mechanism
    // Structure: Single passage that reveals evidence and tracks the reveal state

    // Define UID for this passage
    DEFINE revealUID = entry_point_id
    DEFINE revealName = "Test Case " + testCaseID + ": Evidence Reveal Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateRevealContent() {
        RETURN "Testing evidence reveal functionality"
    }
    
    // Generate SLPN for this passage
    DEFINE revealContent = CreateRevealContent()
    
    DEFINE slpnPassage = "BOT:lin=\"" + revealContent + "\";\n" +
                         "ACT:aty=REVEAL;aet=" + evidenceID + ";\n" +
                         "SET:evt=" + evidenceID + "_REVEALED;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;"
    
    // Validation check
    PROCEDURE ValidateEvidenceReveal(slpnPassage, evidenceID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing evidence reveal"
        VALIDATE slpnPassage CONTAINS "ACT:aty=REVEAL;aet=" + evidenceID
        VALIDATE slpnPassage CONTAINS evidenceID + "_REVEALED;val=true"
        VALIDATE slpnPassage CONTAINS "ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app"
    }
    
    ValidateEvidenceReveal(slpnPassage, evidenceID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_EVIDENCE_REVEAL #}

{# PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}

PROCEDURE GenerateDiagnosticEvidenceExamination(stepIDPrefix, entry_point_id, testCaseID, evidenceID, attributeData, successPassageID, failPassageID) {
    // Primary goal: Create a passage that tests evidence examination and attribute discovery
    // Structure: Series of passages that sets evidence attributes and branches based on examination state
    // Input: attributeData is an object mapping attribute names to values

    // Define UIDs for the passage sequence
    DEFINE examineUID = entry_point_id
    DEFINE examineName = "Test Case " + testCaseID + ": Evidence Examination Test"
    DEFINE setStateUID = "diag_exam_" + testCaseID + "_set_state"
    DEFINE checkStateUID = "diag_exam_" + testCaseID + "_check_state"
    DEFINE successUID = "diag_exam_" + testCaseID + "_success"
    DEFINE failUID = "diag_exam_" + testCaseID + "_fail"
    
    // Create descriptive text for each passage
    PROCEDURE CreateStartContent() {
        RETURN "Testing evidence examination and attribute discovery for " + evidenceID + "."
    }
    
    PROCEDURE CreateSetStateContent() {
        RETURN "Setting state for " + evidenceID + "."
    }
    
    PROCEDURE CreateCheckContent() {
        RETURN "Checking state..."
    }
    
    PROCEDURE CreateSuccessContent() {
        RETURN "Attributes and examined status were set correctly."
    }
    
    PROCEDURE CreateFailContent() {
        RETURN "Attributes and examined status were NOT set correctly."
    }
    
    // Create attribute commands for setting state
    PROCEDURE CreateAttributeSettings(evidenceID, attributeData) {
        DEFINE attributeCommands = ""
        
        // Set the main examined flag
        attributeCommands += "SET:evt=" + evidenceID + "_EXAMINED;val=true;"
        
        // Set each attribute value
        FOR EACH attrName, attrValue IN attributeData {
            attributeCommands += "UAS:asp=" + attrName + ";uty=SET;val=\"" + attrValue + "\";"
        }
        
        RETURN attributeCommands
    }
    
    // 1. Create the start passage with branch to set state
    DEFINE startContent = CreateStartContent()
    DEFINE startPassage = "PSG:uid=" + examineUID + ";nam=\"" + examineName + "\";\n" +
                         "BOT:lin=\"" + startContent + "\";\n" +
                         "brn=BRN:bds=\"Start Test Step\";brp=once;bpr=option-list;bit=blocking;" +
                         "ops=BOP:onm=\"Begin Examination Test\";ods=\"Proceed to the next step in the diagnostic sequence\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + setStateUID + ";"
    
    // 2. Create the set state passage
    DEFINE setStateContent = CreateSetStateContent()
    DEFINE attributeCommands = CreateAttributeSettings(evidenceID, attributeData)
    DEFINE setStatePassage = "PSG:uid=" + setStateUID + ";nam=\"Set Evidence Attributes\";\n" +
                            "BOT:lin=\"" + setStateContent + "\";\n" +
                            attributeCommands + "\n" +
                            "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkStateUID + ";"
    
    // 3. Create the check state passage with branch
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkStatePassage = "PSG:uid=" + checkStateUID + ";nam=\"Verify Evidence State\";\n" +
                              "BOT:lin=\"" + checkContent + "\";\n" +
                              "brn=BRN:bds=\"Verify State\";brp=once;bpr=option-list;bit=blocking;" +
                              "ops=BOP:onm=\"Success Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=eq;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successUID + ";" +
                              "ops=BOP:onm=\"Failure Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=ne;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failUID + ";"
    
    // 4. Create success passage
    DEFINE successContent = CreateSuccessContent()
    DEFINE successPassage = "PSG:uid=" + successUID + ";nam=\"Examination Test Success\";\n" +
                           "BOT:lin=\"" + successContent + "\";\n" +
                           "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successPassageID + ";"
    
    // 5. Create fail passage
    DEFINE failContent = CreateFailContent()
    DEFINE failPassage = "PSG:uid=" + failUID + ";nam=\"Examination Test Failure\";\n" +
                        "BOT:lin=\"" + failContent + "\";\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failPassageID + ";"
    
    // Combine all passages
    DEFINE allPassages = startPassage + "\n\n" + 
                        setStatePassage + "\n\n" + 
                        checkStatePassage + "\n\n" + 
                        successPassage + "\n\n" + 
                        failPassage
    
    // Validation check
    PROCEDURE ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID) {
        // Verify that required elements are present
        VALIDATE allPassages CONTAINS "Testing evidence examination"
        VALIDATE allPassages CONTAINS evidenceID + "_EXAMINED;val=true"
        VALIDATE allPassages CONTAINS successPassageID
        VALIDATE allPassages CONTAINS failPassageID
        VALIDATE allPassages CONTAINS "brn=BRN"
        
        // Verify all attributes are set
        FOR EACH attrName IN attributeData {
            VALIDATE allPassages CONTAINS attrName
        }
        
        // Verify all passage IDs are included
        VALIDATE allPassages CONTAINS successUID
        VALIDATE allPassages CONTAINS failUID
        VALIDATE allPassages CONTAINS setStateUID
        VALIDATE allPassages CONTAINS checkStateUID
    }
    
    ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}

{# PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}

PROCEDURE GenerateDiagnosticMergePoint(stepIDPrefix, entry_point_id, testCaseID, trackOriginPath, nextPassageID) {
    // Primary goal: Create a passage that tests the convergence of multiple paths into a single outcome
    // Structure: Single passage that can be targeted from multiple sources and tracks arrival path

    // Define UID for this passage
    DEFINE mergeUID = entry_point_id
    DEFINE mergeName = "Test Case " + testCaseID + ": Merge Point Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateMergeContent() {
        RETURN "Testing path merge functionality (arrival from multiple sources)"
    }
    
    // Generate SLPN for this passage
    DEFINE mergeContent = CreateMergeContent()
    DEFINE originTracking = ""
    
    // Add optional origin path tracking - use $source_path as a literal, not template syntax
    IF trackOriginPath {
        originTracking = "UAS:asp=arrival_path;uty=SET;val=\"$source_path\";\n"
    }
    
    DEFINE slpnPassage = "BOT:lin=\"" + mergeContent + "\";\n" +
                         originTracking +
                         "UAS:asp=MERGE_POINT_REACHED;uty=SET;val=true;\n" +
                         "brn=BRN:bds=\"Proceed to Next Test\";brp=once;bpr=option-list;bit=blocking;" +
                         "ops=BOP:onm=\"Continue\";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing path merge functionality"
        VALIDATE slpnPassage CONTAINS "MERGE_POINT_REACHED"
        VALIDATE slpnPassage CONTAINS nextPassageID
        
        // Verify origin tracking if enabled
        IF trackOriginPath {
            VALIDATE slpnPassage CONTAINS "arrival_path"
        }
    }
    
    ValidateMergePoint(slpnPassage, trackOriginPath, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_MERGE_POINT #}

{# PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}

PROCEDURE GenerateDiagnosticLoopTest(stepIDPrefix, entry_point_id, testCaseID, loopVarName, maxIterations, exitPassageID) {
    // Primary goal: Create a passage that tests cyclical progression with iteration counter and exit condition
    // Structure: Single self-referencing passage with counter that exits after a certain number of iterations

    // Define UID for this passage
    DEFINE loopUID = entry_point_id
    DEFINE loopName = "Test Case " + testCaseID + ": Loop Test"
    
    // Create descriptive text for the test that includes the dynamic counter
    PROCEDURE CreateLoopContent(loopVarName) {
        RETURN "Testing loop functionality (iteration $" + loopVarName + ")"
    }
    
    // Generate SLPN for this passage
    DEFINE loopContent = CreateLoopContent(loopVarName)
    
    // Create a separate check passage to handle the conditional logic
    DEFINE checkPassageUID = entry_point_id + "_check"
    DEFINE loopPassages = ""
    
    // First passage - increment the counter
    DEFINE slpnPassage = "BOT:lin=\"" + loopContent + "\";\n" +
                         "UAS:asp=" + loopVarName + ";uty=SET;val=$" + loopVarName + " + 1;\n" +
                         "brn=BRN:bds=\"Loop Control\";brp=once;bpr=option-list;bit=blocking;" +
                         "ops=BOP:onm=\"Proceed\";ods=\"Continue to next step\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkPassageUID + ";"
    
    // Check passage - evaluate and branch
    DEFINE checkPassage = "PSG:uid=" + checkPassageUID + ";nam=\"" + loopName + " - Check\";\n" +
                         "BOT:lin=\"Evaluating loop condition...\";\n" +
                         "brn=BRN:bds=\"Loop Evaluation\";brp=once;bpr=option-list;bit=blocking;" +
                         "ops=BOP:onm=\"Exit Loop\";chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations + ";" +
                         "UAS:asp=LOOP_TEST_COMPLETE;uty=SET;val=true;" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + exitPassageID + ";" +
                         "ops=BOP:onm=\"Continue Loop\";chk=CHK:asp=" + loopVarName + ";cty=lt;vlu=" + maxIterations + ";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + entry_point_id + ";"
    
    // Combine the passages
    loopPassages = slpnPassage + "\n\n" + checkPassage
    
    // Validation check
    PROCEDURE ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID) {
        // Verify that required elements are present
        VALIDATE loopPassages CONTAINS "Testing loop functionality"
        VALIDATE loopPassages CONTAINS loopVarName + ";uty=SET;val=$" + loopVarName + " + 1"
        VALIDATE loopPassages CONTAINS "chk=CHK:asp=" + loopVarName + ";cty=gte;vlu=" + maxIterations
        VALIDATE loopPassages CONTAINS "LOOP_TEST_COMPLETE;uty=SET;val=true"
        VALIDATE loopPassages CONTAINS exitPassageID
        VALIDATE loopPassages CONTAINS "tgt=" + entry_point_id
        VALIDATE loopPassages CONTAINS "brn=BRN"
        VALIDATE loopPassages CONTAINS checkPassageUID
    }
    
    ValidateLoopTest(loopPassages, loopVarName, maxIterations, exitPassageID, entry_point_id, checkPassageUID)
    
    RETURN loopPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_LOOP_TEST #}

{# PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}

PROCEDURE GenerateDiagnosticAppNavigation(stepIDPrefix, entry_point_id, testCaseID, targetApp, returnPassageID) {
    // Primary goal: Create a passage that tests navigation between different application interfaces
    // Structure: Single passage that navigates to a specific application and sets state

    // Define UID for this passage
    DEFINE navUID = entry_point_id
    DEFINE navName = "Test Case " + testCaseID + ": Application Navigation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateNavContent(targetApp) {
        RETURN "Testing application navigation to " + targetApp
    }
    
    // Generate SLPN for this passage
    DEFINE navContent = CreateNavContent(targetApp)
    
    DEFINE appTypeMap = {
        "EVIDENCE": "EVIDENCE",
        "DEDUCTION": "DEDUCTION",
        "NOTES": "NOTES",
        "MAP": "MAP",
        "CASE_FILE": "CASE_FILE"
    }
    
    // Lookup the app type or default to the provided value
    DEFINE appType = appTypeMap[targetApp] ? appTypeMap[targetApp] : targetApp
    
    DEFINE slpnPassage = "BOT:lin=\"" + navContent + "\";\n" +
                         "SET:evt=NAV_TO_" + appType + "_APP;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=" + appType + ";tgt=" + targetApp.toLowerCase() + "_app;\n" +
                         "SET:evt=RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\";"
    
    // Validation check
    PROCEDURE ValidateAppNavigation(slpnPassage, targetApp, returnPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing application navigation"
        VALIDATE slpnPassage CONTAINS "NAV_TO_" + appType + "_APP;val=true"
        VALIDATE slpnPassage CONTAINS "ACT:aty=MOVE;amt=AMT:typ=" + appType
        VALIDATE slpnPassage CONTAINS "RETURN_TO_PASSAGE;val=\"" + returnPassageID + "\""
    }
    
    ValidateAppNavigation(slpnPassage, targetApp, returnPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_APP_NAVIGATION #}

{# PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}

PROCEDURE GenerateDiagnosticExitPoint(stepIDPrefix, entry_point_id, testCaseID, testOutcome, resultData) {
    // Primary goal: Create a passage that tests proper system termination and outcome recording
    // Structure: Single passage that records final state and signals test completion
    // Input: resultData is an object of key-value pairs to record as test results

    // Define UID for this passage
    DEFINE exitUID = entry_point_id
    DEFINE exitName = "Test Case " + testCaseID + ": Exit Point"
    
    // Create descriptive text for the test
    PROCEDURE CreateExitContent(testOutcome) {
        RETURN "Test case complete. Validating final state. Outcome: " + testOutcome
    }
    
    // Create result data recording
    PROCEDURE CreateResultRecording(testCaseID, resultData) {
        DEFINE resultCommands = ""
        
        // Record overall test completion
        resultCommands += "SET:evt=TC" + testCaseID + "_COMPLETE;val=true;\n"
        resultCommands += "SET:var=test_outcome;val=\"" + testOutcome + "\";\n"
        
        // Record each result data point
        FOR EACH key, value IN resultData {
            DEFINE dataType = GetDataType(value)
            
            IF dataType == "boolean" {
                resultCommands += "SET:evt=TC" + testCaseID + "_RESULT_" + key + ";val=" + value + ";\n"
            } ELSE {
                resultCommands += "SET:var=TC" + testCaseID + "_RESULT_" + key + ";val=" + (typeof(value) == "string" ? "\"" + value + "\"" : value) + ";\n"
            }
        }
        
        RETURN resultCommands
    }
    
    // Generate SLPN for this passage
    DEFINE exitContent = CreateExitContent(testOutcome)
    DEFINE resultCommands = CreateResultRecording(testCaseID, resultData)
    
    DEFINE slpnPassage = "BOT:lin=\"" + exitContent + "\";\n" +
                         resultCommands + "\n" +
                         "brn=BRN:bds=\"Test Complete\";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm=\"Finalize Test\";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME;"
    
    // Validation check
    PROCEDURE ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Test case complete"
        VALIDATE slpnPassage CONTAINS "Outcome: " + testOutcome
        VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_COMPLETE;val=true"
        VALIDATE slpnPassage CONTAINS "test_outcome;val=\"" + testOutcome + "\""
        VALIDATE slpnPassage CONTAINS "brn=BRN:bds=\"Test Complete\""
        VALIDATE slpnPassage CONTAINS "act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=HOME"
        
        // Verify result data points are recorded
        FOR EACH key IN resultData {
            VALIDATE slpnPassage CONTAINS "TC" + testCaseID + "_RESULT_" + key
        }
    }
    
    ValidateExitPoint(slpnPassage, testCaseID, testOutcome, resultData)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_EXIT_POINT #}

{# PHENOTYPE: DIAGNOSTIC_COMPOUND_CONDITION #}

PROCEDURE GenerateDiagnosticCompoundCondition(stepIDPrefix, entry_point_id, testCaseID, logicalOperator, conditions, truePassageID, falsePassageID) {
    // Primary goal: Create a passage that tests complex condition combinations using logical operators
    // Structure: Single passage with a compound condition (AND/OR/NOT) that branches based on evaluation
    // Input: logicalOperator is "AND", "OR", or "NOT"
    // Input: conditions is a list of condition objects { variable: name, operator: "EQUALS"|"NOT_EQUALS"|etc, value: checkValue }

    // Define UID for this passage
    DEFINE compoundUID = entry_point_id
    DEFINE compoundName = "Test Case " + testCaseID + ": Compound Condition Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateCompoundContent(logicalOperator) {
        RETURN "Testing compound condition with " + logicalOperator + " operator"
    }
    
    // Create compound condition CHK string for branch option
    PROCEDURE CreateCompoundConditionCheck(logicalOperator, conditions) {
        DEFINE checkString = ""
        
        // Special case for NOT (single condition)
        IF logicalOperator == "NOT" {
            DEFINE condition = conditions[0]
            checkString = "chk=CHK:cty=not;chk=CHK:asp=" + condition.variable + ";cty=" + MapOperator(condition.operator) + ";vlu=" + condition.value + ";"
            RETURN checkString
        }
        
        // For AND/OR compound conditions
        checkString = "chk=CHK:cty=" + logicalOperator.toLowerCase() + ";"
        
        // Add each individual condition
        FOR EACH condition IN conditions {
            checkString += "chk=CHK:asp=" + condition.variable + ";cty=" + MapOperator(condition.operator) + ";vlu=" + condition.value + ";"
        }
        
        RETURN checkString
    }
    
    // Helper function to map SLPN operators to CHK format
    FUNCTION MapOperator(operator) {
        DEFINE opMap = {
            "EQUALS": "eq",
            "NOT_EQUALS": "ne", 
            "GREATER_THAN": "gt",
            "LESS_THAN": "lt",
            "GREATER_OR_EQUAL": "gte",
            "LESS_OR_EQUAL": "lte"
        }
        
        RETURN opMap[operator] || "eq" // Default to eq if not found
    }
    
    // Generate SLPN for this passage
    DEFINE compoundContent = CreateCompoundContent(logicalOperator)
    DEFINE conditionCheck = CreateCompoundConditionCheck(logicalOperator, conditions)
    
    DEFINE slpnPassage = "BOT:lin=\"" + compoundContent + "\";\n" +
                        "brn=BRN:bds=\"Compound Condition Evaluation\";brp=once;bpr=option-list;bit=blocking;" +
                        "ops=BOP:onm=\"True Path\";" + conditionCheck +
                        "act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + truePassageID + ";" +
                        "ops=BOP:onm=\"False Path\";act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + falsePassageID + ";"
    
    // Validation check
    PROCEDURE ValidateCompoundCondition(slpnPassage, logicalOperator, conditions, truePassageID, falsePassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing compound condition with " + logicalOperator
        VALIDATE slpnPassage CONTAINS truePassageID
        VALIDATE slpnPassage CONTAINS falsePassageID
        VALIDATE slpnPassage CONTAINS "brn=BRN"
        
        // Verify each condition variable is included
        FOR EACH condition IN conditions {
            VALIDATE slpnPassage CONTAINS condition.variable
        }
        
        // Verify logical operator (in lowercase as used in CHK)
        IF logicalOperator == "NOT" {
            VALIDATE slpnPassage CONTAINS "cty=not"
        } ELSE {
            VALIDATE slpnPassage CONTAINS "cty=" + logicalOperator.toLowerCase()
        }
    }
    
    ValidateCompoundCondition(slpnPassage, logicalOperator, conditions, truePassageID, falsePassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_COMPOUND_CONDITION #}

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

{# PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}

PROCEDURE GenerateDiagnosticSLPNConversionTest(stepIDPrefix, entry_point_id, testCaseID, journeyFormat, expectedSLPN, nextPassageID) {
    // Primary goal: Create a passage that tests conversion from journey format to SLPN notation
    // Structure: Single passage that displays both journey input and expected SLPN output for verification

    // Define UID for this passage
    DEFINE conversionUID = entry_point_id
    DEFINE conversionName = "Test Case " + testCaseID + ": SLPN Conversion Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateConversionContent() {
        RETURN "Testing journey to SLPN conversion"
    }
    
    // Format journey and SLPN for display
    PROCEDURE FormatJourneyAndSLPN(journeyFormat, expectedSLPN) {
        DEFINE journeyString = JSON.stringify(journeyFormat, null, 2)
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = expectedSLPN.replace(/"/g, '\\"')
        
        RETURN "Journey Format: '" + journeyString + "', Expected SLPN: '" + escapedSLPN + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE conversionContent = CreateConversionContent()
    DEFINE formattedData = FormatJourneyAndSLPN(journeyFormat, expectedSLPN)
    
    DEFINE slpnPassage = "BOT:lin=\"" + conversionContent + "\";\n" +
                         "SET:var=conversion_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=CONVERSION_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing journey to SLPN conversion"
        VALIDATE slpnPassage CONTAINS "conversion_test_data"
        VALIDATE slpnPassage CONTAINS "CONVERSION_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateSLPNConversionTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_SLPN_CONVERSION_TEST #}

{# PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}

PROCEDURE GenerateDiagnosticJSONGenerationTest(stepIDPrefix, entry_point_id, testCaseID, slpnInput, expectedJSON, nextPassageID) {
    // Primary goal: Create a passage that tests SLPN-to-JSON transformation
    // Structure: Single passage that displays both SLPN input and expected JSON output for verification

    // Define UID for this passage
    DEFINE jsonGenUID = entry_point_id
    DEFINE jsonGenName = "Test Case " + testCaseID + ": JSON Generation Test"
    
    // Create descriptive text for the test
    PROCEDURE CreateJSONGenContent() {
        RETURN "Testing SLPN to JSON conversion"
    }
    
    // Format SLPN and JSON for display
    PROCEDURE FormatSLPNAndJSON(slpnInput, expectedJSON) {
        // Escape quotes in the SLPN string for embedding in the content
        DEFINE escapedSLPN = slpnInput.replace(/"/g, '\\"')
        DEFINE jsonString = JSON.stringify(expectedJSON, null, 2)
        
        RETURN "SLPN Input: '" + escapedSLPN + "', Expected JSON: '" + jsonString + "'"
    }
    
    // Generate SLPN for this passage
    DEFINE jsonGenContent = CreateJSONGenContent()
    DEFINE formattedData = FormatSLPNAndJSON(slpnInput, expectedJSON)
    
    DEFINE slpnPassage = "BOT:lin=\"" + jsonGenContent + "\";\n" +
                         "SET:var=json_test_data;val=\"" + formattedData + "\";\n" +
                         "SET:evt=JSON_TEST_" + testCaseID + "_COMPLETE;val=true;\n" +
                         "ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=" + nextPassageID + ";"
    
    // Validation check
    PROCEDURE ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID) {
        // Verify that required elements are present
        VALIDATE slpnPassage CONTAINS "Testing SLPN to JSON conversion"
        VALIDATE slpnPassage CONTAINS "json_test_data"
        VALIDATE slpnPassage CONTAINS "JSON_TEST_" + testCaseID + "_COMPLETE"
        VALIDATE slpnPassage CONTAINS nextPassageID
    }
    
    ValidateJSONGenerationTest(slpnPassage, testCaseID, nextPassageID)
    
    RETURN slpnPassage
}

{# END_PHENOTYPE: DIAGNOSTIC_JSON_GENERATION_TEST #}

{# PHENOTYPE: DIAGNOSTIC_COMPLEX_CONDITION #}

PROCEDURE GenerateDiagnosticComplexCondition(stepIDPrefix, entry_point_id, testCaseID, logicalOperator, conditionVars, truePassageID, falsePassageID) {
    // Primary goal: Create a passage structure that tests complex conditions (AND/OR) across multiple variables
    // Structure: Multiple passages for setting variables and direct branch validation with aspect checks
    // Input: logicalOperator is "AND" or "OR"
    // Input: conditionVars is a list of variable names to check in the complex condition

    // Define UIDs for the passage sequence
    DEFINE startUID = entry_point_id
    DEFINE checkUID = entry_point_id + "_check"
    DEFINE trueResultUID = entry_point_id + "_true_result"
    DEFINE falseResultUID = entry_point_id + "_false_result"
    
    // Create variable setting UIDs for each condition var
    DEFINE varSetUIDs = {}
    FOR EACH varName IN conditionVars {
        varSetUIDs[varName + "_true"] = "diag_set_" + varName + "_true_" + testCaseID
        varSetUIDs[varName + "_false"] = "diag_set_" + varName + "_false_" + testCaseID
    }
    
    // Create descriptive text for each passage
    PROCEDURE CreateStartContent() {
        RETURN "Testing complex " + logicalOperator + " condition with multiple variables"
    }
    
    PROCEDURE CreateVariableSetContent(varName, value) {
        RETURN "Setting " + varName + " to " + value
    }
    
    PROCEDURE CreateCheckContent() {
        RETURN "Evaluating complex " + logicalOperator + " condition"
    }
    
    PROCEDURE CreateResultContent(result) {
        RETURN "Complex condition evaluated to " + result + "!"
    }
    
    // 1. Create the start passage with variable setting options
    DEFINE startContent = CreateStartContent()
    DEFINE startPassage = "PSG:uid=" + startUID + ";nam=\"Complex Condition Test\";\n" +
                         "BOT:lin=\"" + startContent + "\";\n" +
                         "brn=BRN:bds=\"Set Variables or Check\";brp=re-playable;bpr=option-list;bit=blocking;"
    
    // Add options for setting each variable true/false
    FOR EACH varName IN conditionVars {
        startPassage += "ops=BOP:onm=\"Set " + varName + " True\";ods=\"Set " + varName + " to true\";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + varSetUIDs[varName + "_true"] + "|"
        
        startPassage += "ops=BOP:onm=\"Set " + varName + " False\";ods=\"Set " + varName + " to false\";" +
                        "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + varSetUIDs[varName + "_false"] + "|"
    }
    
    // Add option to perform the check
    startPassage += "ops=BOP:onm=\"Perform " + logicalOperator + " Check\";ods=\"Test the complex condition\";" +
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkUID + ";"
    
    // 2. Create variable setting passages
    DEFINE varSetPassages = ""
    FOR EACH varName IN conditionVars {
        // True setting passage
        DEFINE trueContent = CreateVariableSetContent(varName, "TRUE")
        DEFINE trueSetPassage = "PSG:uid=" + varSetUIDs[varName + "_true"] + ";nam=\"Set " + varName + " True\";\n" +
                                "BOT:lin=\"" + trueContent + "\";\n" +
                                "UAS:asp=" + varName + ";uty=SET;val=true;\n" +
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=blocking;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        // False setting passage
        DEFINE falseContent = CreateVariableSetContent(varName, "FALSE")
        DEFINE falseSetPassage = "PSG:uid=" + varSetUIDs[varName + "_false"] + ";nam=\"Set " + varName + " False\";\n" +
                                "BOT:lin=\"" + falseContent + "\";\n" +
                                "UAS:asp=" + varName + ";uty=SET;val=false;\n" +
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=blocking;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        varSetPassages += trueSetPassage + "\n\n" + falseSetPassage + "\n\n"
    }
    
    // 3. Create check passage with branch options for complex condition
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkPassage = "PSG:uid=" + checkUID + ";nam=\"Evaluate " + logicalOperator + " Condition\";\n" +
                         "BOT:lin=\"" + checkContent + "\";\n" +
                         "brn=BRN:bds=\"Condition Check\";brp=once;bpr=option-list;bit=blocking;"
    
    // Add success branch with complex condition check
    checkPassage += "ops=BOP:onm=\"True Path\";"
    
    // Add the appropriate check based on logicalOperator
    IF logicalOperator == "AND" {
        checkPassage += "chk=CHK:cty=and;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    } ELSE { // OR case
        checkPassage += "chk=CHK:cty=or;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    }
    
    checkPassage += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + trueResultUID + ";"
    
    // Add failure branch 
    checkPassage += "ops=BOP:onm=\"False Path\";"
    
    // Add the opposite check based on logicalOperator
    IF logicalOperator == "AND" {
        checkPassage += "chk=CHK:cty=not;chk=CHK:cty=and;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    } ELSE { // OR case
        checkPassage += "chk=CHK:cty=not;chk=CHK:cty=or;"
        FOR EACH varName IN conditionVars {
            checkPassage += "chk=CHK:asp=" + varName + ";cty=eq;vlu=true;"
        }
    }
    
    checkPassage += "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + falseResultUID + ";"
    
    // 4. Create result passages
    DEFINE trueContent = CreateResultContent("TRUE")
    DEFINE trueResultPassage = "PSG:uid=" + trueResultUID + ";nam=\"Complex Check: TRUE\";\n" +
                              "BOT:lin=\"" + trueContent + "\";\n" +
                              "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=blocking;" +
                              "ops=BOP:onm=\"Proceed\";ods=\"Continue to next test\";" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + truePassageID + ";"
    
    DEFINE falseContent = CreateResultContent("FALSE")
    DEFINE falseResultPassage = "PSG:uid=" + falseResultUID + ";nam=\"Complex Check: FALSE\";\n" +
                               "BOT:lin=\"" + falseContent + "\";\n" +
                               "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=blocking;" +
                               "ops=BOP:onm=\"Proceed\";ods=\"Continue to next test\";" +
                               "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + falsePassageID + ";"
    
    // Combine all passages
    DEFINE allPassages = startPassage + "\n\n" + 
                        varSetPassages +
                        checkPassage + "\n\n" +
                        trueResultPassage + "\n\n" +
                        falseResultPassage
    
    // Validation check
    PROCEDURE ValidateComplexCondition(allPassages, logicalOperator, conditionVars, truePassageID, falsePassageID) {
        // Verify that required elements are present
        VALIDATE allPassages CONTAINS "Testing complex " + logicalOperator + " condition"
        VALIDATE allPassages CONTAINS truePassageID
        VALIDATE allPassages CONTAINS falsePassageID
        
        // Verify each condition variable is included
        FOR EACH varName IN conditionVars {
            VALIDATE allPassages CONTAINS varName
            VALIDATE allPassages CONTAINS varSetUIDs[varName + "_true"]
            VALIDATE allPassages CONTAINS varSetUIDs[varName + "_false"]
        }
        
        // Verify logical operator
        VALIDATE allPassages CONTAINS "cty=" + logicalOperator.toLowerCase()
        
        // Verify result passages
        VALIDATE allPassages CONTAINS trueResultUID
        VALIDATE allPassages CONTAINS falseResultUID
    }
    
    ValidateComplexCondition(allPassages, logicalOperator, conditionVars, truePassageID, falsePassageID)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_COMPLEX_CONDITION #} 