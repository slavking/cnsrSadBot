from time import sleep
from api import *
import telebot
import re
import sys, os
import random
from datetime import datetime
import config
from urllib2 import urlopen

try:
	from urllib.request import urlretrieve
except ImportError:
	from urllib import urlretrieve

import requests

tbot = telebot.TeleBot(config.token)

if (len(sys.argv) < 2):
	print("Usage: python bot.py [channel]")
	exit()
	
channel = sys.argv[1]

# globals
users = {}

def send_image(url):
	url = url.replace('/home/ph/livechan-js/public/',
	'https://sadchan.sytes.net/')
	f = open('out.jpg','wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

def process_chat(*args):
	#print(args)
	try:
		ident = args[0]["identifier"]
		message = args[0]["body"]
		name = args[0]["name"]
		count = str(args[0]["count"])
		convo = args[0]["convo"]#"General"
		country_name = args[0]["country_name"]
		country = args[0]["country"]
		
		@tbot.message_handler(func=lambda incM: True)
		def handle_text(incM):
			print(incM.text)
			post_chat(incM.text, channel, name = config.name, trip = config.Trip, convo="General",file = '')
			print(config.name + '\n' + incM.text)
		@tbot.message_handler(content_types=['photo'])
		def handle_image(message):
			file_id = message.photo[-1].file_id
			imageIn = tbot.get_file(file_id)
			image_file = requests.get('https://api.telegram.org/file/bot' + config.token + '/' + imageIn.file_path)
			print(image_file)
			with open('in.jpg','wb') as f:
			#	f.write(urllib2.urlopen(image_file).read())
				f.write(image_file.content)
				f.close()
			post_chat('',channel, name=config.name,trip = config.Trip, convo = 'General', file = 'in.jpg')
		
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
try:	
	login(callback=process_chat)
	join_chat(channel)
	print('Joined chat')
except Exception as e:
	print("Connection failed. Check your internet connection. Error message:")
	print(e)

while 1:
	sleep(10)
	tbot.polling(none_stop = True)
