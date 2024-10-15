import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

mail : str = os.getenv('MAIL')
password : str = os.getenv('PASSWORD')

print(f'Mail: {mail}, Password: {password}')

if mail and password:
    try:
        smtObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtObj.starttls()
        smtObj.login(mail, password)

        smtObj.sendmail(mail, 'mbadassou1@gmail.com', 'Subject: So long.\nDear Mawuli, so long and thanks for all the fish.')

        smtObj.quit()
    except Exception as e:
        print(e)
else:
    print('Mail or Password not found in .env file')