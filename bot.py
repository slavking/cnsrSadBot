#remade by cnsr based on livechan API and anna bot code
#added telegram integration
#bot starts receiving incoming data only after sending any outcoming message
#kinda works but not really

from time import sleep
from api import *
import telebot
import re
import sys, os
import random
from datetime import datetime
import config
from urllib2 import urlopen

#im not even sure if i need those imports
try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve

import requests

tbot = telebot.TeleBot(config.token)

#if you don't input channel to connect to'
if (len(sys.argv) < 2):
	print("Usage: python bot.py [channel]")
	exit()

#if you did it just werks
channel = sys.argv[1]

#this should be removed?
# globals
users = {}

#writes image on disk so it could be read by api later
def send_image(url):
	url = url.replace('/home/ph/livechan-js/public/',
	'https://sadchan.sytes.net/')
	f = open('out.jpg','wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

def process_chat(*args):
	#print(args)
	try:
		#get vars from args
		ident = args[0]["identifier"]
		message = args[0]["body"]
		name = args[0]["name"]
		count = str(args[0]["count"])
		convo = args[0]["convo"]#"General"
		country_name = args[0]["country_name"]
		country = args[0]["country"]
		
		#for ekb and those who don't have names
		if ident == ('$2a$10$mAM0oYrjp0bCHFDsGaiB.etG2OGec9NtgRDtoctQiWUZ4zww1nZ9C'):
			name = "ekb-cuck"
		if name == '':
			name = "nameless faggot"
			
		#handles text messages only, text + photo will only be handled as photo by next handler
		@tbot.message_handler(func=lambda incM: True)
		def handle_text(incM):
			print(incM.text)
			post_chat(incM.text, channel, name = config.name, trip = config.Trip, convo="General",file = '')
			print(config.name + '\n' + incM.text)
		#only handles photos, doesnt work with text
		#todo - add text + photo handling
		@tbot.message_handler(content_types=['photo'])
		def handle_image(message):
			file_id = message.photo[-1].file_id
			imageIn = tbot.get_file(file_id)
			image_file = requests.get('https://api.telegram.org/file/bot' + config.token + '/' + imageIn.file_path)
			#print(image_file)
			with open('in.jpg','wb') as f:
				f.write(image_file.content)
				f.close()
			post_chat('',channel, name=config.name,trip = config.Trip, convo = 'General', file = 'in.jpg')
		
		#only sends posts from General conversation
		if convo == "General":
			if "image" in args[0].keys():
				out_image = args[0]["image"]
			else:
				out_image = ''
			out_message = ""
			
			msg = name + ":\n" + message
			if name != config.name:
				if out_image != '':
					send_image(out_image)
					img = open('out.jpg', 'rb')
					tbot.send_photo(config.user_id, img)
					img.close()
				tbot.send_message(config.user_id, msg)
				print(msg)
				
	except Exception as e:
		print(e)
		
#i guess this is better to have than not to?		
try:	
	login(callback=process_chat)
	join_chat(channel)
	print('Joined chat')
except Exception as e:
	print("Connection failed. Check your internet connection. Error message:")
	print(e)

#makes bot wort and tbot poll endlessly(at least while no errors occure)
while 1:
	sleep(10)
	tbot.polling(none_stop = True)
