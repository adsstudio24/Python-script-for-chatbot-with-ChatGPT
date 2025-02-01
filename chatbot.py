import openai
import os
from flask import Flask, request, jsonify

# 🔑 Введи свій API-ключ OpenAI тут або збережи у змінній середовища
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

app = Flask(__name__)

def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    """Відправляє запит у OpenAI API та отримує відповідь"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Помилка: {e}"

@app.route("/chat", methods=["POST"])
def chat():
    """Отримує повідомлення від користувача та відповідає через OpenAI API"""
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Повідомлення не повинно бути порожнім"}), 400
    
    response = chat_with_gpt(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
