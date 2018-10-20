import os, slackclient

CINEMABOT_SLACK_NAME = os.environ.get('CINEMABOT_SLACK_NAME')
CINEMABOT_SLACK_TOKEN = os.environ.get('CINEMABOT_SLACK_TOKEN')

cinemabot_slack_client = slackclient.SlackClient(CINEMABOT_SLACK_TOKEN)

print(CINEMABOT_SLACK_NAME)
print(CINEMABOT_SLACK_TOKEN)
is_ok = cinemabot_slack_client.api_call("users.list").get('ok')
print(is_ok)