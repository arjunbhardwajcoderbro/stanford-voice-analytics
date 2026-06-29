# Stanford Freshman Voice Assistant

A Retell AI voice agent that answers incoming Stanford student questions and sends call data to a FastAPI analytics dashboard.

## What it does

This project lets an incoming Stanford student ask questions by voice, then automatically logs:

- Call transcript
- AI-generated call summary
- User sentiment
- Whether the call was successful
- Call duration
- Estimated call cost

## Tech stack

- Retell AI
- Python
- FastAPI
- Cloudflare Tunnel
- HTML/CSS dashboard
- Webhooks

## Architecture

User speaks to Retell agent  
↓  
Retell handles the voice conversation  
↓  
Retell sends webhook event to FastAPI backend  
↓  
Backend stores transcript and analytics  
↓  
Dashboard displays calls and metrics  

## Why I built this

I wanted to build a real AI application that goes beyond a simple chatbot. This project helped me understand how voice AI products connect to backend systems, how webhooks work, and how call analytics can be used to improve an AI agent.

## Current features

- Voice FAQ assistant for incoming Stanford students
- Webhook endpoint for Retell call events
- Local transcript storage
- Analytics dashboard
- Summary, sentiment, success status, duration, and cost tracking

## Next steps

- Add question categorization
- Add charts for common topics
- Add prompt improvement suggestions
- Deploy publicly
- Add database storage