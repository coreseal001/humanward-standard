# Humanward Reviewer Quickstart v1

## Ten-minute review path

1. Read README.md.
2. Read the A-to-M classification system.
3. Read the declaration-of-intent protocol.
4. Read the modus-operandi disclosure matrix.
5. Read the life-impact atlas.
6. Open one issue template.
7. Submit one improvement, weakness, or classification.

## Technical review path

```powershell
cd "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard\prototypes\humanward-ai-mvp"
python -m pytest
python -m humanward_ai.reviewer_check
python -m humanward_ai.v2_readiness --repo-root "..\.."
```

Expected:

- tests pass,
- reviewer_check overall_pass true,
- v2_readiness overall_pass true.
