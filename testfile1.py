import cv2
import ssl
import smtplib
from threading import Thread   
from playsound import playsound
from email.message import EmailMessage

def play_alarm():
    playsound('Fire_alarm.mp3')
    print("Fire alarm end")
    
def send_mail():
    
    email_sender = 'senders mail'
    email_password = 'senders password'
    email_receiver = 'recievers mail'
    
    subject = 'EMERGENCY'
    body = "fire has been detected at your workplace."
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 587, context=context) as smtp:
        
        smtp.login(email_sender, email_password)
        smtp.send_message(em)

    print('mail sent')

fire = cv2.CascadeClassifier('cascade.xml')
cap = cv2.VideoCapture(0)

runOncePlayAlarm = False
runOnceSendMail = False

while True:
    
    ret, frame = cap.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    firecap = fire.detectMultiScale(frame, 2, 8)
    
    for (x, y, w, h) in firecap:
        
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 3)

        if not runOnceSendMail:

            print('mail initiated')
            s = Thread(target=send_mail)
            s.start()
            runOnceSendMail = True

        if not runOncePlayAlarm:

            print("Fire alarm initiated")
            s=Thread(target=play_alarm)
            s.start()
            runOncePlayAlarm = True

    cv2.imshow('Fire Detection', frame)

    key = cv2.waitKey(1)
    if key == ord('q') or cv2.getWindowProperty('Fire Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
