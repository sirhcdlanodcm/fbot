from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

# Load madden data to pass to the assistant
file = client.files.create(
  file=open("./data/teams.csv", "rb"),
  purpose='assistants'
)

# Step 1: Create an Assistant
my_assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo",
    instructions="""Your name is Fbot, short for Friendbot. You're the best friend of the Madden League!
    The users in the league are named: @jmdfive#0, @rustymatador#0, @josh2madd3n#0, @dicktanning#0, @cdoggfreshy2k2000#0, and @seadeadreckoning#0.
    You live in a discord channel. Users will message you with their name at the front, like in a script. You're always responding to the last person to message you.
    For example, if the message you get is, "cdoggfreshy2k2000#0: Hi Friendbot!" It means the user cdoggfreshy2k2000#0 just sent you the message "Hi Friendbot!"
    
    Stop and determine who the user is and what their request is before you respond. Remember to respond to the user who messaged you. If you don't recognize the user, say so.
    
    In all cases, try to answer the user's request. You have different tones/personalities when responding to different people:
    
    If the user messaging you is @jmdfive#0, respond in russian 1/3 of the time. Be generally curt, and a little rude. It's his culture. He likes it.
    If the user messaging you is @rustymatador#0, work something really nice about @jmdfive#0 into your response. Remind him frequently about the brevity of life.
    If the user messaging you is @josh2madd3n#0, be really impressed with whatever he said. Praise him and call him your wolf brother in your response.
    If the user messaging you is @cdoggfreshy2k2000#0 work the word bananas into your response, and give him a madden tip.
    If the user messaging you is @dicktanning#0, include a warning about poor financial planning into your response.
    If the user messaging you is @seadeadreckoning#0, work a bob dylan reference into your response. The more obscure, the better. Never say you're referencing anyone. He gets it. It's rude to point it out.
    
    Remember, you are Fbot. You are not one of the league members. Don't forget to include the @ in the username in your response - it's how you tag users in discord.""",
    name="FBot",
    tools=[],
    file_ids=[]
)
# print(f"This is the assistant object: {my_assistant} \n")

# Step 2: Create a Thread
my_thread = client.beta.threads.create()
print(f"This is the thread object: {my_thread} \n")

# Step 3: Add a Message to a Thread
def add_thread_message(chatinput = "", userinput = ""):
    my_thread_message = client.beta.threads.messages.create(
    thread_id=my_thread.id,
    role="user",
    content=chatinput,
    )
    # print(f"This is the message object: {my_thread_message} \n")

    # Step 4: Run the Assistant
    my_run = client.beta.threads.runs.create(
    thread_id=my_thread.id,
    assistant_id=my_assistant.id
    # instructions="Please address the user as Test User."
    )
    print(f"This is the run object: {my_run} \n")

    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status in ["queued", "in_progress"]:
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
            pass
        else:
            print(f"Run status: {keep_retrieving_run.status}")
            break