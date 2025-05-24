import json
import difflib
from collections import Counter, defaultdict
import copy

# --- Helper Functions ---

def find_aspects_in_check(check_obj):
    """Recursively finds aspect names within nested check structures."""
    aspects = set()
    if isinstance(check_obj, dict):
        if 'aspect' in check_obj:
            aspects.add(check_obj['aspect'])
        # Recursively check nested structures like 'and', 'or', 'not'
        for key, value in check_obj.items():
            if isinstance(value, (dict, list)):
                 aspects.update(find_aspects_in_check(value)) # Check nested dicts
            # Specifically check lists which might contain check objects (e.g., in 'and'/'or')
            elif key in ('and', 'or') and isinstance(value, list):
                 for item in value:
                     aspects.update(find_aspects_in_check(item))
    elif isinstance(check_obj, list): # Handle lists of checks directly if needed
        for item in check_obj:
            aspects.update(find_aspects_in_check(item))
    return aspects

def attempt_repair(incorrect_key, valid_keys_set, repair_type="key", cutoff=0.8, force_best_match=False):
    """
    Attempts to find a single close match for an incorrect key.
    If force_best_match is True, uses cutoff=0.0 to find the single best match regardless of similarity.
    """
    if not incorrect_key or not isinstance(incorrect_key, str) or not valid_keys_set:
        return None, None # Cannot repair empty/non-string keys or if valid set is empty

    # Always try case-insensitive first as it's exact if it works
    lower_incorrect = incorrect_key.lower()
    case_insensitive_matches = [k for k in valid_keys_set if k.lower() == lower_incorrect]
    if len(case_insensitive_matches) == 1:
        corrected_key = case_insensitive_matches[0]
        if corrected_key != incorrect_key:
             repair_info = f"Repaired {repair_type} via case-insensitive match: '{incorrect_key}' -> '{corrected_key}'"
             return corrected_key, repair_info
        else:
             return corrected_key, None # It was already correct

    # Determine the cutoff for fuzzy matching
    match_cutoff = 0.0 if force_best_match else cutoff
    match_method = "best fuzzy match" if force_best_match else f"fuzzy match (cutoff={cutoff})"

    close_matches = difflib.get_close_matches(incorrect_key, valid_keys_set, n=1, cutoff=match_cutoff)

    if len(close_matches) == 1:
        corrected_key = close_matches[0]
        # Only report as repair if it actually changed the key
        if corrected_key != incorrect_key:
             repair_info = f"Repaired {repair_type} via {match_method}: '{incorrect_key}' -> '{corrected_key}'"
             return corrected_key, repair_info
        else:
             return corrected_key, None # It matched itself, no repair needed
    else:
        # No single close match found (or empty valid_keys_set)
        return None, None

# --- Main Validation/Repair Function ---

