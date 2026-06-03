from flask import Flask, render_template, request, jsonify 
#Flask-web framework which runs my server
#converts Python dictionaries into JSON responses sent back to browser
import groq
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv
#CORS — allows your frontend and backend to communicate even if they're on different ports
import os

app = Flask(__name__)
CORS(app)

# ── AI client testing 1.0 ────────────────────

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
chat_history = [] #a list that stores the conversation 

# ──────────────────────────────────────
#.    SITES dictionary
# ──────────────────────────────────────

SITES = {
    "youtube":          "https://www.youtube.com",
    "wikipedia":        "https://www.wikipedia.com",
    "google":           "https://www.google.com",
    "github":           "https://www.github.com",
    "twitter":          "https://www.twitter.com",
    "reddit":           "https://www.reddit.com",
    "netflix":          "https://www.netflix.com",
    "spotify":          "https://www.spotify.com",
    "amazon prime":     "https://www.primevideo.com",
    "disney plus":      "https://www.disneyplus.com",
    "gmail":            "https://mail.google.com",
    "google drive":     "https://drive.google.com",
    "google docs":      "https://docs.google.com",
    "google maps":      "https://maps.google.com",
    "google translate": "https://translate.google.com",
    "instagram":        "https://www.instagram.com",
    "facebook":         "https://www.facebook.com",
    "linkedin":         "https://www.linkedin.com",
    "tiktok":           "https://www.tiktok.com",
    "discord":          "https://www.discord.com",
    "whatsapp":         "https://web.whatsapp.com",
    "telegram":         "https://web.telegram.org",
    "twitch":           "https://www.twitch.tv",
    "stack overflow":   "https://www.stackoverflow.com",
    "w3schools":        "https://www.w3schools.com",
    "chat gpt":         "https://chat.openai.com",
    "notion":           "https://www.notion.so",
    "trello":           "https://www.trello.com",
    "canva":            "https://www.canva.com",
    "figma":            "https://www.figma.com",
    "coursera":         "https://www.coursera.org",
    "udemy":            "https://www.udemy.com",
    "khan academy":     "https://www.khanacademy.org",
    "amazon":           "https://www.amazon.com",
    "paypal":           "https://www.paypal.com",
    "bbc":              "https://www.bbc.com",
    "cnn":              "https://www.cnn.com",
}
# ──────────────────────────────────────
# Load any custom sites saved by the user
# ──────────────────────────────────────

CUSTOM_SITES_FILE = "custom_sites.txt"
if os.path.exists(CUSTOM_SITES_FILE):
    with open(CUSTOM_SITES_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",", 1)
            if len(parts) == 2:
                SITES[parts[0].lower()] = parts[1]

# ──────────────────────────────────────
# Routes
# ──────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"type": "error", "reply": "Empty query received."})

    query_lower = query.lower()
# ──────────────────────────────────────
# Reset chat
# ──────────────────────────────────────
    if "reset chat" in query_lower:
        chat_history = []
        return jsonify({"type": "system", "reply": "Chat history cleared, sir."})

# ──────────────────────────────────────
# open website
# ──────────────────────────────────────
    for site_name, site_url in SITES.items():
        if f"open {site_name}" in query_lower:
            return jsonify({
                "type": "open_url",
                "reply": f"Opening {site_name}, sir.",
                "url": site_url
            })
# ──────────────────────────────────────
# Time
# ──────────────────────────────────────
    import datetime
    if "the time" in query_lower:
        now = datetime.datetime.now()
        hour = now.strftime("%I").lstrip("0") or "12"
        minute = now.strftime("%M")
        period = now.strftime("%p")
        return jsonify({"type": "reply", "reply": f"Sir, the time is {hour}:{minute} {period}."})
# ──────────────────────────────────────
# date
# ──────────────────────────────────────
    if "the date" in query_lower:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return jsonify({"type": "reply", "reply": f"Today is {today}, sir."})
# ──────────────────────────────────────
# save new website
# ──────────────────────────────────────
    if "remember website" in query_lower:
        return jsonify({
            "type": "remember_website",
            "reply": "Sure! What should I call this website?"
        })

    # ── AI one-shot task ────────────────────────────────────
    if "using artificial intelligence" in query_lower:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": query}],
                temperature=0.7,
                max_tokens=1024,
            )
            result = response.choices[0].message.content.strip()

            # Save to file
            os.makedirs("GROQ", exist_ok=True)
            parts = query.split("intelligence")
            raw = "".join(parts[1:]).strip() if len(parts) > 1 else query[:40].strip()
            safe = "".join(c for c in raw if c.isalnum() or c in " _-").strip() or "response"
            with open(f"GROQ/{safe}.txt", "w") as f:
                f.write(f"Prompt: {query}\n{'*'*40}\n\n{result}")

            return jsonify({"type": "reply", "reply": result})
        except Exception as e:
            return jsonify({"type": "error", "reply": f"AI error: {str(e)}"})

    # ── Conversational chat ─────────────────────────────────
    try:
        chat_history.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a witty and highly intelligent AI assistant "
                        "inspired by Iron Man. Be concise, clever, and spoken-word "
                        "friendly — no markdown, no bullet points, just natural speech. "
                        "Address the user as 'sir' occasionally."
                    ),
                },
                *chat_history,
            ],
            temperature=0.7,
            max_tokens=256,
        )

        reply = response.choices[0].message.content.strip()
        chat_history.append({"role": "assistant", "content": reply})

        # Keep history manageable (last 20 messages)
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]

        return jsonify({"type": "reply", "reply": reply})

    except groq.AuthenticationError:
        return jsonify({"type": "error", "reply": "Authentication failed. Please check your API key."})
    except groq.RateLimitError:
        return jsonify({"type": "error", "reply": "Rate limit reached. Please wait a moment."})
    except Exception as e:
        return jsonify({"type": "error", "reply": f"Error: {str(e)}"})


@app.route("/save-site", methods=["POST"])
def save_site():
    data = request.get_json()
    name = data.get("name", "").strip().lower()
    url = data.get("url", "").strip()

    if not name or not url:
        return jsonify({"success": False, "reply": "Name or URL missing."})

    if not url.startswith("http"):
        url = "https://" + url

    SITES[name] = url

    with open(CUSTOM_SITES_FILE, "a") as f:
        f.write(f"{name},{url}\n")

    return jsonify({
        "success": True,
        "reply": f"Got it, sir. I'll open {name} whenever you ask."
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
