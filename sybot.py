# Connor Stephen 20/2/2018
# Sybot 0.0.1

import json
import time
import requests
import urllib

TOKEN = "533270691:AAE8CchLPpaUfSJnq6NSIDBBUIjo2VPJZgI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# gets the url for the bot API
def get_url(url):
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content

# gets the JSON content from the URL
def get_json_from_url(url):
	content = get_url(url)
	js = json.loads(content)
	return js

# checks for updates from a given chat
def get_updates(offset=None):
	url = URL + "getUpdates?timeout=100"
	if offset:
		url += "?offset={}".format(offset)
	js = get_json_from_url(url)
	return js

# loops through each update and returns biggest ID to call getUpdate again
def get_last_update_id(updates):
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)
	
# sends a reply  for every message received
def echo_all(updates):
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			send_message(text, chat)
		except Exception as e:
			print(e)

def get_last_chat_id_and_text(updates):
	num_updates = len(updates["result"])
	last_update = num_updates - 1
	text = updates["result"][last_update]["message"]["text"]
	chat_id = updates["result"][last_update]["message"]["chat"]["id"]
	return (text, chat_id)


def send_message(text, chat_id):
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	get_url(url)
	

text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)

# main function
def main():
	last_update_id = None
	while True:
		print("Getting updates...")
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			echo_all(updates)
		time.sleep(0.5)
		
# if the main function is called main, then main is called
if __name__ == '__main__':
	main()