def validate_and_repair_twine_state(state_dict, repair_enabled=False, cutoff=0.8):
    """
    Validates and optionally repairs the 'evidence' and 'passages' lists
    within a given state dictionary.
    If repair_enabled, attempts to fix duplicate passage names by renaming
    subsequent occurrences and adding a 'BROKEN_DUPLICATE_RENAMED' tag.
    Always attempts to repair evidence references to the best fuzzy match.
    Uses cutoff for other repairs like aspect names.

    Args:
        state_dict (dict): The dictionary containing 'evidence' and 'passages' lists.
        repair_enabled (bool): If True, attempt to repair errors (including duplicate names).
        cutoff (float): Similarity cutoff for fuzzy matching repairs (e.g., aspects), range 0.0-1.0.

    Returns:
        tuple: (list_of_errors, list_of_repairs, potentially_modified_state_dict)
    """
    errors = []
    repairs = []
    ambiguous_moves = defaultdict(list)
    missing_aspects = set()  # Track missing aspects to be added to init

    current_state = copy.deepcopy(state_dict) # Always deepcopy now, as rename might happen even if other repairs are off

    if not isinstance(current_state, dict):
         return ["Error: Input state is not a dictionary."], [], state_dict

    evidence_list = current_state.get('evidence')
    passages_list = current_state.get('passages')

    if not isinstance(evidence_list, list):
        errors.append("Error: 'evidence' key is missing or not an array in state.")
    if not isinstance(passages_list, list):
        errors.append("Error: 'passages' key is missing or not an array in state.")

    if errors:
        return errors, [], state_dict

    # --- Data Collection --- (Initial pass for detection)
    evidence_uids = {e.get('uid') for e in evidence_list if isinstance(e, dict) and e.get('uid')}
    initial_passage_name_to_uids = defaultdict(list) # Store original mapping
    initial_passage_names = []
    for p in passages_list:
        if isinstance(p, dict):
            name = p.get('name')
            uid = p.get('uid')
            if name:
                 initial_passage_names.append(name)
            if name and uid:
                 initial_passage_name_to_uids[name].append(uid)
            elif name:
                 initial_passage_name_to_uids[name].append("[Missing UID]")

    # --- Duplicate Name Detection --- (Based on initial names)
    name_counts = Counter(initial_passage_names)
    original_duplicate_names = {name for name, count in name_counts.items() if count > 1}

    # --- Rename/Tag Duplicates Pass (if repair enabled) ---
    renamed_passages_map = {} # Keep track of renames {old_name: [new_name_1, new_name_2]} for reporting
    if repair_enabled and original_duplicate_names:
        seen_names_in_pass = set()
        duplicate_counters = Counter()
        broken_tag = {"name": "BROKEN_DUPLICATE_RENAMED", "color": "red"}

        for passage in passages_list:
             if isinstance(passage, dict):
                 name = passage.get('name')
                 uid = passage.get('uid', "[Unknown UID]")
                 if name in original_duplicate_names:
                     if name in seen_names_in_pass:
                         duplicate_counters[name] += 1
                         new_name = f"{name}_{duplicate_counters[name]}"
                         passage['name'] = new_name
                         if name not in renamed_passages_map:
                             renamed_passages_map[name] = []
                         renamed_passages_map[name].append(new_name)
                         if 'tags' not in passage or not isinstance(passage['tags'], list):
                             passage['tags'] = []
                         if broken_tag not in passage['tags']:
                             passage['tags'].append(broken_tag)
                         repairs.append(f"Duplicate Passage Name: Renamed passage (UID: {uid}) from '{name}' to '{new_name}' and added BROKEN tag.")
                     else:
                         seen_names_in_pass.add(name)
                 elif name:
                     seen_names_in_pass.add(name)

    # --- Update FINAL Name/UID Mappings After Potential Rename --- (Used for target validation)
    final_passage_name_to_uids = defaultdict(list)
    final_passage_uid_to_name = {}
    final_passage_uids = set()
    final_passage_names_lower = {} # Map lowercase names to original names
    for p in passages_list:
        if isinstance(p, dict):
            name = p.get('name')
            uid = p.get('uid')
            if name and uid:
                final_passage_name_to_uids[name].append(uid)
                final_passage_uid_to_name[uid] = name
                final_passage_uids.add(uid)
                final_passage_names_lower[name.lower()] = name
            elif name:
                final_passage_name_to_uids[name].append("[Missing UID]")
            elif uid:
                final_passage_uids.add(uid)

    # --- Report Original Duplicates if Repair Not Enabled ---
    if not repair_enabled and original_duplicate_names:
         for name in original_duplicate_names:
             uids = initial_passage_name_to_uids.get(name, []) # Use initial map for reporting UIDs
             uid_str = ", ".join(uids)
             errors.append(f"Duplicate Passage Name Error: Name '{name}' is used by multiple passages (UIDs: {uid_str}). Enable repair mode to rename/tag duplicates or fix manually.")

    if not final_passage_name_to_uids and not any(p.get('name') for p in passages_list if isinstance(p, dict)):
         errors.append("Warning: No passage names found to check for duplicates.")

    # --- Aspect Validation ---
    created_aspects = set()
    init_passage = None
    init_passage_index = -1
    
    for idx, passage in enumerate(passages_list): # Iterate through passages in current_state
        if isinstance(passage, dict) and passage.get('name') == "Initialization":
            init_passage = passage
            init_passage_index = idx
            init_commands = passage.get('commands', [])
            if isinstance(init_commands, list):
                for command in init_commands:
                    if isinstance(command, dict) and command.get('type') == 'createAspect':
                        aspect_name = command.get('aspect')
                        if aspect_name:
                            created_aspects.add(aspect_name)
                        else:
                             errors.append(f"Initialization passage: Found 'createAspect' command missing 'aspect' field: {command}")
            else:
                 errors.append("Initialization passage: 'commands' field is not a list.")
            break

    if not init_passage:
        errors.append("Warning: 'Initialization' passage not found. Cannot validate aspect creation.")
    elif not created_aspects:
         errors.append("Warning: No aspects found created in the 'Initialization' passage.")

    # --- Recursive Command Checker --- (Operates on current_state)
    # Needs access to: errors, repairs, evidence_uids, passage_uids, created_aspects
    # Needs access to: repair_enabled, cutoff
    # Modifies: command dictionaries within current_state if repairs happen
    def check_command(command, parent_obj, parent_key, current_passage_uid, current_passage_name):
        if not isinstance(command, dict):
            errors.append(f"Warning: Found non-dictionary command in passage '{current_passage_name}' (UID: {current_passage_uid}) at {parent_key}")
            return

        command_type = command.get('type')

        try:
            # Check Action Commands
            if command_type == 'action':
                action_type = command.get('actionType')

                if action_type not in ['MOVE', 'HIDE_ALL_EVIDENCE'] and 'evidenceTarget' in command:
                    evidence_target = command.get('evidenceTarget')
                    if evidence_target not in evidence_uids:
                        error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): Action '{action_type}' references non-existent evidence UID in 'evidenceTarget': '{evidence_target}'"
                        repaired = False
                        if repair_enabled:
                            # Use force_best_match=True for evidence
                            corrected_key, repair_info = attempt_repair(evidence_target, evidence_uids, "evidence UID", force_best_match=True)
                            if corrected_key:
                                command['evidenceTarget'] = corrected_key
                                repairs.append(f"{error_msg} -> {repair_info}")
                                repaired = True
                        if not repaired:
                             errors.append(error_msg)

                elif action_type == 'MOVE':
                    move_target_data = command.get('moveTarget')
                    if isinstance(move_target_data, dict):
                        target_type = move_target_data.get('type')
                        if target_type == 'passage' and 'passageTarget' in move_target_data:
                            # Extract the target from MOVE action
                            passage_target = move_target_data.get('passageTarget')
                            
                            # Check if it's a UID first (direct match against final_passage_uids)
                            if passage_target in final_passage_uids:
                                # It's a valid UID - no error needed
                                pass
                            # If not a UID, check if it's a name (case-insensitive)
                            elif passage_target.lower() in final_passage_names_lower:
                                # Get the correct case version of the name
                                correct_case_name = final_passage_names_lower[passage_target.lower()]
                                if repair_enabled:
                                    # Fix the case in the moveTarget
                                    move_target_data['passageTarget'] = correct_case_name
                                    repairs.append(f"Fixed case sensitivity in passage target: '{passage_target}' -> '{correct_case_name}'")
                                # Check if the target name was originally a duplicate
                                if correct_case_name in original_duplicate_names:
                                    source_info = f"Passage '{current_passage_name}' (UID: {current_passage_uid})"
                                    ambiguous_moves[correct_case_name].append(source_info)
                            else:
                                # Neither a valid UID nor a valid name - try to find closest match
                                if repair_enabled:
                                    # Try to find closest matching passage with very low cutoff
                                    closest_matches = difflib.get_close_matches(passage_target, list(final_passage_uids) + list(final_passage_names_lower.keys()), n=1, cutoff=0.3)
                                    if closest_matches:
                                        closest_match = closest_matches[0]
                                        # If the match is a name, get its UID
                                        if closest_match in final_passage_names_lower:
                                            closest_match = final_passage_names_lower[closest_match]
                                        move_target_data['passageTarget'] = closest_match
                                        repairs.append(f"Fixed non-existent passage target: '{passage_target}' -> '{closest_match}'")
                                    else:
                                        # No close match found - point to initialization passage as fallback
                                        move_target_data['passageTarget'] = "p-init"
                                        repairs.append(f"Fixed non-existent passage target by pointing to initialization: '{passage_target}' -> 'p-init'")
                                else:
                                    # Neither a valid UID nor a valid name
                                    error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): MOVE action references non-existent passage (neither UID nor name) in 'moveTarget.passageTarget': '{passage_target}'"
                                    errors.append(error_msg)
                        elif target_type == 'evidence' and 'evidenceTarget' in move_target_data:
                            # Evidence checks remain unchanged
                            evidence_target = move_target_data.get('evidenceTarget')
                            if evidence_target not in evidence_uids:
                                error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): MOVE action references non-existent evidence UID in 'moveTarget.evidenceTarget': '{evidence_target}'"
                                repaired = False
                                if repair_enabled:
                                    # Use force_best_match=True for evidence
                                    corrected_key, repair_info = attempt_repair(evidence_target, evidence_uids, "evidence UID", force_best_match=True)
                                    if corrected_key:
                                        move_target_data['evidenceTarget'] = corrected_key
                                        repairs.append(f"{error_msg} -> {repair_info}")
                                        repaired = True
                                if not repaired:
                                     errors.append(error_msg)
                    else:
                         errors.append(f"Passage '{current_passage_name}' (UID: {current_passage_uid}): MOVE action has invalid 'moveTarget' data.")

            # Check UpdateAspect Commands
            elif command_type == 'updateAspect':
                 aspect_to_update = command.get('aspect')
                 if aspect_to_update:
                     if aspect_to_update not in created_aspects:
                         error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): updateAspect command references uncreated aspect: '{aspect_to_update}'"
                         repaired = False
                         if repair_enabled:
                            # Use default cutoff for aspects (force_best_match=False)
                            corrected_key, repair_info = attempt_repair(aspect_to_update, created_aspects, "aspect name", cutoff=cutoff)
                            if corrected_key:
                                command['aspect'] = corrected_key
                                repairs.append(f"{error_msg} -> {repair_info}")
                                repaired = True
                            else:
                                # Add to missing_aspects if we couldn't find a close match
                                missing_aspects.add(aspect_to_update)
                                repaired = True
                         if not repaired:
                             errors.append(error_msg)
                 else:
                      errors.append(f"Passage '{current_passage_name}' (UID: {current_passage_uid}): updateAspect command missing 'aspect' field: {command}")

            # --- Recursive Checks for Nested Commands ---
            elif command_type == 'bot':
                branch = command.get('branch')
                if branch:
                    check_command(branch, command, 'branch', current_passage_uid, current_passage_name)

            elif command_type == 'branch':
                options = command.get('options', [])
                if isinstance(options, list):
                     for i, option in enumerate(options):
                         if isinstance(option, dict):
                             aspect_check = option.get('aspectCheck')
                             if aspect_check and isinstance(aspect_check, dict):
                                 check_details = aspect_check.get('check')
                                 if check_details:
                                    referenced_aspects = find_aspects_in_check(check_details)
                                    invalid_aspects_found = {a for a in referenced_aspects if a not in created_aspects}
                                    if invalid_aspects_found:
                                         for aspect in invalid_aspects_found:
                                             error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): Branch option '{option.get('name', f'[Index {i}]')}' uses uncreated aspect in aspectCheck: '{aspect}'"
                                             if repair_enabled:
                                                # Add to missing_aspects for later creation
                                                missing_aspects.add(aspect)
                                             else:
                                                errors.append(error_msg)

                             actions = option.get('actions', [])
                             if isinstance(actions, list):
                                 for j, action in enumerate(actions):
                                     check_command(action, option, f'actions[{j}]', current_passage_uid, current_passage_name)

            elif command_type == 'trigger':
                targets = command.get('targets', [])
                if isinstance(targets, list):
                    for i, target in enumerate(targets):
                         if isinstance(target, dict) and 'evidenceTarget' in target:
                            evidence_target = target.get('evidenceTarget')
                            if evidence_target is not None and evidence_target not in evidence_uids:
                                error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): Trigger target {i} references non-existent evidence UID: '{evidence_target}'"
                                repaired = False
                                if repair_enabled:
                                    # Use force_best_match=True for evidence
                                    corrected_key, repair_info = attempt_repair(evidence_target, evidence_uids, "evidence UID", force_best_match=True)
                                    if corrected_key:
                                        target['evidenceTarget'] = corrected_key
                                        repairs.append(f"{error_msg} -> {repair_info}")
                                        repaired = True
                                if not repaired:
                                    errors.append(error_msg)
                actions = command.get('actions', [])
                if isinstance(actions, list):
                    for i, action in enumerate(actions):
                         check_command(action, command, f'actions[{i}]', current_passage_uid, current_passage_name)

            elif command_type == 'chatTrigger':
                 actions = command.get('actions', [])
                 if isinstance(actions, list):
                     for i, action in enumerate(actions):
                          check_command(action, command, f'actions[{i}]', current_passage_uid, current_passage_name)

            elif command_type == 'intro':
                actions = command.get('actions', [])
                if isinstance(actions, list):
                    for i, action in enumerate(actions):
                        check_command(action, command, f'actions[{i}]', current_passage_uid, current_passage_name)

            elif command_type == 'passwordGuesser':
                guess_list = command.get('guessList', [])
                if isinstance(guess_list, list):
                     for i, guess in enumerate(guess_list):
                         if isinstance(guess, dict):
                             actions = guess.get('actions', [])
                             if isinstance(actions, list):
                                 for j, action in enumerate(actions):
                                     check_command(action, guess, f'actions[{j}]', current_passage_uid, current_passage_name)

            elif command_type == 'if':
                aspect_check = command.get('aspectCheck')
                if aspect_check and isinstance(aspect_check, dict):
                    check_details = aspect_check.get('check')
                    if check_details:
                        referenced_aspects = find_aspects_in_check(check_details)
                        invalid_aspects_found = {a for a in referenced_aspects if a not in created_aspects}
                        if invalid_aspects_found:
                             for aspect in invalid_aspects_found:
                                 error_msg = f"Passage '{current_passage_name}' (UID: {current_passage_uid}): 'if' command uses uncreated aspect in aspectCheck: '{aspect}'"
                                 if repair_enabled:
                                    # Add to missing_aspects for later creation
                                    missing_aspects.add(aspect)
                                 else:
                                    errors.append(error_msg)
                actions = command.get('actions', [])
                if isinstance(actions, list):
                     for i, action in enumerate(actions):
                         check_command(action, command, f'actions[{i}]', current_passage_uid, current_passage_name)

        except Exception as e:
            errors.append(f"Error processing command in passage '{current_passage_name}' (UID: {current_passage_uid}). Command: {command}. Error: {e}")


    # --- Iterate and Validate/Repair All Passages --- (Using current_state)
    if isinstance(passages_list, list):
        for i, passage in enumerate(passages_list):
            if not isinstance(passage, dict):
                errors.append(f"Found non-dictionary item in 'passages' list at index {i}: {passage}")
                continue

            passage_uid = passage.get('uid')
            passage_name = passage.get('name')
            # Handle missing UID/Name for error reporting context
            if not passage_uid:
                errors.append(f"Found passage at index {i} with missing UID: {passage}")
                if not passage_name: passage_name = "[Unknown Name]"
                passage_uid = f"[Missing UID at Index {i}]"
            elif not passage_name:
                 errors.append(f"Found passage with missing Name (UID: {passage_uid}): {passage}")
                 passage_name = "[Missing Name]"


            commands_list = passage.get('commands')
            if isinstance(commands_list, list):
                for j, command_item in enumerate(commands_list):
                     # Pass the passage dict as parent, and 'commands' list + index as key info
                     check_command(command_item, passage, f'commands[{j}]', passage_uid, passage_name)
            elif commands_list is not None:
                 errors.append(f"Passage '{passage_name}' (UID: {passage_uid}) has 'commands' field that is not a list.")

    # --- Add Ambiguous Move Warnings --- (After all passages checked)
    if ambiguous_moves:
         for name, sources in ambiguous_moves.items():
             source_str = "; ".join(sources)
             renamed_versions = renamed_passages_map.get(name, [])
             target_suggestion = f" (e.g., {', '.join(renamed_versions)})" if renamed_versions else ""
             errors.append(f"Ambiguous MOVE Target Warning: Original passage name/UID '{name}' was duplicated. MOVE actions targeting it from sources [{source_str}] may now incorrectly point to the first instance. Please manually check if they should target a renamed version{target_suggestion} instead.")

    # --- Add missing aspects to the Initialization passage if repair is enabled
    if repair_enabled and missing_aspects and init_passage:
        for aspect in missing_aspects:
            # Create a new createAspect command
            create_aspect_cmd = {
                "type": "createAspect",
                "aspect": aspect,
                "value": 0  # Default initial value
            }
            
            # Add to the initialization passage commands
            if 'commands' not in init_passage or not isinstance(init_passage['commands'], list):
                init_passage['commands'] = []
            
            # Add the command and update the created_aspects set
            init_passage['commands'].append(create_aspect_cmd)
            created_aspects.add(aspect)
            repairs.append(f"Added missing aspect '{aspect}' to Initialization passage with default value 0")
    
    # Return errors, repairs, and the potentially modified state
    return errors, repairs, current_state


