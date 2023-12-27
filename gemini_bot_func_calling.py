#gemini_bot_func_calling.py
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part
import logging
from dotenv import load_dotenv
from create_ticket import create_ticket, app

load_dotenv()

# Initialize Vertex AI Gemini Model
model = GenerativeModel("gemini-pro")


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


create_ticket_func = generative_models.FunctionDeclaration(
  name="create_ticket",
  description="Creates a ticket in a Slack channel. This function takes the subject, type of question, and detailed description.",
  parameters={
      "type": "object",
      "properties": {
        "subject": {
          "type": "string",
          "description": "Subject of the ticket."
        },
        "type_of_question": {
          "type": "string",
          "description": "Type of question or issue."
        },
        "description": {
          "type": "string",
          "description": "Detailed description of the issue."
        }
      },
      "required": [
        "subject",
        "type_of_question",
        "description"
      ]
    },
)

ticket_tool = generative_models.Tool(
  function_declarations=[create_ticket_func]
)


def model_response(text):
    response = model.generate_content(
        text,
        generation_config={"temperature": 0},
        tools=[ticket_tool],
    )
    if response.candidates:
        function_args = response.candidates[0].content.parts[0].function_call
        return function_args
    else:
        return "No response generated."
    return response

#Test function 
#print(model_response("I need help with my computer."))

# Function calling Model Chat
def function_calling_chat(message, from_user):
    # Start the chat and send the initial message
    context = "You are an internal IT support agent that helps to log tickets based on user messages. "
    function_calling_chat = model.start_chat()
    full_message = f"{context}\n{message}"
    model_response = function_calling_chat.send_message(full_message, tools=[ticket_tool])

    # Check if model returned a function call
    for candidate in model_response.candidates:
        for part in candidate.content.parts:
            if hasattr(part, 'function_call') and part.function_call.name == "create_ticket":
                # Initialize variables
                type_of_question = ""
                subject = ""
                description = ""

                # Extract fields from the function call args, treating it as a dictionary
                args = part.function_call.args
                if "type_of_question" in args:
                    type_of_question = args["type_of_question"]
                if "subject" in args:
                    subject = args["subject"]
                if "description" in args:
                    description = args["description"]

                # Call the create_ticket function
                ticket_response = create_ticket(app.client, subject, from_user, type_of_question, description)

                # Format the response for the model
                formatted_response = {
                    "content": {"ticket_creation_status": ticket_response.get("message", "Ticket creation failed")}
                }

                # Send the response back to the model and get final response
                final_model_response = function_calling_chat.send_message(
                    Part.from_function_response(
                        name="create_ticket",
                        response=formatted_response
                    ),
                    tools=[ticket_tool]
                )

                # Debugging: Print the entire final_model_response
                print("Debug - Final model_response:", final_model_response)

                # Extract and return only the text part from the final response
                final_text = ""
                for candidate in final_model_response.candidates:
                    for part in candidate.content.parts:
                        try:
                            # Attempt to access the text attribute
                            text = part.text
                            final_text = text
                            break
                        except ValueError:
                            # Part has no text, continue to the next part
                            continue

                    if final_text:
                        break
                return final_text

    # If no function call was made, return an empty string or a default message
    return "No function call was made in response."

#print(function_calling_chat("I need help with my computer.", "U052337J8QH"))

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#Message Handler
@app.message("")  
def message_handler(message, say, ack):
    ack()
    # Extract the text and user_id from the message payload.
    message_text = message.get('text', '')
    from_user = message.get('user', '')
    
    #Call the function_calling_chat function
    ai_response = function_calling_chat(message_text, from_user)
    
    # Send the response to Slack
    say(text=ai_response, thread_ts=message['ts'])

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()