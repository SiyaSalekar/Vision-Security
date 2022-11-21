


#this file will handle messages of pubnub


from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# FOR DEALING WITH .ENV FILE WHERE publish/subscribe key are stored

from dotenv import load_dotenv
import os

load_dotenv()

#GETTING THE KEYS FOR PUBUN PUBLISH/SUBSCRIBE
PUBNUB_PUBLISH_KEY=os.environ["PUBNUB_PUBLISH_KEY"]
PUBNUB_SUBSCRIBE_KEY=os.environ["PUBNUB_SUBSCRIBE_KEY"]


print(PUBNUB_SUBSCRIBE_KEY)
print(PUBNUB_PUBLISH_KEY)





pnconfig = PNConfiguration()

pnconfig.subscribe_key = PUBNUB_SUBSCRIBE_KEY
pnconfig.publish_key = PUBNUB_PUBLISH_KEY
