import math,collections,re,random,time,datetime
from RestrictedMessage import RestrictedMessage
message = RestrictedMessage()

"""
shitty docs
for perfect compatibility, run on python 3.10[.12]

the variable `response` will be the discord response message
set response to None or '' to not send a message
"""

# randomize case of original message
response = ''.join(random.choice((c.lower(),c.upper())) for c in message.content)