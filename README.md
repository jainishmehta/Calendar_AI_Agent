# Calendar_AI_Agent
Created calendar AI agent using Langchain to set up meeting using user input and LLM. 

1. Use quickstart.py script from Google Calendar API to authenication with the program using Google Client library.
Follow this guide to understand this:
https://developers.google.com/workspace/calendar/api/quickstart/python
Run this script to get the credentials.json and token.json, you need to authorize access.
```bash
python3 quickstart.py
```
The agent can then take a user-inputted event to add to the calendar if not already booked. Run 
```bash
python3 calendar_agent.py
```
