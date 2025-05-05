# Diagnostic Journey: System Integration Test Suite

## Testing Overview

**COMPREHENSIVE DIAGNOSTIC TEST SEQUENCE: VALIDATING END-TO-END SYSTEM FUNCTIONALITY**

*This diagnostic journey defines a complete test sequence that validates all critical pathways through the story creation and delivery system - from initial journey specification through SLPN syntax to JSON generation. Each test case isolates specific functionality while the complete sequence verifies integrated operation across the entire pipeline.*

*The primary focus is technical validation, not narrative quality. Test cases use minimal content focused on structure verification rather than telling a compelling story.*

**Goal:** Provide a systematic verification mechanism for all core system components, edge cases, and integration points to ensure reliable functionality across the entire pipeline.

**Note:** This journey relies on pre-defined test evidence items (`test_evidence_01`, `test_evidence_02`, etc.) existing in the system. Several test passages explicitly reference and manipulate these items to verify proper functionality.

**(Phase 1: Initialization & Linear Progression)**

* **Associated Diagnostics:** `DIAGNOSTIC_ENTRY_POINT`, `DIAGNOSTIC_LINEAR_TEST` (Test Cases 01-03)
* **Testing Goal:** Validate system initialization, state setting, and straightforward passage sequencing. Confirm variables and events are properly assigned and maintained.
* **Test Delivery:** Create an entry point that initializes the test environment, followed by a series of linear progression steps that modify state and move forward along a predetermined path.

* **Test Cases & Phenotypes:**

    1. **Test Case:** System Initialization
        * **Purpose:** Initialize the test environment with required state variables.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "diag_tc01"
            * `entry_point_id`: "TC01_ENTRY"
            * `testCaseID`: "01"
            * `testDescription`: "Basic System Initialization"
            * `initialState`: { "test_counter": 0, "system_ready": true }
            * `nextPassageID`: "TC01_LINEAR_1"
        * **Technical Validation Goal:** System correctly initializes state variables and begins test sequence.

    2. **Test Case:** Linear Step 1
        * **Purpose:** Verify simple passage progression and state modification.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "diag_tc01"
            * `entry_point_id`: "TC01_LINEAR_1"
            * `testCaseID`: "01"
            * `stepNumber`: 1
            * `totalSteps`: 3
            * `stateChanges`: { "test_counter": 1 }
            * `nextPassageID`: "TC01_LINEAR_2"
        * **Technical Validation Goal:** System correctly modifies state and proceeds to next passage.

    3. **Test Case:** Linear Step 2
        * **Purpose:** Verify continued progression and cumulative state changes.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "diag_tc01"
            * `entry_point_id`: "TC01_LINEAR_2"
            * `testCaseID`: "01"
            * `stepNumber`: 2
            * `totalSteps`: 3
            * `stateChanges`: { "test_counter": 2 }
            * `nextPassageID`: "TC01_LINEAR_3"
        * **Technical Validation Goal:** System maintains and updates previously set state variables.

    4. **Test Case:** Linear Step 3
        * **Purpose:** Complete linear sequence and prepare for branching tests.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "diag_tc01"
            * `entry_point_id`: "TC01_LINEAR_3"
            * `testCaseID`: "01"
            * `stepNumber`: 3
            * `totalSteps`: 3
            * `stateChanges`: { "test_counter": 3, "linear_sequence_complete": true }
            * `nextPassageID`: "TC02_ENTRY"
        * **Technical Validation Goal:** Linear progression successful; system ready for branch testing.

**(Phase 2: Branching Logic Testing)**

* **Associated Diagnostics:** `DIAGNOSTIC_BRANCH_TEST_BINARY`, `DIAGNOSTIC_BRANCH_TEST_MULTI`, `DIAGNOSTIC_COMPOUND_CONDITION` (Test Cases 02-04)
* **Testing Goal:** Validate the system's ability to properly evaluate conditions and follow the correct branching paths.
* **Test Delivery:** Create test passages that exercise binary (if/else), multi-way (if/elif/elif/else), and compound (AND/OR/NOT) conditional branches.

