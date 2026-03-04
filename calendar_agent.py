from re import search
from langchain_google_community import CalendarToolkit, CalendarSearchEvents, GetCalendarsInfo, CalendarCreateEvent
from langchain_google_community.calendar.utils import (
    build_calendar_service, 
    get_google_credentials
)
from datetime import datetime, timedelta
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

credentials = get_google_credentials(       
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)

api_resource = build_calendar_service(credentials=credentials)
toolkit = CalendarToolkit(api_resource=api_resource)    

tools = toolkit.get_tools()
print(tools)
search = CalendarSearchEvents(api_resource=api_resource)
calendars_info = GetCalendarsInfo(api_resource=api_resource)
calendar_infos = calendars_info.invoke({})
print(calendar_infos)

load_dotenv()
today = datetime.now().strftime("%Y-%m-%d 00:00:00")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 23:59:59")
results = search.invoke({
    'calendars_info': calendar_infos,
    "min_datetime": '2026-01-01 00:00:00',
    "max_datetime": tomorrow,
})
user_event = input("What event did you want to look for?")
work_meeting = False
for result in results:
    print(result['summary'])
    llm = ChatOllama(model='qwen2.5:0.5b', temperature=0.2)
    prompt = f"You are a helpful assistant only answering in the format of 'yes' or 'no' that can help me understand events in my calendar. The event is: {result['summary']}. Does it denote {user_event}?"
    response = llm.invoke(prompt).content
    print("Response: ", response)
    work_meeting = False
    if response.startswith('yes'):
        print(result['summary'])
        work_meeting = True
    else:
        print('Not a work meeting with my boss at OpenAi')

if not work_meeting:
    input("Do you want to create the event? (y/n)")
    if response.startswith('y'):
        try:
            CalendarCreateEvent(api_resource=api_resource).invoke({
                'name': {user_event},
                'timezone': 'America/Edmonton',
                'args_schema':{
                    'summary':  {user_event}
                },
                'calendar_id': 'primary',
                'summary':  {user_event},
                'start_datetime': str((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 13:00:00")),
                'end_datetime': str((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 14:00:00"))
            })
        except Exception as e:
            print("Error creating event: ", e)