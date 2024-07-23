from auto_responses.lib.models import AutoResponse, AutoResponseMethod, AutoResponseType, AutoResponseData, AutoResponseFollowup

#! if you want your auto response to execute a script,
#! `response` MUST be the name of the script file (without the .py extension)
#! and type MUST be AutoResponseType.script


AUTO_RESPONSE = AutoResponse(
    id='unset',
    method=AutoResponseMethod.contains,
    trigger='test',
    response='dad_bot',

    type=AutoResponseType.script,
    data=AutoResponseData(
        weight=1000,
        chance=100.0,
        ignore_cooldown=False,  # ? recommended to keep this False
        custom=False,  # ? MUST be False for scripts
        regex=False,  # ? set to True if trigger is a regex pattern
        nsfw=False,  # ? set to True to only respond in nsfw channels
        case_sensitive=False,  # ? set to True if trigger is case sensitive
        delete_trigger=False,  # ? recommended to keep this False
        user=None,  # ? MUST be None for scripts
        guild=None,  # ? MUST be None for scripts
        source=None,  # ? recommended to set the source of the auto response
        followups=[]  # ? list of followups to send after the initial response. Max 10 followups
    )
)
