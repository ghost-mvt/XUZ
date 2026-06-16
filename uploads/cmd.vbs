Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

Desktop = shell.SpecialFolders("Desktop")
FolderPath = Desktop & "\1"

If Not fso.FolderExists(FolderPath) Then
    MsgBox "لم يتم العثور على مجلد 1"
    WScript.Quit
End If

Key = 23

Set folder = fso.GetFolder(FolderPath)

For Each file In folder.Files

    Set input = fso.OpenTextFile(file.Path, 1)
    data = input.ReadAll
    input.Close

    encrypted = ""

    For i = 1 To Len(data)
        encrypted = encrypted & Chr(Asc(Mid(data,i,1)) Xor Key)
    Next

    Set output = fso.OpenTextFile(file.Path, 2)
    output.Write encrypted
    output.Close

Next

MsgBox "تم تحويل محتويات مجلد 1"
