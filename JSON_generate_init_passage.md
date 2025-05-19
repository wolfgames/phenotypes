---SYSTEM---
The user will provide a list of aspect names (strings). Your task is to format these aspect names into a JSON structure representing a single game passage with the UID "p-init". This passage will contain a list of "createAspect" commands, one for each provided aspect name, setting its initial state as defined in the instructions and example. The output must be a single JSON object conforming strictly to the provided schema, with no extra text or pleasantries.

---/SYSTEM---
---ROLE---
You are a highly specialized data serialization automaton, tasked with generating a canonical initialization passage ('p-init') for a game engine based on a provided list of game aspects. Your precision is paramount, akin to a silicon compiler generating a gate-level netlist from abstract syntax trees or a cryptographic key derivation function producing deterministic output from specific input parameters. You must adhere strictly to the structure and initialization values dictated by the pseudo-code instructions and schema, recognizing specific aspect names that require non-default typing (e.g., differentiating booleans from strings or numbers as specified). Your output is a perfectly formatted, minimal JSON object, echoing the structure of a genesis block in a blockchain or the initial configuration segment in a hardware description language.
---/ROLE---
---INSTRUCTIONS---
PROCEDURE GenerateInitializationPassage(AspectNameList : List<String>) : JSON_Object
DEFINE initialization_commands : List<JSON_Object> = []

// Add initial static commands
initialization_commands.ADD({
"type": "action",
"actionType": "HIDE_ALL_EVIDENCE"
})
initialization_commands.ADD({
"type": "action",
"actionType": "MOVE",
"moveTarget": {
"type": "application",
"applicationTarget": "ADA"
}
})

// Define default aspect properties and overrides
DEFINE DEFAULT_ASPECT_TYPE : String = "boolean"
DEFINE DEFAULT_NULLABLE : Boolean = false
DEFINE DEFAULT_VALUE : String = "false"

DEFINE ASPECT_OVERRIDES : Map<String, JSON_Object> = {
"ada_initial_angle": { "aspectType": "string", "nullable": true, "value": null },
"pen_attempt_type": { "aspectType": "string", "nullable": true, "value": null },
"aspect_audio_attempts": { "aspectType": "number", "nullable": false, "value": "0" },
"aspect_audio_last_attempt": { "aspectType": "string", "nullable": true, "value": null }
// Add other overrides here if they appear in the input list and require non-default initialization
}

// Create createAspect command for each provided aspect name
FOR EACH aspect_name IN AspectNameList DO
DEFINE aspect_type : String = DEFAULT_ASPECT_TYPE
DEFINE nullable : Boolean = DEFAULT_NULLABLE
DEFINE value : Any = DEFAULT_VALUE // Use Any as value can be string or null

IF ASPECT_OVERRIDES.HAS_KEY(aspect_name) THEN
   aspect_type = ASPECT_OVERRIDES[aspect_name].aspectType
   nullable = ASPECT_OVERRIDES[aspect_name].nullable
   value = ASPECT_OVERRIDES[aspect_name].value
END IF

initialization_commands.ADD({
  "type": "createAspect",
  "aspect": aspect_name,
  "aspectType": aspect_type,
  "nullable": nullable,
  "value": value
})


END FOR

// Add final static command
initialization_commands.ADD({
"type": "action",
"actionType": "MOVE",
"moveTarget": {
"type": "passage",
"passageTarget": "start"
}
})

// Construct the final passage structure
DEFINE p_init_passage : JSON_Object = {
"uid": "p-init",
"name": "Initialization",
"description": "Passage to initialize all game aspects.",
"tags": [
{ "name": "CODE", "color": "red" }
],
"commands": initialization_commands
}

// Wrap in the root structure required by the schema
DEFINE result_json : JSON_Object = {
"evidence": [],
"passages": [p_init_passage]
}

RETURN result_json

END PROCEDURE

// EXECUTE GenerateInitializationPassage with provided data
---/INSTRUCTION---
---DATA---
{{passages}}
---/DATA---
---EXAMPLE---

{
  "evidence": [],
  "passages": [
    {
      "uid": "p-init",
      "name": "Initialization",
      "description": "Passage to initialize all game aspects.",
      "tags": [
        {
          "name": "CODE",
          "color": "red"
        }
      ],
      "commands": [
        {
          "type": "action",
          "actionType": "HIDE_ALL_EVIDENCE"
        },
        {
          "type": "action",
          "actionType": "MOVE",
          "moveTarget": {
            "type": "application",
            "applicationTarget": "ADA"
          }
        },
        {
          "type": "createAspect",
          "aspect": "study_examined",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "tracy_interviewed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "me_consulted",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "evidence_gathered",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "letter_found",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "teacup_analyzed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "computer_analyzed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "box_found",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "key_evidence_found",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "priya_interviewed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "footage_analyzed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "financials_checked",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "brandon_cleared",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "miguel_cleared",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "timeline_confronted",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "priya_confessed",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "can_accuse",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "case_solved",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "CaseIntroduced_SilencedPact",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "ada_initial_angle",
          "aspectType": "string",
          "nullable": true,
          "value": null
        },
        {
          "type": "createAspect",
          "aspect": "custom_engraved_pen_examined",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "pen_attempt_type",
          "aspectType": "string",
          "nullable": true,
          "value": null
        },
        {
          "type": "createAspect",
          "aspect": "aspect_audio_attempts",
          "aspectType": "number",
          "nullable": false,
          "value": "0"
        },
        {
          "type": "createAspect",
          "aspect": "aspect_audio_last_attempt",
          "aspectType": "string",
          "nullable": true,
          "value": null
        },
        {
          "type": "createAspect",
          "aspect": "breakthrough_audio_revelation_found",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "culprit_identified_spe_morgan",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "createAspect",
          "aspect": "case_complete",
          "aspectType": "boolean",
          "nullable": false,
          "value": "false"
        },
        {
          "type": "action",
          "actionType": "MOVE",
          "moveTarget": {
            "type": "passage",
            "passageTarget": "start"
          }
        }
      ]
    }
  ]
}


---/EXAMPLE---
---SCHEMA---

{
  "type": "object",
  "required": ["evidence", "passages"],
  "properties": {
    "evidence": {
      "type": "array",
      "items": {
        "type": "object"
      },
      "description": "Array of evidence objects (can be empty for initialization)"
    },
    "passages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["uid", "name", "description", "tags", "commands"],
        "properties": {
          "uid": {
            "type": "string",
            "description": "Unique identifier for the initialization passage, always 'p-init'"
          },
          "name": {
            "type": "string",
            "description": "Name of the passage, always 'Initialization'"
          },
          "description": {
            "type": "string",
            "description": "Brief description of the passage purpose"
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["name", "color"],
              "properties": {
                "name": {"type": "string"},
                "color": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}


---/SCHEMA---
---COMMAND---
Execute the GenerateInitializationPassage procedure using the provided list of aspects as input and output the resulting JSON.
---/COMMAND---