# --- Example of how to call it in a notebook cell ---
#if __name__ == '__main__': # Use this guard if pasting into a script that might also be imported

# 1. Set parameters
should_repair = True
fuzzy_cutoff = 0.8 # Use a more sensible default cutoff for other repairs

print("\n--- Running Validation ---")
# 2. Call the function
errors, repairs, final_state = validate_and_repair_twine_state(
    state, # Pass your state dictionary
    repair_enabled=should_repair,
    cutoff=fuzzy_cutoff
)

# 3. Print results (Keep this section as is)
print("\n--- Repairs Applied ---")
if repairs:
    for i, r in enumerate(repairs, 1): print(f"{i}. {r}\n")
else:
    print("None")

print("\n--- Errors Remaining ---")
if errors:
    for i, e in enumerate(errors, 1): print(f"{i}. {e}\n")
else:
    print("None")

# 4. Update the original 'state' variable IF repairs were made
print("\n--- Updating State ---")
if repairs and should_repair: # Use 'repairs' which contains the list returned
    print(f"Updating original 'state' variable with {len(repairs)} applied repairs.")
    state['evidence'] = final_state['evidence'] # Update specific keys
    state['passages'] = final_state['passages']
else:
    print("No repairs applied or repair was disabled. Original 'state' variable remains unchanged.")

