# Slack Bot with Vertex AI Integration

## Overview
This repo contains sample implementations of Gemini AI API for a slack application. Example includes simple text generation and function calling in Gemini 

[![Watch the full setup video for Slack and Vertex AI Here](https://img.youtube.com/vi/-ocvFMjr_xE/maxresdefault.jpg)](https://youtu.be/-ocvFMjr_xE?si=V3eB0gV7E8KWk-OE)


## Features
- Text Generation with Gemini AI API via Vertex AI Service 
- Function Calling - Create Ticket Example 


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

### Running the pure Gemini Bot for Text Generation 
```bash
python gemini_bot.py
```

### Running the pure Gemini Bot for Function Calling 
 ```bash
python gemini_bot_func_calling.py
```

## Usage
Once the bot is running, it will listen to messages in Slack. When a message is received, it processes the text using the Vertex AI API and provides a response. This is designed to be used as a DM with the bot. 
