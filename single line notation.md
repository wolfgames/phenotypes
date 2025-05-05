
## Single-Line Passage Notation (SLPN) Documentation

### 1. Introduction & Purpose

The Single-Line Passage Notation (SLPN) is a highly compact, symbolic format designed to represent the structure and content of a game passage (originally conceived for Twine-like structures) entirely on a single line of text.

**Primary Goals:**

*   **Conciseness:** Drastically reduce the character count compared to formats like Twee or JSON. This was initially explored for potential use with Language Models (LLMs) where input/output token count can be a constraint.
*   **Machine Parsability:** While dense, the format follows strict rules intended to be unambiguously parsed by a dedicated script or program.
*   **Lossless Representation (Goal):** Aims to capture all essential information from the source passage structure (commands, content, branching, conditions, actions).

**Disclaimer:** This format prioritizes extreme conciseness over human readability. It requires a robust, custom parser to convert it to a usable format (like JSON) and is inherently more error-prone during manual creation or editing than more verbose formats.

### 2. Syntax Overview

A passage is represented as a continuous sequence of commands on a single line.

*   **Command Structure:** `CMD:param1=value1;param2=value2|value3;param3="quoted value";...;NXT:param=val;...`
*   **Command Codes (`CMD`, `NXT`):** Three-letter uppercase codes represent specific commands or structural elements (e.g., `PSG` for Passage Start, `BOT` for Bot Message).
*   **Command Separator (`:`):** A colon separates the command code from its parameters.
*   **Parameter Separator (`;`):** A semicolon separates key-value parameter pairs within a command *and* separates the end of one command's parameters from the start of the next command code.
*   **Key-Value Separator (`=`):** An equals sign separates a parameter key (three-letter lowercase code) from its value.
*   **List Item Separator (`|`):** A vertical bar separates individual items within a parameter value that represents a list (e.g., multiple lines in a bot message, multiple options in a branch).
*   **Whitespace:** Whitespace (spaces, tabs) is generally **ignored** unless it is part of a quoted value. It can be used for visual separation during debugging but has no semantic meaning.
*   **Quoting (`"`):** Double quotes are **required** around any parameter value that contains special characters (`;`, `:`, `=`, `|`) or significant leading/trailing/internal whitespace that must be preserved. Standard escaping rules (e.g., `\"` for a literal quote within a quoted string) apply.

### 3. Command Reference

The following commands form the basis of the notation. Parameter codes are lowercase.

