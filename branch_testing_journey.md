# Branching Options Diagnostic Journey

## Testing Overview

**COMPREHENSIVE BRANCH OPTIONS TEST SEQUENCE: VALIDATING ALL BRANCH TYPES AND PARAMETERS**

*This diagnostic journey defines a focused test sequence that validates all branching options and parameters available in the casemaker system. Each test case isolates specific branching functionality with specific attention to branch option parameters, presentation types, and integration methods.*

*The primary focus is technical validation of branching mechanics, not narrative quality. Test cases use minimal content focused on structure verification rather than telling a compelling story.*

**Goal:** Provide a systematic verification mechanism for all branch types, parameters, and integration points to ensure reliable branching functionality across the entire system.

**Note:** This journey relies on pre-defined test evidence items (`test_evidence_01`, `test_evidence_02`, etc.) existing in the system. Several test passages explicitly reference and manipulate these items to verify proper functionality.

**(Phase 1: Basic Branch Types)**

* **Associated Diagnostics:** `DIAGNOSTIC_ENTRY_POINT`, `DIAGNOSTIC_BRANCH_TEST_BINARY`, `DIAGNOSTIC_BRANCH_TEST_MULTI`
* **Testing Goal:** Validate the core branch types - binary, multi-way, and condition-based branching
* **Test Delivery:** Create entry points and branching tests for each branch type

* **Test Cases & Phenotypes:**

    1. **Test Case:** System Initialization
        * **Purpose:** Initialize the test environment with required state variables.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc01"
            * `entry_point_id`: "TC01_ENTRY"
            * `testCaseID`: "01"
            * `testDescription`: "Branch Types Test Initialization"
            * `initialState`: { 
                "branch_counter": 0, 
                "test_var_a": 1, 
                "test_var_b": 2, 
                "test_var_c": 3,
                "test_flag": true,
                "seen_evidence": false
             }
            * `nextPassageID`: "TC01_BINARY_BRANCH"
        * **Technical Validation Goal:** System correctly initializes state variables for branch testing.

    2. **Test Case:** Binary Branch (if/else)
        * **Purpose:** Test basic binary branching based on a condition.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_BRANCH_TEST_BINARY`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc01"
            * `entry_point_id`: "TC01_BINARY_BRANCH"
            * `testCaseID`: "01"
            * `conditionVar`: "test_flag"
            * `conditionValue`: true
            * `pathAPassageID`: "TC01_PATH_A"
            * `pathBPassageID`: "TC01_PATH_B"
        * **Technical Validation Goal:** System correctly evaluates boolean condition and follows intended path.

    3. **Test Case:** Path A Result
        * **Purpose:** Record result from taking Path A in binary branch.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc01"
            * `entry_point_id`: "TC01_PATH_A"
            * `testCaseID`: "01"
            * `stepNumber`: 1
            * `totalSteps`: 1
            * `stateChanges`: { "binary_branch_result": "A" }
            * `nextPassageID`: "TC02_ENTRY"
        * **Technical Validation Goal:** System correctly records the branch path taken.

    4. **Test Case:** Path B Result
        * **Purpose:** Record result from taking Path B in binary branch.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc01"
            * `entry_point_id`: "TC01_PATH_B"
            * `testCaseID`: "01"
            * `stepNumber`: 1
            * `totalSteps`: 1
            * `stateChanges`: { "binary_branch_result": "B" }
            * `nextPassageID`: "TC02_ENTRY"
        * **Technical Validation Goal:** System correctly records the branch path taken.

    5. **Test Case:** Multi-way Branch Entry
        * **Purpose:** Setup for testing multi-way branching.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc02"
            * `entry_point_id`: "TC02_ENTRY"
            * `testCaseID`: "02"
            * `testDescription`: "Multi-way Branch Test"
            * `initialState`: { "branch_counter": 0 }
            * `nextPassageID`: "TC02_MULTI_BRANCH"
        * **Technical Validation Goal:** System is prepared for multi-way branch test.

    6. **Test Case:** Multi-way Branching (switch/case)
        * **Purpose:** Test multi-way branching based on different values.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_BRANCH_TEST_MULTI`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc02"
            * `entry_point_id`: "TC02_MULTI_BRANCH"
            * `testCaseID`: "02"
            * `conditionVar`: "test_var_a"
            * `conditions`: [
                { "value": 1, "targetPassageID": "TC02_PATH_1" },
                { "value": 2, "targetPassageID": "TC02_PATH_2" },
                { "value": 3, "targetPassageID": "TC02_PATH_3" }
            ]
            * `defaultPassageID`: "TC02_DEFAULT_PATH"
        * **Technical Validation Goal:** System correctly routes to the appropriate path based on variable value.

    7. **Test Case:** Multi-way Result Paths
        * **Purpose:** Record results from each path in the multi-way branch.
        * **Diagnostic Phenotype:** Various `DIAGNOSTIC_LINEAR_TEST` passages
        * **Path Results Configuration:** Each path sets a unique result identifier and proceeds to TC03_ENTRY
        * **Technical Validation Goal:** System correctly processes each branch option.

