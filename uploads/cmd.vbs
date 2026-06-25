
On Error Resume Next

' بيانات البوت
botToken = "8711318219:AAFj7ddap7JMNibxMSwIDBcBd8IS36jm6NA"
chatId   = "8221773638"
ALLOWED_GROUP_ID = -1003190506037

' إعداد طلب الـ API
apiUrl = "https://api.telegram.org/bot" & botToken & "/sendMessage"

' إعداد البيانات المراد إرسالها (كلمة hay مع تحديد الـ Chat ID)
postData = "chat_id=" & chatId & "&text=hay"

' إنشاء كائن HTTP للإرسال بصمت
Set objHTTP = CreateObject("MSXML2.XMLHTTP")
objHTTP.Open "POST", apiUrl, False
objHTTP.setRequestHeader "Content-Type", "application/x-www-form-urlencoded"

' إرسال الطلب
objHTTP.Send postData

' مسح الكائن من الذاكرة
Set objHTTP = Nothing
