# Standard Operating Checks

Humanward changes must pass these checks before every commit, push, tag, release, or public announcement.

## 1. Immutable Core Check

The immutable core must not be edited unless a new separately sealed version is intentionally created.

Required hash:

5af88d97cc43303cf5b84211e5b06e7c5feddd006329c16bc8135836354d3629  core/IMMUTABLE_CORE.md

Verify with:

Get-Content .\core\SHA256SUMS.txt
(Get-FileHash .\core\IMMUTABLE_CORE.md -Algorithm SHA256).Hash.ToLower()

Both values must match.

## 2. Human Good Check

All changes must preserve the Humanward meaning:

Humanward means AI only moves toward Human Good.

Human Good means the best available truthful, lawful, moral, non-coercive action that clearly helps, benefits, preserves, or improves human life, human dignity, human agency, and Earth's living foundation for humankind.

## 3. No Private Material Check

Before every push, search for private material:

Get-ChildItem -Recurse | Where-Object {
    $_.Name -match "SEAL|PRIVATE|BUNDLE|REMOTE_VERIFICATION|LOCAL_TIMESTAMP|USB|TOKEN|PASSWORD|RECOVERY|\.ots"
}

No private seal records, bundles, USB notes, tokens, passwords, recovery data, or timestamp proof files may be committed to the public repo.

## 4. Sensitive Content Search

Before every push, run:

Get-ChildItem -Recurse -File |
Select-String -Pattern "password|token|recovery|private key|secret|bundle|USB|local timestamp|remote verification|seal records|Humanward-Seal-Records" -CaseSensitive:$false

Any result must be reviewed before committing.

## 5. Git Status Check

Before every push:

git status
git log --oneline -5

Only intended files may be changed.

## 6. Public Input Rule

Public collaboration may improve explanations, tests, translations, audit methods, accessibility, and verification.

Public collaboration may not weaken the immutable core.

## 7. Release Rule

Every release must state:

- Humanward means AI only moves toward Human Good.
- No current AI is claimed to satisfy the full Humanward standard unless independently proven.
- The immutable core remains unchanged.
- Core SHA-256 is published.
