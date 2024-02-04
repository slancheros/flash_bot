from fastapi import FastAPI, Request, Response
from logging import Logger
import os

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv()
slack_token = os.environ.get("SLACK_BOT_TOKEN")
logger = Logger("flash_bot")

api = FastAPI()
slack_app = App(token=slack_token)
app_handler = SlackRequestHandler(slack_app)

@api.get("/")
def read_root():
    return {"Hello": "World"}

@api.post("/")
def slack_challenge(request:Request):
    print(request)
    if request.json and "challenge" in request.json:
        print("Received challenge")
        return Response(content="challenge", media_type="application/json")
    else:
        print("Got unknown request incoming")
        print(request.json)
    return



@slack_app.command("/llm_bot")
def llm(ack, say):
    ack("Received /llm command.")
    say("Hello, LLM!")

@slack_app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


@api.post("/slack/events")
async def endpoint(req: Request):
    logger.log("I got here")
    return await app_handler.handle(req)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=3000)
