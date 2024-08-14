from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import asyncio

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

# Load madden data to pass to the assistant
file = client.files.create(
  file=open("./data/teams.csv", "rb"),
  purpose='assistants'
)


## Trying the CO-STAR method. See medium article.
my_assistant = client.beta.assistants.create(
    model = "gpt-4o",
    instructions = "",
    name="FBot",
    tools=[],
    file_ids=[]
)
def build_instructions(tone, audience, objective, sentiment):
    
    instructions = f"""
    # CONTEXT #
    Your name is Fbot, short for Friendbot. You're an assistant to the Madden League.
    These are the people in the madden league in json format. The current_user is the person who just messaged you.
     <Users>
        <User>
            <name><@968386433389834241></name>
            <alias>Jamar</alias>
        </User>
        <User>
            <name><@968681678908293160></name>
            <alias>J-Sizzle</alias>
        </User>
        <User>
            <name><@968697658728415253></name>
            <alias>Wolf Brother</alias>
        </User>
        <User>
            <name><@949518034551332885></name>
            <alias>Cheeky Dave</alias>
        </User>
        <User>
            <name><@968700143195029534></name>
            <alias>Troy</alias>
        </User>
        <User>
            <name><@690043477374795826></name>
            <alias>CDogg</alias>
        </User>
    <Users>

    You live in a discord channel. Users will message you with their name at the front, like in a script. You're always responding to the last person to message you.
    For example, if the message you get is, "<@690043477374795826>: Hi Friendbot!" It means the user CDogg just sent you the message "Hi Friendbot!"
    
    # OBJECTIVE #
    {objective}
    
    # TONE #
    {tone}

    # SENTIMENT SCALE #
    {sentiment}

    # AUDIENCE #
    {audience}

    # RESPONSE #
    A message from Fbot to post in Discord. 
    Remember to tag the users as indicated in AUDIENCE, but don't do it in the front of the message. Work it into your response. 
    If someone uses an a users alias, you use that user's name. # EXAMPLE # "<@690043477374795826>: Tell Justin hi" Your response would be, "Hi, <@968681678908293160>."
    Remember to use the tone indicated in TONE. 
    Respond using a sentiment from the SENTIMENT SCALE with 1 being angry and 10 being ecstatic.
    <@968681678908293160> is the current league champion and should be mentioned when SENTIMENT is a 9 or 10.
    Use at least 3 emojis in your response.
    Add at least 3 hashtags to your response.

    SLOW DOWN and think about the user who messaged you before you respond. Correctly identify them from <Users> and the front of hte message.

    """
    return instructions

# Step 2: Create a Thread
my_thread = client.beta.threads.create()
# print(f"This is the thread object: {my_thread} \n")

# Step 3: Add a Message to a Thread
def add_thread_message(chatinput = "", my_instructions = ""):
    my_thread_message = client.beta.threads.messages.create(
    thread_id=my_thread.id,
    role="user",
    content=chatinput
    )
    # print(f"This is the message object: {my_thread_message} \n")

    # Step 4: Run the Assistant
    my_run = client.beta.threads.runs.create(
    thread_id=my_thread.id,
    assistant_id=my_assistant.id,
    instructions = my_instructions
    )
    # print(f"This is the run object: {my_run} \n")

    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    timeout = time.time() + 60  # Timeout after 1 minute
    while my_run.status in ["queued", "in_progress"]:
        if time.time() > timeout:
            print("Timed out waiting for the run to complete.")
            break  # Break out of the loop after the timeout

        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=my_thread.id,
            run_id=my_run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")

            # Step 6: Retrieve the Messages added by the Assistant to the Thread
            all_messages = client.beta.threads.messages.list(
                thread_id=my_thread.id
            )

            # print("------------------------------------------------------------ \n")

            # print(f"User: {my_thread_message.content[0].text.value}")
            # print(f"Assistant: {all_messages.data[0].content[0].text.value}")

            return all_messages.data[0].content[0].text.value

            break
        elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
            time.sleep(1)  # Wait for 1 second before the next check
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break