**(Phase 2: Branch Presentation Types)**

* **Associated Diagnostics:** Custom branch presentation tests
* **Testing Goal:** Validate the different branch presentation options (option-list, block-panel, etc.)
* **Test Delivery:** Create test passages that demonstrate each presentation type.

* **Test Cases & Phenotypes:**

    8. **Test Case:** Branch Presentation Setup
        * **Purpose:** Initialize testing of branch presentation types.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc03"
            * `entry_point_id`: "TC03_ENTRY"
            * `testCaseID`: "03"
            * `testDescription`: "Branch Presentation Types Test"
            * `initialState`: { "presentation_test_ready": true }
            * `nextPassageID`: "TC03_OPTION_LIST"
        * **Technical Validation Goal:** System is prepared for branch presentation tests.

    9. **Test Case:** Option List Presentation
        * **Purpose:** Test the "option-list" branch presentation.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing option-list branch presentation";
        brn=BRN:bds="Option List Presentation";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="Option 1";ods="First option description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC03_CARD_PANEL;
        ops=BOP:onm="Option 2";ods="Second option description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC03_CARD_PANEL;
        ```
        * **Technical Validation Goal:** System correctly displays options in list format.

    10. **Test Case:** Card Panel Presentation
        * **Purpose:** Test the "card-panel" branch presentation.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing card-panel branch presentation";
        brn=BRN:bds="Card Panel Presentation";brp=once;bpr=card-panel;bit=blocking;
        ops=BOP:onm="Card 1";ods="First card description";img="card1_image";imd="Card 1 image description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC03_BLOCK_PANEL;
        ops=BOP:onm="Card 2";ods="Second card description";img="card2_image";imd="Card 2 image description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC03_BLOCK_PANEL;
        ```
        * **Technical Validation Goal:** System correctly displays options as cards with images.

    11. **Test Case:** Block Panel Presentation
        * **Purpose:** Test the "block-panel" branch presentation.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing block-panel branch presentation";
        brn=BRN:bds="Block Panel Presentation";brp=once;bpr=block-panel;bit=blocking;
        ops=BOP:onm="Block 1";ods="First block description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC04_ENTRY;
        ops=BOP:onm="Block 2";ods="Second block description";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC04_ENTRY;
        ```
        * **Technical Validation Goal:** System correctly displays options as block panels.

**(Phase 3: Branch Integration Types)**

* **Associated Diagnostics:** Custom branch integration tests
* **Testing Goal:** Validate the different branch integration types (blocking, inline, ada)
* **Test Delivery:** Create test passages that demonstrate each integration type.

* **Test Cases & Phenotypes:**

    12. **Test Case:** Branch Integration Setup
        * **Purpose:** Initialize testing of branch integration types.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc04"
            * `entry_point_id`: "TC04_ENTRY"
            * `testCaseID`: "04"
            * `testDescription`: "Branch Integration Types Test"
            * `initialState`: { "integration_test_ready": true }
            * `nextPassageID`: "TC04_BLOCKING"
        * **Technical Validation Goal:** System is prepared for branch integration tests.

    13. **Test Case:** Blocking Integration
        * **Purpose:** Test the "blocking" integration type.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing blocking integration type";
        brn=BRN:bds="Blocking Integration";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="Option A";ods="Continue to next test";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC04_INLINE;
        ```
        * **Technical Validation Goal:** System correctly displays branch that blocks progression until selected.

    14. **Test Case:** Inline Integration
        * **Purpose:** Test the "inline" integration type.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing inline integration type";
        brn=BRN:bds="Inline Integration";brp=once;bpr=option-list;bit=inline;
        ops=BOP:onm="Option A";ods="Continue to next test";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC04_ADA;
        ```
        * **Technical Validation Goal:** System correctly displays branch inline with content.

    15. **Test Case:** ADA Integration
        * **Purpose:** Test the "ada" integration type.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing ada integration type";
        brn=BRN:bds="ADA Integration";brp=once;bpr=option-list;bit=ada;
        ops=BOP:onm="Option A";ods="Continue to next test";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_ENTRY;
        ```
        * **Technical Validation Goal:** System correctly integrates branch within ADA message.

