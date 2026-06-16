
' =============================================
' كود VBS - نافذة ترتطم بحواف الشاشة (تقريبي)
' =============================================

Dim WshShell, objFSO
Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

Dim x, y, dx, dy
Dim screenWidth, screenHeight
Dim title, msg

' أبعاد الشاشة التقريبية
screenWidth = 1920
screenHeight = 1080

' بداية عشوائية
Randomize
x = Int(Rnd * screenWidth)
y = Int(Rnd * screenHeight)
dx = 15   ' سرعة أفقية
dy = 12   ' سرعة رأسية

title = "النافذة الراقصة - اضغط Cancel للإغلاق"

Do
    msg = "النافذة ترتطم بالحواف!" & vbCrLf & vbCrLf & _
          "X: " & x & " | Y: " & y & vbCrLf & _
          "اضغط Cancel للإيقاف"
    
    ' عرض النافذة
    answer = MsgBox(msg, vbOKCancel + vbInformation, title)
    
    If answer = 2 Then Exit Do   ' Cancel = إغلاق
    
    ' تحريك الموقع
    x = x + dx
    y = y + dy
    
    ' ارتطام بالحواف (انعكاس)
    If x <= 0 Or x >= screenWidth Then dx = -dx
    If y <= 0 Or y >= screenHeight Then dy = -dy
    
    ' محاولة تحريك النافذة (تعمل جزئياً)
    WshShell.SendKeys "% {SPACE}m"   ' Alt + Space + m (Move)
    WScript.Sleep 50
    ' محاولة وضعها في الموقع الجديد (غير دقيق 100%)
    WshShell.SendKeys "{TAB}{TAB}{TAB}" & x & "{TAB}" & y & "{ENTER}"
    
    WScript.Sleep 80   ' سرعة الحركة
Loop

WScript.Echo "تم إيقاف النافذة الراقصة!"
