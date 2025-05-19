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
                        "brn=BRN:bds=\"Compound Condition Evaluation\";brp=once;bpr=option-list;bit=ada;" +
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