* **Test Cases & Phenotypes:**

    1. **Test Case:** Binary Branching
        * **Purpose:** Validate simple binary condition evaluation.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_BRANCH_TEST_BINARY`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc02"
            * `entry_point_id`: "TC02_ENTRY"
            * `testCaseID`: "02"
            * `testDescription`: "Binary Branch Test"
            * `initialState`: { "branch_counter": 0 }
            * `nextPassageID`: "TC02_BINARY_BRANCH"
        * **Branch Test Inputs:**
            * `stepIDPrefix`: "diag_tc02"
            * `entry_point_id`: "TC02_BINARY_BRANCH"
            * `testCaseID`: "02"
            * `conditionVar`: "test_counter"
            * `conditionValue`: 3
            * `pathAPassageID`: "TC02_PATH_A"
            * `pathBPassageID`: "TC02_PATH_B"
        * **Path A/B Setup:** Both paths should be linear tests that set a branch_result variable to "A" or "B", then both converge on TC03_ENTRY.
        * **Technical Validation Goal:** System correctly evaluates condition and follows intended path.

    2. **Test Case:** Multi-way Branching
        * **Purpose:** Test multiple branching options with various conditions.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_BRANCH_TEST_MULTI`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc03"
            * `entry_point_id`: "TC03_ENTRY"
            * `testCaseID`: "03"
            * `testDescription`: "Multi-way Branch Test"
            * `initialState`: { "branch_counter": 0 }
            * `nextPassageID`: "TC03_MULTI_BRANCH"
        * **Multi-Branch Test Inputs:**
            * `stepIDPrefix`: "diag_tc03"
            * `entry_point_id`: "TC03_MULTI_BRANCH"
            * `testCaseID`: "03"
            * `conditionVar`: "test_counter"
            * `conditions`: [
                { "value": 1, "targetPassageID": "TC03_PATH_1" },
                { "value": 2, "targetPassageID": "TC03_PATH_2" },
                { "value": 3, "targetPassageID": "TC03_PATH_3" }
            ]
            * `defaultPassageID`: "TC03_DEFAULT_PATH"
        * **Technical Validation Goal:** System correctly routes to the appropriate path based on condition value.

    3. **Test Case:** Compound Condition
        * **Purpose:** Validate complex logical conditions using AND/OR/NOT.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_COMPOUND_CONDITION`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc04"
            * `entry_point_id`: "TC04_ENTRY"
            * `testCaseID`: "04"
            * `testDescription`: "Compound Condition Test"
            * `initialState`: { "condition_a": true, "condition_b": false, "condition_c": true }
            * `nextPassageID`: "TC04_COMPOUND"
        * **Compound Condition Inputs:**
            * `stepIDPrefix`: "diag_tc04"
            * `entry_point_id`: "TC04_COMPOUND"
            * `testCaseID`: "04"
            * `logicalOperator`: "AND"
            * `conditions`: [
                { "variable": "condition_a", "operator": "EQUALS", "value": true },
                { "variable": "condition_c", "operator": "EQUALS", "value": true }
            ]
            * `truePassageID`: "TC04_CONDITION_TRUE"
            * `falsePassageID`: "TC04_CONDITION_FALSE"
        * **Technical Validation Goal:** Complex logical condition evaluation works correctly.

**(Phase 3: Evidence System Testing)**

* **Associated Diagnostics:** `DIAGNOSTIC_EVIDENCE_REVEAL`, `DIAGNOSTIC_EVIDENCE_EXAMINATION` (Test Cases 05-06)
* **Testing Goal:** Validate the evidence system's functionality for revealing, tracking, and examining evidence items.
* **Test Delivery:** Create test passages that reveal evidence items, set their attributes, and verify proper examination functionality.

* **Test Cases & Phenotypes:**

    1. **Test Case:** Evidence Reveal
        * **Purpose:** Test the evidence reveal mechanism and state tracking.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_EVIDENCE_REVEAL`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc05"
            * `entry_point_id`: "TC05_ENTRY"
            * `testCaseID`: "05"
            * `testDescription`: "Evidence Reveal Test"
            * `initialState`: { "evidence_system_ready": true }
            * `nextPassageID`: "TC05_REVEAL"
        * **Evidence Reveal Inputs:**
            * `stepIDPrefix`: "diag_tc05"
            * `entry_point_id`: "TC05_REVEAL"
            * `testCaseID`: "05"
            * `evidenceID`: "test_evidence_01"
            * `nextPassageID`: "TC06_ENTRY"
        * **Technical Validation Goal:** Evidence is correctly revealed and tracked in the system state.

    2. **Test Case:** Evidence Examination
        * **Purpose:** Test evidence examination and attribute discovery.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_EVIDENCE_EXAMINATION`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc06"
            * `entry_point_id`: "TC06_ENTRY"
            * `testCaseID`: "06"
            * `testDescription`: "Evidence Examination Test"
            * `initialState`: { }
            * `nextPassageID`: "TC06_EXAMINE"
        * **Evidence Examination Inputs:**
            * `stepIDPrefix`: "diag_tc06"
            * `entry_point_id`: "TC06_EXAMINE"
            * `testCaseID`: "06"
            * `evidenceID`: "test_evidence_01"
            * `attributeData`: { 
                "evidence_attr_date": "2023-05-15", 
                "evidence_attr_type": "Document" 
            }
            * `successPassageID`: "TC06_EXAMINE_SUCCESS"
            * `failPassageID`: "TC06_EXAMINE_FAIL"
        * **Technical Validation Goal:** Evidence attributes are correctly set and examination state is properly tracked.

**(Phase 4: Advanced Flow Control)**

* **Associated Diagnostics:** `DIAGNOSTIC_MERGE_POINT`, `DIAGNOSTIC_LOOP_TEST`, `DIAGNOSTIC_APP_NAVIGATION` (Test Cases 07-09)
* **Testing Goal:** Validate advanced flow control mechanisms including path convergence, cyclical progression, and application-level navigation.
* **Test Delivery:** Create test passages that merge multiple paths, implement loops with iteration tracking, and navigate between application interfaces.

* **Test Cases & Phenotypes:**

    1. **Test Case:** Path Merge
        * **Purpose:** Test convergence of multiple paths into a single outcome.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_MERGE_POINT`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc07"
            * `entry_point_id`: "TC07_ENTRY"
            * `testCaseID`: "07"
            * `testDescription`: "Path Merge Test"
            * `initialState`: { "merge_ready": true }
            * `nextPassageID`: "TC07_MERGE"
        * **Merge Point Inputs:**
            * `stepIDPrefix`: "diag_tc07"
            * `entry_point_id`: "TC07_MERGE"
            * `testCaseID`: "07"
            * `trackOriginPath`: true
            * `nextPassageID`: "TC08_ENTRY"
        * **Technical Validation Goal:** System correctly handles merging paths and tracks arrival path if configured.

    2. **Test Case:** Loop Iteration
        * **Purpose:** Test cyclical progression with iteration counter and exit condition.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_LOOP_TEST`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc08"
            * `entry_point_id`: "TC08_ENTRY"
            * `testCaseID`: "08"
            * `testDescription`: "Loop Test"
            * `initialState`: { "loop_counter": 0 }
            * `nextPassageID`: "TC08_LOOP"
        * **Loop Test Inputs:**
            * `stepIDPrefix`: "diag_tc08"
            * `entry_point_id`: "TC08_LOOP"
            * `testCaseID`: "08"
            * `loopVarName`: "loop_counter"
            * `maxIterations`: 3
            * `exitPassageID`: "TC09_ENTRY"
        * **Technical Validation Goal:** Loop iteration works correctly and terminates at specified threshold.

    3. **Test Case:** Application Navigation
        * **Purpose:** Test navigation between different application interfaces.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_APP_NAVIGATION`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc09"
            * `entry_point_id`: "TC09_ENTRY"
            * `testCaseID`: "09"
            * `testDescription`: "App Navigation Test"
            * `initialState`: { }
            * `nextPassageID`: "TC09_NAV"
        * **App Navigation Inputs:**
            * `stepIDPrefix`: "diag_tc09"
            * `entry_point_id`: "TC09_NAV"
            * `testCaseID`: "09"
            * `targetApp`: "EVIDENCE"
            * `returnPassageID`: "TC10_ENTRY"
        * **Technical Validation Goal:** System correctly handles navigation between different application interfaces.

