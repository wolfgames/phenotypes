# Diagnostic Phenotype Guidelines: Testing System Integration

## Introduction

This guide outlines Diagnostic Phenotypes, a specialized set of structures designed to validate and test the complete workflow of our crime investigation creation system. Unlike Narrative or Gameplay Phenotypes which focus on player experience, Diagnostic Phenotypes are technical constructs created to ensure that the journey from conceptual design through SLPN (Story Logic Passage Notation) conversion to final JSON implementation works correctly. They represent the minimum viable components needed to test each system feature in isolation.

## Core Concepts

Diagnostic Phenotypes are built on these principles:

- **Isolation Testing**: Each phenotype targets a specific pathway or feature of the system
- **Minimal Complexity**: Uses simplified content to focus on structure validation rather than narrative quality
- **Complete Coverage**: Collectively tests all system pathways and edge cases
- **Technical Verification**: Ensures data flows correctly through all transformation stages
- **System Validation**: Confirms that interconnected components function as expected

## Testing Workflow

A recommended process for using Diagnostic Phenotypes:

1. **Base Component Testing**: Verify fundamental elements like characters, locations and items function correctly
2. **Path Validation**: Test each branching path type in isolation
3. **Sequence Verification**: Confirm that multi-step sequences progress correctly
4. **Trigger Testing**: Validate that conditional elements activate appropriately
5. **Format Transformation**: Check conversion between journey format, SLPN, and final JSON
6. **Integration Checking**: Verify connections between narrative and gameplay elements
7. **Edge Case Validation**: Test boundary conditions and unusual configurations
8. **Full-system Testing**: Run comprehensive tests combining multiple phenotypes

## Phenotype Descriptions

### Test Definitions

#### Diagnostic_Character_Definition

- **Purpose**: To validate character data structure and handling.
- **Structure**: Minimal implementation of character properties including unique ID, name, role, and basic attributes necessary for system function.
- **Example Use**: Creating test character "TC-01" with minimal required fields to validate character referencing in other phenotypes.

#### Diagnostic_Relationship_Definition

- **Purpose**: To test relationship data structures and character connections.
- **Structure**: Simplified relationship definition with unique ID, involved characters, type, and basic descriptors.
- **Example Use**: Creating "TR-01" connecting two test characters with minimal attributes to verify relationship handling.

#### Diagnostic_Location_Definition

- **Purpose**: To validate location referencing and property handling.
- **Structure**: Basic location properties including ID, name, description, and minimal attributes necessary for system validation.
- **Example Use**: Defining "TL-01" test location to verify location-based triggers and navigation functions.

#### Diagnostic_Object_Definition

- **Purpose**: To test object properties and interaction capabilities.
- **Structure**: Minimal object definition with ID, name, type, location, and basic interaction properties.
- **Example Use**: Creating "TO-01" test object to verify evidence handling, examination, and property access.

### Test Propositions

#### Diagnostic_Linear_Proposition

- **Purpose**: To test straightforward, linear progression through the system.
- **Structure**: Simple proposition with clear start, action, and outcome with no branching.
- **Example Use**: Creating basic "Step A leads to Step B" sequence to verify linear progression.

#### Diagnostic_Branch_Proposition

- **Purpose**: To validate conditional branching functionality.
- **Structure**: Proposition with decision point and multiple outcome paths based on player choices or evidence status.
- **Example Use**: Testing 2-way, 3-way, and complex branching to ensure path selection functions correctly.

#### Diagnostic_Merge_Proposition

- **Purpose**: To test the convergence of multiple paths into a single outcome.
- **Structure**: Definition of multiple entry points that lead to a common result or next step.
- **Example Use**: Creating multiple test paths that funnel into a single conclusion to verify path merging.

#### Diagnostic_Loop_Proposition

- **Purpose**: To test cyclical progression and escape conditions.
- **Structure**: Circular path definition with specified entry, loop conditions, and exit criteria.
- **Example Use**: Creating a repeatable sequence that requires specific conditions to exit, testing iteration handling.

### Test Evidence Elements

#### Diagnostic_Evidence_Item

- **Purpose**: To validate evidence creation, properties, and examination.
- **Structure**: Minimal evidence definition with required properties, examination states, and discoverable attributes.
- **Example Use**: Creating "TE-01" evidence item to test reveal mechanics, examination functionality, and attribute access.

#### Diagnostic_Evidence_Collection

- **Purpose**: To test grouping and processing of multiple evidence items.
- **Structure**: Collection definition with member items and collective processing rules.
- **Example Use**: Creating a test group of related evidence to verify collection handling and aggregate processing.

#### Diagnostic_Evidence_Transformation

- **Purpose**: To validate state changes in evidence over time.
- **Structure**: Definition of evidence state transitions based on player actions or system events.
- **Example Use**: Testing evidence that changes properties after examination or combination with other elements.

### Test Triggers and Conditions

#### Diagnostic_Action_Trigger

- **Purpose**: To test action-based event activation.
- **Structure**: Definition of actions that trigger system responses or state changes.
- **Example Use**: Creating test triggers for "examine," "combine," or "analyze" actions to verify event handling.

#### Diagnostic_State_Condition

- **Purpose**: To validate state-based conditionals.
- **Structure**: Definition of system states that affect available options or pathways.
- **Example Use**: Testing conditions like "evidence collected" or "location visited" to verify conditional logic.

#### Diagnostic_Compound_Condition

- **Purpose**: To test complex condition combinations.
- **Structure**: Multi-factor condition definition using logical operators (AND, OR, NOT).
- **Example Use**: Creating test conditions requiring multiple criteria to be satisfied, verifying complex conditional logic.

### Test System Integration Points

#### Diagnostic_Entry_Point

- **Purpose**: To validate system initialization and starting states.
- **Structure**: Definition of initial conditions, available options, and starting environment.
- **Example Use**: Creating test case starting points to verify system initialization and entry point handling.

#### Diagnostic_Exit_Point

- **Purpose**: To test proper system termination and outcome recording.
- **Structure**: Definition of end states, outcome summaries, and terminal conditions.
- **Example Use**: Creating test conclusion points to verify system shutdown and result recording.

#### Diagnostic_Checkpoint

- **Purpose**: To test save state and progress markers.
- **Structure**: Definition of persistent state snapshots at key progression points.
- **Example Use**: Creating test save points to verify state preservation and restoration.

### Test Data Transformation

#### Diagnostic_SLPN_Conversion

- **Purpose**: To validate conversion from conceptual journey to SLPN notation.
- **Structure**: Paired journey elements and expected SLPN outputs for verification.
- **Example Use**: Creating test cases with known journey-to-SLPN mappings to verify notation generation.

#### Diagnostic_JSON_Generation

- **Purpose**: To test SLPN-to-JSON transformation.
- **Structure**: SLPN examples with expected JSON output structures.
- **Example Use**: Creating test SLPN snippets to verify correct JSON structure generation.

#### Diagnostic_Full_Pipeline

- **Purpose**: To test end-to-end workflow from concept to final implementation.
- **Structure**: Complete examples traversing all transformation stages.
- **Example Use**: Creating comprehensive test cases that flow through the entire system to verify complete integration.

By using these Diagnostic Phenotypes, developers can systematically verify each component and pathway in the system, ensuring reliable conversion from conceptual journey elements to functioning SLPN and JSON implementations. 