
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os
import json
import requests
import random

app = Flask(__name__)

CLICK_FILE = 'data/clicks.json'
EVENT_LOG = 'data/events.json'

backup_advice = {
    "normal": [
        "Налий собі чаю й зроби глибокий вдих.",
        "Просто почни. Не ідеально, але почни.",
        "Кнопка натиснута — значить, вже не все дарма."
    ],
    "sos": [
        "Чувак, та без тебе ця планета перекинеться! Видихни і назад у гру.",
        "Воно всім важко. Але саме ти — головний танк у цьому рейді.",
        "Ніхто не знає, що робить. Просто прикинься впевненим — і вперед.",
        "Кофеїн, музика і твій характер — цього вистачить, щоб вистояти.",
        "Світ горить. Але поки ти тримаєшся — ще не все втрачено.",
        "Ти вже дійшов сюди. Це більше, ніж робить більшість. Поважай це.",
        "Пофіг, що не ідеально. Ти живий, і це вже win.",
        "Це фігня. Ти сильніший. Ще пару годин — і вже кращий горизонт.",
        "Ти не зламаний. Просто світ кривий. Ти — ок.",
        "Ця кнопка — сигнал. І ти вже його подав. А тепер — дихай."
        "Згадай Чувака із 'Великого Лебовського': він взагалі не парився!"
    ],
    "good": [
        "Поділись добрим словом з кимось сьогодні.",
        "Спробуй зробити комусь день. Навіть просто 'дякую' — магія.",
        "Твоя енергія зараз — як маленьке сонце. Світи далі."
    ],
    "smoke": [
        "Ти взагалі молодець, що натиснув цю кнопку. Серйозно.",
        "Все трохи тліє — але ти ще в грі. І це вже круто.",
        "Нічого не вирішуй. Просто посиди. І видихни.",
        "Натискання цієї кнопки вже краще за багато інших справ."
    ]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-advice")
def get_advice():
    mode = request.args.get("mode", "normal")
    print(f"[DEBUG] Режим: {mode}")

    try:
        if mode == "normal":
            response = requests.get("https://api.adviceslip.com/advice", timeout=5)
            advice = response.json()["slip"]["advice"]

        elif mode == "sos":
            advice = random.choice(backup_advice["sos"])

        elif mode == "good":
            response = requests.get("https://www.boredapi.com/api/activity", timeout=5)
            advice = "Спробуй: " + response.json()["activity"]

        elif mode == "smoke":
            advice = random.choice(backup_advice["smoke"])

        else:
            advice = random.choice(backup_advice["normal"])

    except Exception as e:
        print(f"[ERROR] API-запит не вдався: {e}")
        advice = random.choice(backup_advice.get(mode, backup_advice["normal"]))

    return jsonify({"advice": advice})

def read_clicks():
    if not os.path.exists(CLICK_FILE):
        return 0
    with open(CLICK_FILE, 'r') as f:
        return json.load(f).get('count', 0)

def write_clicks(count):
    with open(CLICK_FILE, 'w') as f:
        json.dump({'count': count}, f)

def log_event(mode):
    event = {
        'timestamp': datetime.utcnow().isoformat(),
        'mode': mode
    }
    if not os.path.exists(EVENT_LOG):
        events = []
    else:
        with open(EVENT_LOG, 'r') as f:
            events = json.load(f)
    events.append(event)
    with open(EVENT_LOG, 'w') as f:
        json.dump(events, f, indent=2)

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    mode = data.get('mode', 'unknown')
    count = read_clicks() + 1
    write_clicks(count)
    log_event(mode)
    return jsonify({'status': 'ok', 'count': count})

@app.route('/stats')
def stats():
    count = read_clicks()
    return jsonify({'clicks': count})

if __name__ == "__main__":
    app.run(debug=True)