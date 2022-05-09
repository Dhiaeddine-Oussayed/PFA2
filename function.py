import time
import datetime
from pygame import mixer  # pip install pygame


def getCurrentday():
    tody = datetime.datetime.now()
    currentDay = datetime.date(tody.year, tody.month, tody.day).strftime('%A')
    return currentDay


def playAlarm():
    mixer.init()
    mixer.music.load(r'Alarm.mp3')
    mixer.music.play()


def timer(temp):  # temp en second !!!!
    print("Timer has Start!")
    if temp > 5:
        time.sleep(temp - 5)
        for i in range(5):
            time.sleep(1)
            print("Timer finished in ", 5 - i)
        print("Timer is finished !!!")
        playAlarm()


def alarm(hour, minute,
          days):  # days list of days Max 7 -->["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    time_now = datetime.datetime.now()
    while True:
        time.sleep(1)
        # print(datetime.datetime.now().strftime("%H:%M:%S"))
        if str(getCurrentday()) in days:
            if (int(hour) == int(time_now.hour) and int(minute) == int(time_now.minute)):
                print("wake up!")
                playAlarm()
                time.sleep(30)


def sendMail(msg, recever):  
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail_content = msg
    #The mail addresses and password
    sender_address = 'marwenijawher7@gmail.com'
    sender_pass = 'mot de passe'
    receiver_address = recever
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


# -----------------------------------------------------------------------------------------------------------------------------------
# EXEMPLES:
sendMail("Hello,\nThis is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.\nThank You","harbawijawher@gmail.com")
# alarm(9,8,["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
# timer(10)

# -----------------------------------------------------------------------------------------------------------------------------------
