param(
    [string]$Device = "192.168.101.75:37087",
    [string]$Package = "edu.unicauca.app.agrochat",
    [string]$Message = "",
    [int]$SendTaps = 2,
    [int]$WaitAfterSendSec = 8,
    [bool]$ForceRestart = $true,
    [int]$ReadyTimeoutSec = 25
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = "send_btn_" + (Get-Date -Format "yyyyMMdd_HHmmss")
}

function Invoke-Adb {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    $prevEAP = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $output = & adb -s $Device @Args 2>&1
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $prevEAP
    if ($exitCode -ne 0) {
        throw "adb fallo: adb -s $Device $($Args -join ' ')"
    }
    return $output
}

function Get-CenterFromBounds {
    param([string]$Bounds)
    if ($Bounds -match '\[(\d+),(\d+)\]\[(\d+),(\d+)\]') {
        $x1 = [int]$matches[1]
        $y1 = [int]$matches[2]
        $x2 = [int]$matches[3]
        $y2 = [int]$matches[4]
        return @{
            X = [int](($x1 + $x2) / 2)
            Y = [int](($y1 + $y2) / 2)
            Raw = $Bounds
        }
    }
    return $null
}

function Get-UiXml {
    param(
        [string]$RemotePath,
        [string]$LocalPath
    )
    Invoke-Adb shell uiautomator dump $RemotePath | Out-Null
    Invoke-Adb pull $RemotePath $LocalPath | Out-Null
    return Get-Content $LocalPath -Raw
}

function Get-BoundsFromXml {
    param(
        [string]$Xml,
        [string]$Pattern
    )
    $m = [regex]::Match($Xml, $Pattern)
    if ($m.Success -and $m.Groups.Count -ge 2) {
        return $m.Groups[1].Value
    }
    return $null
}

function Convert-ToAdbInputText {
    param([string]$Text)
    $safe = $Text.Trim()
    $safe = $safe -replace '\s+', '%s'
    $safe = $safe -replace '[^a-zA-Z0-9%._\-]', '_'
    return $safe
}

function Wait-ChatReady {
    param(
        [int]$TimeoutSec,
        [string]$LocalUiPath
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        $xml = Get-UiXml "/sdcard/ui_send_btn_ready.xml" $LocalUiPath

        $busy = $xml -match 'text="Generando respuesta\.\.\."'
        $enabledEditBounds = Get-BoundsFromXml $xml 'class="android.widget.EditText"[^>]*enabled="true"[^>]*bounds="(\[[^"]+\])"'
        if (-not $enabledEditBounds) {
            $enabledEditBounds = Get-BoundsFromXml $xml 'class="android.widget.EditText"[^>]*bounds="(\[[^"]+\])"[^>]*enabled="true"'
        }

        if (-not $enabledEditBounds) {
            $chatBounds = Get-BoundsFromXml $xml 'content-desc="Modo Chat"[^>]*bounds="(\[[^"]+\])"'
            if (-not $chatBounds) {
                $chatBounds = Get-BoundsFromXml $xml 'content-desc="Mensajes"[^>]*bounds="(\[[^"]+\])"'
            }
            if ($chatBounds) {
                $chatCenter = Get-CenterFromBounds $chatBounds
                Write-Host "ACTION=tap_chat_button bounds=$($chatCenter.Raw) center=$($chatCenter.X),$($chatCenter.Y)"
                Invoke-Adb shell input tap $($chatCenter.X) $($chatCenter.Y) | Out-Null
                Start-Sleep -Milliseconds 700
                continue
            }
        }

        if ($enabledEditBounds -and -not $busy) {
            return $enabledEditBounds
        }
        Start-Sleep -Seconds 1
    }
    return $null
}

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$tmpDir = Join-Path $projectRoot "tmp_ui"
$logDir = Join-Path $projectRoot "logs"
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$ui1 = Join-Path $tmpDir "ui_send_btn_step1.xml"
$ui2 = Join-Path $tmpDir "ui_send_btn_step2.xml"
$ui3 = Join-Path $tmpDir "ui_send_btn_step3.xml"
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $logDir ("send_button_" + $ts + ".log")

Write-Output "DEVICE=$Device"
Write-Output "PACKAGE=$Package"
Write-Output "MESSAGE_RAW=$Message"

$prevEAP = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& adb connect $Device 2>&1 | Out-Null
$ErrorActionPreference = $prevEAP
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo conectar por ADB a $Device"
}

Invoke-Adb logcat -c | Out-Null

if ($ForceRestart) {
    Invoke-Adb shell am force-stop $Package | Out-Null
    Start-Sleep -Seconds 1
}

Invoke-Adb shell am start -n "$Package/.MainActivity" | Out-Null
Start-Sleep -Seconds 2