def check_move_command(passage_uid, command, ctx, json_state, final_passage_uids, final_passage_name_to_uids, ambiguous_moves):
    errors = []
    repairs = []
    
    # MOVE commands
    if command.get("action", "").strip().upper() == "MOVE":
        # Get the move target
        move_target = command.get("moveTarget", {})
        # Check if it is a valid object, if not we need to repair it
        if not isinstance(move_target, dict):
            errors.append(f"{passage_uid}: MOVE action specified without valid moveTarget object")
            return errors, repairs
            
        passage_target = move_target.get("passageTarget", "")
        
        if ctx.debug:
            print(f"DEBUG: Checking MOVE target '{passage_target}' from passage {passage_uid}")
            print(f"DEBUG: Is target in UIDs? {passage_target in final_passage_uids}")
            if passage_target not in final_passage_uids:
                print(f"DEBUG: Is target in names? {passage_target in final_passage_name_to_uids}")
                if passage_target in final_passage_name_to_uids:
                    print(f"DEBUG: Target maps to UIDs: {final_passage_name_to_uids[passage_target]}")
        
        # First check if the passage_target is a valid UID
        if passage_target in final_passage_uids:
            return errors, repairs
        
        # If not a UID, check if it's a valid name
        if passage_target not in final_passage_name_to_uids:
            errors.append(f"{passage_uid}: MOVE action references non-existent passage name or UID '{passage_target}'")
            return errors, repairs
            
        # Check for ambiguous moves (when a name maps to multiple UIDs)
        target_uids = final_passage_name_to_uids[passage_target]
        if len(target_uids) > 1:
            if passage_target not in ambiguous_moves:
                ambiguous_moves[passage_target] = []
            ambiguous_moves[passage_target].append(passage_uid)
            
    return errors, repairs