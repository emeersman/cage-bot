import json, urllib2
from slackclient import SlackClient


BOT_NAME = 'cage'

token = 'xoxb-18542847283-QG1ykRGyUF7tLgXMkD7sBoNH'

if __name__ == "__main__":
    response = urllib2.urlopen("https://slack.com/api/users.list?token=" + token)
    data = json.loads(response.read())
    if data['ok']:
        # retrieve all users so we can find our bot
        users = data['members']
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)