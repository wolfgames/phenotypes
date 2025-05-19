---EXAMPLE---

## Example 1: SLPN Passage with Branch Options and Conditional Logic (Updated with Tree-of-Thought)

### SLPN Input:
```
PSG:uid=interview_priya;nam="Interview Priya Shah";tag=INTERVIEW;CNT;BOT:lin="Priya Shah polished shocked. 'Yes, Amara called yesterday re: docs. Met study 4 PM. Standard stuff. Left 4:30.' Feels off.";act=UAS:asp=priya_interviewed;uty=SET;val=true;brn=BRN:bds="Interview Options";brp=re-playable;bpr=option-list;bit=blocking;ops=BOP:onm="Check Financial Background";ods="Look for motive.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=priya_financials|BOP:onm="Confront with Timeline Evidence";ods="If security footage available.";cnd=CND:typ=checkAspect;asp=footage_analyzed;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=confront_priya_timeline|BOP:onm="Confront with Box Evidence";ods="If hearth evidence found.";cnd=CND:typ=checkAspect;asp=key_evidence_found;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=confront_priya_evidence|BOP:onm="End Interview";ods="Return to interview hub.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=interview_hub;
```

### Tree-of-Thought Reasoning:

1. PASSAGE ANALYSIS
   - Type: Narrative passage with interview content and choices
   - Commands:
     * PSG: Defines passage with uid and name
     * BOT: Contains interview text and nested branch
     * UAS: Updates aspect priya_interviewed to true
     * BRN: Contains multiple branch options with conditions
   - Nested Structures:
     * Branch within bot message
     * Multiple BOP commands within branch
     * CND conditions within some BOP commands
   - Validation Notes:
     * Need to verify all passage targets exist
     * Need to ensure proper nesting of branch in bot message

2. REFERENCE VALIDATION
   - Passage References:
     * priya_financials
     * confront_priya_timeline
     * confront_priya_evidence
     * interview_hub
   - Evidence References: None in this passage
   - Fallback Values:
     * Will use first valid passage as fallback if needed

3. STRUCTURE PLANNING
   - JSON Structure:
     * Top level: passage object with uid, name, tags
     * Commands array with bot, updateAspect, and branch
     * Bot message will contain expanded text and branch
     * Branch will contain options with conditions and actions
   - Special Cases:
     * Need to wrap branch in bot message
     * Need to expand compact interview text
     * Need to handle conditional options properly

4. ADA TEXT EXPANSION
   - The transpiler must use the ADA personality defined in the tree-of-thought (TOT) plan
   - All text expansions should follow the style and personality characteristics provided in the TOT
   - The EXPAND_TEXT_AS_ADA procedure should use guidance from the tree-of-thought for tone and style
   - Compact notation like "[SEE: Evidence] [LEARN: New clue]" should be expanded into natural, conversational dialog
   - No hardcoded voice or persona should be applied - only use what's provided in the tree-of-thought
   - Example texts shown in this document are generic placeholders that should be replaced with text matching the TOT personality

