import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

mail = os.getenv('MAIL')
password = os.getenv('PASSWORD')

print(mail)

smtObj = smtplib.SMTP('smtp.gmail.com', 587)
smtObj.starttls()
smtObj.login(mail, password)

smtObj.sendmail(mail, 'mbadassou1@gmail.com', 'Subject: So long.\nDear Mawuli, so long and thanks for all the fish.')

smtObj.quit()