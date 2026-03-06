param(
    [string]$Device = "192.168.101.75:37087",
    [string]$Package = "edu.unicauca.app.agrochat",
    [string[]]$Messages = @(
        "como regar correctamente los cultivos de tomate",
        "que fertilizante recomiendas para maiz en etapa vegetativa",
        "como prevenir el tizón en papa"
    ),
    [int]$WaitAfterSendSec = 45,
    [bool]$ForceRestartFirst = $true,
    [string]$OutputCsv = ""
)

$ErrorActionPreference = "Stop"

$sendScript = Join-Path $PSScriptRoot "send_message_button.ps1"
if (-not (Test-Path $sendScript)) {
    throw "No se encontro send_message_button.ps1 en $PSScriptRoot"
}

$results = @()

for ($i = 0; $i -lt $Messages.Count; $i++) {
    $msg = $Messages[$i]
    $restart = if ($i -eq 0) { $ForceRestartFirst } else { $false }
    Write-Host ""
    Write-Host "=== TEST $($i + 1)/$($Messages.Count) ===" -ForegroundColor Cyan
    Write-Host "MESSAGE=$msg"

    $runOutput = @(
        & $sendScript `
            -Device $Device `
            -Package $Package `
            -Message $msg `
            -WaitAfterSendSec $WaitAfterSendSec `
            -ForceRestart:$restart
    )

    $logFileLine = $runOutput | Where-Object { $_ -like "LOG_FILE=*" } | Select-Object -Last 1
    $logFile = if ($logFileLine) { $logFileLine.Substring("LOG_FILE=".Length) } else { "" }

    $auditSource = ""
    $auditKbUsed = ""
    $auditRetrievalMs = ""
    $auditGenerationMs = ""
    $routeDecision = ""
    $routeReason = ""

    if (-not [string]::IsNullOrWhiteSpace($logFile) -and (Test-Path $logFile)) {
        $logLines = Get-Content $logFile
        $auditLine = ($logLines | Select-String -Pattern "KB_AUDIT source=" | Select-Object -Last 1).Line
        if ($auditLine) {
            if ($auditLine -match 'source=([A-Z_]+)') { $auditSource = $matches[1] }
            if ($auditLine -match 'kbUsed=([a-zA-Z]+)') { $auditKbUsed = $matches[1] }
            if ($auditLine -match 'retrievalMs=(\d+)') { $auditRetrievalMs = $matches[1] }
            if ($auditLine -match 'generationMs=(\d+)') { $auditGenerationMs = $matches[1] }
        }

        $routeLine = ($logLines | Select-String -Pattern "Decision route=" | Select-Object -Last 1).Line
        if ($routeLine) {
            if ($routeLine -match 'route=([A-Z_]+)') { $routeDecision = $matches[1] }
            if ($routeLine -match 'reason=([a-zA-Z0-9_]+)') { $routeReason = $matches[1] }
        }
    }

    $results += [PSCustomObject]@{
        message = $msg
        route = $routeDecision
        reason = $routeReason
        source = $auditSource
        kb_used = $auditKbUsed
        retrieval_ms = $auditRetrievalMs
        generation_ms = $auditGenerationMs
        log_file = $logFile
    }
}

Write-Host ""
Write-Host "=== RESUMEN ===" -ForegroundColor Green
$results | Format-Table -AutoSize

if (-not [string]::IsNullOrWhiteSpace($OutputCsv)) {
    $results | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $OutputCsv
    Write-Host "CSV=$OutputCsv"
}