**(Phase 5: Transformation Testing)**

* **Associated Diagnostics:** `DIAGNOSTIC_SLPN_CONVERSION_TEST`, `DIAGNOSTIC_JSON_GENERATION_TEST` (Test Cases 10-11)
* **Testing Goal:** Validate conversion between journey format, SLPN notation, and final JSON implementation.
* **Test Delivery:** Create test passages that validate the transformation of journey elements to SLPN and SLPN to JSON.

* **Test Cases & Phenotypes:**

    1. **Test Case:** Journey to SLPN Conversion
        * **Purpose:** Test conversion from journey format to SLPN notation.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_SLPN_CONVERSION_TEST`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc10"
            * `entry_point_id`: "TC10_ENTRY"
            * `testCaseID`: "10"
            * `testDescription`: "SLPN Conversion Test"
            * `initialState`: { }
            * `nextPassageID`: "TC10_CONVERSION"
        * **SLPN Conversion Inputs:**
            * `stepIDPrefix`: "diag_tc10"
            * `entry_point_id`: "TC10_CONVERSION"
            * `testCaseID`: "10"
            * `journeyFormat`: {
                "passage_type": "linear",
                "text": "Test passage",
                "next": "next_passage_id"
            }
            * `expectedSLPN`: 'BOT:lin="Test passage";ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=next_passage_id;'
            * `nextPassageID`: "TC11_ENTRY"
        * **Technical Validation Goal:** Journey format correctly converts to SLPN notation.

    2. **Test Case:** SLPN to JSON Conversion
        * **Purpose:** Test SLPN to JSON transformation.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_JSON_GENERATION_TEST`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc11"
            * `entry_point_id`: "TC11_ENTRY"
            * `testCaseID`: "11"
            * `testDescription`: "JSON Generation Test"
            * `initialState`: { }
            * `nextPassageID`: "TC11_JSON_GEN"
        * **JSON Generation Inputs:**
            * `stepIDPrefix`: "diag_tc11"
            * `entry_point_id`: "TC11_JSON_GEN"
            * `testCaseID`: "11"
            * `slpnInput`: 'BOT:lin="Test passage";ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=next_passage_id;'
            * `expectedJSON`: {
                "type": "bot",
                "line": "Test passage",
                "actions": [
                    {
                        "type": "move",
                        "amount": {
                            "type": "passage"
                        },
                        "target": "next_passage_id"
                    }
                ]
            }
            * `nextPassageID`: "TC12_ENTRY"
        * **Technical Validation Goal:** SLPN notation correctly converts to JSON structure.

