# Diagnostic Phenotype Dictionary

This dictionary provides a comprehensive reference for all diagnostic phenotypes used to test the complete story creation pipeline from conceptual journey through SLPN notation to JSON implementation.

## Base Test Components

### Diagnostic_Character_Definition
A minimal character structure used to test character data handling and referencing.
```
character_id: "TC-01"
name: "Test Character 01"
role: "Test Subject"
status: "Active"
```

### Diagnostic_Location_Definition
A minimal location structure used to test location referencing and property validation.
```
location_id: "TL-01"
name: "Test Location 01"
description: "A simple test environment"
access_level: "Unrestricted"
```

### Diagnostic_Object_Definition
A minimal object structure used to test object handling and interaction capabilities.
```
object_id: "TO-01"
name: "Test Object 01"
type: "Evidence"
description: "A simple test object with examinable properties"
location: "TL-01"
```

### Diagnostic_Relationship_Definition
A minimal relationship structure used to test character connections and relationship data flow.
```
relationship_id: "TR-01"
character_a: "TC-01"
character_b: "TC-02"
type: "Test_Connection"
status: "Active"
```

## Test Propositions

### Diagnostic_Linear_Proposition
A simple sequential flow between points A and B used to test basic progression.
```
proposition_id: "TLP-01"
start_point: "passage_a"
end_point: "passage_b"
condition: "None"
```

### Diagnostic_Branch_Proposition
A conditional path fork used to test branching capabilities and condition evaluation.
```
proposition_id: "TBP-01"
start_point: "branch_origin"
conditions: [
  {
    "condition": "test_counter = 1",
    "destination": "path_a"
  },
  {
    "condition": "test_counter = 2",
    "destination": "path_b"
  }
]
default_destination: "fallback_path"
```

### Diagnostic_Merge_Proposition
A convergence point for multiple paths used to test path recombination.
```
proposition_id: "TMP-01"
entry_points: ["path_a", "path_b", "path_c"]
merge_point: "common_destination"
track_origin: true
```

### Diagnostic_Loop_Proposition
A cyclical pathway used to test iteration handling and exit conditions.
```
proposition_id: "TLOP-01"
entry_point: "loop_start"
iteration_variable: "loop_counter"
exit_condition: "loop_counter >= 3"
exit_point: "loop_exit"
```

## Test Evidence Elements

### Diagnostic_Evidence_Item
A basic evidence object used to test evidence creation, reveal, and examination.
```
evidence_id: "TE-01"
name: "Test Evidence 01"
type: "Document"
content: "This is test evidence content."
examinable_attributes: ["date", "sender", "recipient"]
```

### Diagnostic_Evidence_Collection
A grouped set of evidence items used to test collection handling.
```
collection_id: "TEC-01"
name: "Test Evidence Collection"
items: ["TE-01", "TE-02", "TE-03"]
relationship: "Related test items"
```

### Diagnostic_Evidence_Transformation
An evidence item that changes state based on player actions, used to test state transitions.
```
evidence_id: "TET-01"
name: "Transforming Test Evidence"
initial_state: "Encrypted"
transformation_trigger: "Decryption tool applied"
final_state: "Decrypted"
revealed_content: "This is previously hidden test content."
```

## Test Passages

### DIAGNOSTIC_ENTRY_POINT
An initialization passage that sets up starting conditions and variables for a test sequence.
```
BOT:lin="Diagnostic Test Case 01: System Initialization";
SET:evt=TC01_INITIALIZED;val=true;
SET:var=test_counter;val=0;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_linear_test;
```

### DIAGNOSTIC_LINEAR_TEST
A straight-line passage that tests simple progression and state modification.
```
BOT:lin="Testing linear progression (Step 1 of 3)";
SET:var=test_counter;val=1;
SET:evt=TC01_STEP1_COMPLETE;val=true;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_linear_test_step2;
```

### DIAGNOSTIC_BRANCH_TEST_BINARY
A two-way conditional passage that tests simple branching logic.
```
BOT:lin="Testing binary branching condition";
IF:cnd=CNT:var=test_counter;op=EQUALS;val=2;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_a;
ELSE:
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_b;
```

### DIAGNOSTIC_BRANCH_TEST_MULTI
A multi-way conditional passage that tests complex branching logic with multiple conditions.
```
BOT:lin="Testing multi-way branching conditions";
IF:cnd=CNT:var=test_counter;op=EQUALS;val=3;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_a;
ELIF:cnd=CNT:var=test_counter;op=EQUALS;val=2;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_b;
ELIF:cnd=CNT:var=test_counter;op=EQUALS;val=1;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_c;
ELSE:
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_fallback;
```

