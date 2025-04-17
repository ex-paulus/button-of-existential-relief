
from flask import Flask, render_template, jsonify, request
import requests
import random

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
