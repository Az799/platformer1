# 🎮 Game Project with Flask Backend & Godot Frontend

![Godot Engine](https://img.shields.io/badge/GODOT-%23FFFFFF.svg?style=for-the-badge&logo=godot-engine)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## ⚠️ Prerequisites Warning

**You must have these installed before using this repository:**
- [Godot Engine](https://godotengine.org/download) (Latest stable version)
- [PyCharm Community](https://www.jetbrains.com/pycharm/download/) (or any Python IDE)

> ❗ Without these tools, the project **will not work** properly.


## 📂 Project Structure
```
your-game/
│
├── godot-project/          # All Godot-related files
│   ├── assets/             # Sprites, sounds, etc.
│   ├── scenes/             # Godot scene files (.tscn)
│   ├── scripts/            # GDScript files (.gd)
│   ├── project.godot       # Godot project file
│   ├── .gitattributes      # Godot-specific git config
│   └── .gitignore          # Godot-specific ignores
│
├── flask-backend/          # Python backend
│   ├── Main.py             
│   ├── .idea               # Virtual environment
│   └── .venv               # IDE config
│
└── README.md               # Updated documentation
```

## ⚠️ Requirements

| Tool | Purpose | Download |
|------|---------|----------|
| Godot 4.2+ | Game development | [godotengine.org](https://godotengine.org/download) |
| Python 3.10+ | Backend server | [python.org](https://www.python.org/downloads/) |
| PyCharm (Recommended) | Python IDE | [jetbrains.com](https://www.jetbrains.com/pycharm/) |

## 🚀 Setup Guide
put everything but the `Main.py` into a folder named "platformer1" <br>
with `Main.py` create a flask server

### Godot Client
1. Open `"path/platformer1"` in Godot Editor
2. Run the main scene (F5)

### Flask Server
```bash

pip install flask
pip install bcrypt
pip install mysql-connector-python
```
# On Windows:
```
.venv\Scripts\activate
```
