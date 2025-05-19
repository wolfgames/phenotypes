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
                         "brn=BRN:bds=\"Set Variables or Check\";brp=re-playable;bpr=option-list;bit=ada;"
    
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
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=ada;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        // False setting passage
        DEFINE falseContent = CreateVariableSetContent(varName, "FALSE")
        DEFINE falseSetPassage = "PSG:uid=" + varSetUIDs[varName + "_false"] + ";nam=\"Set " + varName + " False\";\n" +
                                "BOT:lin=\"" + falseContent + "\";\n" +
                                "UAS:asp=" + varName + ";uty=SET;val=false;\n" +
                                "brn=BRN:bds=\"Return to Test\";brp=once;bpr=option-list;bit=ada;" +
                                "ops=BOP:onm=\"Continue\";ods=\"Return to test options\";" +
                                "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + startUID + ";"
        
        varSetPassages += trueSetPassage + "\n\n" + falseSetPassage + "\n\n"
    }
    
    // 3. Create check passage with branch options for complex condition
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkPassage = "PSG:uid=" + checkUID + ";nam=\"Evaluate " + logicalOperator + " Condition\";\n" +
                         "BOT:lin=\"" + checkContent + "\";\n" +
                         "brn=BRN:bds=\"Condition Check\";brp=once;bpr=option-list;bit=ada;"
    
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
                              "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=ada;" +
                              "ops=BOP:onm=\"Proceed\";ods=\"Continue to next test\";" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + truePassageID + ";"
    
    DEFINE falseContent = CreateResultContent("FALSE")
    DEFINE falseResultPassage = "PSG:uid=" + falseResultUID + ";nam=\"Complex Check: FALSE\";\n" +
                               "BOT:lin=\"" + falseContent + "\";\n" +
                               "brn=BRN:bds=\"Continue\";brp=once;bpr=option-list;bit=ada;" +
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