**(Phase 4: Branch Option Parameters)**

* **Associated Diagnostics:** Custom branch option parameter tests
* **Testing Goal:** Validate the additional branch option parameters (imageAlias, imageDescription, checkAspect)
* **Test Delivery:** Create test passages that demonstrate various branch option parameters.

* **Test Cases & Phenotypes:**

    16. **Test Case:** Branch Option Parameters Setup
        * **Purpose:** Initialize testing of branch option parameters.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc05"
            * `entry_point_id`: "TC05_ENTRY"
            * `testCaseID`: "05"
            * `testDescription`: "Branch Option Parameters Test"
            * `initialState`: { 
                "parameters_test_ready": true,
                "evidence_examined": false,
                "footage_analyzed": false 
             }
            * `nextPassageID`: "TC05_IMAGE_TEST"
        * **Technical Validation Goal:** System is prepared for branch option parameter tests.

    17. **Test Case:** Image Alias and Description
        * **Purpose:** Test branch options with image alias and description.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing branch options with image alias and description";
        brn=BRN:bds="Image Parameters";brp=once;bpr=card-panel;bit=blocking;
        ops=BOP:onm="Option with Image";ods="This option has an image";img="test_image_01";imd="This is a test image showing a document";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_ASPECT_CHECK;
        ops=BOP:onm="Option without Image";ods="This option has no image";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_ASPECT_CHECK;
        ```
        * **Technical Validation Goal:** System correctly displays branch options with and without images.

    18. **Test Case:** Aspect Check Parameter (Conditional Options)
        * **Purpose:** Test branch options with aspect check conditions.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing branch options with aspect check conditions";
        brn=BRN:bds="Conditional Options";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="Always Available";ods="This option is always available";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_NEXT;
        ops=BOP:onm="Evidence Examined";ods="Only if evidence examined";chk=CHK:asp=evidence_examined;cty=eq;vlu=true;
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_NEXT;
        ops=BOP:onm="Footage Analyzed";ods="Only if footage analyzed";chk=CHK:asp=footage_analyzed;cty=eq;vlu=true;
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC05_NEXT;
        ```
        * **Technical Validation Goal:** System correctly displays or hides branch options based on conditions.

    19. **Test Case:** Conditional Options Setup
        * **Purpose:** Set up state for testing conditional options.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_LINEAR_TEST`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc05"
            * `entry_point_id`: "TC05_NEXT"
            * `testCaseID`: "05"
            * `stepNumber`: 1
            * `totalSteps`: 1
            * `stateChanges`: { "evidence_examined": true }
            * `nextPassageID`: "TC05_ASPECT_CHECK_RETEST"
        * **Technical Validation Goal:** System correctly updates state to enable conditional options.

    20. **Test Case:** Aspect Check Retest
        * **Purpose:** Test branch options with modified aspect conditions.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Re-testing conditional options after state change";
        brn=BRN:bds="Updated Conditional Options";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="Always Available";ods="This option is always available";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_ENTRY;
        ops=BOP:onm="Evidence Examined (Now Available)";ods="Should be available now";chk=CHK:asp=evidence_examined;cty=eq;vlu=true;
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_ENTRY;
        ops=BOP:onm="Footage Analyzed (Still Hidden)";ods="Should remain hidden";chk=CHK:asp=footage_analyzed;cty=eq;vlu=true;
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_ENTRY;
        ```
        * **Technical Validation Goal:** System correctly updates available options after state changes.

