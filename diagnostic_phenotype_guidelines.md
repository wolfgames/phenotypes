# SLPN Diagnostic Phenotypes Guide: Testing System Components and Integration

## Introduction

This guide explains the Diagnostic Testing Phenotypes in SLPN (Story Logic Passage Notation) designed specifically to validate the complete pipeline from conceptual journey to SLPN notation to JSON implementation. Unlike narrative or gameplay phenotypes which focus on player experience, these diagnostic phenotypes serve as technical test cases to verify system functionality, data flow, and integration points.

## Core Concepts

Diagnostic Phenotypes are based on these technical principles:

- **Component Isolation**: Each phenotype targets a specific system pathway or feature
- **Minimal Implementation**: Uses simplified content to focus on structure validation
- **Technical Verification**: Ensures data transformation works correctly across all stages
- **Complete Coverage**: Collectively tests all phenotype types and edge cases
- **System Verification**: Confirms that interconnected components function as expected

## Diagnostic Flow Overview

The testing progression using diagnostic phenotypes follows this sequence:

1. **Entry Point Validation**: Testing system initialization and validates the entry passage structure.
2. **Linear Path Testing**: Verifying straightforward progression between passages
3. **Branch Testing**: Validating conditional paths and proper branch handling
4. **Evidence Testing**: Confirming evidence reveal and examination functionality
5. **Navigation Testing**: Verifying movement between system components
6. **Exit Point Validation**: Testing proper termination and outcome recording

## Phenotype Descriptions

### DIAGNOSTIC_ENTRY_POINT

**Purpose**: Tests system initialization and validates the entry passage structure.

**Structure**:
- System initialization text (via BOT)
- Initial state setting (via SET)
- Navigation to first test passage

**Example**:
```
BOT:lin="Diagnostic Test Case 01: System Initialization";
SET:evt=TC01_INITIALIZED;val=true;
SET:var=test_counter;val=0;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_linear_test;
```

### DIAGNOSTIC_LINEAR_TEST

**Purpose**: Tests straightforward progression between passages with no branching.

**Structure**:
- Test description text (via BOT)
- State modification (via SET)
- Navigation to next test passage

**Example**:
```
BOT:lin="Testing linear progression (Step 1 of 3)";
SET:var=test_counter;val=1;
SET:evt=TC01_STEP1_COMPLETE;val=true;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_linear_test_step2;
```

### DIAGNOSTIC_BRANCH_TEST_BINARY

**Purpose**: Tests simple two-way branching based on a condition.

**Structure**:
- Test description text (via BOT)
- Conditional branch (via IF/ELSE)
- Navigation to different passages based on condition

**Example**:
```
BOT:lin="Testing binary branching condition";
IF:cnd=CNT:var=test_counter;op=EQUALS;val=2;
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_a;
ELSE:
  ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_branch_path_b;
```

### DIAGNOSTIC_BRANCH_TEST_MULTI

**Purpose**: Tests complex multi-way branching with several conditions.

**Structure**:
- Test description text (via BOT)
- Multiple conditional branches (via IF/ELIF/ELSE)
- Navigation to different passages based on multiple conditions

**Example**:
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

**Purpose**: Tests the evidence reveal mechanism and related state changes.

**Structure**:
- Test description text (via BOT)
- Evidence reveal command (REVEAL action)
- State modification tracking the reveal
- Navigation to evidence examination

**Example**:
```
BOT:lin="Testing evidence reveal functionality";
ACT:aty=REVEAL;aet=test_evidence_01;
SET:evt=EVIDENCE_01_REVEALED;val=true;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### DIAGNOSTIC_EVIDENCE_EXAMINATION

**Purpose**: Tests the evidence examination process and attribute discovery.

**Structure**:
- Test description text (via BOT)
- Evidence attribute discovery (SET actions)
- State changes based on examination
- Navigation to next test based on findings

**Example**:
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

**Purpose**: Tests the convergence of multiple paths into a single outcome.

**Structure**:
- Test description text (via BOT)
- State recording of arrival path
- Common next step navigation

**Example**:
```
BOT:lin="Testing path merge functionality (arrival from multiple sources)";
SET:var=arrival_path;val="{{$source_path}}";
SET:evt=MERGE_POINT_REACHED;val=true;
ACT:aty=MOVE;amt=AMT:typ=PASSAGE;tgt=tc01_post_merge_test;
```

### DIAGNOSTIC_LOOP_TEST

**Purpose**: Tests cyclical progression with iteration counter and exit condition.

**Structure**:
- Test description text (via BOT)
- Loop counter increment
- Conditional exit from loop
- Navigation based on loop status

**Example**:
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

**Purpose**: Tests navigation between different application interfaces.

**Structure**:
- Test description text (via BOT)
- Navigation to specific application interface
- State recording of navigation event

**Example**:
```
BOT:lin="Testing application navigation";
SET:evt=NAV_TO_EVIDENCE_APP;val=true;
ACT:aty=MOVE;amt=AMT:typ=EVIDENCE;tgt=evidence_app;
```

### DIAGNOSTIC_EXIT_POINT

**Purpose**: Tests proper system termination and outcome recording.

**Structure**:
- Test description text (via BOT)
- Final state recording
- End of test case signaling

**Example**:
```
BOT:lin="Test case complete. Validating final state.";
SET:evt=TC01_COMPLETE;val=true;
SET:var=test_outcome;val="success";
ACT:aty=END;amt=AMT:typ=TEST;tgt=tc01_results;
```

## Implementation Guidelines

### Best Practices

1. **Isolation**: Each test passage should validate one specific functionality
2. **State Tracking**: Use SET commands to track test progress for validation
3. **Comprehensive Coverage**: Create tests for every phenotype type and edge case
4. **Verification Points**: Include explicit state checks at critical points
5. **Streamlined Flow**: Keep test passages simple and focused on technical validation

### Integration with System Phenotypes

Diagnostic Phenotypes should methodically test each essential system function:

- Use `DIAGNOSTIC_ENTRY_POINT` to test initialization and starting conditions
- Test all branch types with `DIAGNOSTIC_BRANCH_TEST_BINARY` and `DIAGNOSTIC_BRANCH_TEST_MULTI`
- Validate evidence handling with `DIAGNOSTIC_EVIDENCE_REVEAL` and `DIAGNOSTIC_EVIDENCE_EXAMINATION`
- Test path convergence with `DIAGNOSTIC_MERGE_POINT`
- Validate cyclical structures with `DIAGNOSTIC_LOOP_TEST`
- Test system navigation with `DIAGNOSTIC_APP_NAVIGATION`
- Verify proper termination with `DIAGNOSTIC_EXIT_POINT`

### Test Suite Organization

- Group related test phenotypes into logical test suites
- Create comprehensive test cases that verify complete system pathways
- Include edge case tests that validate boundary conditions
- Create regression tests for previously identified issues
- Document expected outcomes for each test case

## Technical Requirements

- All diagnostic phenotype IDs should follow the pattern `tc##_test_name` for easy identification
- Variable names should be descriptive of their testing purpose
- Event flags should clearly indicate what system state they're validating
- Test passages should include minimal content focused on technical verification
- Each test suite should begin with an entry point and conclude with an exit point
- Test outcomes should be explicitly recorded for verification

By following this guide, you can create comprehensive diagnostic test phenotypes that validate the complete pipeline from journey concept through SLPN notation to final JSON implementation, ensuring all system components function correctly in isolation and integration. 