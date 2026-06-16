Option Explicit

Dim fso, folder, file, key, flagFile
Dim folderPath, adodbStream, bytes, i
Dim byteArr()
Dim shell, userInput

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' Dynamically get the Desktop path for any user
' Masaüstü yolunu herhangi bir kullanıcı için dinamik olarak alır
folderPath = shell.ExpandEnvironmentStrings("%USERPROFILE%") & "\Desktop\1"
flagFile = folderPath & "\.locked"
key = 123 

' Check if folder exists
' Klasörün var olup olmadığını kontrol et
If Not fso.FolderExists(folderPath) Then
    MsgBox "Folder '1' not found on Desktop." & vbCrLf & "Masaüstünde '1' klasörü bulunamadı.", vbCritical, "Error / Hata"
    WScript.Quit
End If

' Check if locked
' Kilitli mi kontrol et
If Not fso.FileExists(flagFile) Then
    ProcessFiles()
    fso.CreateTextFile(flagFile, True).Close
Else
    ' Password prompt
    ' Parola istemi
    userInput = InputBox("Enter password to unlock:" & vbCrLf & "Kilidi açmak için parola girin:", "Authentication / Kimlik Doğrulama")

    If userInput = "123" Then
        ProcessFiles()
        If fso.FileExists(flagFile) Then fso.DeleteFile(flagFile)
    Else
        MsgBox "Incorrect password!" & vbCrLf & "Yanlış parola!", vbCritical, "Access Denied / Erişim Reddedildi"
    End If
End If

Sub ProcessFiles()
    Set folder = fso.GetFolder(folderPath)
    For Each file In folder.Files
        If file.Name <> ".locked" Then
            Set adodbStream = CreateObject("ADODB.Stream")
            adodbStream.Type = 1 ' TypeBinary
            adodbStream.Open
            adodbStream.LoadFromFile file.Path
            
            bytes = adodbStream.Read
            adodbStream.Close
            
            ReDim byteArr(LenB(bytes) - 1)
            
            ' XOR operation
            ' XOR işlemi
            For i = 0 To LenB(bytes) - 1
                byteArr(i) = AscB(MidB(bytes, i + 1, 1)) Xor key
            Next
            
            adodbStream.Open
            adodbStream.Write byteArr
            adodbStream.SaveToFile file.Path, 2 ' adSaveCreateOverWrite
            adodbStream.Close
            Set adodbStream = Nothing
        End If
    Next
End Sub
