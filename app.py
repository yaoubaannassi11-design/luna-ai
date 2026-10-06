import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

api_key = os.environ.get("CODECRAFT_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://codecraftapi.com/v1"
)

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Luna AI</title>
<style>
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f5f5f7;
}
.header {
    background: #111827;
    color: white;
    padding: 18px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}
.chat {
    height: calc(100vh - 130px);
    overflow-y: auto;
    padding: 15px;
}
.message {
    padding: 12px 15px;
    margin: 10px 0;
    border-radius: 16px;
    max-width: 85%;
    line-height: 1.5;
    white-space: pre-wrap;
}
.user {
    background: #2563eb;
    color: white;
    margin-left: auto;
}
.bot {
    background: white;
    color: #111;
}
.input-area {
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;
    padding: 10px;
    background: white;
    box-sizing: border-box;
}
input {
    flex: 1;
    padding: 13px;
    border: 1px solid #ddd;
    border-radius: 25px;
    font-size: 16px;
}
button {
    margin-left: 8px;
    padding: 13px 18px;
    border: none;
    border-radius: 25px;
    background: #2563eb;
    color: white;
    font-weight: bold;
}
</style>
</head>

<body>

<div class="header">🌙 Luna AI</div>

<div id="chat" class="chat">
    <div class="message bot">
        Bonjour 👋 Je suis Luna AI, propulsé par GPT-5.6 Luna.
    </div>
</div>

<div class="input-area">
    <input id="message" placeholder="Écris ton message..." 
           onkeydown="if(event.key==='Enter') envoyer()">
    <button onclick="envoyer()">Envoyer</button>
</div>

<script>
let historique = [];

async function envoyer() {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) return;

    ajouterMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                history: historique
            })
        });

        const data = await response.json();

        if (data.reply) {
            ajouterMessage(data.reply, "bot");

            historique.push({
                role: "user",
                content: message
            });

            historique.push({
                role: "assistant",
                content: data.reply
            });
        } else {
            ajouterMessage("Une erreur est survenue.", "bot");
        }

    } catch (error) {
        ajouterMessage("Impossible de contacter Luna AI.", "bot");
    }
}

function ajouterMessage(text, type) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");

    div.className = "message " + type;
    div.textContent = text;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")
    history = data.get
