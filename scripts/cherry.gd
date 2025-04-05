extends Area2D

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var label: Label = $"../Player/Camera2D/Label"
@onready var label_3: Label = $"../Player/Camera2D/Label3"
@onready var http_request: HTTPRequest = HTTPRequest.new()

var start_time: int

func _ready() -> void:
	add_child(http_request)
	http_request.request_completed.connect(_on_http_request_completed)
	http_request.timeout = 5  # Set 5-second timeout
	start_time = Time.get_ticks_msec()

func _on_body_entered(body: Node2D) -> void:
	animated_sprite.play("Collect")
	
	# Calculate elapsed time
	var elapsed_time = (Time.get_ticks_msec() - start_time) / 1000.0
	var rounded_time = snapped(elapsed_time, 0.1) #0.1 = zaokhroulit na desetiny
	
	print("\nGoodgame")
	print("Time taken to collect the cherry: " + str(rounded_time) + " seconds")
	label_3.text = "Time taken to collect the cherry: " + str(rounded_time) + " seconds"
	label.text = "Yatta!"
	
	# Save the score to global variable
	GlobalVar.score = rounded_time
	
	# Send score to server if logged in
	if GlobalVar.logedin:
		print("User is logged in, attempting to send score...")
		send_score_to_server(rounded_time)
	else:
		print("User not logged in, score not sent to server")

func send_score_to_server(score: float):
	var url = "http://127.0.0.1:5000/update_score_Liskahra"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({
		"username": GlobalVar.username,
		"score": score
	})
	
	print("\nSending score to server:")
	print("URL: ", url)
	print("Headers: ", headers)
	print("Body: ", body)
	
	# Cancel any pending request first
	if http_request.get_http_client_status() != HTTPClient.STATUS_DISCONNECTED:
		http_request.cancel_request()
	
	var error = http_request.request(url, headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		push_error("HTTP request failed to start. Error code: ", error)
		print("❌ Failed to send request. Check server URL and network connection.")
	else:
		print("✅ Request sent successfully")

func _on_http_request_completed(result, response_code, headers, body):
	print("\nFull response:")
	print("Result:", result)
	print("Code:", response_code)
	print("Headers:", headers)
	print("Body:", body.get_string_from_utf8())
	
	if result != HTTPRequest.RESULT_SUCCESS:
		print("❌ Request failed completely")
		return
		
	var json = JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		var response = json.get_data()
		
		match response_code:
			200:
				if response.get("was_updated", false):
					print("✅ New high score saved:", response["new_score"])
					label.text = "New record: " + str(response["new_score"])
				else:
					print("ℹ️ Score not improved")
					label.text = "Good try! (Best: " + str(response["new_score"]) + ")"
			404:
				print("❌ Endpoint not found")
			_:
				print("❌ Unexpected response")

func _on_animated_sprite_2d_animation_finished() -> void:
	if animated_sprite.animation == "Collect":
		queue_free()
