
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' الحصول على مسار سطح المكتب لجميع نسخ ويندوز
DesktopPath = objShell.SpecialFolders("Desktop")

' اسم الملف الذي سيتم إنشاؤه
FilePath = DesktopPath & "\MyFile.txt"

' إنشاء الملف وكتابة محتوى داخله
Set File = objFSO.CreateTextFile(FilePath, True)
File.WriteLine "تم إنشاء هذا الملف بواسطة VBScript"
File.Close

MsgBox "تم إنشاء الملف على سطح المكتب بنجاح"
