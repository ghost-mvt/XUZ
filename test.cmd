# ==========================================
# إعادة ضبط النظام (Clean Slate)
# ==========================================
$taskName = "LabAutoScreenshot"
$scriptPath = "$env:APPDATA\screenshot_bot.ps1"

# 1. حذف المهمة المجدولة القديمة إن وجدت
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "تم حذف المهمة القديمة."
}

# 2. حذف نسخة السكربت القديمة في المسار الدائم لضمان استبدالها
if (Test-Path $scriptPath) {
    Remove-Item $scriptPath -Force
    Write-Host "تم حذف الملف القديم من المسار الدائم."
}

# (بعد هذا الجزء، سيقوم الكود الخاص بك بالاستمرار في منطق التثبيت الأصلي
# الذي قمنا بكتابته في الرد السابق، وسيعتبرها "مرة أولى")

