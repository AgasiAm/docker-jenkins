#!/usr/bin/env python
import pika, os, time, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Mail sending function
def send_mail(msgbody):
  msgsplit=msgbody.split(',')
  subject=format_subject(msgsplit)
  msg = MIMEMultipart()
  msg['From'] = 'testmail@lsoft.am'
  msg['To'] = 'agasi.gevorgyan@gmail.com'
  msg['Subject'] = 'From Jenkins status of %r' % subject
  message=msgbody
  msg.attach(MIMEText(message))
  msg.attach(MIMEText(message))

  mailServer = smtplib.SMTP('lsoft.am')
  mailServer.ehlo()
  mailServer.login('testmail@lsoft.am','6Wp=2PfFB$c-')
  mailServer.sendmail('testmail@lsoft.am','agasi.gevorgyan@gmail.com',msg.as_string())

  mailServer.close()

  return

# Find jon name from message to use in mail subject
def format_subject(msg):
  for i in range(len(msg)):
    if 'build_job_name' in msg[i]:
      msg1=msg[i]
      msg2=msg1.split(':')
      break
    i=i+1
  return(msg2[1])

# Access the CLODUAMQP_URL environment variable and parse it 
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@jenkins-rabbitmq:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.exchange_declare(exchange='jenkins',exchange_type='direct',durable=True)
channel.queue_declare(queue='jenkins',durable='True') # Declare a queue
channel.queue_bind(queue='jenkins',exchange='jenkins',routing_key='buildjenkins') 

# Create a function which is called on incoming messages
def callback(ch, method, properties, body):
  send_mail(body)

# Set up subscription on the queue
channel.basic_consume(callback,
  queue='jenkins',
  no_ack=True)

# Start consuming 
channel.start_consuming()
connection.close()
