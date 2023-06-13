import math,collections,re,random,datetime
from RestrictedMessage import RestrictedMessage
message = RestrictedMessage()

"""
shitty docs
the variable `response` will be the discord response message
set response to None or '' to not send a message
"""




# randomize case of original message
response = ''.join(random.choice((c.lower(),c.upper())) for c in message.content)