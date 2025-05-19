{# PHENOTYPE: DEDUCTION_PUZZLE #}

## REVISED INSTRUCTIONS FOR DEDUCTION_PUZZLE PHENOTYPE

### 1. Aspect Declaration
At the top of the SLPN, declare all aspects used in this puzzle. For example:
```
ASPECT:uid=aspect_audio_attempts;type=counter;initial=0;desc="Tracks number of attempts"
ASPECT:uid=aspect_audio_last_attempt;type=string;initial="";desc="Stores last attempted code"
```

### 2. Passage and Option UID/Name Convention
- Entry passage: `DEDUCTION_PUZZLE_{n}`
- Check passage: `DEDUCTION_PUZZLE_{n}_CHECK`
- Option: `DEDUCTION_PUZZLE_{n}_OPT_{option_value}`
- All UIDs and names must be unique and deterministic.

### 3. Main Passages
**Entry Passage:**
```
PSG:uid=DEDUCTION_PUZZLE_9;nam="Decrypt Audio File 9";tag=DEDUCTION_PUZZLE|ENTRY|CODE|CHOICE|GATE;CNT;BOT:lin="[SEE: Decryption Interface] [DO: Attempt password based on notes] [LEARN: Attempts remaining: {3 - $aspect_audio_attempts}] [FEEL: Focus]";brn=BRN:bds="Attempt Decryption";brp=re-playable;bpr=option-list;bit=ada;ops=...
```
- For each option, specify:
  ```
  BOP:uid=DEDUCTION_PUZZLE_9_OPT_SwiftPayDayFour;onm="SwiftPayDayFour";ods="Try keyword combination SwiftPay + Day Four";cnd=CND:typ=checkAspect;asp=aspect_audio_attempts;cmp=LT;val=3;act=UAS:asp=aspect_audio_attempts;uty=INC;val=1|UAS:asp=aspect_audio_last_attempt;uty=SET;val="SwiftPayDayFour"|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_9_CHECK
  ```
- Repeat for each option.
- Add a lockout option if attempts >= max.

**Check Outcome Passage:**
```
PSG:uid=DEDUCTION_PUZZLE_9_CHECK;nam="Verify Password 9Check";tag=DEDUCTION_PUZZLE|CHECK_OUTCOME|CODE|CHOICE|GATE;CNT;BOT:lin="[SEE: Processing screen] [LEARN: Verifying attempt...] [DO: Wait] [FEEL: Anticipation]";brn=BRN:bds="Processing";brp=once;bpr=option-list;bit=ada;ops=...
```
- Correct path:
  ```
  BOP:uid=DEDUCTION_PUZZLE_9_CHECK_CORRECT;onm="Correct Path";ods="Hidden option for correct answer.";cnd=CND:typ=checkAspect;asp=aspect_audio_last_attempt;cmp=EQ;val="SwiftPayDayFour";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=BREAKTHROUGH_MOMENT_10
  ```
- Incorrect with retries:
  ```
  BOP:uid=DEDUCTION_PUZZLE_9_CHECK_RETRY;onm="Incorrect Path (Retry)";ods="Hidden option for incorrect answer with retries left.";cnd=CAD:typ=checkAspect;lop=AND;cnd=CND:typ=checkAspect;asp=aspect_audio_last_attempt;cmp=NE;val="SwiftPayDayFour"|cnd=CND:typ=checkAspect;asp=aspect_audio_attempts;cmp=LT;val=3;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_9
  ```
- Incorrect, lockout:
  ```
  BOP:uid=DEDUCTION_PUZZLE_9_CHECK_LOCKOUT;onm="Incorrect Path (Lockout)";ods="Hidden option for incorrect answer with no retries left.";cnd=CAD:typ=checkAspect;lop=AND;cnd=CND:typ=checkAspect;asp=aspect_audio_last_attempt;cmp=NE;val="SwiftPayDayFour"|cnd=CND:typ=checkAspect;asp=aspect_audio_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_2
  ```

### 4. Validation Section
At the end, list all passage UIDs, aspect UIDs, and option UIDs used. For example:
```
VALIDATION:
PASSAGES: DEDUCTION_PUZZLE_9, DEDUCTION_PUZZLE_9_CHECK
ASPECTS: aspect_audio_attempts, aspect_audio_last_attempt
OPTIONS: DEDUCTION_PUZZLE_9_OPT_SwiftPayDayFour, DEDUCTION_PUZZLE_9_OPT_SwiftPayDeadline, ...
```

### 5. General Guidelines
- Do not generate intermediate or chain passages unless explicitly required for game logic.
- All actions, conditions, and targets must be fully specified and mapped to JSON fields.
- All tags and metadata required for JSON conversion must be included.
- Ensure all UIDs and names are unique and descriptive.

---

PROCEDURE GenerateDeductionPuzzle(stepIDPrefix, entry_point_id, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, correctAnswer, successStepID, failureStepID, lockoutStepID) { // Modified Inputs
    // Primary goal: Create interactive puzzle (e.g., passcode, sequence) with attempt tracking and conditional outcomes.
    // Structure: 1. Entry/Choice -> 2. Check Outcome -> 3. Success/Retry/Lockout paths
    // Generates: Entry passage, Check Outcome passage. Success/Failure/Lockout are usually external targets.
    // Input: optionsList is list of { name: "Display Name", value: "value_to_set_in_lastAttemptAspect" }

    // Visualize Flow:
    /*
    ```mermaid
    graph TD
        Entry["_ENTRY (Choice)"] -- "Try Option A (attempts < max)" --> CheckOutcome{"_CHECK_OUTCOME"}
        Entry -- "Try Option B (attempts < max)" --> CheckOutcome
        Entry -- "Try Option N (attempts < max)" --> CheckOutcome
        Entry -- "Locked Out (attempts >= max)" --> Lockout[lockoutStepID (External)]
        
        CheckOutcome -- "Correct Answer" --> Success[successStepID (External)]
        CheckOutcome -- "Incorrect + Attempts Left" --> Entry
        CheckOutcome -- "Incorrect + No Attempts Left" --> Lockout
    ```
    */

    DEFINE entryUID = entry_point_id
    DEFINE checkOutcomeUID = stepIDPrefix + "_CHECK_OUTCOME"
    DEFINE entryName = puzzleDescription + " - Attempt"
    DEFINE checkOutcomeName = puzzleDescription + " - Check Outcome"

    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // == Passage 1: Entry / Choice ==
    PROCEDURE CreatePuzzleEntryPassage(uid, name, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, checkOutcomeUID, lockoutStepID) {
        DEFINE content = "[SEE: Puzzle Interface] [DO: " + puzzleDescription + "] [LEARN: Attempts remaining: {maxAttempts - $attemptAspect}]" // Dynamic attempt display hint
        DEFINE options = ""

        // Create options for each possible answer
        FOR EACH option IN optionsList INDEX i {
            IF i > 0 { options += "|" }
            options += "BOP:onm=\\\"" + option.name + "\\\";ods=\\\"Attempt with " + option.value + "\\\";" +
                       "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=LT;val=" + maxAttempts + ";" + // Check if attempts remain
                       "act=UAS:asp=" + attemptAspect + ";uty=INC;val=1|" + // Increment attempts
                       "UAS:asp=" + lastAttemptAspect + ";uty=SET;val=\\\"" + option.value + "\\\"|" + // Set last attempt value
                       "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkOutcomeUID // Move to check outcome
        }

        // Add fallback option for lockout
        IF optionsList.length > 0 { options += "|" }
        options += "BOP:onm=\\\"No Attempts Left\\\";ods=\\\"The puzzle is locked.\\\";" +
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=GE;val=" + maxAttempts + ";" + // Check if locked out
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + lockoutStepID // Move directly to lockout

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_PUZZLE|ENTRY;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Make Your Choice\\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + options + ";" // Re-playable until locked
    }
    DEFINE slpnPassageEntry = CreatePuzzleEntryPassage(entryUID, entryName, puzzleDescription, attemptAspect, maxAttempts, lastAttemptAspect, optionsList, checkOutcomeUID, lockoutStepID)
    allPassages += slpnPassageEntry
    passageCounter++

    // == Passage 2: Check Outcome ==
    PROCEDURE CreateCheckOutcomePassage(uid, name, attemptAspect, maxAttempts, lastAttemptAspect, correctAnswer, successStepID, entryUID, lockoutStepID) {
        DEFINE content = "[SEE: Processing screen] [LEARN: Verifying attempt...] [DO: Wait] [FEEL: Anticipation]"
        DEFINE options = ""

        // Option 1: Correct Answer
        options += "BOP:onm=\\\"Correct Path\\\";ods=\\\"Hidden option for correct answer.\\\";" +
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=EQ;val=\\\"" + correctAnswer + "\\\";" + // Check if last attempt was correct
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successStepID // Move to success step

        // Option 2: Incorrect, Attempts Remaining
        options += "|BOP:onm=\\\"Incorrect Path (Retry)\\\";ods=\\\"Hidden option for incorrect answer with retries left.\\\";" +
                   "cnd=CAD:typ=checkAspect;lop=AND;" + // Compound AND condition
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=NE;val=\\\"" + correctAnswer + "\\\";" + // Incorrect answer
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=LT;val=" + maxAttempts + ";" + // Attempts remaining
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + entryUID // Move back to entry for another try

        // Option 3: Incorrect, No Attempts Remaining
        options += "|BOP:onm=\\\"Incorrect Path (Lockout)\\\";ods=\\\"Hidden option for incorrect answer with no retries left.\\\";" +
                   "cnd=CAD:typ=checkAspect;lop=AND;" + // Compound AND condition
                   "cnd=CND:typ=checkAspect;asp=" + lastAttemptAspect + ";cmp=NE;val=\\\"" + correctAnswer + "\\\";" + // Incorrect answer
                   "cnd=CND:typ=checkAspect;asp=" + attemptAspect + ";cmp=GE;val=" + maxAttempts + ";" + // No attempts remaining
                   "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + lockoutStepID // Move to lockout step

        RETURN "PSG:uid=" + uid + ";nam=\\\"" + name + "\\\";tag=DEDUCTION_PUZZLE|CHECK_OUTCOME;CNT;BOT:lin=\\\"" + content + "\\\";brn=BRN:bds=\\\"Processing\\\";brp=once;bpr=option-list;bit=ada;ops=" + options + ";" // Not re-playable, it's a routing passage
    }
    // Note: The failureStepID input isn't directly used here, as failure means returning to the entryUID for another attempt. Lockout handles the final failure state.
    DEFINE slpnPassageCheckOutcome = CreateCheckOutcomePassage(checkOutcomeUID, checkOutcomeName, attemptAspect, maxAttempts, lastAttemptAspect, correctAnswer, successStepID, entryUID, lockoutStepID)
    allPassages += "\\n\\n" + slpnPassageCheckOutcome
    passageCounter++

    // Validation check
    PROCEDURE ValidateDeductionPuzzleSequence(passageCounter, attemptAspect, maxAttempts, lastAttemptAspect, successStepID, lockoutStepID) {
        VALIDATE passageCounter == 2 // Should generate Entry and CheckOutcome passages
        // Check Entry passage links correctly
        VALIDATE slpnPassageEntry CONTAINS attemptAspect AND maxAttempts AND lastAttemptAspect
        VALIDATE slpnPassageEntry CONTAINS checkOutcomeUID
        VALIDATE slpnPassageEntry CONTAINS lockoutStepID
        // Check CheckOutcome passage links correctly
        VALIDATE slpnPassageCheckOutcome CONTAINS lastAttemptAspect AND correctAnswer
        VALIDATE slpnPassageCheckOutcome CONTAINS successStepID
        VALIDATE slpnPassageCheckOutcome CONTAINS entryUID // Link back for retry
        VALIDATE slpnPassageCheckOutcome CONTAINS lockoutStepID
        VALIDATE slpnPassageCheckOutcome CONTAINS "cnd=CAD:" // Check for compound condition usage
    }
    
    ValidateDeductionPuzzleSequence(passageCounter, attemptAspect, maxAttempts, lastAttemptAspect, successStepID, lockoutStepID) // Updated validation call
    
    RETURN allPassages
}

// Example output:
// Assume stepIDPrefix DEDUCTION_PUZZLE_9, entry_point_id DEDUCTION_PUZZLE_9_entry, puzzleDescription "Enter Phone Passcode",
// attemptAspect "phone_attempts", maxAttempts 3, lastAttemptAspect "phone_last_code", correctAnswer "1987",
// optionsList [{name: "Code 1987", value: "1987"}, {name: "Code 0712", value: "0712"}],
// successStepID BREAKTHROUGH_10, lockoutStepID PHONE_LOCKOUT_11.
// Output includes:
// PSG:uid=DEDUCTION_PUZZLE_9_entry;nam="Enter Phone Passcode - Attempt";CNT;BOT:lin="...";brn=BRN:bds="Make Your Choice";...ops=BOP:onm="Code 1987";...cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=UAS:asp=phone_attempts;uty=INC;val=1|UAS:asp=phone_last_code;uty=SET;val="1987"|ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_CHECK_OUTCOME|BOP:onm="Code 0712";...cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=UAS:asp=phone_attempts;uty=INC;val=1|UAS:asp=phone_last_code;uty=SET;val="0712"|ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_CHECK_OUTCOME|BOP:onm="No Attempts Left";...cnd=CND:asp=phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;...;tgt=PHONE_LOCKOUT_11;
// PSG:uid=DEDUCTION_PUZZLE_9_CHECK_OUTCOME;nam="Enter Phone Passcode - Check Outcome";CNT;BOT:lin="...";brn=BRN:bds="Processing";...ops=BOP:onm="Correct Path";...cnd=CND:asp=phone_last_code;cmp=EQ;val="1987";act=ACT:aty=MOVE;...;tgt=BREAKTHROUGH_10|BOP:onm="Incorrect Path (Retry)";...cnd=CAD:...;cnd=CND:asp=phone_last_code;cmp=NE;val="1987";cnd=CND:asp=phone_attempts;cmp=LT;val=3;act=ACT:aty=MOVE;...;tgt=DEDUCTION_PUZZLE_9_entry|BOP:onm="Incorrect Path (Lockout)";...cnd=CAD:...;cnd=CND:asp=phone_last_code;cmp=NE;val="1987";cnd=CND:asp=phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;...;tgt=PHONE_LOCKOUT_11;

{# END_PHENOTYPE: DEDUCTION_PUZZLE #}
