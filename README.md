🎙️ Voice Agent Analytics Dashboard

A lightweight analytics platform for Retell-powered voice agents.

🌐 Live Demo: https://stanford-voice-analytics.onrender.com/dashboard

🎓 Example Deployment: Stanford Freshman FAQ Assistant

Overview

Voice AI developers often need to manually inspect conversations to understand how their agents are performing.

This project automatically ingests Retell webhook events, stores conversation data, and surfaces meaningful metrics through a clean FastAPI dashboard.

The included demo uses a Stanford Freshman FAQ assistant, but the analytics platform is designed to work with any Retell-powered voice agent.

Features
📞 Receives Retell webhook events
📝 Stores transcripts and call metadata
📊 Tracks success rate and conversation metrics
💰 Calculates call duration and cost
🧠 Automatically categorizes conversations by topic
💡 Generates AI-powered product insights
🚀 Live dashboard deployed on Render
Architecture
Caller
   │
   ▼
Retell Voice Agent
   │
   ▼
Webhook (/webhook)
   │
   ▼
FastAPI Backend
   │
   ▼
Analytics Dashboard
Dashboard
Analytics Overview




Conversation Analytics




Agent Insights




Tech Stack
Python
FastAPI
Uvicorn
Retell AI
GitHub
Render
Running Locally
Clone the repository
git clone https://github.com/arjunbhardwajcoderbro/stanford-voice-analytics.git
cd stanford-voice-analytics
Install dependencies
pip install -r requirements.txt
Start the backend
uvicorn main:app --reload
Open the dashboard
http://localhost:8000/dashboard
Deployment

The application is deployed on Render and automatically redeploys whenever new commits are pushed to the main branch.

Live URL:

https://stanford-voice-analytics.onrender.com/dashboard

Why I Built This

As I explored voice AI, I realized that webhook events contain far more value than raw transcripts alone.

I wanted to build a lightweight analytics layer that automatically transforms Retell webhook events into actionable insights for developers—including conversation summaries, topic categorization, success metrics, cost tracking, and product analytics.

The Stanford Freshman FAQ assistant serves as the demonstration use case, while the broader goal is to build tooling that helps developers evaluate and improve voice agents.

Future Work
Prompt A/B testing
Historical trend analysis
Multi-agent dashboards
Semantic conversation search
Real-time monitoring
AI-generated prompt improvement suggestions
Exportable reports
Repository

GitHub:

https://github.com/arjunbhardwajcoderbro/stanford-voice-analytics

About This Project

This project was built to better understand how production voice agents connect to backend systems through webhooks and how conversation data can be transformed into actionable analytics.

While the current demo focuses on a Stanford Freshman FAQ assistant, the underlying architecture is designed to support analytics for any Retell-powered voice application.

Built with ❤️ using FastAPI, Retell AI, Render, and Python.