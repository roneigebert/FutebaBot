#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, json
import sys

class TelegramBot:

	def __init__(self, api_key, last_message = None):
		self.api_key = api_key
		self.last_message = last_message

	def start(self):
		while True:
			messages = self.get_messages()
			if messages:
				self.last_message = messages[len(messages)-1]['update_id']
			for message in messages:
				self.send_response( messages )
			break

	def get_messages(self):
		messages_url = self.updates_urls()
		messages = self.get_json( messages_url )
		return messages['result']

	def send_response(self, message):
		print message

	def updates_urls(self):
		url = "https://api.telegram.org/bot%s/getUpdates" % self.api_key
		off_set = self.last_message + 1 if self.last_message else self.last_message
		query = self.url_query( offset=off_set )
		return url + query

	def url_query(self, **kwargs):
		query = ''
		for key, value in kwargs.iteritems():
			if key and value:
				if query:
					query += '&'
				query += key + '=' + value
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