### DIAGNOSTIC_EVIDENCE_REVEAL
A passage that tests the evidence reveal mechanism and state tracking.
```
BOT:lin="Testing evidence reveal functionality";
ACT:aty=REVEAL;aet=test_evidence_01;
SET:evt=EVIDENCE_01_REVEALED;val=true;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### DIAGNOSTIC_EVIDENCE_EXAMINATION
A passage that tests evidence examination and attribute discovery.
```
BOT:lin="Testing evidence examination functionality";
SET:evt=EVIDENCE_01_EXAMINED;val=true;
SET:var=evidence_attribute;val="test_value";
IF:cnd=CNT:evt=EVIDENCE_01_EXAMINED;op=EQUALS;val=true;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_evidence_reaction;
ELSE:
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_evidence_fallback;
```

### DIAGNOSTIC_MERGE_POINT
A passage that tests the convergence of multiple paths into a single outcome.
```
BOT:lin="Testing path merge functionality (arrival from multiple sources)";
SET:var=arrival_path;val="{{$source_path}}";
SET:evt=MERGE_POINT_REACHED;val=true;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_post_merge_test;
```

### DIAGNOSTIC_LOOP_TEST
A passage that tests cyclical progression with iteration counting and exit condition.
```
BOT:lin="Testing loop functionality (iteration {{$loop_counter}})";
SET:var=loop_counter;val={{$loop_counter + 1}};
IF:cnd=CNT:var=loop_counter;op=GREATER_OR_EQUAL;val=3;
  SET:evt=LOOP_TEST_COMPLETE;val=true;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_loop_exit;
ELSE:
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_loop_test;
```

### DIAGNOSTIC_APP_NAVIGATION
A passage that tests navigation between different application interfaces.
```
BOT:lin="Testing application navigation";
SET:evt=NAV_TO_EVIDENCE_APP;val=true;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### DIAGNOSTIC_EXIT_POINT
A passage that tests proper system termination and outcome recording.
```
BOT:lin="Test case complete. Validating final state.";
SET:evt=TC01_COMPLETE;val=true;
SET:var=test_outcome;val="success";
ACT:aty=END;amt=AMT:typ=TEST;tgt=tc01_results;
```

## Test Conditions

### Diagnostic_Action_Trigger
A condition that activates based on player action, used to test event handling.
```
trigger_id: "TAT-01"
action_type: "Examine"
target: "TE-01"
resulting_event: "EVIDENCE_01_EXAMINED"
```

### Diagnostic_State_Condition
A condition based on system state, used to test state-dependent branching.
```
condition_id: "TSC-01"
variable: "test_counter"
operator: "equals"
value: 2
evaluation: "test_counter equals 2"
```

### Diagnostic_Compound_Condition
A multi-factor condition using logical operators, used to test complex conditional logic.
```
condition_id: "TCC-01"
logical_operation: "AND"
subconditions: [
  {
    "variable": "test_counter",
    "operator": "greater_than",
    "value": 1
  },
  {
    "variable": "evidence_01_revealed",
    "operator": "equals",
    "value": true
  }
]
evaluation: "(test_counter > 1) AND (evidence_01_revealed = true)"
```

## Test System Integration

### Diagnostic_SLPN_Conversion
A test case pairing journey elements with expected SLPN output to verify notation generation.
```
test_id: "TSLPN-01"
journey_input: {
  "passage_type": "linear",
  "text": "Test passage",
  "next": "next_passage_id"
}
expected_slpn: 'BOT:lin="Test passage";ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=next_passage_id;'
```

### Diagnostic_JSON_Generation
A test case pairing SLPN notation with expected JSON structure to verify transformation.
```
test_id: "TJSON-01"
slpn_input: 'BOT:lin="Test passage";ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=next_passage_id;'
expected_json: {
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
```

### Diagnostic_Full_Pipeline
A comprehensive test case that verifies the entire workflow from concept to implementation.
```
test_id: "TFP-01"
journey_elements: [
  {
    "type": "entry_point",
    "text": "System initialization",
    "initial_state": {
      "test_counter": 0
    },
    "next": "linear_test"
  },
  {
    "type": "linear",
    "text": "Linear progression test",
    "state_changes": {
      "test_counter": 1
    },
    "next": "branch_test"
  },
  {
    "type": "branch",
    "text": "Branch test",
    "conditions": [
      {
        "condition": "test_counter = 1",
        "destination": "evidence_test"
      }
    ],
    "default": "exit_point"
  }
]
expected_output: [
  {
    "passage_id": "entry_point",
    "slpn": "BOT:lin=\"System initialization\";SET:var=test_counter;val=0;ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=linear_test;"
  },
  {
    "passage_id": "linear_test",
    "slpn": "BOT:lin=\"Linear progression test\";SET:var=test_counter;val=1;ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=branch_test;"
  },
  {
    "passage_id": "branch_test",
    "slpn": "BOT:lin=\"Branch test\";IF:cnd=CNT:var=test_counter;op=EQUALS;val=1;ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=evidence_test;ELSE:ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=exit_point;"
  }
]
``` 