$prevEAP2 = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$appPid = (& adb -s $Device shell pidof -s $Package 2>&1 | Out-String).Trim()
$ErrorActionPreference = $prevEAP2
if ([string]::IsNullOrWhiteSpace($appPid)) {
    Write-Host "WARN=no_pid_found_for_package"
} else {
    Write-Output "APP_PID=$appPid"
}

$editBounds = @(Wait-ChatReady -TimeoutSec $ReadyTimeoutSec -LocalUiPath $ui1) | Select-Object -Last 1

if (-not $editBounds) {
    throw "Chat no listo: no se encontro EditText habilitado antes del timeout"
}

$editCenter = Get-CenterFromBounds $editBounds
Write-Output "EDIT_BOUNDS=$($editCenter.Raw)"
Write-Output "EDIT_CENTER=$($editCenter.X),$($editCenter.Y)"

$safeMessage = Convert-ToAdbInputText $Message
Write-Output "MESSAGE_SENT=$safeMessage"
Invoke-Adb shell input tap $($editCenter.X) $($editCenter.Y) | Out-Null
Start-Sleep -Milliseconds 500

# Nunca usar Enter para enviar; solo escribimos texto y luego pulsamos el boton Enviar.
Invoke-Adb shell input text $safeMessage | Out-Null
Start-Sleep -Milliseconds 700

$xml2 = Get-UiXml "/sdcard/ui_send_btn_step2.xml" $ui2
$sendBounds = Get-BoundsFromXml $xml2 'content-desc="Enviar"[^>]*bounds="(\[[^"]+\])"'
if (-not $sendBounds) {
    throw "No se encontro boton Enviar en la UI"
}

$sendCenter = Get-CenterFromBounds $sendBounds
Write-Output "SEND_BOUNDS=$($sendCenter.Raw)"
Write-Output "SEND_CENTER=$($sendCenter.X),$($sendCenter.Y)"

for ($i = 1; $i -le [Math]::Max($SendTaps, 1); $i++) {
    Write-Output "ACTION=tap_send_button index=$i center=$($sendCenter.X),$($sendCenter.Y)"
    Invoke-Adb shell input tap $($sendCenter.X) $($sendCenter.Y) | Out-Null
    Start-Sleep -Milliseconds 250
}

Start-Sleep -Seconds $WaitAfterSendSec
$prevEAP3 = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$allLogs = @()
if (-not [string]::IsNullOrWhiteSpace($appPid)) {
    $allLogs = @(& adb -s $Device logcat --pid=$appPid -d -v time 2>&1)
}
if (-not $allLogs -or $allLogs.Count -eq 0) {
    $allLogs = @(& adb -s $Device logcat -d -v time 2>&1)
}
$ErrorActionPreference = $prevEAP3
$allLogs | Set-Content -Path $logFile -Encoding UTF8

$sentLogs = $allLogs | Select-String -Pattern "MainActivity.*Mensaje:" -SimpleMatch:$false
$routingLogs = $allLogs | Select-String -Pattern "MainActivity.*(Decision route=|KB_AUDIT|KB search:|Decision: KB_ABSTAIN|Decision: LLM mode|Fallback:|LLM guard)|SemanticSearchHelper.*(findTopKContexts|Grounding:)" -SimpleMatch:$false
$timingLogs = $allLogs | Select-String -Pattern "PerfLogger.*(llm\.generateAgriResponse\.total|llm\.generateComplete|llm\.generateAgriResponse\.buildPrompt)|findTopKContexts|runNetIds|llm\.runGreedyDecoding|MindSporeHelper" -SimpleMatch:$false

$xml3 = Get-UiXml "/sdcard/ui_send_btn_step3.xml" $ui3
$textStillInInput = [regex]::IsMatch(
    $xml3,
    'class="android.widget.EditText"[^>]*>.*?text="' + [regex]::Escape($safeMessage) + '"',
    [System.Text.RegularExpressions.RegexOptions]::Singleline
)
$messageVisibleInChat = $xml3 -match [regex]::Escape($safeMessage)

Write-Output "VERIFY_TEXT_STILL_IN_UI=$textStillInInput"
Write-Output "VERIFY_MESSAGE_VISIBLE_IN_CHAT=$messageVisibleInChat"
Write-Output "LOG_FILE=$logFile"
Write-Output "--- SENT LOGS ---"
if ($sentLogs) {
    $sentLogs | Select-Object -Last 8 | ForEach-Object { $_.Line }
} else {
    Write-Output "NO_SENT_LOGS_FOUND"
}
Write-Output "--- ROUTING/AUDIT LOGS ---"
if ($routingLogs) {
    $routingLogs | Select-Object -Last 30 | ForEach-Object { $_.Line }
} else {
    Write-Output "NO_ROUTING_LOGS_FOUND"
}
Write-Output "--- TIMING LOGS ---"
if ($timingLogs) {
    $timingLogs | Select-Object -Last 20 | ForEach-Object { $_.Line }
} else {
    Write-Output "NO_TIMING_LOGS_FOUND"
}
