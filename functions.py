from email import message
from email.mime.text import MIMEText
from smtplib import SMTP

#FUNCTION TO SEND AN EMAIL WITH THE INFORMATION OBTAINED AS PARAMETER
def mail(list):

    from_address = "from_adrdress@mdomain.gob.ar"
    to_address = 'to_address@mdomain.gob.ar'

    if list:
        message = f'Se recomienda cambiar la base de  {list}'
    else:
        message = 'No hay bases para cambiar'
    
    #I ASSIGN ALL THE DATA REFERRING TO THE MAIL
    mime_message = MIMEText(message , "plain")
    mime_message["From"] = from_address
    mime_message["To"] = to_address
    mime_message["Subject"] = 'ALERTA TAMAÑO DE BASE'

    #METHODS REFERRED TO THE MAIL SERVER
    smtp = SMTP("outlook.office365.com", 25)
    smtp.connect("outlook.office365.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(from_address, "Password")
    
    
    #METHOD TO SEND THE MAIL RECEIVING THE NECESSARY PARAMETERS
    smtp.sendmail(from_address, to_address, mime_message.as_string())
    smtp.quit()