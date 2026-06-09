$ErrorActionPreference = "Stop"

$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
$EvidenceDir = Join-Path $Repo "evidence"
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Out = Join-Path $EvidenceDir "HUMANWARD_PROTECTION_REVIEW_$Stamp.md"

Set-Location $Repo

$CoreHash = (Get-FileHash ".\core\IMMUTABLE_CORE.md" -Algorithm SHA256).Hash
$GitStatus = git status --short
$TrackedLogs = git ls-files "*audit_chain.jsonl" "*review_queue.jsonl" "*signed_audit_export.json"
$RecentLog = git log --oneline -8
$Tags = git tag --list "humanward-public-v*"

$Lines = @()
$Lines += "# Humanward Protection Review"
$Lines += ""
$Lines += "Timestamp: $Stamp"
$Lines += ""
$Lines += "## Core hash"
$Lines += ""
$Lines += $CoreHash
$Lines += ""
$Lines += "## Git status"
$Lines += ""
if ($GitStatus) { $Lines += $GitStatus } else { $Lines += "clean or no short-status output" }
$Lines += ""
$Lines += "## Tracked generated logs"
$Lines += ""
if ($TrackedLogs) { $Lines += $TrackedLogs } else { $Lines += "none" }
$Lines += ""
$Lines += "## Recent commits"
$Lines += ""
$Lines += $RecentLog
$Lines += ""
$Lines += "## Public version tags"
$Lines += ""
$Lines += $Tags
$Lines += ""
$Lines += "## Notes"
$Lines += ""
$Lines += "Review manually for secrets/private keys before release."

$Lines | Set-Content $Out -Encoding UTF8

Write-Host "Protection review created:"
Write-Host $Out
