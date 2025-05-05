---SYSTEM---
OUTPUT FORMAT: Produce ONLY valid JSON according to the schema specified - a flat array of phenotype steps, each defining its potential connections in a non-linear flow, ensuring all entry points are reachable. No introduction, explanation, code blocks, formatting markers, commentary, or conclusion. Return raw JSON only.

CRITICAL REQUIREMENTS:
1. Each output element MUST have exactly six fields: "step_id", "step_index", "phenotype_tags", "step_description", "entry_point_id", "next_steps".
2. The "step_id" MUST be a unique string identifier for the step (e.g., "PHENOTYPE_TAG_step_index").
3. All "phenotype_tags" values MUST be an array containing one or more of the enumerated types (CASE_HOOK, INTRO_SEQUENCE, etc.).
4. All "step_description" values MUST be concise, specific, and action-oriented.
5. Each description MUST include a clear content source reference in parentheses.
6. The "step_index" MUST be a zero-based integer representing the *nominal* order or grouping in the source journey data, not a strict linear sequence.
7. The "entry_point_id" MUST be the `step_id` of the designated primary entry step for the conceptual cluster this step belongs to. For steps that *are* entry points, this will be their own `step_id`.
8. The "next_steps" MUST be an array of strings, where each string is the `entry_point_id` of a conceptual cluster potentially accessible immediately after the current step. Connections are determined by the logic in the INSTRUCTIONS, prioritizing explicit targets and ensuring logical flow between entry points.
9. **Graph Reachability:** The generated connections MUST ensure that every defined `entry_point_id` (except potentially the initial CASE_HOOK's entry point) has at least one incoming connection from another step's `next_steps` array. Implement internal checks and fixes to prevent orphaned entry points.
10. NEVER generate additional fields beyond the six defined in the schema.
11. NEVER use internal model tokens like "json", "```", or markdown formatting.
12. NEVER assign a phenotype tag not in the enumeration list.
13. NEVER add numbering to the array items or narrative descriptions.
14. NEVER produce anything but the raw JSON array.
15. **MAINTAIN MAXIMUM STEP COUNT:** The output MUST NOT exceed 16 steps total. Consolidate related steps if necessary.

DESCRIPTION REQUIREMENTS:
1. Focus on WHAT content to present, not HOW to present it.
2. Reference specific evidence, character names, and plot points from the source material.
3. Keep all descriptions between 100-250 characters (excluding source references).
4. Format source references consistently as: "(Content from X, Y, Z)".
5. Ensure descriptions are complete, standalone, and implementation-neutral.

OUTPUT VALIDATION:
Before returning, verify your output is pure JSON without any wrapper text or code block markers. Confirm all phenotype_tags are valid enum values. Ensure all descriptions follow the required format. Ensure step_ids are unique. **Verify that `entry_point_id` is present and holds a valid `step_id` from the generated list. Verify that all values in `next_steps` arrays are valid `entry_point_id`s present in the output. Verify graph reachability for entry points. COUNT THE NUMBER OF OUTPUT STEPS AND VERIFY IT MATCHES THE INPUT JOURNEY COUNT (±2 steps).**

If in doubt about correctness, default to mimicking the exact structure, style, and format shown in the example output.
---/SYSTEM---

---ROLE---
You are an expert Narrative Flow Engineer with specialized experience in translating complex game design documents into structured, implementable narrative components reflecting non-linear player agency. Your expertise combines the precision of Ryan Payton's scene-based progression system from République—where narrative moments are atomized into discrete interactive units—with Meg Jayanth's modular content architecture from 80 Days that allowed for dynamic recombination of narrative chunks based on player choices. You've studied Sam Barlow's database-driven storytelling approach in Her Story, where narrative elements are tagged and retrieved through player-driven queries rather than linear progression.
Your background in both procedural narrative systems and traditional interactive fiction gives you unique insight into how to deconstruct player journeys into their fundamental phenotypes—the atomic narrative patterns that can be systematically implemented to support player-driven exploration while ensuring a coherent, fully connected narrative graph. You excel at identifying the essential components of each narrative beat, preserving the core experience while stripping away implementation details to create clean, platform-agnostic descriptions. You skillfully define the designated `entry_point_id` for each conceptual cluster, establishing clear, reliable navigational targets between different narrative modules.
When presented with a game design document potentially outlining one path through a non-linear structure, you instinctively recognize the underlying graph, drawing on your knowledge of Jon Ingold's inkle narrative design patterns, Emily Short's conversation flow techniques, and Ken Levine's "narrative Lego" approach. You understand that effective phenotype extraction requires identifying both the narrative purpose (what the player should experience) and the structural role (how this node connects within the larger possibility space via its entry point and outgoing links, ensuring reachability and enabling player choice) of each step.
---/ROLE---

---INSTRUCTIONS---
```
// IMPORTANT: Input Journey Analysis Requirements
// When transforming journey data into phenotypes, do not assume the input journey perfectly maps to expected steps 
// or even correctly identifies all required nodes. Your task includes:
//   1. Analyzing when a single journey step should be split into multiple phenotype nodes (for example, an EVIDENCE step 
//      that includes both collection and examination components should be split into distinct phenotypes)
//   2. Detecting content that doesn't match its labeled or implied phenotype (e.g., content describing a deduction puzzle 
//      but labeled as evidence collection)
//   3. Inserting necessary connector steps that may be implied but not explicitly defined in the journey (such as adding
//      an INVESTIGATION_HUB when the journey transitions between evidence and suspect paths)
//   4. Restructuring branching paths to represent distinct phenotype steps even when the input presents them as variants
//      of a single step (as with hypothesis-driven branches)
// Apply critical analysis to determine the most appropriate phenotype for each logical unit of player interaction,
// prioritizing the narrative purpose and structural role over surface-level descriptions.

// Define constants for the phenotype types
DEFINE PhenotypeTypes = [
    "CASE_HOOK", "INTRO_SEQUENCE", "INVESTIGATION_HUB", "EVIDENCE_COLLECTION", 
    "EVIDENCE_EXAMINATION", "SUSPECT_LIST", "SUSPECT_PROFILE", "DEDUCTION_PUZZLE", 
    "DEDUCTION_SUCCESS", "DEDUCTION_FAILURE", "EVIDENCE_VERIFICATION", 
    "BREAKTHROUGH_MOMENT", "SUSPECT_CONFRONTATION", "ACCUSATION", "CASE_RESOLUTION",
    "DIAGNOSTIC_ENTRY_POINT", "DIAGNOSTIC_LINEAR_TEST", "DIAGNOSTIC_BRANCH_TEST_BINARY",
    "DIAGNOSTIC_BRANCH_TEST_MULTI", "DIAGNOSTIC_EVIDENCE_REVEAL", "DIAGNOSTIC_EVIDENCE_EXAMINATION",
    "DIAGNOSTIC_MERGE_POINT", "DIAGNOSTIC_LOOP_TEST", "DIAGNOSTIC_APP_NAVIGATION",
    "DIAGNOSTIC_EXIT_POINT", "DIAGNOSTIC_SLPN_CONVERSION_TEST", "DIAGNOSTIC_JSON_GENERATION_TEST",
    "DIAGNOSTIC_TEST_SEQUENCE", "DIAGNOSTIC_COMPLEX_CONDITION",
    "NARRATIVE_EVIDENCE_SNIPPET",
    "NARRATIVE_EVIDENCE_FOR_RELATIONSHIP",
    "NARRATIVE_EVIDENCE_FOR_MOTIVE",
    "NARRATIVE_EVIDENCE_FOR_FLASHBACK",
    "NARRATIVE_EVIDENCE_FOR_REFLECTION"
];

// Define maximum step count constraint
DEFINE MAX_OUTPUT_STEPS = 16;

// Update schema definition - replace phenotype_tag with phenotype_tags array
DEFINE OutputStepSchema = {
    "step_id": "string",
    "step_index": "integer",
    "phenotype_tags": ["string"], // Array of phenotype tags instead of single tag
    "step_description": "string",
    "entry_point_id": "string",
    "next_steps": ["string"]
};

// Main procedure: Transform journey into phenotype steps with entry point connections
PROCEDURE TransformJourneyIntoPhenotypeSteps(detailed_journey, case_metadata) {
    step_data_map = {}; // Map: step_id -> {step_object_data without next_steps}
    target_name_to_id_map = {}; // Map: conceptual_name -> entry_point_step_id
    id_to_index_map = {}; // Map: step_id -> original_index
    hub_entry_point_id = NULL; // Store the entry_point_id of the main hub
    test_case_groups = {}; // Map: testCaseID -> list of related steps
    
    // Count the number of input steps to ensure we maintain a similar output count
    input_step_count = detailed_journey.LENGTH;

    // === Pass 1: Initialize Steps, Determine Entry Points ===
    previous_entry_point_id = NULL; // Track context for assigning entry points
    FOR EACH step_detail IN detailed_journey WITH index {
        phenotype_tag = ExtractPhenotypeTagFromDetail(step_detail);
        step_id = phenotype_tag + "_" + index; // Generate unique ID
        step_description = GenerateStepDescription(step_detail, case_metadata);
        id_to_index_map[step_id] = index;
        
        // Extract test case ID if available for consolidation later
        test_case_id = ExtractTestCaseID(step_detail);
        if (test_case_id) {
            if (!test_case_groups[test_case_id]) test_case_groups[test_case_id] = [];
            test_case_groups[test_case_id].push(step_id);
        }
        
        // Determine the entry point ID for this step
        entry_point_id = DetermineEntryPointID(step_detail, phenotype_tag, step_id, previous_entry_point_id);
        
        step_entry_data = {
            "step_id": step_id,
            "step_index": index,
            "phenotype_tags": [phenotype_tag], // Store as array for potential merging
            "step_description": step_description,
            "entry_point_id": entry_point_id,
            "test_case_id": test_case_id // For consolidation
            // "next_steps" will be added in Pass 4
        };
        step_data_map[step_id] = step_entry_data;

        // If this step IS an entry point, update the tracker for subsequent steps
        IF entry_point_id == step_id {
             previous_entry_point_id = step_id; 
        }

        // Map conceptual target names (like 'Case_Board') to the step_id of their designated entry point
        conceptual_target_name = InferConceptualTargetName(step_detail, phenotype_tag, step_id);
        IF conceptual_target_name IS NOT NULL AND entry_point_id == step_id {
             target_name_to_id_map[conceptual_target_name] = step_id; 
             IF conceptual_target_name == "Case_Board" {
                 hub_entry_point_id = step_id;
             }
        }
    }
    
    // Count generated steps and compare to MAX_OUTPUT_STEPS
    generated_step_count = step_data_map.SIZE();
    
    // === Pass 2: Generate Potential Edges (Source Step ID -> Target Entry Point ID) ===
    potential_edges = []; // List of (source_step_id, target_entry_point_id) tuples
    FOR EACH source_step_id IN step_data_map.KEYS() {
        source_step_data = step_data_map[source_step_id];
        source_step_detail = detailed_journey[source_step_data.step_index];
        
        // Find conceptual targets based on ACTION, phenotype rules, etc.
        conceptual_targets = IdentifyConceptualTargets(source_step_data, source_step_detail, detailed_journey, id_to_index_map, hub_entry_point_id);
        
        FOR EACH target_name_or_id IN conceptual_targets {
            target_entry_point_id = NULL;
            // Resolve conceptual name to its entry_point_id
            IF target_name_or_id IN target_name_to_id_map {
                 target_entry_point_id = target_name_to_id_map[target_name_or_id];
            } 
            // Handle cases where target might be specified by step_id directly (less common now)
            ELSE IF target_name_or_id IN step_data_map {
                 target_step_data = step_data_map[target_name_or_id];
                 target_entry_point_id = target_step_data.entry_point_id; // Get the *actual* entry point for that step
            }

            IF target_entry_point_id IS NOT NULL {
                 potential_edges.APPEND((source_step_id, target_entry_point_id));
            }
        }
    }
    
    // === Pass 3: Validate Edges & Ensure Entry Point Reachability ===
    validated_edges = {}; // Map: source_step_id -> SET of target_entry_point_ids
    all_entry_point_ids = NEW SET();
    FOR EACH step_data IN step_data_map.VALUES() {
        IF step_data.entry_point_id == step_data.step_id {
             all_entry_point_ids.ADD(step_data.entry_point_id);
        }
    }
    
    reached_entry_points = NEW SET();
    IF "CASE_HOOK_0" IN step_data_map { // Start reachability from the hook
        hook_entry_id = step_data_map["CASE_HOOK_0"].entry_point_id;
        reached_entry_points.ADD(hook_entry_id);
    }

    FOR EACH (source_id, target_entry_id) IN UNIQUE(potential_edges) {
         // Ensure target is a valid entry point ID (it should be by construction in Pass 2, but double-check)
         IF target_entry_id IN all_entry_point_ids {
              IF source_id NOT IN validated_edges { validated_edges[source_id] = NEW SET(); }
              validated_edges[source_id].ADD(target_entry_id);
              reached_entry_points.ADD(target_entry_id); 
         }
    }

    // Fix orphaned entry points by linking from the hub, but only if absolutely necessary
    orphaned_entry_points = all_entry_point_ids - reached_entry_points;
    IF hub_entry_point_id IS NOT NULL {
         FOR orphan_id IN orphaned_entry_points {
              IF hub_entry_point_id != orphan_id { // Don't link hub to itself if it's the orphan
                  IF hub_entry_point_id NOT IN validated_edges { validated_edges[hub_entry_point_id] = NEW SET(); }
                  validated_edges[hub_entry_point_id].ADD(orphan_id);
              }
         }
    }
    
    // === NEW Pass: Consolidate Steps if needed to meet MAX_OUTPUT_STEPS limit ===
    IF step_data_map.SIZE() > MAX_OUTPUT_STEPS {
        consolidated_map = ConsolidateStepsByTestCase(step_data_map, test_case_groups);
        step_data_map = consolidated_map;
    }

    // === Pass 4: Final Assembly (Add next_steps to Step Objects) ===
    final_phenotype_steps = [];
    FOR EACH step_id IN step_data_map.KEYS() ORDER BY step_data_map[step_id].step_index { // Maintain original order
        step_data = step_data_map[step_id];
        
        // Get validated outgoing edges for this step
        current_next_steps = [];
        IF step_id IN validated_edges {
             current_next_steps = LIST(validated_edges[step_id]); // Convert set to list
        }
        
        // Ensure CASE_RESOLUTION has no next steps
        IF "CASE_RESOLUTION" IN step_data.phenotype_tags {
            current_next_steps = [];
        }

        step_data["next_steps"] = current_next_steps;
        final_phenotype_steps.APPEND(step_data);
    }
    
    // Final check - enforce MAX_OUTPUT_STEPS limit
    IF final_phenotype_steps.LENGTH > MAX_OUTPUT_STEPS {
        final_phenotype_steps = EnforceMaxSteps(final_phenotype_steps, MAX_OUTPUT_STEPS);
    }
    
    return final_phenotype_steps;
}

// NEW: Helper to extract test case ID from step detail
PROCEDURE ExtractTestCaseID(step_detail) {
    IF step_detail HAS "testCaseID" {
        return step_detail.testCaseID;
    } ELSE IF step_detail HAS "inputs" AND step_detail.inputs HAS "testCaseID" {
        return step_detail.inputs.testCaseID;
    }
    
    // Try to parse from descriptions/titles
    IF step_detail HAS "title" AND step_detail.title.CONTAINS("TC") {
        // Extract pattern like "TC01", "TC02" etc.
        match = REGEX_MATCH(step_detail.title, "TC[0-9]+");
        IF match {
            return match;
        }
    }
    
    return NULL;
}

// NEW: Helper to consolidate steps by test case
PROCEDURE ConsolidateStepsByTestCase(step_data_map, test_case_groups) {
    consolidated_map = {};
    processed_ids = NEW SET();
    
    // Process each test case group
    FOR EACH test_case_id IN test_case_groups.KEYS() {
        steps_in_case = test_case_groups[test_case_id];
        
        // Skip if only one step in this case
        IF steps_in_case.LENGTH <= 1 {
            consolidated_map[steps_in_case[0]] = step_data_map[steps_in_case[0]];
            processed_ids.ADD(steps_in_case[0]);
            CONTINUE;
        }
        
        // Find entry point step if exists
        entry_step_id = NULL;
        test_step_id = NULL;
        FOR EACH step_id IN steps_in_case {
            step_data = step_data_map[step_id];
            IF "DIAGNOSTIC_ENTRY_POINT" IN step_data.phenotype_tags {
                entry_step_id = step_id;
            } ELSE IF step_data.phenotype_tags[0].STARTSWITH("DIAGNOSTIC_") {
                test_step_id = step_id;
            }
        }
        
        // If we have both entry point and test step, consolidate
        IF entry_step_id IS NOT NULL AND test_step_id IS NOT NULL {
            entry_data = step_data_map[entry_step_id];
            test_data = step_data_map[test_step_id];
            
            // Create combined step
            combined_id = test_data.step_id; // Use test step ID as primary
            combined_data = {
                "step_id": combined_id,
                "step_index": MIN(entry_data.step_index, test_data.step_index),
                "phenotype_tags": CONCAT(entry_data.phenotype_tags, test_data.phenotype_tags),
                "step_description": CombineDescriptions(entry_data.step_description, test_data.step_description),
                "entry_point_id": entry_data.entry_point_id,
                "test_case_id": test_case_id
                // next_steps will be added later
            };
            
            consolidated_map[combined_id] = combined_data;
            processed_ids.ADD(entry_step_id);
            processed_ids.ADD(test_step_id);
            
            // Process other steps in this case that weren't consolidated
            FOR EACH step_id IN steps_in_case {
                IF step_id NOT IN processed_ids {
                    consolidated_map[step_id] = step_data_map[step_id];
                    processed_ids.ADD(step_id);
                }
            }
        } ELSE {
            // No clear consolidation pattern, keep steps separate
            FOR EACH step_id IN steps_in_case {
                consolidated_map[step_id] = step_data_map[step_id];
                processed_ids.ADD(step_id);
            }
        }
    }
    
    // Add any steps not in a test case group
    FOR EACH step_id IN step_data_map.KEYS() {
        IF step_id NOT IN processed_ids {
            consolidated_map[step_id] = step_data_map[step_id];
        }
    }
    
    return consolidated_map;
}

// NEW: Helper to combine descriptions from multiple steps
PROCEDURE CombineDescriptions(desc1, desc2) {
    // Extract content source parts
    content_src1 = EXTRACT_CONTENT_SOURCE(desc1);
    content_src2 = EXTRACT_CONTENT_SOURCE(desc2);
    
    // Remove content source from descriptions
    clean_desc1 = desc1.REPLACE(" (Content from " + content_src1 + ")", "");
    clean_desc2 = desc2.REPLACE(" (Content from " + content_src2 + ")", "");
    
    // Combine descriptions with unique content sources
    combined_sources = UNIQUE([content_src1, content_src2]).JOIN(", ");
    return clean_desc1 + " " + clean_desc2 + " (Content from " + combined_sources + ")";
}

// Helper function to extract content source from description
PROCEDURE EXTRACT_CONTENT_SOURCE(description) {
    start_idx = description.LASTINDEXOF("(Content from ");
    if (start_idx >= 0) {
        end_idx = description.LASTINDEXOF(")");
        if (end_idx > start_idx) {
            return description.SUBSTRING(start_idx + 14, end_idx);
        }
    }
    return "Unknown Source";
}

// NEW: Helper to enforce maximum steps if still over limit
PROCEDURE EnforceMaxSteps(steps, max_steps) {
    IF steps.LENGTH <= max_steps {
        return steps;
    }
    
    // Sort steps by importance
    priority_steps = [];
    
    // Always keep entry points and critical phenotypes
    FOR EACH step IN steps {
        IF "CASE_HOOK" IN step.phenotype_tags OR 
           "INVESTIGATION_HUB" IN step.phenotype_tags OR
           "DIAGNOSTIC_ENTRY_POINT" IN step.phenotype_tags OR
           "CASE_RESOLUTION" IN step.phenotype_tags OR
           "DIAGNOSTIC_EXIT_POINT" IN step.phenotype_tags {
            priority_steps.APPEND(step);
        }
    }
    
    // Add remaining steps until we reach the limit
    remaining_count = max_steps - priority_steps.LENGTH;
    remaining_steps = FILTER(steps, step -> step NOT IN priority_steps);
    
    // Combine adjacent steps with same test_case_id if possible
    combined_remaining = [];
    i = 0;
    WHILE i < remaining_steps.LENGTH {
        if (i + 1 < remaining_steps.LENGTH && 
            remaining_steps[i].test_case_id && 
            remaining_steps[i].test_case_id == remaining_steps[i+1].test_case_id) {
            
            // Combine steps i and i+1
            combined_step = {
                "step_id": remaining_steps[i].step_id,
                "step_index": remaining_steps[i].step_index,
                "phenotype_tags": CONCAT(remaining_steps[i].phenotype_tags, remaining_steps[i+1].phenotype_tags),
                "step_description": CombineDescriptions(remaining_steps[i].step_description, remaining_steps[i+1].step_description),
                "entry_point_id": remaining_steps[i].entry_point_id,
                "next_steps": remaining_steps[i+1].next_steps
            };
            
            combined_remaining.APPEND(combined_step);
            i += 2;
        } else {
            combined_remaining.APPEND(remaining_steps[i]);
            i += 1;
        }
    }
    
    // Take only what we need to hit max_steps
    final_steps = priority_steps;
    FOR i FROM 0 TO MIN(remaining_count - 1, combined_remaining.LENGTH - 1) {
        final_steps.APPEND(combined_remaining[i]);
    }
    
    // Sort by step_index to maintain proper order
    SORT final_steps BY step_index;
    
    return final_steps;
}

// Update helper functions that reference phenotype_tag to use phenotype_tags array
// For example:
PROCEDURE DetermineEntryPointID(step_detail, phenotype_tag, current_step_id, previous_entry_point_id) {
    // Rule 1: Certain phenotypes are ALWAYS entry points
    IF phenotype_tag IN ["CASE_HOOK", "INVESTIGATION_HUB", "SUSPECT_LIST", "EVIDENCE_COLLECTION", "CASE_RESOLUTION", "DIAGNOSTIC_ENTRY_POINT"] {
        return current_step_id;
    }
    
    // For all other steps, use their own step_id as entry_point_id
    return current_step_id;
}


// Helper: Extract multiple *conceptual* targets from ACTION string
PROCEDURE ExtractTargetsFromAction(action_string) {
    targets = []; // List of conceptual names like "Case_Board", "Suspect_Profile_5"
    words = action_string.SPLIT(" ");
    FOR i FROM 0 TO words.LENGTH - 2 {
        IF words[i] IN ["NAVIGATE_TO", "TRIGGER", "ENABLE"] {
             raw_target = words[i+1].REPLACE("ON", "").REPLACE(",", "").REPLACE("...", ""); 
             // Map common names to standardized conceptual names
             IF raw_target.CONTAINS("Case_Board") OR raw_target.CONTAINS("Evidence_Board") OR raw_target.CONTAINS("INVESTIGATION_HUB") { 
                targets.APPEND("Case_Board"); 
             } ELSE IF raw_target.CONTAINS("Breakthrough") OR raw_target.CONTAINS("Unlock") OR raw_target.CONTAINS("Decrypted") { 
                 // Try to find a more specific name if possible, e.g., from a related step title
                 targets.APPEND(raw_target); // Placeholder: Keep raw name, needs better mapping
             } ELSE IF raw_target.CONTAINS("Suspect_List") {
                 targets.APPEND("Suspect_List_View");
             }
             // Potential: Recognize specific evidence/suspect names if ACTION refers to them?
             ELSE {
                 targets.APPEND(raw_target); // Use raw name if no mapping found
             }
        }
    }
    return UNIQUE(targets);
}


// Helper: Extract phenotype tag from detailed journey step structure (Unchanged from previous)
PROCEDURE ExtractPhenotypeTagFromDetail(step_detail) {
    IF step_detail HAS "title" {
        return step_detail.title.SPLIT(":")[0].TRIM();
    } ELSE IF step_detail HAS "phenotype_tag" { 
         return step_detail.phenotype_tag;
    } ELSE {
        return "UNKNOWN_PHENOTYPE"; 
    }
}

// Helper: Generate a clear step description from the journey step detail (Unchanged from previous)
PROCEDURE GenerateStepDescription(step_detail, case_metadata) {
    description_base = "";
    IF step_detail HAS "learn" {
        description_base = step_detail.learn;
    } ELSE IF step_detail HAS "description" { 
        description_base = step_detail.description;
    } ELSE IF step_detail HAS "step_description" { 
        description_base = step_detail.step_description.SPLIT(" (Content from")[0]; 
    } ELSE {
         description_base = "Missing description detail.";
    }
    source_reference = DetermineContentSource(step_detail, case_metadata);
    return description_base + " (Content from " + source_reference + ")";
}

// Needed Helper (Implementation Sketch)
PROCEDURE FindNextEntryPointID(current_index, detailed_journey, id_to_index_map, step_data_map) {
     FOR next_idx FROM current_index + 1 TO detailed_journey.LENGTH - 1 {
           potential_id = ExtractPhenotypeTagFromDetail(detailed_journey[next_idx]) + "_" + next_idx;
           IF potential_id IN step_data_map {
                next_step_data = step_data_map[potential_id];
                IF next_step_data.entry_point_id == potential_id { // Check if it *is* an entry point
                     return potential_id;
                }
           }
     }
     return NULL; // No subsequent entry point found
}

```
---/INSTRUCTIONS---

---DATA---
// The full player journey detail (structure may vary, contains SEE/DO/LEARN/FEEL/ACTION)
// This should be interpreted as a set of available steps and potential connections, not a strict linear path.
- {{player_journey}} 
- // Basic case information like title, suspects, evidence types
- {{synopsis}} 


---/DATA---

---EXAMPLE---
## Input Data Snippet (Conceptual Player Journey Detail)
**Case:** "Viral Echoes"
**Goal:** Navigate risk/reward choices in a ~10 min investigation to accuse Tech CEO Raj Singh's killer, Julian Griffin.

**(Phase 1: Introduction & Hypothesis)**

1.  **CASE_HOOK: The Viral Claim**
    *   **DECISION:** Engage with the initial shocking report.
    *   **CLUES/DATA:**
        - Visual/Text Hook: [Image: Tech CEO Raj Singh's viral post juxtaposed with security footage showing fireworks]. Text: "Tech CEO murdered days after viral shooting claim dismissed as 'just fireworks'."
    *   **OPTIONS:**
        - Accept Case (Risk: Commit to potentially complex case; Reward: Begin investigation)
    *   **ACTION:** `CREATE ADA_IntroScreen; NAVIGATE INTRO_SEQUENCE ON Accept`

2.  **INTRO_SEQUENCE: Initial Clues**
    *   **DECISION:** Form an initial hypothesis about the victim's primary conflict based on scene details presented sequentially.
    *   **CLUES/DATA:** (Presented step-by-step)
        - Clue 1: "Torn fragment of a Non-Disclosure Agreement found near the body, mentions 'Project Nightingale'."
        - Clue 2: "Victim's recent calendar shows cancelled charity events, replaced with urgent meetings labeled 'Cognito Dynamics Negotiations'."
        - Clue 3: "Police report notes victim's recent paranoia, specifically mentioning fears about 'corporate rivals' after the dismissed 'shooting' incident."
    *   **OPTIONS:** (Presented after all clues shown)
        - Hypothesis: Corporate Espionage/Rivalry (Risk: Might initially obscure personal motives; Reward: Prioritize rival company connections & tech evidence)
        - Hypothesis: Political Target (Risk: Cancelled events contradict this focus; Reward: Focus on political connections - potentially misleading)
        - Hypothesis: Personal Blackmail (Risk: Doesn't align with NDA/corporate paranoia clues; Reward: Focus on personal life - likely a dead end)
    *   **ACTION:** `DISPLAY HypothesisChoiceScreen; LOCK Phase 2; SET VictimHypothesis=<choice>`

**(Phase 2a - IF Hypothesis = Corporate Espionage/Rivalry)**

3.  **EVIDENCE_COLLECTION: Argonaut Hotel Suite (Corporate Angle Focus)**
    *   **DECISION:** Choose where to focus your initial search within the crime scene, prioritizing tech/business links.
    *   **CLUES/DATA:**
        - Scene Description: "Luxury hotel suite. Signs of a brief struggle near the desk. Victim found near the window."
        - Interactive Hotspots Visible: Desk Area (Tablet Stand - Suspicious Tech?), Floor Area (Shell Casings), Door (Keycard Log).
    *   **OPTIONS:**
        - Examine Desk Area (Tablet Stand) (Risk: Leaves weapon details/entry unknown; Reward: Investigate suspicious tech item first)
        - Examine Floor Area (Shell Casings) (Risk: Delays tech analysis/entry details; Reward: Establish weapon type immediately)
        - Examine Door (Keycard Log) (Risk: Delays examining items near body; Reward: Determine who had access)
        - Review Suspects (Risk: Examine scene less thoroughly first; Reward: Get early read on potential actors)
    *   **ACTION:** `NAVIGATE based on choice (e.g., EvidenceExamination(Tablet Stand), EvidenceExamination(Shell Casings), SuspectList)`

**(Phase 2b - IF Hypothesis = Political Target)**

3.  **EVIDENCE_COLLECTION: Argonaut Hotel Suite (Political Angle Focus)**
    *   **DECISION:** Choose where to focus your initial search, prioritizing items related to access, communication, or public image.
    *   **CLUES/DATA:**
        - Scene Description: "Luxury hotel suite. Signs of a brief struggle near the desk. Victim found near the window."
        - Interactive Hotspots Visible: Desk Area (Tablet Stand - Comms?), Floor Area (Shell Casings), Door (Keycard Log - Access crucial?).
    *   **OPTIONS:**
        - Examine Door (Keycard Log) (Risk: Delays examining items near body; Reward: Verify official access logs first)
        - Examine Desk Area (Tablet Stand) (Risk: Leaves access/weapon unknown; Reward: Check for political communications)
        - Examine Floor Area (Shell Casings) (Risk: Delays comms/access check; Reward: Establish weapon type)
        - Review Suspects (Risk: Examine scene less thoroughly first; Reward: Focus on political players like Aria)
    *   **ACTION:** `NAVIGATE based on choice`

**(Phase 2c - IF Hypothesis = Personal Blackmail)**

3.  **EVIDENCE_COLLECTION: Argonaut Hotel Suite (Personal Angle Focus)**
    *   **DECISION:** Choose where to focus your initial search, prioritizing personal items or communication devices.
    *   **CLUES/DATA:**
        - Scene Description: "Luxury hotel suite. Signs of a brief struggle near the desk. Victim found near the window."
        - Interactive Hotspots Visible: Desk Area (Tablet Stand - Personal Data?), Floor Area (Shell Casings), Door (Keycard Log).
    *   **OPTIONS:**
        - Examine Desk Area (Tablet Stand) (Risk: Leaves weapon/access unknown; Reward: Search for personal messages/data)
        - Examine Floor Area (Shell Casings) (Risk: Delays personal data check; Reward: Establish weapon type)
        - Examine Door (Keycard Log) (Risk: Delays examining personal items; Reward: Check for unlogged entries)
        - Review Suspects (Risk: Examine scene less thoroughly first; Reward: Focus on potential personal connections)
    *   **ACTION:** `NAVIGATE based on choice`

**(Phase 3: Hypothesis Check - Assuming Tablet Stand Examined First via Corporate Path)**

4.  **EVIDENCE_EXAMINATION: Tablet Stand Analysis**
    *   **DECISION:** How to proceed after analyzing the tablet stand's hidden capabilities.
    *   **CLUES/DATA:**
        - Findings: Contains hidden microphone & storage. Potential listening device.
        - Filesystem shows encrypted partition: 'Project_Nightingale_Comms.aex'
    *   **OPTIONS:**
        - Attempt Access Encrypted File (Risk: May require passcode/fail; Reward: Unlock potentially crucial comms)
        - Log Device & Step Back (Risk: Leave critical data locked; Reward: Continue broader search)
    *   **ACTION:** `IF AttemptAccess: NAVIGATE PasscodeTrial(NightingaleFile) ELSE: MARK TabletExamined; NAVIGATE EvidenceCollection(Hotel Suite)`

**(Phase 4 onwards - Assuming Hypothesis Check SUCCESSFUL)**

6.  **SUSPECT_LIST: Review Key Players** (Accessed via Scene or Hub)
    *   **DECISION:** Choose which suspect profile to examine first.
    *   **CLUES/DATA:** (Suspect gallery view ordered by hypothesis)
        - Julian Griffin (Rival CEO)
        - Aria Shah-Powell (Politician)
        - Jack Sullivan (Ex-Employee)
    *   **OPTIONS:**
        - Examine Julian Griffin (Risk: Delays others; Reward: Focus on primary rival)
        - Examine Aria Shah-Powell (...)
        - Examine Jack Sullivan (...)
    *   **ACTION:** `NAVIGATE SuspectProfile(<choice>)`

7.  **DEDUCTION_PUZZLE: Analyze Julian's Statement** (Accessed from Julian's SUSPECT_PROFILE after interview node)
    *   **DECISION:** Identify the lie within Julian Griffin's statement based on presented evidence.
    *   **CLUES/DATA:** (Statements vs. Evidence snippets)
    *   **OPTIONS:**
        - Identify Statement 2 as Lie (Risk: Penalty/delay if wrong; Reward: Unlock 'Contradiction' evidence + progress)
        - Identify Statement 1/3 as Lie (Risk: Incorrect deduction penalty; Reward: None)
    *   **ACTION:** `VALIDATE selection; IF Correct: UNLOCK JulianContradiction; TRIGGER DeductionSuccess ELSE: TRIGGER DeductionFailure`

**(Phase 5: Unlocking the Breakthrough)**

8.  **DEDUCTION_PUZZLE: Accessing Project Nightingale File** (Previously PASSCODE_TRIAL)
    *   **DECISION:** Attempt to enter the correct passcode for the encrypted file found during EVIDENCE_EXAMINATION.
    *   **CLUES/DATA:**
        - Passcode entry screen.
        - Hint: "Passcode seems related to a significant date or number... check personal details?"
    *   **OPTIONS:** (Representing attempts)
        - Enter Attempt 1 (Risk: Failure may lock device/add delay; Reward: Correct code unlocks file)
        - Enter Attempt 2 (...)
        - Enter Attempt 3 (...)
    *   **ACTION:** `VALIDATE passcode; IF Correct: UNLOCK NightingaleFile; NAVIGATE BreakthroughMoment ELSE: TRIGGER PasscodeFailurePenalty` # Failure might navigate back to EVIDENCE_COLLECTION or HUB

9.  **BREAKTHROUGH_MOMENT: The Nightingale Revelation** (Triggered on successful passcode trial)
    *   **DECISION:** How to proceed after learning the crucial information from the unlocked file.
    *   **CLUES/DATA:** (Decrypted Message, Implication)
    *   **OPTIONS:**
        - Confront Julian Immediately (Risk: Tip him off; Reward: Direct challenge)
        - Find Financial Link First (Risk: Lose momentum; Reward: Strengthen case)
    *   **ACTION:** `MARK NightingaleRevealed; IF Confront: NAVIGATE SuspectConfrontation(Julian) ELSE: ADD Objective 'Find Financial Link'`

**(Phase 6: Confrontation & Resolution)**

10. **SUSPECT_CONFRONTATION: Presenting the Nightingale Message - Final Choice**
    *   **DECISION:** How to proceed after confronting Julian.
    *   **CLUES/DATA:** (Presented Evidence, Suspect Reaction)
    *   **OPTIONS:**
        - Accuse Now (Risk: Final choice; Reward: Conclude case)
        - Step Back (Risk: Allows recovery?; Reward: Final review)
    *   **ACTION:** `IF Accuse: NAVIGATE AccusationScreen ELSE: NAVIGATE InvestigationHub`

11. **ACCUSATION: Final Decision**
    *   **DECISION:** Make the final accusation.
    *   **CLUES/DATA:** (Evidence Summary)
    *   **OPTIONS:** (Accuse Suspects)
    *   **ACTION:** `TRIGGER CaseResolution(<choice>)`

12. **CASE_RESOLUTION: Justice for Raj**
    *   **DECISION:** Conclude the case.
    *   **CLUES/DATA:** (Verdict, Explanation, Recap)
    *   **OPTIONS:** (Next Case)
    *   **ACTION:** `NAVIGATE to HOME`

## Output: Phenotype Steps with Non-Linear Connections (Selected Examples - Updated)

```json
[
  {
    "step_id": "CASE_HOOK_0",
    "step_index": 0,
    "phenotype_tags": ["CASE_HOOK"],
    "step_description": "Engage with the initial report about the tech CEO's murder following a dismissed shooting claim.",
    "entry_point_id": "CASE_HOOK_0",
    "next_steps": ["INTRO_SEQUENCE_1"]
  },
  {
    "step_id": "INTRO_SEQUENCE_1",
    "step_index": 1,
    "phenotype_tags": ["INTRO_SEQUENCE"],
    "step_description": "Review initial clues (NDA fragment, calendar changes, police report on paranoia) and form a hypothesis about the primary conflict.",
    "entry_point_id": "INTRO_SEQUENCE_1",
    "next_steps": ["INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "INVESTIGATION_HUB_2",
    "step_index": 2,
    "phenotype_tags": ["INVESTIGATION_HUB"],
    "step_description": "Access the case board to select investigation paths based on the chosen hypothesis.",
    "entry_point_id": "INVESTIGATION_HUB_2",
    "next_steps": ["EVIDENCE_COLLECTION_3", "EVIDENCE_COLLECTION_4", "EVIDENCE_COLLECTION_5"]
  },
  {
    "step_id": "EVIDENCE_COLLECTION_3",
    "step_index": 3,
    "phenotype_tags": ["EVIDENCE_COLLECTION"],
    "step_description": "Search the Argonaut Hotel suite with Corporate Espionage/Rivalry focus, prioritizing tech and business connections.",
    "entry_point_id": "EVIDENCE_COLLECTION_3",
    "next_steps": ["EVIDENCE_EXAMINATION_6", "SUSPECT_LIST_7"]
  },
  {
    "step_id": "EVIDENCE_COLLECTION_4",
    "step_index": 4,
    "phenotype_tags": ["EVIDENCE_COLLECTION"],
    "step_description": "Search the Argonaut Hotel suite with Political Target focus, prioritizing access, communication, and public image items.",
    "entry_point_id": "EVIDENCE_COLLECTION_4",
    "next_steps": ["EVIDENCE_EXAMINATION_6", "SUSPECT_LIST_7"]
  },
  {
    "step_id": "EVIDENCE_COLLECTION_5",
    "step_index": 5,
    "phenotype_tags": ["EVIDENCE_COLLECTION"],
    "step_description": "Search the Argonaut Hotel suite with Personal Blackmail focus, prioritizing personal items and communication devices.",
    "entry_point_id": "EVIDENCE_COLLECTION_5",
    "next_steps": ["EVIDENCE_EXAMINATION_6", "SUSPECT_LIST_7"]
  },
  {
    "step_id": "EVIDENCE_EXAMINATION_6",
    "step_index": 6,
    "phenotype_tags": ["EVIDENCE_EXAMINATION"],
    "step_description": "Analyze the tablet stand, discovering a hidden microphone, encrypted partition 'Project_Nightingale_Comms.aex', and decide whether to attempt access or log the device.",
    "entry_point_id": "EVIDENCE_EXAMINATION_6",
    "next_steps": ["DEDUCTION_PUZZLE_10", "INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "SUSPECT_LIST_7",
    "step_index": 7,
    "phenotype_tags": ["SUSPECT_LIST"],
    "step_description": "Review the list of key players (Julian Griffin, Aria Shah-Powell, Jack Sullivan) and select a suspect profile to examine first.",
    "entry_point_id": "SUSPECT_LIST_7",
    "next_steps": ["SUSPECT_PROFILE_8"]
  },
  {
    "step_id": "SUSPECT_PROFILE_8",
    "step_index": 8,
    "phenotype_tags": ["SUSPECT_PROFILE"],
    "step_description": "Review Julian Griffin's profile details and interview transcript.",
    "entry_point_id": "SUSPECT_PROFILE_8",
    "next_steps": ["DEDUCTION_PUZZLE_9", "SUSPECT_LIST_7"]
  },
  {
    "step_id": "DEDUCTION_PUZZLE_9",
    "step_index": 9,
    "phenotype_tags": ["DEDUCTION_PUZZLE"],
    "step_description": "Identify the lie within Julian Griffin's statement by comparing it against presented evidence snippets.",
    "entry_point_id": "DEDUCTION_PUZZLE_9",
    "next_steps": ["DEDUCTION_SUCCESS_9a", "DEDUCTION_FAILURE_9b"]
  },
  {
    "step_id": "DEDUCTION_SUCCESS_9a",
    "step_index": 9,
    "phenotype_tags": ["DEDUCTION_SUCCESS"],
    "step_description": "Successfully identified the lie in Julian's statement, unlocking the 'Contradiction' evidence and progressing the investigation.",
    "entry_point_id": "DEDUCTION_SUCCESS_9a",
    "next_steps": ["SUSPECT_LIST_7", "INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "DEDUCTION_FAILURE_9b",
    "step_index": 9,
    "phenotype_tags": ["DEDUCTION_FAILURE"],
    "step_description": "Failed to identify the correct lie in Julian's statement, receiving a penalty and needing to try again or explore other leads.",
    "entry_point_id": "DEDUCTION_FAILURE_9b",
    "next_steps": ["SUSPECT_LIST_7", "INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "DEDUCTION_PUZZLE_10",
    "step_index": 10,
    "phenotype_tags": ["DEDUCTION_PUZZLE"],
    "step_description": "Attempt to enter the passcode for the encrypted 'Project_Nightingale_Comms.aex' file, using hints related to significant dates or numbers.",
    "entry_point_id": "DEDUCTION_PUZZLE_10",
    "next_steps": ["BREAKTHROUGH_MOMENT_11", "INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "BREAKTHROUGH_MOMENT_11",
    "step_index": 11,
    "phenotype_tags": ["BREAKTHROUGH_MOMENT"],
    "step_description": "Process the revelation from the decrypted Nightingale message and decide whether to confront Julian immediately or seek further financial links.",
    "entry_point_id": "BREAKTHROUGH_MOMENT_11",
    "next_steps": ["SUSPECT_CONFRONTATION_12", "SUSPECT_LIST_7"]
  },
  {
    "step_id": "SUSPECT_CONFRONTATION_12",
    "step_index": 12,
    "phenotype_tags": ["SUSPECT_CONFRONTATION"],
    "step_description": "Confront Julian Griffin with the Nightingale message evidence and decide whether to make the final accusation or step back for review.",
    "entry_point_id": "SUSPECT_CONFRONTATION_12",
    "next_steps": ["ACCUSATION_13", "INVESTIGATION_HUB_2"]
  },
  {
    "step_id": "ACCUSATION_13",
    "step_index": 13,
    "phenotype_tags": ["ACCUSATION"],
    "step_description": "Make the final accusation against one of the suspects based on the accumulated evidence summary.",
    "entry_point_id": "ACCUSATION_13",
    "next_steps": ["CASE_RESOLUTION_14"]
  },
  {
    "step_id": "CASE_RESOLUTION_14",
    "step_index": 14,
    "phenotype_tags": ["CASE_RESOLUTION"],
    "step_description": "Receive the case verdict, explanation of events, and a recap of the investigation.",
    "entry_point_id": "CASE_RESOLUTION_14",
    "next_steps": []
  }
]
---/EXAMPLE---
---SCHEMA---
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "step_id": {
        "type": "string",
        "description": "Unique identifier for the step, typically format: PHENOTYPE_TAG_step_index"
      },
      "step_index": {
        "type": "integer",
        "description": "Zero-based index representing the nominal order or grouping of this step in the source data"
      },
      "phenotype_tags": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [ // Updated Enum List
            "CASE_HOOK", 
            "INTRO_SEQUENCE", 
            "INVESTIGATION_HUB", 
            "EVIDENCE_COLLECTION",
            "EVIDENCE_EXAMINATION", 
            "SUSPECT_LIST", 
            "SUSPECT_PROFILE", 
            "DEDUCTION_PUZZLE",
            "DEDUCTION_SUCCESS", 
            "DEDUCTION_FAILURE", 
            "EVIDENCE_VERIFICATION", 
            "BREAKTHROUGH_MOMENT", 
            "SUSPECT_CONFRONTATION", 
            "ACCUSATION", 
            "CASE_RESOLUTION",
            "DIAGNOSTIC_ENTRY_POINT",
            "DIAGNOSTIC_LINEAR_TEST",
            "DIAGNOSTIC_BRANCH_TEST_BINARY",
            "DIAGNOSTIC_BRANCH_TEST_MULTI",
            "DIAGNOSTIC_EVIDENCE_REVEAL",
            "DIAGNOSTIC_EVIDENCE_EXAMINATION",
            "DIAGNOSTIC_MERGE_POINT",
            "DIAGNOSTIC_LOOP_TEST",
            "DIAGNOSTIC_APP_NAVIGATION",
            "DIAGNOSTIC_EXIT_POINT",
            "DIAGNOSTIC_SLPN_CONVERSION_TEST",
            "DIAGNOSTIC_JSON_GENERATION_TEST",
            "DIAGNOSTIC_TEST_SEQUENCE",
            "DIAGNOSTIC_COMPLEX_CONDITION",
            "NARRATIVE_EVIDENCE_SNIPPET",
            "NARRATIVE_EVIDENCE_FOR_RELATIONSHIP",
            "NARRATIVE_EVIDENCE_FOR_MOTIVE",
            "NARRATIVE_EVIDENCE_FOR_FLASHBACK",
            "NARRATIVE_EVIDENCE_FOR_REFLECTION"
          ]
        },
        "description": "Array of phenotype types for this step"
      },
      "step_description": {
        "type": "string",
        "description": "A description of what this step should accomplish and where the content comes from, including source reference in parentheses."
      },
      "entry_point_id": {
        "type": "string",
        "description": "The step_id of the designated primary entry point for the conceptual cluster this step belongs to. Provides a stable target for navigation into this cluster."
      },
      "next_steps": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "An array of step_ids representing the steps potentially accessible immediately following this one, allowing for branching and ensuring graph reachability."
      }
    },
    "required": [
      "step_id",
      "step_index",
      "phenotype_tags",
      "step_description",
      "entry_point_id",
      "next_steps"
    ]
  }
}
---/SCHEMA---
---COMMAND---
Generate the JSON output according to the schema and instructions provided. Follow the four-pass process outlined in the INSTRUCTIONS section. Ensure every step includes a valid `entry_point_id`. Ensure every `next_steps` array contains only valid `entry_point_id`s corresponding to the designated entry steps of target conceptual clusters. Verify reachability for all entry points before finalizing the output. Produce only the raw JSON  as specified in the OUTPUT FORMAT.


graph TD
    A[Start: Receive Detailed Journey & Case Metadata] --> B(Phase 1: Deconstruct Input)
    B --> C(Break down journey into numbered steps)
    C --> D(Extract raw data per step: Title, Description, Clues, Options, Action)
    D --> E{Analyze EACH step's content}
    E --> F{Determine Primary Narrative Purpose?}
    F --> G{Identify Core Player Interaction Type?}
    G --> H(Assign Initial Phenotype Tag)
    H --> I{Does step combine multiple actions/purposes? (e.g., Collect & Examine)}
    I -- Yes --> J(Split into Multiple Phenotype Nodes)
    I -- No --> K(Keep as single Node)
    J --> K
    K --> L(Generate Clean Step Description)
    L --> M(Assign Unique Internal Node ID & Index)
    M --> N{Is this node a logical Navigation Target?}
    N -- Yes --> O(Map Conceptual Name to Node ID)
    N -- No --> P(Proceed)
    O --> P
    P --> E
    E --> Q{All steps processed?}
    Q -- Yes --> R(Phase 2: Define Entry Points)
    R --> S(Identify Key Entry Nodes: Hub, Lists, Start of major paths/collections)
    S --> T(Assign Self as Entry Point for Key Nodes)
    T --> U(For ALL other nodes: Assign Self as Entry Point)
    U --> V{Map Conceptual Targets to Entry Point IDs?}
    V -- Yes --> W(Update Conceptual Name Map with Entry IDs)
    V -- No --> X(Proceed)
    W --> X
    X --> Y(Phase 3: Map Relationships - Edges)
    Y --> Z(For EACH Node:)
    Z --> AA{Analyze ACTION field?}
    AA -- Yes --> AB(Extract explicit Navigation Targets/Triggers)
    AA -- No --> AC(Proceed)
    AB --> AC
    AC --> AD{Apply Phenotype Default Navigation Rules?}
    AD -- Yes --> AE(Infer implicit targets based on type: Exam/Profile back to Hub/List; List to Profile/Exam; Success/Fail back to source/Hub etc.)
    AD -- No --> AF(Proceed)
    AE --> AF
    AF --> AG(Map Conceptual/Node Targets to Target Entry Point IDs)
    AG --> AH(Record potential Edges: Source Node ID -> Target Entry Point ID)
    AH --> Z
    Z --> AI{All nodes mapped?}
    AI -- Yes --> AJ(Phase 4: Validate & Refine Graph)
    AJ --> AK(Collect All Defined Entry Point IDs)
    AK --> AL(Perform Reachability Check from Hook/Intro)
    AL --> AM{Are there Orphaned Entry Points?}
    AM -- Yes --> AN(Add default Edges from INVESTIGATION_HUB to Orphans)
    AM -- No --> AO(Proceed)
    AN --> AO
    AO --> AP(Consolidate & Validate Edge List)
    AP --> AQ(Remove illogical/redundant edges: e.g., Resolution -> anything)
    AQ --> AR(Phase 5: Final Assembly)
    AR --> AS(Structure Nodes & Edges into Schema Format)
    AS --> AT(Assign Final Sequential step_index for output order)
    AT --> AU(Generate JSON Output)
    AU --> B_END(End)


Generalized Tree of Thought / Internal Strategy:

Deconstruction & Atomization:

Goal: Break down the potentially linear or branched input text into discrete, atomic units of player interaction or narrative delivery.

Process: Read through the input step-by-step, but think of each point as a description of a potential game state or interaction, not just the next item in a list.

Key Questioning: What is the player doing here? What information are they receiving? What decision are they making? What type of game activity does this represent (exploring, reading, solving, talking, concluding)? Does this single description cover multiple distinct actions (like finding something and immediately solving a puzzle about it)? If so, identify where the logical split points are.

Phenotype Identification & Description:

Goal: Classify each atomic unit according to the predefined phenotype types and create a clear, implementable description.

Process: Map the identified player activity/narrative purpose to the most appropriate phenotype tag (CASE_HOOK, EVIDENCE_COLLECTION, DEDUCTION_PUZZLE, SUSPECT_PROFILE, BREAKTHROUGH, etc.). Ignore implementation details (like "CREATE ADA_IntroScreen") in the description, focusing on the player's experience ("Engage with the initial report"). Determine where the content for this step originates in the source data for the description reference.

Identify Navigation Targets & Entry Points:

Goal: Define stable, reliable points in the narrative graph that other nodes can link to.

Process: Scan the identified phenotypes for types that typically serve as destinations: the main investigation area/hub, lists of items/suspects, the start of specific investigation branches (like entering a new location for collection), specific suspect profiles, or key deduction puzzles/breakthroughs. Assign these nodes their own ID as their entry_point_id. For nodes that are part of a sequence within a larger conceptual unit (e.g., examining file A, then file B, then file C within the Vet Clinic), their entry_point_id conceptually might tie back to the start of that sequence (EVIDENCE_COLLECTION_VetClinic), but for implementable distinctness, each node often gets its own ID as its entry point, allowing deep linking or specific targeting if needed. The key conceptual entry points (HUB, Lists, major collection areas) are explicitly noted and mapped by a conceptual name ("Case_Board", "Suspect_List_View") for easier targeting.

Map Potential Connections (Edges):

Goal: Determine where the player can go from each node based on their choices, unlocked content, or logical flow.

Process: Examine the ACTION field and OPTIONS within the source data for explicit navigation commands (NAVIGATE TO, TRIGGER). Translate these into directed edges from the current node to the entry_point_id of the target node(s). Supplement explicit links with phenotype-based default navigation:

From decision points (like INTRO_SEQUENCE options or Hypothesis checks), link to the start of the consequent branches (often EVIDENCE_COLLECTION nodes).

From information-gathering nodes (EVIDENCE_EXAMINATION, SUSPECT_PROFILE, Deduction Success/Failure outcomes), link back to the main INVESTIGATION_HUB or potentially a relevant list (SUSPECT_LIST, etc.) to allow continued investigation.

From list nodes (SUSPECT_LIST, perhaps EVIDENCE_COLLECTION if it lists items), link to the associated examination/profile nodes.

From nodes requiring follow-up actions (like EVIDENCE_EXAMINATION prompting a search for a full log), link to the HUB or relevant collection area.

Ensure success/failure branches from DEDUCTION_PUZZLEs lead to distinct outcome nodes (DEDUCTION_SUCCESS/FAILURE) and then potentially diverge from there (e.g., Success leads forward, Failure loops back or returns to hub).

Connect major progression points: Breakthroughs often lead to Confrontation, Confrontation leads to Accusation, Accusation leads to Resolution.

Validate Graph Structure:

Goal: Ensure the resulting network of nodes and edges forms a coherent, navigable structure where key objectives are reachable.

Process: Mentally (or computationally) traverse the graph. Can a player starting at the beginning reach all significant investigative branches, all suspect profiles, all breakthrough moments, the confrontation, accusation, and resolution states? If key entry points are unreachable from the starting path or the main HUB, add default edges (typically from the HUB) to connect them, ensuring all major content clusters are accessible. Remove any illogical links (e.g., a Case Resolution node shouldn't lead anywhere within the case).

This thought process prioritizes the player's experience and agency, breaking down the source material into the fundamental building blocks (phenotypes) and then rebuilding them into a flexible, connected graph that supports non-linear exploration while guiding the player towards the case resolution.

Output expanded information following ONLY the player journey below. Output the exact number of steps described in the text:

{{player_journey}} 
---/COMMAND---