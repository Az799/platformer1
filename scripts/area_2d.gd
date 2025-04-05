extends Area2D

@onready var animation_player: AnimationPlayer = $"../AnimationPlayer"
@onready var label: Label = $"../../Player/Camera2D/Label"

func _on_body_entered(body):
	if body is CharacterBody2D and GlobalVar.i >= 11:
		print("Fox detected!")
		animation_player.play("movexd")
	else:
		label.text = str(GlobalVar.i) + "/11"
