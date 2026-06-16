Option Explicit

Dim fso, shell, folderPath, folder, file, key, flagFile
Dim userInput, i, binaryData, byteArr()
Dim inputStream, outputStream

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' Setup paths / Yolların ayarlanması
folderPath = shell.SpecialFolders("Desktop") & "\1"
flagFile = folderPath & "\.locked"
key = 123 

' Check if folder exists / Klasörün var olup olmadığını kontrol et
If Not fso.FolderExists(folderPath) Then
    MsgBox "Folder '1' not found!" & vbCrLf & "'1' klasörü bulunamadı!", vbCritical, "Error / Hata"
    WScript.Quit
End If

' If .locked does not exist, encrypt / .locked yoksa şifrele
If Not fso.FileExists(flagFile) Then
    ProcessFiles()
    fso.CreateTextFile(flagFile, True).Close
    MsgBox "Files encrypted." & vbCrLf & "Dosyalar şifrelendi.", vbInformation, "Success / Başarılı"
Else
    ' If .locked exists, ask for password to decrypt / .locked varsa şifreyi çöz
    userInput = InputBox("Enter password to decrypt:" & vbCrLf & "Şifreyi çözmek için parola girin:", "Authentication / Kimlik Doğrulama")

    If userInput = "123" Then
        ProcessFiles()
        If fso.FileExists(flagFile) Then fso.DeleteFile(flagFile)
        MsgBox "Files decrypted." & vbCrLf & "Dosyaların şifresi çözüldü.", vbInformation, "Success / Başarılı"
    Else
        MsgBox "Incorrect password!" & vbCrLf & "Yanlış parola!", vbCritical, "Access Denied / Erişim Reddedildi"
    End If
End If

Sub ProcessFiles()
    Set folder = fso.GetFolder(folderPath)
    For Each file In folder.Files
        If file.Name <> ".locked" Then
            ' Read Binary / İkili oku
            Set inputStream = CreateObject("ADODB.Stream")
            inputStream.Type = 1
            inputStream.Open
            inputStream.LoadFromFile file.Path
            binaryData = inputStream.Read
            inputStream.Close
            
            ' Perform XOR / XOR işlemini gerçekleştir
            ReDim byteArr(LenB(binaryData) - 1)
            For i = 0 To LenB(binaryData) - 1
                byteArr(i) = AscB(MidB(binaryData, i + 1, 1)) Xor key
            Next
            
            ' Write Binary / İkili yaz
            Set outputStream = CreateObject("ADODB.Stream")
            outputStream.Type = 1
            outputStream.Open
            outputStream.Write byteArr
            outputStream.SaveToFile file.Path, 2
            outputStream.Close
        End If
    Next
End Sub
