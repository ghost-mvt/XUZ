Option Explicit

Dim userInput

userInput = InputBox("اكتب النص هنا:", "إدخال")

If userInput <> "" Then
    MsgBox "أدخلت: " & userInput, vbInformation, "النتيجة"
Else
    MsgBox "لم يتم إدخال شيء", vbExclamation, "تنبيه"
End If
