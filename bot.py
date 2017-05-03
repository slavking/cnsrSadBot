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
import config
from urllib2 import urlopen
import hbot
import requests

import urllib
from bs4 import BeautifulSoup, Comment

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


base_url = 'http://www.worldtimeserver.com/current_time_in_'

class Opener(urllib.FancyURLopener):
	version = 'App/1.7'

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
		
		print(country)	
		
		def get_time():
			c = ''
			result = ''
			result_time = ''
			local_country = country
			print('a - ' + country)
			for char in country:
				if char.isalpha():
					c += char
			c = c[:2]
			url = base_url + c + '.aspx'	
			r = Opener().open(url)
			soup = BeautifulSoup(r,'lxml')
			#get time
			time_comments = soup.findAll(text=lambda text:isinstance(text,Comment))
			for x in time_comments:
				y = ''
				for char in x:
					if char != ' ':
						y += char
				if re.match('ServerTimewithseconds:',y):
					result = y
			for char in result:
				if not char.isalpha():
					result_time += char
			result_time = result_time[1:]
			#get city + country
			city_found = soup.find('h1',{'class':'placeNameH1'})
			city = city_found.text
			#cleaning up city output
			city = re.sub('\s+','',city)
			city = ' '.join(re.findall('[A-Z][^A-Z]*',city))
			#print result
			return ('Time in {0} is {1}'.format(city, result_time))
		
		
		help_msg = 'no help message defined'
		
		#for ekb and those who don't have names
		#todo - add separate file dictionary for idents + names of nameless		
		if ident == ('$2a$10$mAM0oYrjp0bCHFDsGaiB.etG2OGec9NtgRDtoctQiWUZ4zww1nZ9C'):
			name = "ekb-cuck"
		if name == '':
			name = "nameless faggot"
		
		#gets time
		if re.match(message,'.htime'):
			out_msg = out_msg = '>>' + count + '\n' + get_time()
			post_chat(out_msg, channel, name = config.name,trip = config.Trip,convo = 'General', file = '')
		
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
