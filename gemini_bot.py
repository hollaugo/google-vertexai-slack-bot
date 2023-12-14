import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize Vertex AI
vertexai.init(project="prompt-circle-learn", location="us-central1")

def generate(text):
    model = GenerativeModel("gemini-pro-vision")
    inputs = [text]  # Text is directly added as a string

    responses = model.generate_content(
        inputs,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        }
    )

    # Extract the response text and return
    if responses.candidates:
        return responses.candidates[0].content.parts[0].text
    else:
        return "No response generated."



# Initialize the Slack app
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#Message Handler
@app.message("")  
def message_handler(message, say, ack):
    ack()
    text = message.get('text', '')

    # Call the generate function with text only
    ai_response = generate(text)

    # Send the response to Slack
    say(text=ai_response, thread_ts=message['ts'])


@app.event("file_shared")
def handle_file_shared_events(body, logger):
    logger.info(f"File shared event received: {body}")



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
