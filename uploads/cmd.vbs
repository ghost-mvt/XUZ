Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' جلب سطح مكتب المستخدم الحالي تلقائياً
Desktop = shell.SpecialFolders("Desktop")

' اسم المجلد
FolderPath = Desktop & "\1"

If Not fso.FolderExists(FolderPath) Then
    MsgBox "المجلد 1 غير موجود على سطح المكتب"
    WScript.Quit
End If

MsgBox "تم العثور على المجلد: " & FolderPath
