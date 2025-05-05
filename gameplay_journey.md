**Case:** The Bathtub Betrayal
**Goal:** Navigate a risk/reward investigation to uncover the truth behind Iryna Anderson-Chen's death and identify her killer.

**(Phase 1: Introduction & Theory Choice)**

1.  **CASE_HOOK: Case Introduction & Decision**
    *   **DECISION:** Accept or Decline the Case?
    *   **CLUES/DATA:**
        *   Visual Hook: Photo of opulent Pacific Heights mansion bathroom, police tape visible near tub.
        *   Text Hook: "Tech executive wife found drowned in bathtub at mansion, staged as suicide. Blood spatter screams murder. Missing phone holds dark secrets."
        *   Context Summary: High-profile victim, initial suicide ruling contradicted by forensic hints. Three individuals stand to benefit from her death.
    *   **OPTIONS:**
        - Accept Case (Risk: High stakes, complex financial and personal angles; Reward: Opportunity to uncover a hidden truth and deliver justice)
        - Decline Case (Risk: A murderer potentially walks free; Reward: Avoid delving into a twisted web of wealth and betrayal)
    *   **ACTION:** `IF Accept: NAVIGATE INTRO_SEQUENCE_Start ELSE: NAVIGATE HOME`

2.  **INTRO_SEQUENCE: Initial Theory Choice**
    *   **DECISION:** Based on the initial scene and preliminary information, which theory seems most promising to investigate first?
    *   **CLUES/DATA:**
        *   Theory 1 (The Husband's Desperation - True Positive): Husband James Chen, CEO, gambling debts, staged suicide for insurance/assets. Evidence Snippet: Initial report hints at staged scene.
        *   Theory 2 (The Lover's Jealousy - False Positive): Personal trainer Emma Sullivan, close friend, possible affair/beneficiary, alibi shaky. Evidence Snippet: Beneficiary of Iryna's will.
        *   Theory 3 (The Business Conspiracy - False Negative): Business Partner Qasim Al-Suwaidi or Politician Jordan Powell, financial motives, but staging seems personal. Evidence Snippet: Both have financial interests in Iryna's success.
    *   **OPTIONS:**
        - Pursue: The Husband's Desperation (Risk: Could overlook other key players; Reward: Prioritize financial trail and marital secrets)
        - Pursue: The Lover's Jealousy (Risk: May be a red herring; Reward: Explore personal relationships and alibis)
        - Pursue: The Business Conspiracy (Risk: Staging doesn't fit a simple business hit; Reward: Focus on corporate and political connections)
    *   **ACTION:** `LOCK Phase 2; SET ChosenTheory=<choice>; NAVIGATE to Phase 2 start based on ChosenTheory (e.g., EVIDENCE_COLLECTION)`

**(Phase 2: Initial Investigation State)**

3.  **EVIDENCE_COLLECTION: Argonaut Hotel Suite (Initial Sweep - Framed by Chosen Theory)**
    *   **DECISION:** Begin searching the Argonaut Hotel Suite based on your initial hypothesis.
    *   **CLUES/DATA:**
        *   Scene Description: Opulent mansion suite, signs of recent disturbance contained to bathroom area.
        *   Framed Hotspots: Bathroom (crime scene focus), James's Home Office (potential financial/personal docs), Living Room (area mentioned by witness).
    *   **OPTIONS:**
        - Focus on the Bathroom (Risk: Might miss crucial context elsewhere; Reward: Direct interaction with primary crime scene)
        - Start with James's Home Office (Risk: Could be a distraction if not central; Reward: Potential to find financial/business clues quickly)
        - Examine the Living Room Area (Risk: Least likely spot for direct evidence; Reward: Might find overlooked personal items)
    *   **ACTION:** `NAVIGATE to selected hotspot (e.g., EVIDENCE_EXAMINATION or unlock relevant data)`

**(Phase 3: Hypothesis Check & Core Investigation)**

4.  **EVIDENCE_VERIFICATION: Forensic Analysis Results - Blood Spatter**
    *   **DECISION:** Interpret the new forensic finding in light of your current theory.
    *   **CLUES/DATA:**
        *   Evidence: Blood spatter analysis report.
        *   Finding: Spatter pattern near the tub indicates forced submersion and struggle, contradicting initial suicide appearance.
    *   **OPTIONS:**
        - Confirm Theory: This supports a staged suicide by an attacker. (Risk: If wrong, waste time pursuing wrong attacker; Reward: Validates focus on murder, not suicide)
        - Re-evaluate: This could still be a struggle *during* a suicide attempt. (Risk: Could miss signs of foul play; Reward: Maintains possibility of complex suicide scenario)
        - Dismiss: It's an anomaly, focus on other evidence. (Risk: Ignore critical physical evidence; Reward: Continue pursuing original lead unchecked)
    *   **ACTION:** `VALIDATE interpretation against true scenario (staged suicide); IF Correct: TRIGGER DeductionSuccess (ValidInterpretation); NAVIGATE InvestigationHub ELSE: TRIGGER DeductionFailure (Misinterpretation); MARK HypothesisChallenged; NAVIGATE INTRO_SEQUENCE_Start` # Sends player back to reconsider theory if wrong

5.  **INVESTIGATION_HUB: Plan Your Next Step**
    *   **DECISION:** What area do you want to investigate or who do you want to look into next?
    *   **CLUES/DATA:**
        *   Available Locations: Argonaut Hotel Suite, Police Precinct (Evidence Lockup, Interview Rooms).
        *   Known Suspects: James Chen, Emma Sullivan, Qasim Al-Suwaidi, Jordan Powell.
        *   Available Actions: Review Evidence, Examine Suspect Profiles, Visit Locations.
    *   **OPTIONS:**
        - Visit: Police Precinct (Risk: May not have crime scene context; Reward: Access official reports/evidence lockup)
        - Review: Suspect List (Risk: Passive information gathering; Reward: Get overview of suspects & profiles)
        - Review: Evidence Log (Risk: Might lose sense of urgency; Reward: Deep dive into collected clues)
    *   **ACTION:** `NAVIGATE to selected activity (e.g., EVIDENCE_COLLECTION, SUSPECT_LIST, EVIDENCE_EXAMINATION)`

6.  **SUSPECT_LIST: Review Suspects**
    *   **DECISION:** Which suspect's profile do you want to examine in detail?
    *   **CLUES/DATA:** (Brief overview of each suspect and their potential connection based on initial info)
        *   James Chen: Husband, initial inconsistencies, financial link potential.
        *   Emma Sullivan: Personal Trainer, close friend, beneficiary, alibi questions.
        *   Qasim Al-Suwaidi: Business Partner, financial motive link.
        *   Jordan Powell: Politician, financial motive link, alibi questions.
    *   **OPTIONS:**
        - Examine James Chen (Risk: May reinforce bias prematurely; Reward: Focus on primary person at scene)
        - Examine Emma Sullivan (Risk: Follow personal lead that might be minor; Reward: Investigate relationship and alibi)
        - Examine Qasim Al-Suwaidi (Risk: Business angle might be complex; Reward: Investigate financial ties)
        - Examine Jordan Powell (Risk: Political ties might be complex; Reward: Investigate political influence and alibi)
    *   **ACTION:** `NAVIGATE SuspectProfile(<choice>)`

7.  **SUSPECT_PROFILE: James Chen**
    *   **DECISION:** Analyze James Chen's profile and initial statement.
    *   **CLUES/DATA:**
        *   Profile: CEO, Iryna's husband, gambling addiction confirmed by financial records.
        *   Initial Statement: "I called 911 as soon as I found Iryna in the tub."
        *   Known Evidence: Financial records showing debt, blood spatter report (contradicts suicide).
    *   **OPTIONS:**
        - Analyze Statement for Contradiction (Risk: Might misinterpret; Reward: Unlocks Deduction Puzzle)
        - Review Financial Records (Risk: Delays statement analysis; Reward: Solidifies motive evidence)
        - Return to Suspect List (Risk: Lose focus; Reward: Review other suspects)
    *   **ACTION:** `IF Analyze Statement: NAVIGATE DeductionPuzzle(JamesStatement) ELSE IF Review Financial: NAVIGATE EvidenceExamination(FinancialRecords) ELSE: NAVIGATE SuspectList`

**(Phase 4: Deduction & Analysis)**

8.  **DEDUCTION_PUZZLE: Analyze James Chen's Statement**
    *   **DECISION:** Identify the lie in James Chen's statement based on the evidence.
    *   **CLUES/DATA:**
        *   Statement 1: "I was there, but I didn't do anything wrong."
        *   Statement 2: "It was just a normal initiation ritual that got out of hand." (Red Herring - this is from synopsis, but not James's *initial* statement in provided data. Use true statement from data). -> Corrected: Use the statement provided in the data section.
        *   James's actual statement: *"Look, I was there, but I didn't do anything wrong. It was just a normal initiation ritual that got out of hand. I called 911 as soon as I found Iryna in the tub."* - Let's use the 'Called 911' part vs timing.
        *   Statement 1 (Proposed Truth 1): "I was at the mansion when Iryna died." (Supported by his own admission)
        *   Statement 2 (Proposed Truth 2): "I found Iryna unresponsive in the bathtub." (Supported by his 911 call)
        *   Statement 3 (Proposed Lie): "I called 911 as soon as I found Iryna in the tub." (Contradicted by timeline/potential staging time)
        *   Evidence: Timeline of events, initial scene observations suggesting staging.
    *   **OPTIONS:**
        - Identify Statement 3 (Called 911 as soon as) as the Lie (Risk: Penalty/delay if wrong; Reward: Unlocks 'Timing Contradiction' evidence + progress)
        - Identify Statement 1 (Was at mansion) as the Lie (Risk: Incorrect deduction penalty; Reward: None)
        - Identify Statement 2 (Found unresponsive) as the Lie (Risk: Incorrect deduction penalty; Reward: None)
    *   **ACTION:** `VALIDATE selection; IF Correct (Stmt 3): TRIGGER DeductionSuccess; UNLOCK TimingContradictionEvidence; NAVIGATE InvestigationHub ELSE: TRIGGER DeductionFailure; NAVIGATE SuspectProfile(James)`

9.  **EVIDENCE_COLLECTION: Police Precinct - Evidence Lockup**
    *   **DECISION:** Search the evidence lockup for items collected from the scene or suspects.
    *   **CLUES/DATA:**
        *   Available items: Sedative bottle found near tub, James's financial records, items from suspects (e.g., Emma's phone records, Qasim's laptop, Jordan's calendar). Missing: Iryna's iPhone.
        *   Hint: The missing iPhone is a key piece...
    *   **OPTIONS:**
        - Examine Sedative Bottle (Risk: Might just confirm dosage; Reward: Link specific substance to scene)
        - Examine Financial Records (Risk: Already summarized; Reward: Deeper dive into James's debt specifics)
        - Search for Missing iPhone (Risk: May not be in standard lockup; Reward: Could find lead to breakthrough)
    *   **ACTION:** `IF Search for iPhone: MARK iPhoneSearchAttempted; IF iPhoneSearchAttempted AND TimingContradictionEvidenceUnlocked: NAVIGATE DeductionPuzzle(iPhoneLocation) ELSE: ADD Clue "iPhone not found here"; NAVIGATE InvestigationHub ELSE IF Examine Sedative: NAVIGATE EvidenceExamination(SedativeBottle) ELSE IF Examine Financial: NAVIGATE EvidenceExamination(FinancialRecords)` # Gated unlock for iPhone location deduction

10. **DEDUCTION_PUZZLE: Where is the iPhone?**
    *   **DECISION:** Based on available evidence (Timing Contradiction, Financial Motive), where might James have hidden Iryna's iPhone?
    *   **CLUES/DATA:**
        *   Clue 1: James delayed calling 911 after finding her.
        *   Clue 2: James is deeply in debt and needs money/assets.
        *   Clue 3: The iPhone contains proof of his gambling, affair, and Iryna's divorce/hidden camera.
        *   Hint: Think about where someone hides things related to money or secrets.
    *   **OPTIONS:**
        - At Home (Risk: Too risky, police searched; Reward: Found quickly)
        - With a Friend (Risk: Involves another person; Reward: Found)
        - In a Bank Safe Deposit Box (Risk: Requires warrant/specific lead; Reward: Most secure place for secrets/valuables)
        - Destroyed (Risk: Can't recover data; Reward: Ends search)
    *   **ACTION:** `VALIDATE selection; IF Correct (Safe Deposit Box): TRIGGER DeductionSuccess; UNLOCK SafeDepositBoxWarrant; NAVIGATE EvidenceCollection(Bank) ELSE: TRIGGER DeductionFailure; NAVIGATE InvestigationHub`

11. **EVIDENCE_COLLECTION: Bank Safe Deposit Box**
    *   **DECISION:** Access the safe deposit box.
    *   **CLUES/DATA:** Warrant secured based on deduction. Box registered to James Chen.
    *   **OPTIONS:**
        - Open the Box (Risk: May be empty or contain decoy; Reward: Access contents)
    *   **ACTION:** `UNHIDE iPhoneInBox; NAVIGATE EvidenceExamination(IrynaiPhone)`

12. **EVIDENCE_EXAMINATION: Iryna's iPhone (Locked)**
    *   **DECISION:** Access the locked iPhone.
    *   **CLUES/DATA:** iPhone recovered. Password protected. Tech specialist needed.
    *   **OPTIONS:**
        - Send to Tech Specialist (Risk: Time delay; Reward: Unlock attempt)
        - Try Common Passcodes (Risk: May lock device; Reward: Quick access if lucky)
    *   **ACTION:** `IF Send to Specialist: NAVIGATE DeductionPuzzle(iPhonePasscodeTrial) ELSE IF Try Common: TRIGGER DeductionFailure (FailedQuickAttempt); NAVIGATE EVIDENCE_EXAMINATION(IrynaiPhone)` # Forces specialist path

13. **DEDUCTION_PUZZLE: Unlock iPhone (Passcode Trial)**
    *   **DECISION:** The tech specialist needs the passcode. Use info about Iryna.
    *   **CLUES/DATA:**
        *   Passcode entry screen.
        *   Hint from Specialist: "Iryna used facial recognition, but also a simple numerical code. It might be related to something very important to her..."
        *   Relevant Clues (from profile/events): Marriage date (2011), Startup year (2013), Research breakthrough year (2021), Husband's birthday, Pet's birthday?
    *   **OPTIONS:** (Representing attempts with common/relevant number formats)
        - Enter: 0922 (Marriage Month/Day) (Risk: Attempt penalty; Reward: Correct code unlocks file)
        - Enter: 2013 (Startup Year) (Risk: Attempt penalty; Reward: ...)
        - Enter: 2021 (Breakthrough Year) (Risk: Attempt penalty; Reward: ...)
        - Enter: 1107 (Example wrong birthday) (Risk: Attempt penalty; Reward: ...)
    *   **ACTION:** `VALIDATE passcode; IF Correct (e.g., 0922 or 2011? Let's make it marriage year 2011): TRIGGER DeductionSuccess; UNLOCK IrynaiPhoneContent; NAVIGATE BREAKTHROUGH_MOMENT ELSE: TRIGGER DeductionFailure; PENALTY (e.g., Time Delay, Retry); NAVIGATE DeductionPuzzle(iPhonePasscodeTrial)`

**(Phase 5: Confrontation & Resolution)**

14. **BREAKTHROUGH_MOMENT: The iPhone Revelation**
    *   **DECISION:** What is the most critical information revealed on the iPhone?
    *   **CLUES/DATA:**
        *   Unlocked Content: Text messages (Iryna + Divorce Lawyer re: James's debt/affair), Messages (Iryna + Emma re: intimate relationship hint), Hidden Camera Video (James arguing with Iryna about divorce night of murder).
    *   **OPTIONS:**
        - Focus on Divorce/Debt Texts (Risk: Miss the most direct evidence of crime; Reward: Confirm motive)
        - Focus on Iryna/Emma Texts (Risk: Red herring for culprit; Reward: Confirm relationship angle)
        - Focus on Hidden Camera Video (Risk: Requires viewing; Reward: Direct evidence linking James to final argument/motive just before death)
    *   **ACTION:** `SET KeyRevelation=<choice>; IF KeyRevelation=HiddenCameraVideo: UNLOCK DefinitiveMotiveOpportunity; NAVIGATE SuspectConfrontation(James) ELSE: NAVIGATE InvestigationHub` # Forces path to key evidence

15. **SUSPECT_CONFRONTATION: Confronting James Chen with the Video**
    *   **DECISION:** Present the most damning evidence to James Chen.
    *   **CLUES/DATA:**
        *   Evidence Presented: Hidden camera video of final argument about divorce/debt.
        *   Suspect Reaction: James's composure breaks, shows signs of distress and confession under pressure.
    *   **OPTIONS:**
        - Directly Accuse James Now (Risk: Final step, no turning back; Reward: Proceed to accusation)
        - Present Other Evidence First (Financials, Sedative) (Risk: May allow him to regain composure; Reward: Reinforce evidence chain before accusation)
    *   **ACTION:** `IF Directly Accuse: NAVIGATE ACCUSATION ELSE: MARK EvidenceReinforced; NAVIGATE ACCUSATION`

16. **ACCUSATION: Make Your Final Accusation**
    *   **DECISION:** Based on the evidence, who is responsible for Iryna Anderson-Chen's death?
    *   **CLUES/DATA:**
        *   Evidence Summary (James Chen): Financial records (motive), Blood spatter (means contradiction), Timing contradiction (opportunity staging), iPhone video (definitive motive/opportunity), Sedative evidence (means).
        *   Evidence Summary (Other Suspects): Alibis confirmed or evidence circumstantial/contradicted by forensics/iPhone.
    *   **OPTIONS:**
        - Accuse James Chen (Risk: If wrong, case unsolved; Reward: Bring the true culprit to justice)
        - Accuse Emma Sullivan (Risk: Incorrect accusation; Reward: Incorrect conclusion)
        - Accuse Qasim Al-Suwaidi (Risk: Incorrect accusation; Reward: Incorrect conclusion)
        - Accuse Jordan Powell (Risk: Incorrect accusation; Reward: Incorrect conclusion)
    *   **ACTION:** `VALIDATE accusation against true culprit (James Chen); TRIGGER CASE_RESOLUTION(<choice>)`

17. **CASE_RESOLUTION: The Bathtub Betrayal - Verdict**
    *   **DECISION:** Review the case outcome.
    *   **CLUES/DATA:**
        *   Verdict: James Chen found guilty.
        *   Explanation: Recap of how financial desperation and the impending divorce, captured on Iryna's hidden camera, led James to stage her murder as a suicide, revealed by forensic science and the recovery of her hidden iPhone.
    *   **OPTIONS:**
        - Review Evidence Log (Risk: None; Reward: See full evidence collected)
        - Return to Main Menu (Risk: None; Reward: End case)
    *   **ACTION:** `NAVIGATE HOME`