| Code | Full Name              | Description                                                                 | Parameters (Code, Type, Req?, Description)                                                                                                                                                                      | Example Snippet                                                     |
| :--- | :--------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `PSG`  | Passage Start          | Marks the beginning of a passage definition. Always the first command.      | `uid` (String, Y, Passage unique ID), `nam` (String, Y, Passage display name)                                                                                                                                        | `PSG:uid=p1;nam="Start Room";...`                                   |
| `UPD`  | Updates Block Start    | *[Conceptual]* Marks the start of aspect updates (originally from Twine `:: Updates` block). Often followed by `CAS` or `UAS`. Requires a corresponding `END` if used explicitly, but often implicit. | *(None)*                                                                                                                                                                             | `...;UPD;CAS:...;UAS:...;END;...`                                   |
| `CAS`  | Create Aspect          | Defines a new aspect (variable).                                            | `asp` (String, Y, Aspect name), `typ` (Enum, Y, `boolean`\|`number`\|`string`), `val` (Any, Y, Initial value matching `typ`)                                                                                           | `...;CAS:asp=keyFound;typ=boolean;val=false;...`                      |
| `UAS`  | Update Aspect          | Modifies an existing aspect's value.                                        | `asp` (String, Y, Aspect name), `uty` (Enum, Y, `SET`\|`INCREMENT`), `val` (Any, Y, New value or increment amount)                                                                                                  | `...;UAS:asp=score;uty=INCREMENT;val=10;...`                        |
| `CNT`  | Content Block Start    | *[Conceptual]* Marks the start of main passage content (originally from Twine passage body). Often followed by `BOT`, `ACT`, `BRN`. Requires a corresponding `END` if used explicitly, but often implicit. | *(None)*                                                                                                                                                                             | `...;CNT;BOT:...;BRN:...;END;...`                                   |
| `BOT`  | Bot Message            | Represents a message displayed by the game/bot.                             | `lin` (List<String\|Object>, Y, Pipe-separated lines. See `LIN`), `brn` (Object, N, Optional nested Branch. See `BRN`)                                                                                                | `...;BOT:lin="Hello|Examine the desk?";brn=BRN:...;...`               |
| `LIN`  | Bot Line               | *[Implicit/Sub-Format]* Represents a single line within a `BOT` command's `lin` list. Can be a simple string or include an image prompt. | `txt` (String, N, Text content), `img` (String, N, Image generation prompt). *Note:* If complex, might need quoting/escaping like `"{txt:\"Line 1\", img:\"A desk\"}|{txt:\"Line 2\"}"`. Simple strings don't need this. | *(Used within `BOT:lin` parameter)*                                 |
| `BRN`  | Branch Command         | Defines a player choice point. Can be nested in `BOT` or standalone.       | `bds` (String, Y, Branch prompt/description), `brp` (Enum, Y, `re-playable`\|`once`), `bpr` (Enum, Y, `option-list`\|`block-panel`), `bit` (Enum, Y, `standalone`\|`blocking`), `ops` (List<Object>, Y, Pipe-separated options. See `BOP`) | `...;BRN:bds="What do you do?";brp=once;bpr=option-list;bit=blocking;ops=BOP:...|BOP:...;...` |
| `BOP`  | Branch Option          | Defines a single choice within a `BRN`.                                     | `onm` (String, Y, Option display name), `ods` (String, Y, Option description), `cnd` (Object, N, Display condition. See `CND`/`COR`/`CAD`), `img` (String, N, Optional image prompt), `act` (List<Object>, Y, Pipe-separated actions. See `ACT`/`BOT`) | `BOP:onm="Examine";ods="Look closer";act=ACT:...`                   |
| `CND`  | Condition (Simple)     | A simple check on an aspect value (used for `BOP` display or `IFF`).      | `typ` (Const, Y, `checkAspect`), `asp` (String, Y, Aspect name), `cmp` (Enum, Y, Operator e.g., `EQ`, `NEQ`, `GT`, `LT`), `val` (Any, Y, Value to compare against)                                                          | `CND:typ=checkAspect;asp=keyFound;cmp=EQ;val=true`                  |
| `COR`  | Condition (OR)         | Logical OR combination of multiple conditions.                              | `typ` (Const, Y, `checkAspect`), `lop` (Const, Y, `OR`), `cnd` (List<Object>, Y, Pipe-separated `CND`/`COR`/`CAD` objects)                                                                                             | `COR:typ=checkAspect;lop=OR;cnd=CND:...|CND:...`                        |
| `CAD`  | Condition (AND)        | Logical AND combination of multiple conditions.                             | `typ` (Const, Y, `checkAspect`), `lop` (Const, Y, `AND`), `cnd` (List<Object>, Y, Pipe-separated `CND`/`COR`/`CAD` objects)                                                                                            | `CAD:typ=checkAspect;lop=AND;cnd=CND:...|CND:...`                        |
| `ACT`  | Action Command         | Represents an action performed by the game (often triggered by `BOP`).      | `aty` (Enum, Y, Action type e.g., `MOVE`, `REVEAL`), `amt` (Object, N, Move target details if `aty=MOVE`. See `AMT`), `aet` (String, N, Evidence target UID/alias if not `MOVE` or `HIDE_ALL_EVIDENCE`)               | `ACT:aty=REVEAL;aet=evidence_key_123;...`                           |
| `AMT`  | Action Move Target     | *[Sub-Format]* Defines the target for a `MOVE` action.                     | `typ` (Enum, Y, `passage`\|`evidence`\|`application`), `tgt` (String, Y, Target name/UID based on `typ`)                                                                                                          | `AMT:typ=passage;tgt=NextRoom`                                      |
| `IFF`  | If Command             | Executes actions conditionally based on an aspect check.                   | `chk` (Object, Y, Condition check. See `CND`/`COR`/`CAD`), `ifa` (List<Object>, Y, Pipe-separated actions (`ACT`/`BOT`) to execute if check passes)                                                              | `IFF:chk=CND:...;ifa=ACT:...|BOT:...;...`                          |
| `END`  | Block End              | *[Conceptual/Optional]* Explicitly marks the end of a `UPD` or `CNT` block if needed for clarity or complex nesting. Often implicitly ended by the start of the next major block or end of line. | *(None)*                                                                                                                                                                             | `...;UPD;...;END;CNT;...;END`                                       |

**Note on Parameter Representation:**
*   **Simple Values:** `param=value` (e.g., `uid=passage1`, `val=true`, `val=10`).
*   **Quoted Values:** `param="value with ; chars"`
*   **Lists (Simple Strings):** `param=item1|item2|item3` (e.g., `lin="Line 1|Line 2"`)
*   **Lists (Complex Objects):** `param=CMD1:...|CMD2:...` (e.g., `ops=BOP:...|BOP:...`, `act=ACT:...|BOT:...`). Each object in the list starts with its appropriate command code.
*   **Nested Objects:** Represented directly using their command code and parameters (e.g., `brn=BRN:bds=...;ops=...;...`)

