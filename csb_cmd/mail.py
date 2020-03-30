import smtplib,ssl

from csb_cmd.db import db

# XXX: does no escaping
def send(to, subject, message):
  fromaddr = 'cybersocbot@gmail.com'
  msg = 'Subject: {}\n{}'.format(subject, message)
  username = 'cybersocbot@gmail.com'
  password = db.get_token("email")
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, to, msg)
  server.quit()
