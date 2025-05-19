{# PHENOTYPE: EVIDENCE_COLLECTION #}

PROCEDURE GenerateEvidenceCollection(stepIDPrefix, entry_point_id, locationScenes, returnPassage) {
    // Primary goal: Create multiple passages, one for each scene/area within a broader location, for discovering evidence.
    // Structure: Generates N passages, where N is the number of items in locationScenes list.
    // Input: locationScenes is a list of objects, each with { id, name, description, evidenceItems (list of {id, name, type, examineStepID}) }

    DEFINE allPassages = ""
    DEFINE passageCounter = 0

    // Loop through each scene defined for this location
    FOR EACH scene IN locationScenes INDEX i {
        // Create a unique ID for this specific scene passage
        // The FIRST scene passage (i=0) uses the entry_point_id
        DEFINE sceneUID = IF i == 0 THEN entry_point_id ELSE stepIDPrefix + "_" + scene.id
        DEFINE sceneName = scene.name

        // Step 1: Create descriptive scene content
        PROCEDURE CreateSceneDescription(description) {
            DEFINE see = "[SEE: " + description + "]"
            DEFINE do = "[DO: Examine the area for evidence]"
            DEFINE learn = "[LEARN: Look for anything that seems out of place]"
            RETURN see + " " + do + " " + learn
        }
        DEFINE sceneContent = CreateSceneDescription(scene.description)

        // Step 2: Create evidence examination options for this scene
        PROCEDURE CreateEvidenceOptionsForScene(evidenceItems, returnPassage) {
            DEFINE options = ""
            FOR EACH item IN evidenceItems INDEX j {
                IF j > 0 { options += "|" }
                // Each evidence item gets its own option
                options += "BOP:onm=\\\"" + item.name + "\\\";img=\\\"evidence_" + item.id + "\\\";" +
                          "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + item.examineStepID
            }
            // Add return option
            IF evidenceItems.length > 0 { options += "|" }
            options += "BOP:onm=\\\"Return\\\";img=\\\"return_to_location\\\";" +
                      "act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=" + returnPassage
            RETURN options
        }
        DEFINE sceneOptions = CreateEvidenceOptionsForScene(scene.evidenceItems, returnPassage)

        // Step 3: Format the SLPN for this specific scene passage
        DEFINE slpnScenePassage = "PSG:uid=" + sceneUID + ";nam=\\\"" + sceneName + "\\";tag=EVIDENCE_COLLECTION|SCENE;CNT;BOT:lin=\\\"" + 
                                 sceneContent + "\\";brn=BRN:bds=\\"Examine " + sceneName + "\\";brp=re-playable;bpr=option-list;bit=ada;ops=" + 
                                 sceneOptions + ";"
        
        
        IF i > 0 { allPassages += "\n\n" }
        allPassages += slpnScenePassage
        passageCounter++
    }
    
    // Validation check
    PROCEDURE ValidateEvidenceCollection(passageCounter, locationScenes) {
        VALIDATE passageCounter == locationScenes.length
        // Check that each scene passage has appropriate options
        FOR EACH scene IN locationScenes {
            VALIDATE scene.evidenceItems.length > 0
            // Validate that each evidence item has required fields
            FOR EACH item IN scene.evidenceItems {
                VALIDATE item.id AND item.name AND item.type AND item.examineStepID
            }
        }
    }
    
    ValidateEvidenceCollection(passageCounter, locationScenes)
    
    RETURN allPassages
}

{# END_PHENOTYPE: EVIDENCE_COLLECTION #}
