from slackclient import slackclient, time
import random
from flask import Flask, request, make_response, Response
import json

SOCKET_DELAY = 1.5

CINEMABOT_SLACK_NAME = os.environ.get('CINEMABOT_SLACK_NAME')
CINEMABOT_SLACK_TOKEN = os.environ.get('CINEMABOT_SLACK_TOKEN')
CINEMABOT_SLACK_ID = os.environ.get('CINEMABOT_SLACK_ID')

cinemabot_slack_client = slackclient.SlackClient(CINEMABOT_SLACK_TOKEN)

app = Flask(__name__)

def post_message(message, channel):
    cinemabot_slack_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)

def get_mention(user):
    return '<@{user}>'.format(user=user)

cinemabot_slack_mention = get_mention(CINEMABOT_SLACK_ID)

def is_for_me(event):
    type = event.get('type')
    if type and type == 'message' and not(event.get('user')==CINEMABOT_SLACK_ID):
        if is_private(event):
            return True
        text = event.get('text')
        channel = event.get('channel')
        if cinemabot_slack_mention in text.strip().split(): 
            return True
 
def say_hi(user_mention):
    response_template = random.choice(['Hello, How are you {mention}? :)',
                                       'Hi!',
                                       'Hi, {mention}, How are you?'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):=
    response_template = random.choice(['see you later! :)',
                                       'Take care, {mention}!',
                                       'Bye, {mention}!'])
    return response_template.format(mention=user_mention)

def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['Hello, How are you?', 'Hi!'])

def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['Goodbye!', 'Bye, Take Care!'])

def handle_message(message, user, channel):
    if is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention), channel=channel)
    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention), channel=channel)

def message_actions():
    message_action = json.loads(request.form["payload"])
    user_id = message_action["user"]["id"]

    if message_action["type"] == "interactive_message":
        SNACK_ORDERS[user_id]["message_ts"] = message_action["message_ts"]

        open_dialog = slack_client.api_call(
            "dialog.open",
            trigger_id=message_action["trigger_id"],
            dialog={ "text": "Would you like to attend a panel?",
                     "attachments": [
        {
                        "text": "Choose a conversation to join! :) ",
                        "fallback": "You are unable to choose a panel",
                        "callback_id": "wopr_game",
                        "color": "",
                        "attachment_type": "default",
                        "actions": [
                                {
                                    "name": "film",
                                    "text": "First Man",
                                    "type": "button",
                                    "value": "first_man"
                                },
                                {
                                    "name": "film",
                                    "text": "Widows",
                                    "type": "button",
                                    "value": "widows"
                                },
                                {
                                    "name": "film",
                                    "text": "Burning",
                                    "style": "danger",
                                    "type": "button",
                                     "value": "burning",
                                "confirm": {
                                    "title": "Are you sure?",
                                    "text": "Wouldn't you prefer a good heist in Widows? ;) ",
                                    "ok_text": "Yes",
                                    "dismiss_text": "No"
                                }
                             }
                         ]
                      }
                 ]
}
             )

        print(open_dialog)

        slack_client.api_call(
            "chat.update",
            channel=PANEL_ORDERS[user_id]["order_channel"],
            ts=message_action["message_ts"],
            text="Taking up your RSVP...",
            attachments=[]
        )

    elif message_action["type"] == "dialog_submission":
        panel_order = PANEL_ORDERS[user_id]

        slack_client.api_call(
            "chat.update",
            channel=PANEL_ORDERS[user_id]["order_channel"],
            ts=panel_order["message_ts"],
            text=":See You!",
            attachments=[]
        )

    return make_response("", 200)

def handle_command(slack_api, command, channel):
    EXAMPLE_COMMAND = 'do'
    if command.lower().startswith(EXAMPLE_COMMAND) or command.lower().startswith('Test'):
        slack_api.rtm_send_message(channel, 'Working! please do further command :)')
    elif command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().startswith('hello') or command.lower().startswith('who are you'):
        slack_api.rtm_send_message(channel, 'Hey, i am FilmFest18s Bot, how may I help you?')
    else:
        print 'Invalid Command: Not Understood'
        slack_api.rtm_send_message(channel, 'Invalid Command: Not Understood')

def run():
    if cinemabot_slack_client.rtm_connect():
        print('[.] FilmFest18 is running! you did it')
        while True:
            event_list = cinemabot_sslack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')

if __name__=='__main__':
    run()