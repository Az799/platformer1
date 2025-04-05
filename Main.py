import bcrypt
import mysql.connector
from flask import Flask, request, jsonify


# Initialize Flask app
application = Flask(__name__)


# Database connection with debug information
try:
    database = mysql.connector.connect(
        host="dbs.spskladno.cz",
        user="student20",
        password="spsnet",
        database="vyuka20"
    )
    cursor = database.cursor(dictionary=True)

    # Debug connection info
    print("✅ Successfully connected to MySQL!")
    print(f"MySQL Server Version: {database.get_server_version()}")
    cursor.execute("SELECT DATABASE()")
    print(f"Current Database: {cursor.fetchone()['DATABASE()']}")

except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    exit(1)


# Hash password function
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


# Verify password function
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# ... after database connection ...
try:
    cursor.execute("""
        SELECT update_priv 
        FROM mysql.db 
        WHERE Db = 'vyuka20' AND User = 'student20'
    """)
    print("\n🔐 Update Permissions:", cursor.fetchone())
except Exception as e:
    print("❌ Permission check failed:", e)

try:
    cursor.execute("SHOW GRANTS FOR CURRENT_USER")
    print("\n🔐 Database Permissions:")
    for grant in cursor.fetchall():
        print(grant["Grants"])
except Exception as e:
    print(f"❌ Permission check failed: {e}")


@application.route("/register_Liskahra", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    print(f"\n📝 Registration attempt: {data}")  # Debug

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # 🔍 Check if user already exists
        cursor.execute("SELECT username FROM Liskahra WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"⚠️ User '{username}' already exists")
            return jsonify({"error": "User already exists"}), 409  # Conflict

        # ✅ Register new user
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO Liskahra (username, password, score) VALUES (%s, %s, 0)",
            (username, hashed_password)
        )
        database.commit()
        print(f"✅ User '{username}' registered successfully")
        return jsonify({
            "success": True,
            "message": "User registered",
            "username": username
        }), 201

    except mysql.connector.Error as err:
        print(f"❌ Registration error: {err}")
        return jsonify({"error": str(err)}), 500



@application.route("/login_Liskahra", methods=["POST"])
def login():
    """User login"""
    data = request.get_json()
    print(f"\n🔑 Login attempt: {data}")  # Debug

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        cursor.execute(
            "SELECT username, password, score FROM Liskahra WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()

        if result is None:
            print(f"❌ User '{username}' not found")
            return jsonify({"error": "User not found"}), 404

        if check_password(password, result["password"]):
            print(f"✅ User '{username}' logged in successfully")
            return jsonify({
                "success": True,
                "message": "Login successful",
                "username": username,
                "score": result["score"]
            }), 200
        else:
            print(f"❌ Incorrect password for '{username}'")
            return jsonify({"error": "Incorrect password"}), 403
    except mysql.connector.Error as err:
        print(f"❌ Login error: {err}")
        return jsonify({"error": str(err)}), 500


@application.before_request
def log_request():
    print(f"\n📨 Incoming {request.method} request to {request.path}")
    print("Headers:", dict(request.headers))
    print("Body:", request.get_data(as_text=True))


@application.route("/update_score_Liskahra", methods=["POST"])
def update_score():
    data = request.get_json()
    print(f"\n🎯 Score update request: {data}")

    try:
        username = data['username']
        new_score = float(data['score'])

        # Get fresh connection
        db = mysql.connector.connect(
            host="dbs.spskladno.cz",
            user="student20",
            password="spsnet",
            database="vyuka20"
        )
        cursor = db.cursor(dictionary=True)

        # 1. Get current score
        cursor.execute("SELECT score FROM Liskahra WHERE username = %s", (username,))
        current = cursor.fetchone()

        if not current:
            db.close()
            return jsonify({"error": "User not found"}), 404

        current_score = current['score'] or float('inf')  # Handle NULL as infinite

        # 2. Only update if new score is better (lower time)
        if new_score < current_score:
            cursor.execute(
                "UPDATE Liskahra SET score = %s WHERE username = %s",
                (new_score, username)
            )
            db.commit()
            message = "New high score!"
        else:
            message = "Score not improved"

        # 3. Return verification
        cursor.execute("SELECT score FROM Liskahra WHERE username = %s", (username,))
        result = cursor.fetchone()
        db.close()

        return jsonify({
            "success": True,
            "message": message,
            "new_score": result['score'],
            "was_updated": new_score < current_score
        }), 200

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Print table structure at startup
    try:
        cursor.execute("DESCRIBE Liskahra")
        print("\n📊 Table Structure:")
        for column in cursor.fetchall():
            print(f"{column['Field']}: {column['Type']}")
    except mysql.connector.Error as err:
        print(f"❌ Failed to check table structure: {err}")

    # Start the Flask app
    print("\n🚀 Starting Flask server...")
    application.run(host='0.0.0.0', port=5000, debug=True)