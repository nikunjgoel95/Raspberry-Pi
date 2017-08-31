from flask import Flask, flash, render_template, redirect, request, url_for
import  MySQLdb
from random import uniform
#from flask_appconfig import AppConfig
#from flask_bootstrap import Bootstrap

app = Flask(__name__)

import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from gpiozero import LightSensor, Buzzer

GPIO.setwarnings(False)

#app.config['MYSQL_HOST'] = '127.0.0.1'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'greenhouse'
#mysql= MySQldb.connect(app)
db=MySQLdb.connect('localhost','root','1234','greenhouse')

GPIO.setmode(GPIO.BCM)
#GPIO.setup(8,GPIO.IN)
GPIO.setup(15,GPIO.IN)
#GPIO.setup(12,GPIO.IN)

sensor = Adafruit_DHT.DHT11
ldr= LightSensor(14)
pin=23
count=0

def check():
	count=1
	#cur=mysql.connection.cursor()
	cur=db.cursor()
	cur.execute("SELECT * from data")
	results = cur.fetchall()
	ver = results[0]
	if(ver is None):
		print False
	else:
		print True

while True:
	if count is None:
		check()
	#time.sleep(1)
	ldr_val=ldr.value*10
	print(ldr_val)
	#print('\n')
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
    		print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
		time.sleep(0.5)
	else:
    		print('Failed to get reading. Try again!')

	if GPIO.input(15):
		rand=uniform(0,8)
		print (rand)
		time.sleep(0.5)
	else:
		print ('Moisture Absent')
	cur=db.cursor()
	cur.execute("SELECT MAX(sno) from data")
	max_sno=cur.fetchone()
	temp= ''
	temp= str(max_sno[0]+1)+ ","
	temp+="'"+str(temperature)+"','"+str(humidity)+"','"+str(ldr_val)+"','"+str(rand)+"'"
	tem="INSERT INTO `greenhouse`.`data` (`sno`, `temperature`, `humidity`, `light`, `moisture`) VALUES ("+temp+")"
	#print tem
	cur.execute(tem)
	db.commit()
	time.sleep(3.0)
