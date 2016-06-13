# FutebaBot
Bot criado para o telegram com finalidade do usuário poder obter as tabelas classifiatórios dos principais campeonatos de futebol do mundo.
As informações a respeito dos campeonatos são obtidas do site [Placar UOL](https://esporte.uol.com.br/placaruol/), sendo assim, o bot pode apresentar problemas decorrentes de eventuais problemas no site da UOL.

##Funcionamento
Bot deve obter as mensagens de https://api.telegram.org/bot{token_telegram}/getUpdates e respondê-las, de acordo com os comandos escritos pelo usuário:<br/>
"**/start**" ou "**/help**": O bot deve mostrar um texto de boas vindas, especificando os comandos disponíveis.<br/>
"**/campeonatos**": Deve retornar a lista de campeonatos disponíveis<br/>
"**Nome do campeonato (Ex: Brasileirão)**": Deve verificar se existe um campeonato, caso exista deve retornar a tabela classificatória, e caso não exista mostra uma mensagen indicando a inexistência do campeonato.

##Iniciando o bot
Para rodar o bot são necessários 3 parâmetros:<br/>
***1º - Telegram Token:*** É necessário que o usuário possua um token (mais informações podem ser encontradas no site do [Telegram](https://core.telegram.org/bots)).<br/>
***2º - Last Message Id:*** É o Id da mensagem no qual o bot deve dar continuidade no envio das mensagens, este parâmetro é importante para evitar que o bot responda mensagens já respondidas (mais informações sobre o ID da mensagem podem ser encontrados na documentação do método [getUpdates](https://core.telegram.org/bots/api#getupdates) - verificar o parâmetro offset).
Caso ainda não existam mensagens ou o usuário não queira evitar duplicidade no envio de mensagens pode ser utilizado o valor 0.<br/>
***3º - Proxy:*** Por fim, é possível utilizar um proxy para as requisições do bot, este é opcional.
<br/><br/>
O comando para iniciar o bot ficará neste formato:
```
python bot.py <telegram_token> <last_message_id> <proxy - ex: http://localhost:8888 - optional>
```

##Demo
Uma versão deste bot já está disponível para uso:
https://telegram.me/FutebaBot
