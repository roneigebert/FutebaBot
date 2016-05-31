#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, json
import sys
import time


class TelegramBot:

	def __init__(self, api_key):
		self.api_key = api_key

	def start(self):
		while True:
			messages = self.get_messages()
			if messages:
				self.last_message = messages[len(messages)-1]['update_id']
			for message in messages:
				self.send_response( message )
			time.sleep(3)

	def get_messages(self):
		messages_url = self.updates_urls()
		messages = self.get_json( messages_url )
		return messages['result']

	def send_response(self, message):
		response_text = self.response_for( message['message']['text'] )
		chat_id = message['message']['chat']['id']
		url = "https://api.telegram.org/bot%s/sendMessage" % self.api_key
		query = self.url_query( chat_id=chat_id, text=response_text )
		self.access_url( url+query )

	def response_for(self, text):
		if text == '/start' or text == '/help':
			return 'Seja bem vindo meu caro querido S2. Digite o nome do campeonato para obter informações'
		return 'Estamos trabalhando para poder lhe ajudar.\nEnquanto isso você poder capinar um lote'

	def updates_urls(self):
		return "https://api.telegram.org/bot%s/getUpdates" % self.api_key

	def url_query(self, **kwargs):
		query = ''
		for key, value in kwargs.iteritems():
			if key and value:
				if query:
					query += '&'
				query += key + '=' + urllib2.quote(str(value))
		return '?' + query if query else ''

	def get_json(self, url):
		response = self.access_url( url )
		return json.loads(response.read())

	def access_url(self, url):
		return urllib2.urlopen( url )

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Required args: <api_key>'
		exit(1)
	bot = TelegramBot( sys.argv[1] )
	bot.start();