{# PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}

PROCEDURE GenerateDiagnosticEvidenceExamination(stepIDPrefix, entry_point_id, testCaseID, evidenceID, attributeData, successPassageID, failPassageID) {
    // Primary goal: Create a passage that tests evidence examination and attribute discovery
    // Structure: Series of passages that sets evidence attributes and branches based on examination state
    // Input: attributeData is an object mapping attribute names to values

    // Define UIDs for the passage sequence
    DEFINE examineUID = entry_point_id
    DEFINE examineName = "Test Case " + testCaseID + ": Evidence Examination Test"
    DEFINE setStateUID = "diag_exam_" + testCaseID + "_set_state"
    DEFINE checkStateUID = "diag_exam_" + testCaseID + "_check_state"
    DEFINE successUID = "diag_exam_" + testCaseID + "_success"
    DEFINE failUID = "diag_exam_" + testCaseID + "_fail"
    
    // Create descriptive text for each passage
    PROCEDURE CreateStartContent() {
        RETURN "Testing evidence examination and attribute discovery for " + evidenceID + "."
    }
    
    PROCEDURE CreateSetStateContent() {
        RETURN "Setting state for " + evidenceID + "."
    }
    
    PROCEDURE CreateCheckContent() {
        RETURN "Checking state..."
    }
    
    PROCEDURE CreateSuccessContent() {
        RETURN "Attributes and examined status were set correctly."
    }
    
    PROCEDURE CreateFailContent() {
        RETURN "Attributes and examined status were NOT set correctly."
    }
    
    // Create attribute commands for setting state
    PROCEDURE CreateAttributeSettings(evidenceID, attributeData) {
        DEFINE attributeCommands = ""
        
        // Set the main examined flag
        attributeCommands += "SET:evt=" + evidenceID + "_EXAMINED;val=true;"
        
        // Set each attribute value
        FOR EACH attrName, attrValue IN attributeData {
            attributeCommands += "UAS:asp=" + attrName + ";uty=SET;val=\"" + attrValue + "\";"
        }
        
        RETURN attributeCommands
    }
    
    // 1. Create the start passage with branch to set state
    DEFINE startContent = CreateStartContent()
    DEFINE startPassage = "PSG:uid=" + examineUID + ";nam=\"" + examineName + "\";\n" +
                         "BOT:lin=\"" + startContent + "\";\n" +
                         "brn=BRN:bds=\"Start Test Step\";brp=once;bpr=option-list;bit=ada;" +
                         "ops=BOP:onm=\"Begin Examination Test\";ods=\"Proceed to the next step in the diagnostic sequence\";" +
                         "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + setStateUID + ";"
    
    // 2. Create the set state passage
    DEFINE setStateContent = CreateSetStateContent()
    DEFINE attributeCommands = CreateAttributeSettings(evidenceID, attributeData)
    DEFINE setStatePassage = "PSG:uid=" + setStateUID + ";nam=\"Set Evidence Attributes\";\n" +
                            "BOT:lin=\"" + setStateContent + "\";\n" +
                            attributeCommands + "\n" +
                            "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + checkStateUID + ";"
    
    // 3. Create the check state passage with branch
    DEFINE checkContent = CreateCheckContent()
    DEFINE checkStatePassage = "PSG:uid=" + checkStateUID + ";nam=\"Verify Evidence State\";\n" +
                              "BOT:lin=\"" + checkContent + "\";\n" +
                              "brn=BRN:bds=\"Verify State\";brp=once;bpr=option-list;bit=ada;" +
                              "ops=BOP:onm=\"Success Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=eq;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successUID + ";" +
                              "ops=BOP:onm=\"Failure Path\";chk=CHK:asp=" + evidenceID + "_EXAMINED;cty=ne;vlu=true;" +
                              "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failUID + ";"
    
    // 4. Create success passage
    DEFINE successContent = CreateSuccessContent()
    DEFINE successPassage = "PSG:uid=" + successUID + ";nam=\"Examination Test Success\";\n" +
                           "BOT:lin=\"" + successContent + "\";\n" +
                           "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + successPassageID + ";"
    
    // 5. Create fail passage
    DEFINE failContent = CreateFailContent()
    DEFINE failPassage = "PSG:uid=" + failUID + ";nam=\"Examination Test Failure\";\n" +
                        "BOT:lin=\"" + failContent + "\";\n" +
                        "ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + failPassageID + ";"
    
    // Combine all passages
    DEFINE allPassages = startPassage + "\n\n" + 
                        setStatePassage + "\n\n" + 
                        checkStatePassage + "\n\n" + 
                        successPassage + "\n\n" + 
                        failPassage
    
    // Validation check
    PROCEDURE ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID) {
        // Verify that required elements are present
        VALIDATE allPassages CONTAINS "Testing evidence examination"
        VALIDATE allPassages CONTAINS evidenceID + "_EXAMINED;val=true"
        VALIDATE allPassages CONTAINS successPassageID
        VALIDATE allPassages CONTAINS failPassageID
        VALIDATE allPassages CONTAINS "brn=BRN"
        
        // Verify all attributes are set
        FOR EACH attrName IN attributeData {
            VALIDATE allPassages CONTAINS attrName
        }
        
        // Verify all passage IDs are included
        VALIDATE allPassages CONTAINS successUID
        VALIDATE allPassages CONTAINS failUID
        VALIDATE allPassages CONTAINS setStateUID
        VALIDATE allPassages CONTAINS checkStateUID
    }
    
    ValidateEvidenceExamination(allPassages, evidenceID, attributeData, successPassageID, failPassageID)
    
    RETURN allPassages
}

{# END_PHENOTYPE: DIAGNOSTIC_EVIDENCE_EXAMINATION #}
