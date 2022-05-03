import time
import datetime
from pygame import mixer #pip install pygame


def getCurrentday():
    tody = datetime.datetime.now()
    currentDay = datetime.date(tody.year,tody.month,tody.day).strftime('%A')
    return currentDay
    
def playAlarm(): 
    mixer.init()
    mixer.music.load(r'Alarm.mp3')
    mixer.music.play()

def timer(temp): #temp en second !!!!
      print("Timer has Start!")
      if temp > 5:
          time.sleep(temp-5)
          for i in range(5):
              time.sleep(1)
              print("Timer finished in ",5-i)
          print("Timer is finished !!!")
          playAlarm()
      else:
          for i in range(temp):
              temp.sleep(1)
              print("Timer finished in ",5-i,"Second")
          temp.sleep(1)  
          print("Timer is finished !!!")
          playAlarm()    
      
def alarm(hour,minute,days):#days list of days Max 7 -->["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    time_now=datetime.datetime.now()
    while True:
        time.sleep(1)
        #print(datetime.datetime.now().strftime("%H:%M:%S"))
        if str(getCurrentday()) in days:
            if (int(hour) == int(time_now.hour) and int(minute) == int(time_now.minute)) :
                print("wake up!")
                playAlarm()
                time.sleep(30)
def sendMail(msg,recever):#pip install sib_api_v3_sdk
    import time
    import sib_api_v3_sdk
    from sib_api_v3_sdk.rest import ApiException
    from pprint import pprint

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "My Subject"
    html_content = "<html><body><h1>"+msg+"</h1></body></html>"
    sender = {"name":"John Doe","email":"harbawijawher@gmail.com"}
    to = [{"email":recever,"name":"Jane Doe"}]
    headers = {"Some-Custom-Name":"unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
#-----------------------------------------------------------------------------------------------------------------------------------
#EXEMPLES:
#sendMail("This is my first transactional email","harbawijawher@gmail.com")        
#alarm(9,8,["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
#timer(10)

#-----------------------------------------------------------------------------------------------------------------------------------