5. FINAL VALIDATION
   - Required Fields:
     * All passage fields present
     * All command types properly structured
     * All branch options have required fields
   - Schema Compliance:
     * Structure matches schema requirements
     * All references validated
     * Proper nesting maintained

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "interview_priya",
      "name": "Interview Priya Shah",
      "description": "Passage description.",
      "tags": [
        {
          "name": "INTERVIEW",
          "color": "blue"
        },
        {
          "name": "CODE",
          "color": "purple"
        },
        {
          "name": "CHOICE",
          "color": "green"
        },
        {
          "name": "GATE",
          "color": "orange"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Interview Options",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "blocking",
            "options": [
              {
                "type": "branchOption",
                "name": "Check Financial Background",
                "aspectCheck": null,
                "description": "Look for motive.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "priya_financials"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Confront with Timeline Evidence",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "eq",
                    "aspect": "footage_analyzed",
                    "target": true,
                    "aspectUid": "footage_analyzed"
                  }
                },
                "description": "If security footage available.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "confront_priya_timeline"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Confront with Box Evidence",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "eq",
                    "aspect": "key_evidence_found",
                    "target": true,
                    "aspectUid": "key_evidence_found"
                  }
                },
                "description": "If hearth evidence found.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "confront_priya_evidence"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "End Interview",
                "aspectCheck": null,
                "description": "Return to interview hub.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "interview_hub"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        },
        {
          "type": "updateAspect",
          "aspect": "priya_interviewed",
          "operation": "SET",
          "value": "true"
        }
      ]
    }
  ]
}
```

## Example 2: SLPN Passage with Standalone Branch (Updated with ADA text)

### SLPN Input:
```
PSG:uid=investigation_hub;nam="Investigation Hub";tag=HUB_MENU;CNT;BRN:bds="Coordinate Investigation";brp=re-playable;bpr=option-list;bit=blocking;ops=BOP:onm="Collect Evidence";ods="Gather potential evidence.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=evidence_collection|BOP:onm="Interview Suspects";ods="Speak with people involved.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=interview_hub;
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "investigation_hub",
      "name": "Investigation Hub",
      "description": "Passage description.",
      "tags": [
        {
          "name": "HUB_MENU",
          "color": "blue"
        },
        {
          "name": "CHOICE",
          "color": "green"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Coordinate Investigation",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "blocking",
            "options": [
              {
                "type": "branchOption",
                "name": "Collect Evidence",
                "aspectCheck": null,
                "description": "Gather potential evidence.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "evidence_collection"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Interview Suspects",
                "aspectCheck": null,
                "description": "Speak with people involved.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "interview_hub"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## Example 3: SLPN Passage with Evidence Reveal Action and EVidence MOVE (automatically opens the evidence in the evidence viewer)

### SLPN Input:
```
PSG:uid=router_log_result;nam="Router Log Results";tag=EVIDENCE_DISCOVERY;CNT;BOT:lin="Router logs show Alex device accessing files 2AM, contradicts alibi.";act=ACT:aty=REVEAL;evt=evidence_router_logs;eva="Router Logs";brn=BRN:bds="Next Step";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm="Return to Evidence Collection";ods="Continue investigation.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=evidence_collection;
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "router_log_result",
      "name": "Router Log Results",
      "description": "Passage description.",
      "tags": [
        {
          "name": "EVIDENCE_DISCOVERY",
          "color": "blue"
        },
        {
          "name": "EVIDENCE",
          "color": "red"
        },
        {
          "name": "CHOICE",
          "color": "green"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text":"<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Next Step",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "ada",
            "options": [
              {
                "type": "branchOption",
                "name": "Return to Evidence Collection",
                "aspectCheck": null,
                "description": "Continue investigation.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "evidence_collection"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        },
        {
          "type": "action",
          "actionType": "REVEAL",
          "evidenceTarget": "evidence_router_logs",
          "evidenceAlias": "Router Logs"
        },
        {
            "type": "action",
            "actionType": "MOVE",
            "moveTarget": {
              "type": "evidence",
              "evidenceTarget": "evidence_router_logs",
              "evidenceAlias": "Router Logs"
            }
        }
      ]
    }
  ]
}
```

## Example 4: SLPN Passage with Application Move Action

### SLPN Input:
```
PSG:uid=go_to_evidence;nam="Go To Evidence App";tag=NAVIGATION_ACTION;CNT;BOT:lin="Let's review the evidence gathered so far.";act=ACT:aty=MOVE;amt=AMT:typ=application;tgt=EVIDENCE;
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "go_to_evidence",
      "name": "Go To Evidence App",
      "description": "Passage description.",
      "tags": [
        {
          "name": "NAVIGATION_ACTION",
          "color": "blue"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ]
        },
        {
          "type": "action",
          "actionType": "MOVE",
          "moveTarget": {
            "type": "application",
            "applicationTarget": "EVIDENCE"
          }
        }
      ]
    }
  ]
}
```

## Example 5: SLPN Passage with Suspect Reveal and Dossier Navigation

### SLPN Input:
```
PSG:uid=suspect_reveal;nam="Suspect Identified";tag=SUSPECT_REVEAL;CNT;BOT:lin="Based on the fingerprint analysis, we've identified our primary suspect: James Wilson, the victim's business partner. His financial records show large debts and the fingerprints on the murder weapon are a match.";act=ACT:aty=REVEAL;evt=suspect_wilson;eva="James Wilson"|ACT:aty=MOVE;amt=AMT:typ=application;tgt=DOSSIER;
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "suspect_reveal",
      "name": "Suspect Identified",
      "description": "Passage description.",
      "tags": [
        {
          "name": "SUSPECT_REVEAL",
          "color": "blue"
        },
        {
          "name": "EVIDENCE",
          "color": "red"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": <insert ADA response based on TOT personality>,
              "imageAlias": "",
              "imageDescription": ""
            }
          ]
        },
        {
          "type": "action",
          "actionType": "REVEAL",
          "evidenceTarget": "suspect_wilson",
          "evidenceAlias": "James Wilson"
        },
        {
          "type": "action",
          "actionType": "MOVE",
          "moveTarget": {
            "type": "application",
            "applicationTarget": "DOSSIER"
          }
        }
      ]
    }
  ]
}
```


## Important Processing Notes:

1. **Passage UIDs**: Always preserve exactly as specified in the input SLPN
2. **Branch Nesting**: ALL branches must appear inside a bot message in the output, even if they appear as standalone BRN commands in the SLPN input
3. **Move Actions**: All move targets are validated against the full SLPN list
4. **Evidence References**: All evidence targets in REVEAL actions must exist in the evidence array
5. **Aspect Checks**: Follow the correct schema structure for all conditionals
6. **Bot Messages**: Always include empty strings for imageAlias and imageDescription when not specified. **IMPORTANT**: If a BOT command in SLPN does not have a `brn=` parameter, the corresponding JSON `bot` object MUST omit the `branch` key entirely.
7. **Standalone Branches**: For standalone BRN commands in the SLPN, create a bot message with the branch description as text (or default text) to contain the branch.
8. **Action Placement**: Actions defined within nested structures (like `BOP:act=` or `IFF:act=`) MUST be placed *only* within the corresponding JSON array (e.g., `branchOption.actions`, `if.actions`). Do NOT duplicate or move these actions to the top-level `passage.commands`.
9. **UPDATE_ASPECT Structure**: An SLPN command like `ACT:aty=UPDATE_ASPECT;asp=...` or `UAS:asp=...` MUST translate to a JSON object `{ "type": "updateAspect", "aspect": "...", ... }`, NOT `{ "type": "action", "actionType": "UPDATE_ASPECT", ... }`.
10. **Branch Replayability**: All branches MUST use `"replayAbility": "re-executable"`.
11. **Passage Tagging**: Apply tags based on passage content: `NARRATIVE` (green) always, `CODE` (purple) for UAS/IFF, `EVIDENCE` (red) for REVEAL, `CHOICE` (green) for BRN, `GATE` (orange) for conditional BRN options (BOP with cnd=).
12. **Move Action Targets**: `MOVE` actions can target either a passage (`amt=AMT:typ=passage;tgt=passage_uid;`) or a specific application (`amt=AMT:typ=application;tgt=APP_NAME;` where `APP_NAME` is one of `HOME`, `ADA`, `DOSSIER`, `EVIDENCE`). Passage targets are validated; application targets must be one of the allowed names.
13. **Evidence and Suspect Reveals**: REVEAL actions can use either `evidenceTarget`/`evidenceAlias` or `evt`/`eva` parameter formats. Both formats should be properly supported and converted to the standard output format.
14. **Application Navigation**: Support direct navigation to specific applications like EVIDENCE for the evidence browser and DOSSIER for suspect profiles, rather than passage-based navigation.


## Example 6: SLPN Passage with Proper Aspect Update in Dedicated Passage

### SLPN Input:
```
PSG:uid=examine_evidence;nam="Examine Financial Records";tag=FINANCIAL_EXAMINATION;CNT;BOT:lin="[SEE: Company financial records] [LEARN: There's a discrepancy in the accounts from last quarter] [DO: Note this finding or continue]";brn=BRN:bds="Investigation Actions";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm="Note this finding";ods="Add to your case notes";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=update_financial_records_examined_true|BOP:onm="Continue Investigation";ods="Return to the evidence hub";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=evidence_hub;

PSG:uid=update_financial_records_examined_true;nam="Updating Financial Records Status";tag=ASPECT_UPDATE;CNT;UAS:asp=financial_records_examined;uty=SET;val=true;ACT:aty=MOVE;amt=AMT:typ=passage;tgt=evidence_hub;
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "examine_evidence",
      "name": "Examine Financial Records",
      "description": "Passage description.",
      "tags": [
        {
          "name": "FINANCIAL_EXAMINATION",
          "color": "blue"
        },
        {
          "name": "CHOICE",
          "color": "green"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Investigation Actions",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "ada",
            "options": [
              {
                "type": "branchOption",
                "name": "Note this finding",
                "aspectCheck": null,
                "description": "Add to your case notes",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "update_financial_records_examined_true"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Continue Investigation",
                "aspectCheck": null,
                "description": "Return to the evidence hub",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "evidence_hub"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        }
      ]
    },
    {
      "uid": "update_financial_records_examined_true",
      "name": "Updating Financial Records Status",
      "description": "Passage description.",
      "tags": [
        {
          "name": "ASPECT_UPDATE",
          "color": "blue"
        },
        {
          "name": "CODE",
          "color": "purple"
        },
        {
          "name": "UPDATE_ASPECT",
          "color": "purple"
        }
      ],
      "commands": [
        {
          "type": "updateAspect",
          "aspect": "financial_records_examined",
          "operation": "SET",
          "value": "true"
        },
        {
          "type": "action",
          "actionType": "MOVE",
          "moveTarget": {
            "type": "passage",
            "passageTarget": "evidence_hub"
          }
        }
      ]
    }
  ]
}
```

## Important Notes on Aspect Update Passages:

1. **Naming Convention**: The update passage UID must follow the pattern `update_[aspect_name]_[value]` for clarity and to avoid duplicate names.

2. **Minimalist Structure**: The update passage should have:
   - No bot message or narrative text
   - No branch structure at all - just commands directly in the commands array
   - This makes the passage practically invisible to the player

3. **Strict Command Pattern**: 
   - Just two commands in sequence:
     1. The updateAspect command to change the state
     2. A MOVE action to the next logical passage

4. **Branch Option Structure**: Original branch options that would update aspects now simply MOVE to the dedicated update passage instead of containing the update command directly.

5. **Proper Tagging**: Always include the `UPDATE_ASPECT` tag to help identify these passages.
---/EXAMPLE---

## Example 7: SLPN Passage with Intro Steps and Valid Text Types

### SLPN Input:
```
PSG:uid=case_introduction;nam="Case Introduction";tag=INTRO_SEQUENCE;CNT;CMD:typ=intro;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=case_overview;STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=crime_scene_overview;imd="An overview of the crime scene";cmp=CMP:typ=introStepText;txt=TITLE;mnt="The Riverside Mystery";sbt="Case #4872";cmp=CMP:typ=introStepControl;ctt=NEXT_STEP_BUTTON;ctk=PRIMARY;tex="Continue";STP:typ=introStep;cmp=CMP:typ=introStepBG;bgt=IMAGE;img=victim_profile;imd="Profile photo of the victim";cmp=CMP:typ=introStepText;txt=BREAKDOWN;lin="The victim was found in his apartment|Initial forensics suggest time of death between 10pm-12am|No signs of forced entry were observed";cmp=CMP:typ=introStepControl;ctt=FINISH_INTRO_BUTTON;ctk=PRIMARY;tex="Begin Investigation";
```

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "case_introduction",
      "name": "Case Introduction",
      "description": "Passage description.",
      "tags": [
        {
          "name": "INTRO_SEQUENCE",
          "color": "blue"
        },
        {
          "name": "INTRO",
          "color": "blue"
        }
      ],
      "commands": [
        {
          "type": "intro",
          "actions": [
            {
              "type": "action",
              "actionType": "MOVE",
              "moveTarget": {
                "type": "passage",
                "passageTarget": "case_overview"
              }
            }
          ],
          "steps": [
            {
              "type": "introStep",
              "components": [
                {
                  "type": "introStepBG",
                  "backgroundType": "IMAGE",
                  "imageAlias": "crime_scene_overview",
                  "imageDescription": "An overview of the crime scene"
                },
                {
                  "type": "introStepText",
                  "textType": "TITLE",
                  "mainTitle": "The Riverside Mystery",
                  "subTitle": "Case #4872"
                },
                {
                  "type": "introStepControl",
                  "controlType": "NEXT_STEP_BUTTON",
                  "controlKind": "PRIMARY",
                  "text": "Continue"
                }
              ]
            },
            {
              "type": "introStep",
              "components": [
                {
                  "type": "introStepBG",
                  "backgroundType": "IMAGE",
                  "imageAlias": "victim_profile",
                  "imageDescription": "Profile photo of the victim"
                },
                {
                  "type": "introStepText",
                  "textType": "BREAKDOWN",
                  "lines": [
                    "The victim was found in his apartment",
                    "Initial forensics suggest time of death between 10pm-12am",
                    "No signs of forced entry were observed"
                  ]
                },
                {
                  "type": "introStepControl",
                  "controlType": "FINISH_INTRO_BUTTON",
                  "controlKind": "PRIMARY",
                  "text": "Begin Investigation"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Important Notes on Intro Steps:

1. **introStepText Types**: The schema only allows two valid `textType` values:
   - `TITLE`: Must include `mainTitle` and `subTitle` properties
   - `BREAKDOWN`: Must include a `lines` array of strings

2. **Component Order**: Each introStep should have:
   - One `introStepBG` component (for background)
   - One or more `introStepText` components
   - One `introStepControl` component (for navigation)

3. **Control Types**: Valid `controlType` values are:
   - `NEXT_STEP_BUTTON`: For moving to the next intro step
   - `FINISH_INTRO_BUTTON`: For completing the intro sequence

4. **Invalid Properties**: Never use `textType: "TEXT"` as it's not schema-compliant. Always use either `TITLE` or `BREAKDOWN`.

5. **Lines Formatting**: When converting from SLPN format:
   - For `txt=TITLE`, create an object with `mainTitle` and `subTitle`
   - For `txt=BREAKDOWN`, convert pipe-separated text (`lin="text1|text2"`) into an array of strings


Exmample 8:

## Example 8: SLPN Deduction Puzzle with Limited Attempts and Conditional Logic

### SLPN Input:
```
PSG:uid=DEDUCTION_PUZZLE_12;nam="Access Isabella's Phone";tag=DEDUCTION_PUZZLE;CNT;BOT:lin="[SEE: Encrypted phone screen, keypad] [DO: Attempt to guess the passcode] [LEARN: Isabella's phone is locked. Max attempts: 3. Attempts left: {3 - $isabella_phone_attempts}] [FEEL: Challenge]Based on clues from her profile and the case context, what's Isabella's passcode?";brn=BRN:bds="Enter Passcode";brp=re-playable;bpr=option-list;bit=blocking;ops=BOP:onm="FamilyFirst";ods="Try 'FamilyFirst' as the passcode.";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=LT;val=3;act=UAS:asp=isabella_phone_attempts;uty=INC;val=1|UAS:asp=isabella_phone_last_code;uty=SET;val="FamilyFirst"|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12_CHECK_OUTCOME|BOP:onm="ArgMate";ods="Try 'ArgMate' as the passcode.";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=LT;val=3;act=UAS:asp=isabella_phone_attempts;uty=INC;val=1|UAS:asp=isabella_phone_last_code;uty=SET;val="ArgMate"|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12_CHECK_OUTCOME|BOP:onm="TariffPayoff";ods="Try 'TariffPayoff' as the passcode.";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=LT;val=3;act=UAS:asp=isabella_phone_attempts;uty=INC;val=1|UAS:asp=isabella_phone_last_code;uty=SET;val="TariffPayoff"|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12_CHECK_OUTCOME|BOP:onm="No Attempts Left";ods="The phone is locked.";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12_LOCKOUT;

PSG:uid=DEDUCTION_PUZZLE_12_CHECK_OUTCOME;nam="Passcode Check";tag=PUZZLE_OUTCOME;CNT;BOT:lin="[SEE: Processing feedback] [LEARN: Verifying entered passcode...] [DO: Wait] [FEEL: Tension]System verifying passcode.";brn=BRN:bds="Processing Attempt";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm="Correct Path";ods="Hidden option for correct answer.";cnd=CND:typ=checkAspect;asp=isabella_phone_last_code;cmp=EQ;val="TariffPayoff";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=EVIDENCE_EXAMINATION_13|BOP:onm="Incorrect Path (Retry)";ods="Hidden option for incorrect answer with retries left.";cnd=CAD:typ=checkAspect;lop=AND;cnd=CND:typ=checkAspect;asp=isabella_phone_last_code;cmp=NE;val="TariffPayoff";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=LT;val=3;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12|BOP:onm="Incorrect Path (Lockout)";ods="Hidden option for incorrect answer with no retries left.";cnd=CAD:typ=checkAspect;lop=AND;cnd=CND:typ=checkAspect;asp=isabella_phone_last_code;cmp=NE;val="TariffPayoff";cnd=CND:typ=checkAspect;asp=isabella_phone_attempts;cmp=GE;val=3;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=DEDUCTION_PUZZLE_12_LOCKOUT;

PSG:uid=DEDUCTION_PUZZLE_12_LOCKOUT;nam="Phone Locked";tag=PUZZLE_LOCKOUT;CNT;BOT:lin="[SEE: Locked phone screen] [LEARN: You have exceeded the maximum attempts. Isabella's phone is now locked and inaccessible.] [DO: Return to Investigation Hub] [FEEL: Frustration]The device is permanently locked due to too many incorrect attempts.";brn=BRN:bds="Device Locked";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm="Return to Hub";ods="Go back to the main case view.";act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=INVESTIGATION_HUB_7;
```

### Overview
This example demonstrates a complex deduction puzzle with limited attempts - specifically a phone passcode guessing challenge. Key features:

1. **Limited Attempts Mechanic**: The player has only 3 tries to guess the correct passcode
2. **State Tracking**: Uses multiple aspects to track attempts (`isabella_phone_attempts`) and last entered code (`isabella_phone_last_code`)
3. **Complex Conditionals**: Uses aspect checks with `LT` (less than), `GT` (greater than), `EQ` (equals) and `NE` (not equals)
4. **Separate Update Passages**: Each aspect update happens in dedicated passages to maintain clean state management
5. **Outcome Validation**: Special outcome checking passage that routes to different results based on combined conditions
6. **Lockout Mechanism**: If too many incorrect attempts are made, the puzzle becomes inaccessible

### Technical Implementation
The SLPN transpiler converts this into multiple passages with a clear separation of concerns:
- Main UI passage with passcode entry options
- Separate update passages for each aspect change
- Outcome checking passage with complex conditional routing
- Lockout passage for failed attempts

This pattern is essential for managing complex state in narrative games while maintaining clean code structure.

### JSON Output:
```json
{
  "passages": [
    {
      "uid": "DEDUCTION_PUZZLE_12",
      "name": "Access Isabella's Phone",
      "description": "Passage description.",
      "tags": [
        {
          "name": "DEDUCTION_PUZZLE",
          "color": "blue"
        },
        {
          "name": "CHOICE",
          "color": "green"
        },
        {
          "name": "GATE",
          "color": "orange"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Enter Passcode",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "ada",
            "options": [
              {
                "type": "branchOption",
                "name": "FamilyFirst",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "lt",
                    "aspect": "isabella_phone_attempts",
                    "target": 3,
                    "aspectUid": "isabella_phone_attempts"
                  }
                },
                "description": "Try 'FamilyFirst' as the passcode.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "update_isabella_phone_attempts_inc_1_FamilyFirst"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "ArgMate",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "lt",
                    "aspect": "isabella_phone_attempts",
                    "target": 3,
                    "aspectUid": "isabella_phone_attempts"
                  }
                },
                "description": "Try 'ArgMate' as the passcode.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "update_isabella_phone_attempts_inc_1_ArgMate"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "TariffPayoff",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "lt",
                    "aspect": "isabella_phone_attempts",
                    "target": 3,
                    "aspectUid": "isabella_phone_attempts"
                  }
                },
                "description": "Try 'TariffPayoff' as the passcode.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "update_isabella_phone_attempts_inc_1_TariffPayoff"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "No Attempts Left",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "gte",
                    "aspect": "isabella_phone_attempts",
                    "target": 3,
                    "aspectUid": "isabella_phone_attempts"
                  }
                },
                "description": "The phone is locked.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "DEDUCTION_PUZZLE_12_LOCKOUT"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        }
      ]
    },
    {
        "uid": "update_isabella_phone_attempts_inc_1_FamilyFirst",
        "name": "Increment Phone Attempts (FamilyFirst)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_attempts",
                "operation": "increment",
                "value": "1"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "update_isabella_phone_last_code_FamilyFirst"
                }
            }
        ]
    },
    {
        "uid": "update_isabella_phone_last_code_FamilyFirst",
        "name": "Set Last Phone Code (FamilyFirst)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_last_code",
                "operation": "SET",
                "value": "FamilyFirst"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "DEDUCTION_PUZZLE_12_CHECK_OUTCOME"
                }
            }
        ]
    },
    {
        "uid": "update_isabella_phone_attempts_inc_1_ArgMate",
        "name": "Increment Phone Attempts (ArgMate)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_attempts",
                "operation": "increment",
                "value": "1"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "update_isabella_phone_last_code_ArgMate"
                }
            }
        ]
    },
    {
        "uid": "update_isabella_phone_last_code_ArgMate",
        "name": "Set Last Phone Code (ArgMate)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_last_code",
                "operation": "SET",
                "value": "ArgMate"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "DEDUCTION_PUZZLE_12_CHECK_OUTCOME"
                }
            }
        ]
    },
    {
        "uid": "update_isabella_phone_attempts_inc_1_TariffPayoff",
        "name": "Increment Phone Attempts (TariffPayoff)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_attempts",
                "operation": "increment",
                "value": "1"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "update_isabella_phone_last_code_TariffPayoff"
                }
            }
        ]
    },
    {
        "uid": "update_isabella_phone_last_code_TariffPayoff",
        "name": "Set Last Phone Code (TariffPayoff)",
        "description": "Passage description.",
        "tags": [
            {"name": "ASPECT_UPDATE", "color": "blue"},
            {"name": "CODE", "color": "purple"},
            {"name": "UPDATE_ASPECT", "color": "purple"}
        ],
        "commands": [
            {
                "type": "updateAspect",
                "aspect": "isabella_phone_last_code",
                "operation": "SET",
                "value": "TariffPayoff"
            },
            {
                "type": "action",
                "actionType": "MOVE",
                "moveTarget": {
                    "type": "passage",
                    "passageTarget": "DEDUCTION_PUZZLE_12_CHECK_OUTCOME"
                }
            }
        ]
    },
    {
      "uid": "DEDUCTION_PUZZLE_12_CHECK_OUTCOME",
      "name": "Passcode Check",
      "description": "Passage description.",
      "tags": [
        {
          "name": "PUZZLE_OUTCOME",
          "color": "blue"
        },
        {
          "name": "CHOICE",
          "color": "green"
        },
        {
          "name": "GATE",
          "color": "orange"
        },
         {
          "name": "CODE",
          "color": "purple"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Processing Attempt",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "ada",
            "options": [
              {
                "type": "branchOption",
                "name": "Correct Path",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "eq",
                    "aspect": "isabella_phone_last_code",
                    "target": "TariffPayoff",
                    "aspectUid": "isabella_phone_last_code"
                  }
                },
                "description": "Hidden option for correct answer.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "EVIDENCE_EXAMINATION_13"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Incorrect Path (Retry)",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "and",
                    "target": [
                      {
                        "type": "ne",
                        "aspect": "isabella_phone_last_code",
                        "target": "TariffPayoff",
                        "aspectUid": "isabella_phone_last_code"
                      },
                      {
                        "type": "lt",
                        "aspect": "isabella_phone_attempts",
                        "target": 3,
                        "aspectUid": "isabella_phone_attempts"
                      }
                    ]
                  }
                },
                "description": "Hidden option for incorrect answer with retries left.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "DEDUCTION_PUZZLE_12"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              },
              {
                "type": "branchOption",
                "name": "Incorrect Path (Lockout)",
                "aspectCheck": {
                  "type": "checkAspect",
                  "check": {
                    "type": "and",
                    "target": [
                      {
                        "type": "ne",
                        "aspect": "isabella_phone_last_code",
                        "target": "TariffPayoff",
                        "aspectUid": "isabella_phone_last_code"
                      },
                      {
                        "type": "gte",
                        "aspect": "isabella_phone_attempts",
                        "target": 3,
                        "aspectUid": "isabella_phone_attempts"
                      }
                    ]
                  }
                },
                "description": "Hidden option for incorrect answer with no retries left.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "DEDUCTION_PUZZLE_12_LOCKOUT"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        }
      ]
    },
    {
      "uid": "DEDUCTION_PUZZLE_12_LOCKOUT",
      "name": "Phone Locked",
      "description": "Passage description.",
      "tags": [
        {
          "name": "PUZZLE_LOCKOUT",
          "color": "blue"
        },
        {
          "name": "CHOICE",
          "color": "green"
        }
      ],
      "commands": [
        {
          "type": "bot",
          "lines": [
            {
              "text": "<insert ADA response based on TOT personality>",
              "imageAlias": "",
              "imageDescription": ""
            }
          ],
          "branch": {
            "type": "branch",
            "description": "Device Locked",
            "replayAbility": "re-executable",
            "presentation": "option-list",
            "integrationType": "ada",
            "options": [
              {
                "type": "branchOption",
                "name": "Return to Hub",
                "aspectCheck": null,
                "description": "Go back to the main case view.",
                "actions": [
                  {
                    "type": "action",
                    "actionType": "MOVE",
                    "moveTarget": {
                      "type": "passage",
                      "passageTarget": "INVESTIGATION_HUB_7"
                    }
                  }
                ],
                "imageAlias": "",
                "imageDescription": ""
              }
            ]
          }
        }
      ]
    }
  ]
}