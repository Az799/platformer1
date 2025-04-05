extends Control
@onready var username: LineEdit = $VBoxContainer/LineEdit
@onready var password: LineEdit = $VBoxContainer/LineEdit2
@onready var label: Label = $VBoxContainer/Label
@onready var http_request: HTTPRequest = $VBoxContainer/HTTPRequest
var headers = ["Content-Type: application/json"]


func _on_back_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/menu.tscn")


func _on_register_pressed() -> void:
	if password.text == "" or username.text == "":
		label.text = "vyplnte udaje?"
		return
	var formdata = JSON.stringify({"username":username.text,"password":password.text})
	print(formdata)
	http_request.request("http://127.0.0.1:5000/register_Liskahra",headers,HTTPClient.METHOD_POST,formdata)

func _on_http_request_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	print("ahoj")
	
	label.text = "uzivatel registzrovan"
