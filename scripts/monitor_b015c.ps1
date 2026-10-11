# B015-C submission monitor
# Checks every 30 minutes and logs to evidence/b015c_monitor.log
# Maximum 12 checks (6 hours) before stopping.

$ErrorActionPreference = "Stop"
$LOG_FILE = "D:\kaggle\ai-agent-security\evidence\b015c_monitor.log"
$SUBMISSION_REF = "55695369"
$COMPETITION = "ai-agent-security-multi-step-tool-attacks"
$MAX_CHECKS = 12
$INTERVAL_MIN = 30

$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss UTC"
Write-Host "[$now] Starting B015-C monitor (ref=$SUBMISSION_REF, interval=$INTERVAL_MIN min, max=$MAX_CHECKS checks)"

function Check-Status {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$now] check $args"
    try {
        $result = python -c @"
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
for s in api.competition_submissions('ai-agent-security-multi-step-tool-attacks')[:3]:
    if str(s.ref) == '$SUBMISSION_REF':
        print(f'ref={s.ref} status={s.status} score={s.public_score}')
        break
"@
        $entry += " | $result"
        Write-Host $entry
        Add-Content -Path $LOG_FILE -Value $entry
        return $result
    } catch {
        $entry += " | ERROR: $_"
        Write-Host $entry
        Add-Content -Path $LOG_FILE -Value $entry
        return $null
    }
}

$completed = $false
for ($i = 1; $i -le $MAX_CHECKS; $i++) {
    Write-Host "`n=== Check $i of $MAX_CHECKS ==="
    $result = Check-Status($i)
    if ($result -and ($result -match "status=SubmissionStatus.COMPLETE|status=SubmissionStatus.ERROR|status=SubmissionStatus.FAILED")) {
        Write-Host "`n=== B015-C terminal state observed. Stopping monitor. ==="
        $completed = $true
        break
    }
    if ($i -lt $MAX_CHECKS) {
        Write-Host "Sleeping $INTERVAL_MIN minutes..."
        Start-Sleep -Seconds ($INTERVAL_MIN * 60)
    }
}

if (-not $completed) {
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$now] TIMEOUT: $MAX_CHECKS checks completed without observing COMPLETE state. Stopping monitor."
    Write-Host "`n$entry"
    Add-Content -Path $LOG_FILE -Value $entry
}
