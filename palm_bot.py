import os
import vertexai
import json
from dotenv import load_dotenv
from vertexai.preview.language_models import ChatModel
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Initialize the AI model
vertexai.init(project="playground-391915", location="us-central1")
chat_model = ChatModel.from_pretrained("chat-bison@001")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 1024
}
chat = chat_model.start_chat()

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def respond_with_ai(message_text):
    """Send a message to the AI model and get its response."""
    response = chat.send_message(message_text, **parameters)
    return response.text

@app.message("")  # This is the command to trigger the AI response.
def message_handler(message, say):
    # Extract the text from the message payload.
    message_text = message['text']
    
    # Get a response from the AI model.
    ai_response = respond_with_ai(message_text)
    
    # Send the AI's response back to Slack.
    say(ai_response)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
