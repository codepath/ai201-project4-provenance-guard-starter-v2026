# Acceptance criteria

Drafted by AI at the student's explicit request before any scoring results. The student must review and defend these targets; the assignment asks for student-authored criteria.

1. **False positives:** In each of three trials of the same 20 independently human-written English samples (50-300 words, including at least five formal samples), at most one receives `guess: ai`.
   **Why:** A false accusation can damage a writer's reputation. A 5% ceiling is a demanding initial target, not an accuracy claim.

2. **Score spread:** In each of three trials on ten known AI-generated and ten independently human-written samples matched within 20% word count, the mean combined AI score exceeds the mean human score by at least 0.20.
   **Why:** A varying number must carry useful separation, rather than merely changing in the last decimal place.

3. **Label coverage:** Before evaluation, freeze three distinct sample texts in a fixture file. Each must produce its designated label (human, unsure, AI) in all three repeated submissions, and a sweep of 1,001 scores from 0 to 1 must map to exactly one of those labels with boundaries matching the README.
   **Why:** This checks both end-to-end reachability and complete, unambiguous mapping; synthetic scores alone cannot demonstrate text reachability.

4. **Appeals:** For ten existing content IDs, all ten valid appeals return HTTP 200 and `under_review`, append the exact reasoning and correct creator ID, and preserve the original decision. Ten unknown IDs must return 404 without an appeal event.
   **Why:** Every writer needs a reliable challenge path, and the audit trail must show what was challenged.

5. **Bad input:** Every request in a fixed matrix (malformed JSON, non-object JSON, missing fields, nulls, wrong types, blank text/creator/reasoning, text over 20,000 characters, creator IDs over 200 characters, and reasoning over 5,000 characters) returns a JSON 4xx response, makes zero detector calls, and creates no decision or appeal event. A valid 20,000-character text must pass validation.
   **Why:** Predictable validation prevents crashes and unnecessary model work; the inclusive size boundary must be explicit.
