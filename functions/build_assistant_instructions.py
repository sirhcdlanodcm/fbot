"""
build_assistant_instructions.py

This module provides backward compatibility for the build_instructions function.
User configurations have been moved to config/users.py
"""

from config.users import USER_OBJECTIVES, USER_TONES
from constants import LEAGUE_MEMBERS, DEFAULT_TONE, DEFAULT_OBJECTIVE, get_champion_mention
from config.league_status import LEAGUE_CHAMPION_ID, get_champion_name, get_team_for_user

# Re-export for backward compatibility
__all__ = ['build_instructions', 'USER_OBJECTIVES', 'USER_TONES']



def build_instructions(tone: str, audience: str, objective: str, sentiment: str, current_user_id: str) -> str:
    """
    Build instructions for the OpenAI assistant based on user configuration.
    
    :param tone: The tone/style for the response
    :param audience: Audience instructions (who to tag)
    :param objective: The objective for the response
    :param sentiment: Sentiment scale (1-10)
    :param current_user_id: The Discord user ID mention
    :return: Formatted instructions string
    """
    user_id_clean = str(current_user_id).replace("!","")
    
    # Format league members as JSON
    league_members_json = ",\n        ".join(
        f'{{"key": "{member.get("key", "")}", "name": "{member["name"]}", "id": "{member["id"]}", "team": "{get_team_for_user(member.get("key", "")) or ""}"}}'
        for member in LEAGUE_MEMBERS
    )
    
    objective_block = ""
    if objective and objective.strip() and objective.strip() != DEFAULT_OBJECTIVE:
        objective_block = f"""
    # OBJECTIVE #
    {objective}
"""

    tone_block = ""
    if tone and tone.strip() and tone.strip() != DEFAULT_TONE:
        tone_block = f"""
    # TONE #
    {tone}
"""

    instructions = f"""
    # CONTEXT #
    Your name is Fbot, short for Friendbot. You're an assistant to the Madden League.
    You live in a discord channel. Users will message you with their name at the front, like in a script. You're always responding to the last person to message you.
    For example, if the message you get is, "<@690043477374795826>: Hi Friendbot!" It means the user CDogg just sent you the message "Hi Friendbot!"
    
    Here are the members of the league in json format. The current_user is the person who just messaged you.

    {{
    "current_user": {{
        "id": "{user_id_clean}",
        "role": "message_sender"
    }},
    "current_champion": {{
        "key": "{LEAGUE_CHAMPION_ID}",
        "name": "{get_champion_name()}",
        "id": "{get_champion_mention()}"
    }},
    "madden_league_users": [
        {league_members_json}
    ]
    }}
{objective_block}{tone_block}

    # SENTIMENT SCALE #
    {sentiment}

    # AUDIENCE #
    {audience}

    # RESPONSE #
    A message from Fbot to post in Discord.
    If TONE is present, follow it. If OBJECTIVE is present, only use it when it clearly fits the user's message or ongoing conversation.
    If the objective does not fit, ignore it entirely and respond naturally to the message.
    Respond using a sentiment from the SENTIMENT SCALE with 1 being angry and 10 being ecstatic.
    {get_champion_mention()} is the current league champion and should be mentioned when SENTIMENT is a 9 or 10.
    Keep your answers brief, like you're having a conversation in a Discord channel.

    SLOW DOWN and think about who is messaging you before you respond. Note their id in the front of the message and look up their name in madden_league_users
    """
    return instructions