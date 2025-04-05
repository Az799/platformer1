extends Area2D
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var timer: Timer = $Timer
const JUMP_VELOCITY = -300.0
var x = 1 #y/n

func _on_body_entered(funguj: Node2D) -> void:
	if funguj is CharacterBody2D:
		funguj.can_move = 0
		if x == 1:
			funguj.velocity.y = -300
			x = 0
	
	print("you died")
	GlobalVar.i = 0
	timer.start()
	

	
func _on_timer_timeout() -> void:
	get_tree().reload_current_scene()
	