**(Phase 5: Advanced Branch Parameters)**

* **Associated Diagnostics:** Custom advanced branch parameter tests
* **Testing Goal:** Validate the additional branch parameters (replay ability, compound conditions)
* **Test Delivery:** Create test passages that demonstrate advanced branch configurations.

* **Test Cases & Phenotypes:**

    21. **Test Case:** Advanced Parameters Setup
        * **Purpose:** Initialize testing of advanced branch parameters.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc06"
            * `entry_point_id`: "TC06_ENTRY"
            * `testCaseID`: "06"
            * `testDescription`: "Advanced Branch Parameters Test"
            * `initialState`: { 
                "advanced_test_ready": true,
                "condition_1": true,
                "condition_2": false
             }
            * `nextPassageID`: "TC06_REPLAY_TEST"
        * **Technical Validation Goal:** System is prepared for advanced branch parameter tests.

    22. **Test Case:** Replay Ability Test
        * **Purpose:** Test different branch replay types (once, re-playable, re-executable).
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing branch replay ability parameters";
        brn=BRN:bds="Once Only Branch";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="This can only be selected once";
        UAS:asp=selected_once;uty=SET;val=true;
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_REPLAY_TEST_SELF;

        PSG:uid=TC06_REPLAY_TEST_SELF;nam="Replay Test - Re-Playable";
        BOT:lin="Testing re-playable branch";
        brn=BRN:bds="Re-Playable Branch";brp=re-playable;bpr=option-list;bit=blocking;
        ops=BOP:onm="Return to this branch";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_REPLAY_TEST_SELF;
        ops=BOP:onm="Proceed to next test";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC06_COMPOUND_TEST;
        ```
        * **Technical Validation Goal:** System correctly handles different replay ability settings.

    23. **Test Case:** Compound Condition Test
        * **Purpose:** Test branch options with compound conditions (AND/OR/NOT).
        * **Diagnostic Phenotype:** `DIAGNOSTIC_COMPOUND_CONDITION`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc06"
            * `entry_point_id`: "TC06_COMPOUND_TEST"
            * `testCaseID`: "06"
            * `logicalOperator`: "AND"
            * `conditions`: [
                { "variable": "condition_1", "operator": "EQUALS", "value": true },
                { "variable": "condition_2", "operator": "EQUALS", "value": true }
            ]
            * `truePassageID`: "TC06_CONDITION_TRUE"
            * `falsePassageID`: "TC06_CONDITION_FALSE"
        * **Technical Validation Goal:** Compound logical condition evaluation works correctly.

    24. **Test Case:** Compound Condition Results
        * **Purpose:** Record results from compound condition paths.
        * **Custom Linear Test Implementations:**
        ```
        BOT:lin="Compound AND condition evaluated to TRUE";
        SET:var=compound_result;val="both_true";
        ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC07_ENTRY;

        PSG:uid=TC06_CONDITION_FALSE;nam="Compound AND - FALSE Result";
        BOT:lin="Compound AND condition evaluated to FALSE";
        SET:var=compound_result;val="not_both_true";
        ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC07_ENTRY;
        ```
        * **Technical Validation Goal:** System correctly processes and records compound condition results.

**(Phase 6: Branch Action Sequences)**

* **Associated Diagnostics:** Custom branch action sequence tests
* **Testing Goal:** Validate branch options with multiple sequential actions
* **Test Delivery:** Create test passages that demonstrate multi-action branch options.

* **Test Cases & Phenotypes:**

    25. **Test Case:** Action Sequence Setup
        * **Purpose:** Initialize testing of branch action sequences.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc07"
            * `entry_point_id`: "TC07_ENTRY"
            * `testCaseID`: "07"
            * `testDescription`: "Branch Action Sequence Test"
            * `initialState`: { "sequence_test_ready": true }
            * `nextPassageID`: "TC07_MULTI_ACTION"
        * **Technical Validation Goal:** System is prepared for branch action sequence tests.

    26. **Test Case:** Multi-Action Branch Options
        * **Purpose:** Test branch options with multiple sequential actions.
        * **Custom Branch Test Implementation:**
        ```
        BOT:lin="Testing branch options with multiple sequential actions";
        brn=BRN:bds="Multi-Action Options";brp=once;bpr=option-list;bit=blocking;
        ops=BOP:onm="Set State & Move";
        act=UAS:asp=action_1_complete;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC07_RESULT;
        ops=BOP:onm="Set Multiple States";
        act=UAS:asp=action_2a_complete;uty=SET;val=true|UAS:asp=action_2b_complete;uty=SET;val=true|ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC07_RESULT;
        ```
        * **Technical Validation Goal:** System correctly processes multiple sequential actions in branch options.

    27. **Test Case:** Action Sequence Result
        * **Purpose:** Verify results from multi-action branch options.
        * **Custom Linear Test Implementation:**
        ```
        BOT:lin="Checking results of multi-action branch options";
        brn=BRN:bds="Action Results";brp=once;bpr=auto;bit=blocking;
        ops=BOP:onm="Action 1 Complete";chk=CHK:asp=action_1_complete;cty=eq;vlu=true;
        SET:var=sequence_result;val="action_1";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC08_ENTRY;
        ops=BOP:onm="Action 2 Complete";chk=CHK:asp=action_2a_complete;cty=eq;vlu=true;
        SET:var=sequence_result;val="action_2";
        act=ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=TC08_ENTRY;
        ```
        * **Technical Validation Goal:** System correctly processes and verifies multi-action results.

**(Phase 7: Exit and Summary)**

* **Associated Diagnostics:** `DIAGNOSTIC_EXIT_POINT`
* **Testing Goal:** Validate proper test completion and result recording
* **Test Delivery:** Create exit passage that records test results.

* **Test Cases & Phenotypes:**

    28. **Test Case:** Branch Testing Summary
        * **Purpose:** Initialize final test summary.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_ENTRY_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc08"
            * `entry_point_id`: "TC08_ENTRY"
            * `testCaseID`: "08"
            * `testDescription`: "Branch Testing Summary"
            * `initialState`: { "summary_ready": true }
            * `nextPassageID`: "TC08_EXIT"
        * **Technical Validation Goal:** System is prepared for test completion.

    29. **Test Case:** Test Completion
        * **Purpose:** Validate proper test termination and result recording.
        * **Diagnostic Phenotype:** `DIAGNOSTIC_EXIT_POINT`
        * **Inputs:**
            * `stepIDPrefix`: "branch_tc08"
            * `entry_point_id`: "TC08_EXIT"
            * `testCaseID`: "08"
            * `testOutcome`: "success"
            * `resultData`: {
                "total_branch_tests": 7,
                "binary_verified": true,
                "multi_verified": true,
                "presentation_verified": true,
                "integration_verified": true,
                "parameters_verified": true,
                "advanced_verified": true,
                "action_sequence_verified": true
            }
        * **Technical Validation Goal:** System properly records branch test results and terminates the test sequence.

## Implementation Approach

1. **Isolated Testing**: Each branch type and parameter is tested independently to verify correct behavior.
2. **Parameter Verification**: All branch and branch option parameters are explicitly tested.
3. **State Changes**: Tests include manipulation of state variables to verify conditional branching.
4. **Visual Verification**: Certain tests require visual inspection to verify presentation types.

## Expected Outcomes

1. **Option Visibility**: Conditional branch options appear/disappear based on state variables.
2. **Presentation Types**: Different branch presentations (option-list, card-panel, block-panel) display correctly.
3. **Integration Types**: Each integration type (blocking, inline, ada) functions as expected.
4. **Image Support**: Branch options with image alias and description display correctly.
5. **Compound Conditions**: Complex logical conditions evaluate correctly.
6. **Action Sequences**: Multiple sequential actions execute in the proper order.

By executing this Branch Testing Journey, we can systematically validate all branch types, parameters, and behaviors across the system. 