### 4. Nesting and Structure

The order of commands is crucial. The notation relies on sequence to imply structure:

*   A `PSG` command must be first.
*   `CAS` and `UAS` commands typically follow `UPD` (or appear early if `UPD` is implicit).
*   `BOT`, `ACT`, `BRN`, `IFF` typically follow `CNT` (or appear after updates if `CNT` is implicit).
*   A `BRN` command appearing directly within the parameter list of a `BOT` command (e.g., `BOT:lin=...;brn=BRN:...;...`) is considered nested *within* that `BOT` message.
*   `BOP` commands always belong to the most recently preceding `BRN` command (within its `ops` list).
*   `ACT` and `BOT` commands within a `BOP`'s `act` list are executed when that option is chosen.
*   `ACT` and `BOT` commands within an `IFF`'s `ifa` list are executed if the `IFF`'s `chk` condition is met.
*   Conditions (`CND`, `COR`, `CAD`) are typically found within a `BOP`'s `cnd` parameter or an `IFF`'s `chk` parameter. Nested conditions use the `cnd` parameter within `COR` or `CAD`.

Explicit `UPD`, `CNT`, and `END` commands are generally only needed if the default sequential grouping is insufficient or ambiguous, which should be rare in this strict format.

### 5. Full Example

```
PSG:uid=p1;nam="Dimly Lit Room";CNT;BOT:lin="You are in a dimly lit room. A desk sits against one wall.|A single door is set into the opposite wall.";brn=BRN:bds="Action?";brp=once;bpr=option-list;bit=blocking;ops=BOP:onm="Examine Desk";ods="Look closely at the desk";act=ACT:aty=REVEAL;aet=evidence_note_456|BOT:lin="You find a crumpled note."|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=p1;end=true|BOP:onm="Try Door";ods="Check if the door is locked";cnd=CND:typ=checkAspect;asp=doorLocked;cmp=EQ;val=true;act=ACT:aty=MOVE;amt=AMT:typ=passage;tgt=p2_locked_door|BOP:onm="Open Door";ods="Use the key";cnd=CAD:typ=checkAspect;lop=AND;cnd=CND:typ=checkAspect;asp=doorLocked;cmp=EQ;val=true|CND:typ=checkAspect;asp=hasKey;cmp=EQ;val=true;act=UAS:asp=doorLocked;uty=SET;val=false|ACT:aty=MOVE;amt=AMT:typ=passage;tgt=p3_hallway;
```

**Breakdown:**

1.  `PSG:uid=p1;nam="Dimly Lit Room";` - Start passage "p1", named "Dimly Lit Room".
2.  `CNT;` - Start content block (implicit start of commands).
3.  `BOT:lin="You are in a dimly lit room...|A single door...";brn=BRN:...;` - Bot message with two lines, followed by a nested branch.
4.  `BRN:bds="Action?";brp=once;bpr=option-list;bit=blocking;ops=BOP:...|BOP:...|BOP:...;` - Branch definition within the BOT message. `ops` contains three options separated by `|`.
5.  `BOP:onm="Examine Desk";ods="...";act=ACT:...|BOT:...|ACT:...` - First option. `act` list has three pipe-separated actions: `REVEAL`, `BOT`, `MOVE`.
6.  `BOP:onm="Try Door";ods="...";cnd=CND:...;act=ACT:...` - Second option. `cnd` parameter defines a simple condition (`doorLocked == true`). `act` is a `MOVE` action.
7.  `BOP:onm="Open Door";ods="...";cnd=CAD:...;act=UAS:...|ACT:...` - Third option. `cnd` parameter defines an `AND` condition (`doorLocked == true` AND `hasKey == true`). `act` list contains `UAS` (Update Aspect) and `ACT` (Move).

### 6. Parsing Considerations & Limitations

*   **Parser Complexity:** This format *requires* a dedicated, robust parser. Simple string splitting is insufficient due to quoting, nesting, and context-dependent interpretation of separators (`|`, `;`). The parser needs to manage state (e.g., which `BRN` does this `BOP` belong to?).
*   **Error Proneness:** Manual creation or editing is highly susceptible to syntax errors (missing separators, incorrect quoting, wrong command codes) that can be hard to debug.
*   **Readability:** The format is extremely difficult for humans to read and verify.
*   **Extensibility:** Adding new commands or parameters requires updating both the notation definition and the parser.
*   **Ambiguity (Potential):** While designed to be unambiguous, complex nesting or misuse of separators could potentially lead to parsing errors if the parser is not sufficiently robust.

This notation achieves its goal of conciseness but trades off readability, ease of use, and robustness. It's best suited for machine-to-machine communication where a dedicated parser/generator handles the format reliably.
