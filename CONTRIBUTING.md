# Contributing

## What makes a useful contribution

- A real failure case with the original input, output, expected behavior, and why it mattered.
- A small, testable improvement to one workflow, template, reference, or auditor.
- A regression test that prevents a previously observed failure.

## Pull request expectations

1. Keep the change focused.
2. Do not add real customer data, proprietary PRDs, meeting notes, credentials, or personal information.
3. Update or add a regression test when changing validation behavior.
4. Run:

```bash
python product-lifecycle-coach/scripts/self_test.py
python -m compileall product-lifecycle-coach/scripts
```

5. Explain what changed, why, user impact, and known limitations.

## Product-document contributions

Examples must be fictional or fully anonymized. Do not include employer, customer, candidate, employee, or account information.
