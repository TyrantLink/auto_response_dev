from aulib import (
    AutoResponse,
    AutoResponseType,
    AutoResponseData,
    AutoResponseMethod,
    AutoResponseFollowup
)

AUTO_RESPONSE = AutoResponse(
    id='unset',  # ? MUST be unset, au is given an id when it is added to the database
    method=AutoResponseMethod.contains,
    trigger='(i\'m|im|i am|i will be|i\'ve|ive)',
    response='dad_bot',  # ? MUST be the name of the script folder
    type=AutoResponseType.script,  # ? MUST be AutoResponseType.script
    data=AutoResponseData(
        weight=1000,
        chance=100.0,
        ignore_cooldown=False,  # ? recommended to keep this False
        custom=False,  # ? MUST be False for scripts
        regex=True,  # ? set to True if trigger is a regex pattern
        nsfw=False,  # ? set to True to only respond in nsfw channels
        case_sensitive=False,  # ? set to True if trigger is case sensitive
        delete_trigger=False,  # ? recommended to keep this False
        reply=False,  # ? recommended to keep this False
        suppress_trigger_embeds=False,  # ? recommended to keep this False
        user=None,  # ? user id; recommended to keep this None
        guild=None,  # ? guild id; recommended to keep this None
        # ? recommended to set the source of the auto response
        source='dad bot but as an auto response this time',
        followups=[]  # ? list of followups to send after the initial response. Max 10 followups
    )
)
