import os, time, random, urllib2, re
from slackclient import SlackClient
from bs4 import BeautifulSoup

# starterbot's ID as an environment variable
# BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U0JFYQX8B"

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
FACE = "face"
IMAGE = "image me"

sample_responses = ["Have you considered a career in acting?", "HAGGIS!", "I'm a vampire!"]
r = random.Random()  

### TODO ###
# display image instead of URL 

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def image_search(query, num=20):
    query = query.replace(' ', '+')
    url = 'https://www.google.com/search?q=nic+cage+' + query + '&num=' + str(num)
    headers = {'User-agent': 'Mozilla/5.0'}
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")   
    img_objects = soup.findAll('img')
    img_srcs = []
    for img in img_objects:
        img_srcs.append(img.get('src'))
    return r.choice(img_srcs)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if command.endswith(FACE):
        response = "OFF!"
    if "random" in command:
        response = r.choice(sample_responses)
    if IMAGE in command:
        m = re.search(r'\d+$', command)
        n = int(m.group()) if m else None
        response = image_search(command.split(IMAGE, 1)[1].lstrip(), n)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("CageBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")