# 调研与问题验证

调研的目标是降低下一项产品决策的风险，不是生成一篇长报告。先明确要支持的决策，并在需要持续执行时使用 `assets/templates/DISCOVERY_PLAN.md`。

## 1. Frame the research

Define:
- decision to be made;
- current belief or hypothesis;
- critical unknowns;
- evidence threshold appropriate to stakes;
- time and access constraints;
- what would change the decision.

Avoid broad requests such as "research this market" without a decision frame.

## 2. Build the evidence plan

Use only relevant methods:

- **User evidence:** interviews, observations, support logs, workflow shadowing, survey, usage data.
- **Market evidence:** market structure, buyer behavior, budgets, regulation, timing.
- **Competitive evidence:** direct competitors, substitutes, manual workarounds, internal alternatives.
- **Technical evidence:** feasibility spikes, API and platform constraints, latency, data availability, model quality.
- **Business evidence:** willingness to pay, implementation burden, sales cycle, margin, service cost.
- **Operational evidence:** ownership, exception handling, support, audit, deployment, change management.

For current facts, search current primary or authoritative sources. Record publication dates and limitations.

## 3. User and stakeholder discovery

Identify separately:
- end user;
- buyer or budget owner;
- administrator or operator;
- manager or beneficiary;
- approver, compliance, security, or IT;
- people negatively affected by the workflow.

Interview for real behavior, not opinions about hypothetical features. Ask for the latest concrete episode:
- trigger;
- steps;
- tools and handoffs;
- delays and workarounds;
- consequences;
- current success criteria;
- exceptions;
- what has already been tried.

Distinguish stated preference from observed behavior.

## 4. Competitor and alternative analysis

Do not create a feature matrix alone. Analyze:
- target customer and wedge;
- core job and workflow;
- acquisition or deployment model;
- time to value;
- switching cost;
- pricing and packaging when available;
- product strengths;
- user complaints and failure modes;
- what is intentionally omitted;
- which mechanisms transfer to this context and which do not.

Include the real alternative: spreadsheets, manual service, existing enterprise system, doing nothing, or internal process.

## 5. Evidence ledger

For each important claim record:

| Field | Meaning |
|---|---|
| Claim | What might be true |
| Source | Link, file, interview, data query |
| Date | When evidence was created |
| Type | Fact, observation, quote summary, metric, inference |
| Strength | Strong, moderate, weak |
| Limitation | Bias, sample size, staleness, access gap |
| Implication | Product decision affected |

Never convert weak evidence into a confident market fact.

## 6. Synthesis

Produce:
- target segment and stakeholder map;
- current workflow;
- unmet need or opportunity;
- current alternatives;
- evidence supporting and contradicting the opportunity;
- most important assumptions;
- risks and unknowns;
- recommendation: proceed, narrow, test, pause, or stop;
- next cheapest evidence-generating action.

## 7. 研究结论与行动

结论必须给出：继续、收窄、补证、暂停或停止；最关键依据；最强反向证据；下一项最便宜的证据行动。不要用“需要更多研究”作为无期限结论。

## 8. Research quality gate

Check:
- Does evidence relate to the decision?
- Are sources current enough?
- Are primary sources preferred where possible?
- Are users, buyers, and operators distinguished?
- Are contradictory signals represented?
- Are facts separated from interpretation?
- Is the sample limitation explicit?
- Could a cheaper test answer the question better?

For high-stakes products, triangulate important conclusions across at least two independent evidence types.
