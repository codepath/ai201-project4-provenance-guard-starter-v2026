# Capstone acceptance criteria — recorded before evaluation

AI-authored at the user's explicit request. These do not meet the assignment's
unaided-authorship requirement; the student must disclose and defend them.
Scope: Shape A, operational instrumentation of the existing Provenance Guard.
Each criterion receives three independent trials, before and after one fix.

1. **Successful request trace (extension).** In each trial, all three real-model
   submissions return HTTP 200 and have exactly one telemetry record matching
   their X-Request-ID, with UTC timestamp, input summary, output JSON, HTTP status,
   wall milliseconds and process CPU milliseconds. Reason: a missing or duplicate
   trace makes it impossible to reconcile a writer's response with the log.
2. **Rejected request trace (extension, failure).** In each trial, all five cases
   (invalid JSON, missing text, blank creator, oversized text, unknown appeal ID)
   return their expected 400/413/404 status and exactly one matching telemetry
   record containing that status and error. Reason: successful-only telemetry
   hides refused requests and makes failure rates misleading.
3. **Stage attribution (extension).** In each trial, all three successful traces
   have positive model_ms and nonnegative style_ms, combine_ms and audit_ms;
   summed stages must not exceed wall_ms by more than 1 ms. Reason: this is enough
   to locate the expensive stage without pretending a timer is perfectly precise.
4. **Warm local latency (extension).** In each trial all three successful warm
   submissions complete in less than 5,000 ms measured by the HTTP client.
   Model initialization is measured separately and excluded. Reason: five seconds
   is a tolerable interactive local wait, and initialization is a separate cost.
5. **Original workflow preserved (regression).** In each trial one of the three
   real submissions exposes all original decision fields and can be appealed;
   its original decision remains unchanged in /log and an under_review event
   is appended. Target: one complete workflow out of one per trial. Reason:
   operational work must preserve the writer's route to contest a decision.
