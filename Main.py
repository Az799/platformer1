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


@application.route("/get_users_Liskahra", methods=["GET"])
def get_users():
    """Get all users and their scores"""
    try:
        cursor.execute("SELECT username, score FROM Liskahra")
        users = cursor.fetchall()
        return jsonify({"success": True, "users": users}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@application.route("/register_Liskahra", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    print(f"\n📝 Registration attempt: {data}")  # Debug

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = hash_password(password)

    try:
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


@application.route("/update_score_Liskahra", methods=["POST"])
def update_score():
    """Update user score"""
    data = request.get_json()
    print(f"\n🎯 Score update request: {data}")  # Debug

    if not data:
        print("❌ No JSON data received")
        return jsonify({"error": "No JSON data received"}), 400

    username = data.get("username")
    new_score = data.get("score")

    if not username or new_score is None:
        print("❌ Missing username or score")
        return jsonify({"error": "Both username and score are required"}), 400

    try:
        # Verify user exists first
        cursor.execute("SELECT username FROM Liskahra WHERE username = %s", (username,))
        if not cursor.fetchone():
            print(f"❌ User '{username}' not found in database")
            return jsonify({"error": "User not found"}), 404

        # Convert score to float to ensure proper storage/ po tom ig, ted ten server stoji za starou backoru
        score_value = int(new_score)

        # Update score
        cursor.execute(
            "UPDATE Liskahra SET score = %s WHERE username = %s",
            (score_value, username)
        )
        database.commit()

        # Verify update
        cursor.execute("SELECT score FROM Liskahra WHERE username = %s", (username,))
        updated_score = cursor.fetchone()["score"]

        print(f"✅ Updated '{username}' score to {updated_score}")
        return jsonify({
            "success": True,
            "message": "Score updated",
            "username": username,
            "new_score": updated_score
        }), 200

    except ValueError:
        print(f"❌ Invalid score value: {new_score}")
        return jsonify({"error": "Score must be a number"}), 400
    except mysql.connector.Error as err:
        database.rollback()
        print(f"❌ Database error: {err}")
        return jsonify({"error": str(err)}), 500
    except Exception as err:
        database.rollback()
        print(f"❌ Unexpected error: {err}")
        return jsonify({"error": str(err)}), 500


@application.route("/get_leaderboard", methods=["GET"])
def get_leaderboard():
    """Get top 10 scores"""
    try:
        cursor.execute("""
            SELECT username, score 
            FROM Liskahra 
            WHERE score > 0
            ORDER BY score ASC 
            LIMIT 10
        """)
        leaderboard = cursor.fetchall()
        return jsonify({
            "success": True,
            "leaderboard": leaderboard
        }), 200
    except mysql.connector.Error as err:
        print(f"❌ Leaderboard error: {err}")
        return jsonify({"error": str(err)}), 500


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