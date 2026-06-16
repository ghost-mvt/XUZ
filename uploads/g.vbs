Option Explicit

Dim fso, shell, folderPath, folder, file, key, flagFile
Dim userInput, data, encrypted, i

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' Setup path / Yolların ayarlanması
folderPath = shell.SpecialFolders("Desktop") & "\1"
flagFile = folderPath & "\.locked"
key = 123 

' Check if folder exists / Klasörün var olup olmadığını kontrol et
If Not fso.FolderExists(folderPath) Then
    MsgBox "Folder '1' not found!" & vbCrLf & "'1' klasörü bulunamadı!", vbCritical, "Error / Hata"
    WScript.Quit
End If

' Lock/Unlock logic / Kilitleme/Kilidi açma mantığı
If Not fso.FileExists(flagFile) Then
    ' Encrypt / Şifrele
    ProcessFiles()
    fso.CreateTextFile(flagFile, True).Close
    MsgBox "Files encrypted." & vbCrLf & "Dosyalar şifrelendi.", vbInformation, "Success / Başarılı"
Else
    ' Decrypt / Şifreyi çöz
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
            ' Read / Oku
            Dim inputFile
            Set inputFile = fso.OpenTextFile(file.Path, 1)
            data = inputFile.ReadAll
            inputFile.Close
            
            ' Process (XOR) / İşle (XOR)
            encrypted = ""
            For i = 1 To Len(data)
                encrypted = encrypted & Chr(Asc(Mid(data, i, 1)) Xor key)
            Next
            
            ' Write / Yaz
            Dim outputFile
            Set outputFile = fso.OpenTextFile(file.Path, 2)
            outputFile.Write encrypted
            outputFile.Close
        End If
    Next
End Sub
