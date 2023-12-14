# Slack Bot with Vertex AI Integration

## Overview
This Slack bot is designed to process text inputs using the Vertex AI API and supports a custom functionality to send messages back to Slack channels. It listens to messages in Slack, sends the text to the Vertex AI API for processing, and interprets the AI's response for any specific actions like posting messages to a channel.

[![Watch the full setup video for Slack and Vertex AI Here](https://img.youtube.com/vi/-ocvFMjr_xE/maxresdefault.jpg)](https://youtu.be/-ocvFMjr_xE?si=V3eB0gV7E8KWk-OE)


## Features
- Text processing with Vertex AI's Generative Model.
- Custom function to post messages to Slack channels based on AI's response.
- Logging for debugging and monitoring.

## Requirements
- Python 3.9
- Slack Bot and App Token
- Vertex AI project setup

## Installation and Setup

### Slack Setup 
- Go to app.slack.com and Click on Create New App
- Use the From an app manifest option
- Copy the `slack_app_manifest.yaml` to your own manifest and you should be good to go 
- Create Bot and App Level Tokens 

### Clone the Repository
```bash
git clone https://github.com/hollaugo/google-vertexai-slack-bot
cd google-vertexai-slack-bot
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables
Set the following environment variables:
- `SLACK_BOT_TOKEN`: Your Slack Bot User OAuth Token.
- `SLACK_APP_TOKEN`: Your Slack App Token

### Running the Application
```bash
python gemini_bot.py
```

## Usage
Once the bot is running, it will listen to messages in Slack. When a message is received, it processes the text using the Vertex AI API and provides a response. This is designed to be used as a DM with the bot. 
