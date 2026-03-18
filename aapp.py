from flask import Flask, request, jsonify, render_template, redirect, session
import psycopg2
import bcrypt
import secrets
import os

from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "ReplaceWithAStrongSecretKey123!"  # ضع مفتاح قوي هنا
reset_tokens = {}


# ================== SQL Server Connection ==================

DATABASE_URL = "postgresql://admin:102CVlotsiGnGZ7cvQExRmeeqDxRyySM@dpg-d6tctpfpm1nc739g9a20-a.oregon-postgres.render.com/appointmentsdb_wz8r"

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
cur = conn.cursor()

# cur.execute("""
# CREATE TABLE signup2 (
#     "Username" VARCHAR(50) PRIMARY KEY,
#     "Email" VARCHAR(100) UNIQUE,
#     "FirstName" VARCHAR(50),
#     "LastName" VARCHAR(50),
#     "PasswordHash" TEXT,
#     "PhoneNumber" VARCHAR(20) UNIQUE,
#     "IsEmailVerified" INTEGER
# );
# """)

conn.commit()
cur.close()
conn.close()

print("Table created successfully!")

# ================== Login API ==================
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "")

    if not username or not password:
        return jsonify({"ok": False, "message": "Please enter your username and password."}), 400

    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
            SELECT "Username", "PasswordHash"
             FROM signup2
              WHERE "Username" = %s
              """, (username,))
            user = cur.fetchone()

        if not user:
            return jsonify({"ok": False, "message": "Incorrect username or password"}), 401

        stored_hash = user[1]
        if isinstance(stored_hash, memoryview):
            stored_hash = stored_hash.tobytes().decode("utf-8", errors="ignore")
        elif isinstance(stored_hash, (bytes, bytearray)):
            stored_hash = bytes(stored_hash).decode("utf-8", errors="ignore")
        else:
            stored_hash = str(stored_hash)

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return jsonify({"ok": False, "message": "Incorrect username or password"}), 401

        # الموحد: session["username"]
        session["username"] = user[0]
        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "message": f"Server error: {str(e)}"}), 500

# ================== Signup API ==================
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    firstName = (data.get("firstName") or "").strip()
    lastName = (data.get("lastName") or "").strip()
    phoneNumber = (data.get("phoneNumber") or "").strip()
    password = (data.get("password") or "")
    password2 = (data.get("password2") or "")

    if not all([username, email, firstName, lastName, phoneNumber, password, password2]):
        return jsonify({"ok": False, "message": "Please fill in all fields"}), 400

    if password != password2:
        return jsonify({"ok": False, "message": "❌ Passwords do not match"}), 400

    try:
        with get_conn() as conn:
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM signup2 WHERE \"Username\" = %s", (username,))  
            if cur.fetchone():
              return jsonify({"ok": False, "message": "The username already exists"}), 409

            cur.execute("SELECT 1 FROM signup2 WHERE \"Email\" = %s", (email,))
            if cur.fetchone():
                return jsonify({"ok": False, "message": "Email already in use"}), 409

            cur.execute("SELECT 1 FROM signup2 WHERE \"PhoneNumber\" = %s", (phoneNumber,))
            if cur.fetchone():
                return jsonify({"ok": False, "message":"The phone number is already in use."}), 409

            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            cur.execute("""
                INSERT INTO dbo.signup2
                (Username, Email, FirstName, LastName, PasswordHash, PhoneNumber, IsEmailVerified)
                VALUES (%s, %s, %s, %s, %s, %s, 0)
            """, (username, email, firstName, lastName, hashed, phoneNumber))
            conn.commit()

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "message": f"Server error: {str(e)}"}), 500

# ================== Pages ==================
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/page2")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template("page2.html", username=session["username"])

@app.route("/profile")
def account():
    username = session.get("username", "Unknown User")
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT Email, FirstName, LastName, PhoneNumber
                FROM dbo.signup2
                WHERE "Username" = %s
            """, (username,))
            user = cur.fetchone()
            if user:
                email = user.Email
                first_name = user.FirstName
                last_name = user.LastName
                phone = user.PhoneNumber
            else:
                email = "Not found"
                first_name = last_name = phone = ""
    except Exception as e:
        email = "Error"
        first_name = last_name = phone =  ""

    return render_template(
        "profile.html",
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
    )

@app.route("/edit_profile_ajax", methods=["POST"])
def edit_profile_ajax():
    if "username" not in session:
        return jsonify({"ok": False, "message": "Not logged in"}), 401

    username = session["username"]
    data = request.get_json()
    new_first_name = data.get("first_name", "").strip()
    new_phone = data.get("phone", "").strip()

    if not new_first_name or not new_phone:
        return jsonify({"ok": False, "message": "Please fill all fields"}), 400

    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
             UPDATE signup2
             SET "FirstName" = %s, "PhoneNumber" = %s
              WHERE "Username" = %s
             """, (new_first_name, new_phone, username))
            conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})


# ================== Forgot Password ==================
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    reset_link_display = None  # رابط مؤقت للعرض
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        if email:
            with get_conn() as conn:
                cur = conn.cursor()
                cur.execute("SELECT \"Username\" FROM signup2 WHERE \"Email\" = %s", (email,))
                user = cur.fetchone()
                if user:
                    token = secrets.token_urlsafe(16)
                    # تخزين التوكن مع وقت انتهاء صلاحية
                    reset_tokens[token] = {"email": email, "expires": datetime.now() + timedelta(minutes=15)}
                    reset_link = f"http://127.0.0.1:5001/reset_password/{token}"
                    reset_link_display = reset_link  # للعرض مباشرة في الصفحة
    return render_template("forgot_password.html", reset_link=reset_link_display)


# ================== Reset Password ==================
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    data = reset_tokens.get(token)
    if not data or data["expires"] < datetime.now():
        return "Token expired or invalid", 400

    if request.method == "POST":
        new_password = request.form.get("password", "").strip()
        if new_password:
            hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            email = data["email"]
            with get_conn() as conn:
                cur = conn.cursor()
                cur.execute("UPDATE signup2 SET \"PasswordHash\"=%s WHERE \"Email\"=%s", (hashed, email))
                conn.commit()
            reset_tokens.pop(token)  # حذف التوكن بعد الاستخدام
            return """
            <script>
                alert("Password reset successfully!");
                window.location.href = "/";
            </script>
            """
    return render_template("reset_password.html", token=token)

# ================== Pages for products ==================
@app.route("/phones")
def phones():
    if "username" not in session:
        return redirect("/")
    return render_template("phones.html", username=session["username"])

@app.route("/headphones")
def headphones():
    if "username" not in session:
        return redirect("/")
    return render_template("headphones.html", username=session["username"])

@app.route("/laptops")
def laptops():
    if "username" not in session:
        return redirect("/")
    return render_template("laptops.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5001, debug=True)