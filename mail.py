import smtplib
import os
from dotenv import load_dotenv
import imapclient, pyzmail, time, imaplib, requests
from twilio.rest import Client

imaplib._MAXLINE = 10000000

load_dotenv()

mail : str = os.getenv('MAIL_USERNAME')
password : str = os.getenv('MAIL_PASSWORD')
account_sid : str = os.getenv('TWILIO_ACCOUNT_SID')
auth_token : str = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number : str = os.getenv('TWILIO_PHONE_NUMBER')
my_number : str = os.getenv('MY_PHONE_NUMBER')
apiSecret : str = os.getenv('SMS_CHEF_API_SECRET')

def send_mail():
    if mail and password:
        try:
            smt_obj = smtplib.SMTP('smtp.gmail.com', 587)
            smt_obj.starttls()
            smt_obj.login(mail, password)

            smt_obj.sendmail(mail, 'mbadassou1@gmail.com', 'Subject: So long.\nDear Mawuli, so long and thanks for all the fish.')

            smt_obj.quit()
        except Exception as e:
            print(e)
    else:
        print('Mail or Password not found in .env file')

def fetch_today_mail():
    imap_obj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
    imap_obj.login(mail, password)

    imap_obj.select_folder('INBOX', readonly=True)

    today = time.strftime('%d-%b-%Y')

    # day = '14-Oct-2024'

    UID_LIST = imap_obj.search(['SINCE', today, 'UNSEEN'])

    for uid in UID_LIST:
        raw_message = imap_obj.fetch([uid], ['BODY[]', 'FLAGS'])
        message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

        print(f'From: {message.get_addresses("from")}')
        print(f'To: {message.get_addresses("to")}')
        print(f'Subject: {message.get_subject()}')
        print(f'Content: {message.text_part.get_payload().decode("utf-8")}')

        # if should_delete_mail(message.get_addresses("from")[0][1], mail):
        #     imap_obj.delete_messages([uid])
        #     print('Mail deleted')

        send_sms(build_sms_message(message.get_subject(), message.text_part.get_payload().decode("utf-8")))

    imap_obj.logout()

def should_delete_mail(mail_from: str, check_mail: str):
    if mail_from == check_mail:
        return True
    return False

def build_sms_message(subject: str, content: str):
    return f'Subject: {subject}\nContent: {content}'

def send_sms(message: str):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=my_number
    )

    print(message.sid)

# def send_sms_with_smschef(message: str):

#     param = {
#     "secret": apiSecret,
#     "mode": "devices",
#     "sim": 1,
#     "priority": 1,
#     "phone": my_number,
#     "message": message
#     }

#     r = requests.post(url = "https://www.cloud.smschef.com/api/send/sms", params = param)

#     print(r.text)

def main():
    fetch_today_mail()

if __name__ == '__main__':
    main()