Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

Desktop = shell.SpecialFolders("Desktop")
FolderPath = Desktop & "\1"

If fso.FolderExists(FolderPath) Then
    fso.DeleteFolder FolderPath, True
    MsgBox "تم حذف المجلد 1"
Else
    MsgBox "المجلد 1 غير موجود"
End If
