extends HTTPRequest

@onready var http = $"../HTTPRequest"

func _ready():
	var headers = ["Content-Type: application/json"]
	http.request_completed.connect(_get_table)
	http.request("http://127.0.0.1:5000/get_Liskahra", headers)
	print("connected")


func _get_table(result, response_code, headers, body):
	var json = JSON.parse_string(body.get_string_from_utf8())
