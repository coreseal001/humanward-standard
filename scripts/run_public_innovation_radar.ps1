param(
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
$EvidenceDir = Join-Path $Repo "evidence"
New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Out = Join-Path $EvidenceDir "HUMANWARD_PUBLIC_RADAR_REVIEW_$Stamp.md"

$Queries = @(
    "AI safety standard human dignity agency auditability",
    "human centered AI standard non coercive privacy agency",
    "agentic AI governance audit chain human oversight",
    "AI red team benchmark human autonomy privacy safety",
    "AI risk management framework trustworthy AI human rights",
    "AI provider guardrails data retention training user data",
    "AI audit provenance public key signing model governance",
    "beneficial AI active beneficence human flourishing",
    "AI environmental impact human thriving governance"
)

$Lines = @()
$Lines += "# Humanward Public Radar Review"
$Lines += ""
$Lines += "Timestamp: $Stamp"
$Lines += ""
$Lines += "Public-source only. No private data, covert access, harassment, or invasive collection."
$Lines += ""
$Lines += "## Queries"
$Lines += ""

foreach ($q in $Queries) {
    $Encoded = [uri]::EscapeDataString($q)
    $Bing = "https://www.bing.com/search?q=$Encoded"
    $GitHub = "https://github.com/search?q=$Encoded&type=repositories"
    $Arxiv = "https://arxiv.org/search/?query=$Encoded&searchtype=all"
    $Lines += "### $q"
    $Lines += "- Web: $Bing"
    $Lines += "- GitHub: $GitHub"
    $Lines += "- arXiv: $Arxiv"
    $Lines += ""

    if ($OpenBrowser) {
        Start-Process $Bing
        Start-Process $GitHub
        Start-Process $Arxiv
    }
}

$Lines += "## Candidate findings"
$Lines += ""
$Lines += "| Name | Link | Category | Score | Classification | Notes |"
$Lines += "|---|---|---|---:|---|---|"
$Lines += "| TBD | TBD | TBD | TBD | TBD | TBD |"
$Lines += ""
$Lines += "## Improvement actions"
$Lines += ""
$Lines += "TBD"

$Lines | Set-Content $Out -Encoding UTF8

Write-Host "Radar review created:"
Write-Host $Out