**(Phase 6: Completion & Validation)**

* **Associated Diagnostics:** `DIAGNOSTIC_EXIT_POINT` (Test Case 12)
* **Testing Goal:** Validate proper system termination and test outcome recording.
* **Test Delivery:** Create test passages that properly record test results and signal test completion.

* **Test Cases & Phenotypes:**

    1. **Test Case:** Test Completion
        * **Purpose:** Validate proper test termination and result recording.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT` followed by `DIAGNOSTIC_EXIT_POINT`
        * **Entry Point Inputs:**
            * `stepIDPrefix`: "diag_tc12"
            * `entry_point_id`: "TC12_ENTRY"
            * `testCaseID`: "12"
            * `testDescription`: "Test Completion"
            * `initialState`: { "test_summary_ready": true }
            * `nextPassageID`: "TC12_EXIT"
        * **Exit Point Inputs:**
            * `stepIDPrefix`: "diag_tc12"
            * `entry_point_id`: "TC12_EXIT"
            * `testCaseID`: "12"
            * `testOutcome`: "success"
            * `resultData`: {
                "total_passages": 24,
                "branches_verified": true,
                "evidence_verified": true,
                "conversions_verified": true
            }
        * **Technical Validation Goal:** System properly records test results and terminates the test sequence.

**(Phase 7: Comprehensive Test Sequence)**

* **Associated Diagnostics:** `DIAGNOSTIC_TEST_SEQUENCE` (Master Test)
* **Testing Goal:** Validate end-to-end integration of all diagnostic phenotypes in a single comprehensive test sequence.
* **Test Delivery:** Use the meta-phenotype to generate a complete test sequence that integrates all individual test cases.

* **Test Case & Phenotype:**

    1. **Test Case:** Complete System Test
        * **Purpose:** Test complete end-to-end system functionality.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_TEST_SEQUENCE`
        * **Inputs:**
            * `stepIDPrefix`: "diag_master"
            * `rootID`: "MASTER_TEST_ROOT"
            * `testCaseID`: "MASTER"
            * `sequenceConfig`: [ 
                // A complete array containing configurations for all 12 test cases
                // formatted for the DIAGNOSTIC_TEST_SEQUENCE phenotype
                {
                    "type": "ENTRY_POINT",
                    "description": "Master Test Sequence",
                    "initialState": { "master_test": true }
                },
                // Additional test steps would follow here
                {
                    "type": "EXIT_POINT",
                    "testOutcome": "success",
                    "resultData": { "comprehensive_test": "complete" }
                }
            ]
        * **Technical Validation Goal:** System can execute a complete test sequence covering all diagnostic phenotypes.

## Implementation Approach

1. **Iterative Testing**: Begin with simple test cases (linear progression, basic branching) before advancing to more complex scenarios.
2. **State Verification**: Each test case should include verification steps to validate that the system state has been correctly modified.
3. **Edge Case Coverage**: Test with both common and boundary conditions (empty values, maximum iterations, etc.).
4. **Isolation and Integration**: First test each phenotype in isolation, then test interactions between components.
5. **Automated Validation**: Incorporate `VALIDATE` statements within each diagnostic phenotype to confirm proper functionality without manual verification.

## Expected Outcomes

1. **Execution Tracing**: Each test case generates execution logs that confirm proper passage flow and state changes.
2. **Test Completion Flags**: Status flags in the system state record completion and outcome for each test case.
3. **Validation Reports**: Consolidated reports of validation results, identifying any failing tests or components.
4. **Performance Metrics**: Timing data for various operations to identify potential bottlenecks.

By executing this Diagnostic Journey, we can systematically validate all components of the story creation and delivery pipeline, ensuring robust functionality and reliable performance. 