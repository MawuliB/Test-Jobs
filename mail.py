import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

mail = os.getenv('MAIL')
password = os.getenv('PASSWORD')

print(f'Mail: {mail}, Password: {password}')

if mail and password:
    smtObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtObj.starttls()
    print(f'Mail: {mail}, Password: {password}')
    smtObj.login(mail, password)

    smtObj.sendmail(mail, 'mbadassou1@gmail.com', 'Subject: So long.\nDear Mawuli, so long and thanks for all the fish.')

    smtObj.quit()
else:
    print('Mail or Password not found in .env file')