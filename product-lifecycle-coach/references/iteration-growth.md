# Measurement, iteration, retrospective, and PM growth

## 1. Measurement review

For each product outcome, compare:
- intended behavior change;
- observed user behavior;
- product quality and trust;
- operational cost and friction;
- business result;
- counter-metrics or harm.

Segment results by role, cohort, workflow, use case, and failure mode when aggregate metrics hide important differences.

Do not interpret correlation as causation without a credible design. Label inference.

## 2. Feedback synthesis

Combine:
- usage and funnel data;
- support and incident data;
- interviews and observation;
- user edits, overrides, complaints, and feature requests;
- sales and implementation feedback;
- engineering and operational friction;
- AI evaluation and failure cohorts.

Convert feedback into underlying jobs, causes, and constraints. Do not make a roadmap by vote count alone.

## 3. Iteration decision

For each proposed change state:
- evidence and problem;
- affected user and workflow;
- expected outcome;
- alternatives;
- confidence;
- effort and dependencies;
- risk and reversibility;
- learning value;
- recommendation: fix, improve, expand, experiment, defer, or remove.

Use a new change package for material work. Update the existing package only when the intent remains the same.

## 4. Experiment design

Define:
- hypothesis;
- target population;
- intervention and comparison;
- primary metric and guardrails;
- sample or duration rationale;
- instrumentation;
- confounders;
- stop conditions;
- decision rule.

For early enterprise pilots, qualitative evidence and workflow completion may be more useful than false statistical precision.

## 5. Roadmap update

Roadmaps should express outcome and uncertainty:

| Horizon | Outcome | Evidence or hypothesis | Initiative | Dependency | Decision trigger |
|---|---|---|---|---|---|

Remove work whose rationale no longer holds. Preserve the decision history.

## 6. Retrospective

Review:
- intended goal;
- actual outcome;
- what users did;
- what worked;
- what failed and root cause;
- assumptions invalidated;
- decisions that should be preserved;
- process or tooling changes;
- stop-doing list;
- next highest-value uncertainty.

Separate product failure, execution failure, adoption failure, and measurement failure.

## 7. Root-cause discipline

Do not stop at symptoms such as "users did not use it". Check:
- problem importance;
- discoverability;
- onboarding;
- workflow fit;
- trust;
- performance;
- permissions or access;
- incentives;
- organizational change;
- data or integration quality;
- implementation defects.

## 8. PM learning record

After substantial work, record only evidence-based development:

```markdown
### [Date or version] Capability area
- Situation: ...
- Demonstrated strength: ...
- Gap or recurring pattern: ...
- Better mental model: ...
- Next practice: ...
- Later evidence: ...
```

The goal is transfer of judgment, not dependency on the Skill. Over time:
- let the user frame more decisions;
- compare their reasoning to evidence;
- reduce explanation on mastered areas;
- increase challenge on recurring weak areas;
- continue to complete deliverables when requested.

## Skill and process improvement loop

When a real project exposes a workflow defect, treat it as an evaluation case:
1. describe the expected and actual routing;
2. identify the smallest instruction/template/script failure;
3. implement and test the correction;
4. rerun the exposing case and a prior regression case;
5. record remaining limitations and the next test.

Use `continuous-evaluation.md` and `SKILL_EVAL_REPORT.md`. Keep confidential project sources outside the packaged Skill.
