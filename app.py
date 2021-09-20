# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import slack
from flask import Flask
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ.get('SLACK_SIGNING_SECRET'), '/slack/events', app)

client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
BOT_ID = client.api_call('auth.test')['user_id']

print(BOT_ID)
print(os.environ.get('SLACK_SIGNING_SECRET'), os.environ.get('SLACK_TOKEN'))


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    if BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text='Hello World!')


if __name__ == "__main__":
    app.run(debug=True)
