from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename
import os

# --------- UTILS ---------
from utils.bmi_calculator import calculate_bmi
from utils.diet_planner import generate_diet
from utils.workout_planner import generate_workout
from utils.ai_tip import generate_fitness_tip
from utils.chatbot import ask_bot
from utils.food_analyzer import analyze_food_image

# --------- STREAK SYSTEM ---------
from database.streak_db import create_streak_table
from utils.streak_manager import update_streak, get_streak_data

# --------- APP INIT ---------
app = Flask(__name__)
app.secret_key = "ai-fitness-secret-key"

# --------- CREATE STREAK DB ---------
create_streak_table()

# --------- CONFIG ---------
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= GENERATE PLAN =================
@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    age = request.form.get("age")
    gender = request.form.get("gender")

    height = float(request.form.get("height"))
    weight = float(request.form.get("weight"))

    goal = request.form.get("goal")
    custom_goal = request.form.get("custom_goal")

    diet_type = request.form.get("diet")
    budget = request.form.get("budget")

    if goal == "custom" and custom_goal:
        goal = custom_goal

    bmi = calculate_bmi(weight, height)

    # ---- DIET PLAN ----
    diet = generate_diet(diet_type, budget) or []

    # ---- WORKOUT PLAN ----
    workout = generate_workout(goal, bmi) or []

    tip = generate_fitness_tip(goal)

    return render_template(
        "result.html",
        age=age,
        gender=gender,
        bmi=round(bmi, 2),
        goal=goal,
        diet=diet,
        workout=workout,
        tip=tip
    )


# ================= STREAK PAGE =================
@app.route("/streak")
def streak_page():
    streak, best, points, level = get_streak_data()
    return render_template(
        "streak.html",
        streak=streak,
        best=best,
        points=points,
        level=level
    )


@app.route("/complete-today", methods=["POST"])
def complete_today():
    update_streak()
    return redirect("/streak")


# ================= CHAT =================
@app.route("/chat", methods=["GET", "POST"])
def chat():

    if "chat_history" not in session:
        session["chat_history"] = []

    answer = None

    if request.method == "POST":
        question = request.form.get("chat_question")
        answer = ask_bot(question, session["chat_history"])

        session["chat_history"].append({"role": "user", "content": question})
        session["chat_history"].append({"role": "assistant", "content": answer})
        session.modified = True

    return render_template(
        "chat.html",
        chat_answer=answer,
        chat_history=session["chat_history"]
    )


# ================= FOOD ANALYZER =================
@app.route("/upload-food")
def upload_food_redirect():
    return render_template("food_analyzer.html")


@app.route("/analyze-food", methods=["POST"])
def analyze_food():

    if "food_image" not in request.files:
        return render_template("food_analyzer.html", analysis={"error": "No file uploaded"})

    file = request.files["food_image"]

    if file.filename == "":
        return render_template("food_analyzer.html", analysis={"error": "No file selected"})

    if not allowed_file(file.filename):
        return render_template("food_analyzer.html", analysis={"error": "Invalid file type"})

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        analysis = analyze_food_image(file_path)
    except Exception as e:
        analysis = {"error": str(e)}

    uploaded_file_url = url_for("static", filename=f"uploads/{filename}")

    return render_template(
        "food_analyzer.html",
        analysis=analysis,
        uploaded_file_url=uploaded_file_url
    )


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)