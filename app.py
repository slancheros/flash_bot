from fastapi import FastAPI, Request, Response,Form
from logging import Logger
from pydantic import BaseModel
import os

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv()
slack_token = os.environ.get("SLACK_BOT_TOKEN")
logger = Logger("flash_bot")

class Item(BaseModel):
    type: str
    token: str 
    challenge: str


api = FastAPI()
slack_app = App(token=slack_token)
app_handler = SlackRequestHandler(slack_app)

@api.get("/")
def read_root():
    return {"Hello": "World"}

@api.post("/")
def slack_challenge(item:Item):

    if item.challenge:
        print("Received challenge")
        return Response(content=item.challenge, media_type="application/json")
    else:
        print("Got unknown request incoming")
    return

api.post("/llm_bot")
def slack_slash(text: str = Form("missing argument", max_length=20)):

    if text == "help":
        result = {
            "response_type": "in_channel",
            "text": """Hi there! I accept the following commands:
            `/aci health` - show total system health
            """
            }
    else:
        result = {
            "text": "_" + text + "_? I don't know what you're talking about. Please visit `/aci help`"
            }
    return result

@slack_app.command("/llm_bot")
def llm(ack, respond, command):
    ack()
    respond("Prompt: *%s*"%command['text']) 



@api.post("/slack/events")
async def endpoint(req: Request):
    logger.log("I got here")
    return await app_handler.handle(req)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=3000)
