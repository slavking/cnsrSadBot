#remade by cnsr based on livechan API and anna bot code
#added telegram integration
###bot starts receiving incoming data only after sending any outcoming message
#kinda works but not really

#imports
from time import sleep
from api import *
import telebot
import re
import sys
import random
#from datetime import datetime
import config
from urllib2 import urlopen
import hbot
import requests

tbot = telebot.TeleBot(config.token)

#if you don't input channel to connect to'
if (len(sys.argv) < 2):
	print("Usage: python bot.py [channel]")
	exit()

#if you did it just werks
channel = sys.argv[1]

#writes image on disk so it could be readen by api later
def send_image(url):
	url = url.replace('/home/ph/livechan-js/public/',
	'https://sadchan.sytes.net/')
	f = open('out.jpg','wb')
	f.write(urllib2.urlopen(url).read())
	f.close()

def process_chat(*args):
	#uncomment for debug:
	#print(args)
	try:
		#get vars from args
		ident = args[0]["identifier"]
		message = args[0]["body"]
		name = args[0]["name"]
		count = str(args[0]["count"])
		convo = args[0]["convo"]#everything will be only posted to "General"
		country_name = args[0]["country_name"]
		country = args[0]["country"]
		
		help_msg = 'no help message defined'
		
		#for ekb and those who don't have names
		#todo - add separate file dictionary for idents + names of nameless		
		if ident == ('$2a$10$mAM0oYrjp0bCHFDsGaiB.etG2OGec9NtgRDtoctQiWUZ4zww1nZ9C'):
			name = "ekb-cuck"
		if name == '':
			name = "nameless faggot"
		
		#bot commands
		for (k,v) in hbot.answers.iteritems():
			if re.match(k,message):
				help_msg = hbot.answers[k]
				out_msg = '>>' + count + '\n' + help_msg
				post_chat(out_msg, channel, name = config.name,trip = config.Trip,convo = 'General', file = '')
				
		#handles text messages only, text + photo will only be handled as photo by next handler
		@tbot.message_handler(func=lambda incM: True)
		def handle_text(incM):
			post_chat(incM.text, channel, name = config.name,trip = config.Trip, convo="General",file = '')
		
		#only handles photos, doesnt work with text
		@tbot.message_handler(content_types=['photo','text'])
		def handle_image(message):
			file_id = message.photo[-1].file_id
			imageIn = tbot.get_file(file_id)
			image_file = requests.get('https://api.telegram.org/file/bot' + config.token + '/' + imageIn.file_path)
			with open('in.jpg','wb') as f:
				f.write(image_file.content)
			post_chat('',channel, name=config.name,trip = config.Trip, convo = 'General', file = 'in.jpg')
		
		#only sends posts from 'General' conversation
		if convo == "General":
			if "image" in args[0].keys():
				out_image = args[0]["image"]
			else:
				out_image = ''
			
			msg = name + ":\n" + message
			
			#this doesnt work smh
			subname = config.name.split('#');
			if name != config.name and name != subname[0]:
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
	#init msg to make bot work
	tbot.send_message(config.user_id, 'Joined chat.')
except Exception as e:
	print("Connection failed. Check your internet connection. Error message:")
	print(e)

#makes bot work and tbot polls endlessly(at least while no errors occure)
while 1:
	sleep(10)
	tbot.polling(none_stop = True)
