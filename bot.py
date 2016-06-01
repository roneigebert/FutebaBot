#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, json
import sys
import time


class TelegramBot:

	def __init__(self, api_key, last_update_id):
		self.api_key = api_key
		self.last_update_id = last_update_id
		self.campeonatos = None
		self.proxies = {}

	def start(self):
		while True:
			messages = self.get_messages()
			if messages:
				self.last_update_id = messages[len(messages)-1]['update_id']
			for message in messages:
				self.send_response( message['message'] )
			time.sleep(5)

	def get_messages(self):
		url = "https://api.telegram.org/bot%s/getUpdates" % self.api_key
		messages = self.get_json( url, offset=self.last_update_id+1 )
		return messages['result']

	def send_response(self, message):
		self.log( "%s [%s] says: %s" % ( message['from']['first_name'], message['from']['username'], message['text'] ) )
		response_text = self.response_for( message['text'] )
		chat_id = message['chat']['id']
		url = "https://api.telegram.org/bot%s/sendMessage" % self.api_key
		self.access_url( url, chat_id=chat_id, text=response_text  )
		self.log(  "Bot responds: %s" % response_text )

	def response_for(self, text):
		if text == '/start' or text == '/help':
			return 'Seja bem vindo meu caro querido S2\n' \
			'Para ver a lista de campeonatos disponíveis digite /campeonatos\n' \
			'Para ver a tabela classificatória digite o nome do campeonato'
		if text == '/campeonatos':
			return self.texto_campeonatos()
		return self.texto_tabela_classificatoria( text )

	def texto_tabela_classificatoria(self, text):
		if not self.campeonatos:
			self.carregar_campeonatos()
		if not self.campeonatos:
			return 'Desculpe, mas neste momento não podemos atender sua requisição, pois estamos tendo problemas em nossos servidores :('
		nome = self.formatar_nome_campeonato( text )
		if not nome in self.campeonatos:
			return 'Campeonato não encontrado :('
		campeonato = self.campeonatos[ nome ]
		tabela = self.buscar_tabela( campeonato )
		if not tabela:
			return 'Desculpe, mas ocorreu um erro em nossos servidores e não foi possível obter a tabela classificatória :('
		texto_tabela = ''
		for elemento in tabela:
			texto_tabela += elemento['position'] + ' - ' + str(elemento['points']) + ' PTS - ' + elemento['team']['name'] + '\n'
		return texto_tabela.encode('utf8')

	def texto_campeonatos(self):
		if not self.campeonatos:
			self.carregar_campeonatos()
		if not self.campeonatos:
			return 'Desculpe, mas neste momento não podemos atender sua requisição, pois estamos tendo problemas em nossos servidores :('
		texto_campeonatos = ''
		for k, campeonato in self.campeonatos.iteritems():
			texto_campeonatos += campeonato['name'] + '\n'
		return texto_campeonatos.encode('utf8')

	def carregar_campeonatos(self):
		try:
			url = 'http://app.servicos.uol.com.br/c/api/v1/list/championships/'
			dados = self.get_json( url, app='uol-placar-futebol', version=2 )
			lista_campeonatos = dados['championships']
			self.campeonatos = {}
			for campeonato in lista_campeonatos:
				nome = self.formatar_nome_campeonato( campeonato['name'] )
				self.campeonatos[ nome ] = campeonato
		except Exception as e:
			self.campeonatos = None
			self.log(  'Erro ao obter campeonatos: ' + str(e) )

	def buscar_tabela(self, campeonato):
		try:
			url = 'http://app.servicos.uol.com.br/c/api/v1/list/championships/tables/'
			dados = self.get_json( url, app='uol-placar-futebol', championship=campeonato['id'], season=campeonato['season'], version=2 )
			return dados['groups'][0]['ranking']
		except Exception as e:
			self.log( 'Erro ao obter tabela: ' + str(e) )
			return None

	def formatar_nome_campeonato(self, nome):
		return nome.lower().replace(' ', '')

	def get_json(self, url, **kwargs):
		response_text = self.access_url( url, **kwargs )
		return json.loads( response_text )

	def access_url(self, url, **kwargs):
		query = self.url_query( **kwargs )
		return urllib.urlopen( url + query, proxies=self.proxies ).read()

	def set_proxy(self, proxy):
		self.proxies = {'http': proxy, 'https': proxy}
		
	def url_query(self, **kwargs):
		query = ''
		for key, value in kwargs.iteritems():
			if key and value:
				if query:
					query += '&'
				query += key + '=' + urllib.quote(str(value))
		return '?' + query if query else ''

	def log(self, text):
		print text
		sys.stdout.flush()

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print 'Required args: <api_key> <last_update_id> <proxy http://host:port - optional>'
		exit(1)
	bot = TelegramBot( sys.argv[1], int(sys.argv[2]) )
	if len(sys.argv) == 4:
		bot.set_proxy( sys.argv[3] )
	bot.start();