# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import slack
from flask import Flask
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
import requests


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ.get('SLACK_SIGNING_SECRET'), '/slack/events', app)

client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
BOT_ID = client.api_call('auth.test')['user_id']

# print(BOT_ID)
# print(os.environ.get('SLACK_SIGNING_SECRET'), os.environ.get('SLACK_TOKEN'))


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    if BOT_ID != user_id:
        response = requests.get("https://app.pavlok.com/unlocked/remotes/ganesh/vibrate/10")
        if response.ok:
            slack_status_msg = "Stimulus sent!"
        else:
            slack_status_msg = "Something went wrong, unable to send Stimulus"
        print(slack_status_msg)
        client.chat_postMessage(channel=channel_id, text=slack_status_msg)


if __name__ == "__main__":
    app.run(debug=True)
