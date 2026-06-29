from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from datetime import datetime
from collections import Counter

app = FastAPI()
CALLS_FILE = "calls.jsonl"


def categorize_call(text):
    text = (text or "").lower()

    if any(word in text for word in ["housing", "dorm", "roommate", "move in", "move-in"]):
        return "🏠 Housing"
    if any(word in text for word in ["ap score", "class", "course", "advisor", "academic", "major"]):
        return "📚 Academics"
    if any(word in text for word in ["immunization", "vaden", "health", "medical", "vaccine"]):
        return "🩺 Health"
    if any(word in text for word in ["meal", "dining", "food"]):
        return "🍽 Dining"
    if any(word in text for word in ["car", "parking", "bike", "transportation"]):
        return "🚗 Transportation"
    if any(word in text for word in ["orientation", "approaching stanford", "nso"]):
        return "🎉 Orientation"

    return "❓ Other"


@app.get("/")
def home():
    return {"status": "Stanford FAQ backend is running"}


@app.post("/webhook")
async def retell_webhook(request: Request):
    payload = await request.json()
    call = payload.get("call", {})

    record = {
        "received_at": datetime.utcnow().isoformat(),
        "event": payload.get("event"),
        "call_id": call.get("call_id"),
        "agent_id": call.get("agent_id"),
        "transcript": call.get("transcript"),
        "call_analysis": call.get("call_analysis"),
        "duration_ms": call.get("duration_ms"),
        "call_cost": call.get("call_cost", {}).get("combined_cost"),
        "raw_payload": payload,
    }

    with open(CALLS_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    print("Received:", payload.get("event"))
    return {"ok": True}


def load_calls():
    calls = []

    try:
        with open(CALLS_FILE) as f:
            for line in f:
                item = json.loads(line)
                if item.get("event") == "call_analyzed":
                    item["category"] = categorize_call(item.get("transcript"))
                    calls.append(item)
    except FileNotFoundError:
        pass

    calls.reverse()
    return calls


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    calls = load_calls()

    total_calls = len(calls)
    successful = sum(1 for c in calls if c.get("call_analysis", {}).get("call_successful"))
    success_rate = (successful / total_calls * 100) if total_calls else 0
    total_cost = sum((c.get("call_cost") or 0) for c in calls)
    avg_duration = (sum((c.get("duration_ms") or 0) for c in calls) / total_calls / 1000) if total_calls else 0

    topic_counts = Counter(c["category"] for c in calls)
    most_asked_topic = topic_counts.most_common(1)[0][0] if topic_counts else "None"

    insights = []
    if topic_counts:
        top_topic, top_count = topic_counts.most_common(1)[0]
        insights.append(f"Most questions are about {top_topic}, suggesting this is the highest-friction area for incoming students.")
    if success_rate >= 90:
        insights.append("The agent is handling most test calls successfully, which is a good sign for early QA.")
    if avg_duration > 45:
        insights.append("Average calls are relatively long. Shorter answers may improve the voice experience.")
    else:
        insights.append("Average call length is concise, which is good for a voice FAQ assistant.")

    topic_rows = ""
    max_topic_count = max(topic_counts.values()) if topic_counts else 1

    for topic, count in topic_counts.most_common():
        width = int((count / max_topic_count) * 100)
        topic_rows += f"""
        <div class="topic-row">
            <div class="topic-label">
                <span>{topic}</span>
                <strong>{count}</strong>
            </div>
            <div class="bar-bg">
                <div class="bar-fill" style="width:{width}%"></div>
            </div>
        </div>
        """

    call_cards = ""

    for call in calls:
        analysis = call.get("call_analysis", {})
        successful_call = analysis.get("call_successful")
        success_badge = "Successful" if successful_call else "Needs review"
        success_class = "good" if successful_call else "bad"

        duration = (call.get("duration_ms") or 0) / 1000
        cost = call.get("call_cost") or 0

        call_cards += f"""
        <div class="card conversation-card">
            <div class="conversation-top">
                <span class="badge">{call.get("category")}</span>
                <span class="status {success_class}">{success_badge}</span>
            </div>

            <h3>{analysis.get("call_summary", "No summary available")}</h3>

            <div class="mini-grid">
                <div><span>Sentiment</span><strong>{analysis.get("user_sentiment", "Unknown")}</strong></div>
                <div><span>Duration</span><strong>{duration:.1f}s</strong></div>
                <div><span>Cost</span><strong>${cost:.2f}</strong></div>
            </div>

            <details>
                <summary>View transcript</summary>
                <pre>{call.get("transcript", "No transcript available")}</pre>
            </details>
        </div>
        """

    html = f"""
    <html>
    <head>
        <title>Stanford Voice Analytics</title>
        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                background: #f6f4ef;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                color: #1f2933;
            }}

            .page {{
                max-width: 1180px;
                margin: 0 auto;
                padding: 36px 28px 60px;
            }}

            .hero {{
                background: linear-gradient(135deg, #8C1515, #B83A2E);
                color: white;
                padding: 34px;
                border-radius: 24px;
                box-shadow: 0 18px 40px rgba(140, 21, 21, .22);
                margin-bottom: 24px;
            }}

            .eyebrow {{
                text-transform: uppercase;
                letter-spacing: .12em;
                font-size: 13px;
                opacity: .85;
                margin-bottom: 12px;
                font-weight: 700;
            }}

            h1 {{
                font-size: 42px;
                margin: 0 0 12px;
            }}

            .hero p {{
                margin: 0;
                max-width: 720px;
                line-height: 1.55;
                opacity: .95;
                font-size: 17px;
            }}

            .stats {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 16px;
                margin-bottom: 24px;
            }}

            .stat, .card {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 10px 26px rgba(24, 39, 75, .08);
                border: 1px solid rgba(31, 41, 55, .06);
            }}

            .stat {{
                padding: 20px;
            }}

            .stat-label {{
                color: #6b7280;
                font-size: 13px;
                margin-bottom: 8px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: .05em;
            }}

            .stat-number {{
                color: #8C1515;
                font-size: 30px;
                font-weight: 800;
            }}

            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 26px;
            }}

            .card {{
                padding: 24px;
            }}

            .card h2 {{
                margin-top: 0;
            }}

            .insight {{
                padding: 14px 0;
                border-bottom: 1px solid #eee;
                line-height: 1.45;
            }}

            .insight:last-child {{
                border-bottom: none;
            }}

            .topic-row {{
                margin-bottom: 16px;
            }}

            .topic-label {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 7px;
                font-weight: 700;
            }}

            .bar-bg {{
                height: 10px;
                background: #eee7df;
                border-radius: 999px;
                overflow: hidden;
            }}

            .bar-fill {{
                height: 100%;
                background: #8C1515;
                border-radius: 999px;
            }}

            .section-title {{
                margin: 30px 0 16px;
                font-size: 24px;
            }}

            .conversation-card {{
                margin-bottom: 18px;
            }}

            .conversation-top {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 14px;
            }}

            .badge {{
                background: #f1e7e7;
                color: #8C1515;
                border-radius: 999px;
                padding: 7px 12px;
                font-size: 14px;
                font-weight: 800;
            }}

            .status {{
                border-radius: 999px;
                padding: 7px 12px;
                font-size: 13px;
                font-weight: 800;
            }}

            .good {{
                background: #e8f7ee;
                color: #157347;
            }}

            .bad {{
                background: #fdecec;
                color: #b42318;
            }}

            .mini-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
                margin: 18px 0;
            }}

            .mini-grid div {{
                background: #fafafa;
                border-radius: 14px;
                padding: 12px;
            }}

            .mini-grid span {{
                display: block;
                color: #6b7280;
                font-size: 12px;
                margin-bottom: 5px;
                text-transform: uppercase;
                font-weight: 700;
            }}

            details {{
                margin-top: 10px;
            }}

            summary {{
                cursor: pointer;
                font-weight: 800;
                color: #8C1515;
            }}

            pre {{
                white-space: pre-wrap;
                background: #f3f3f3;
                border-radius: 14px;
                padding: 16px;
                line-height: 1.45;
                margin-top: 12px;
                max-height: 360px;
                overflow: auto;
            }}

            @media (max-width: 900px) {{
                .stats, .grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>

    <body>
        <div class="page">
            <div class="hero">
                <div class="eyebrow">Retell AI + FastAPI + Webhooks</div>
                <h1>Stanford Freshman Voice Analytics</h1>
                <p>
                    A voice FAQ assistant for incoming Stanford students, paired with a backend dashboard that captures Retell webhook events, stores transcripts, and turns conversations into actionable product analytics.
                </p>
            </div>

            <div class="stats">
                <div class="stat">
                    <div class="stat-label">Total Calls</div>
                    <div class="stat-number">{total_calls}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Success Rate</div>
                    <div class="stat-number">{success_rate:.0f}%</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Total Cost</div>
                    <div class="stat-number">${total_cost:.2f}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Avg Duration</div>
                    <div class="stat-number">{avg_duration:.1f}s</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Top Topic</div>
                    <div class="stat-number" style="font-size:20px;">{most_asked_topic}</div>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <h2>📊 Most Asked Topics</h2>
                    {topic_rows}
                </div>

                <div class="card">
                    <h2>💡 Agent Improvement Insights</h2>
                    {''.join(f'<div class="insight">{insight}</div>' for insight in insights)}
                </div>
            </div>

            <h2 class="section-title">Recent Conversations</h2>
            {call_cards}
        </div>
    </body>
    </html>
    """

    return html