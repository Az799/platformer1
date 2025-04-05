extends Area2D

var x = 1
var y = 1
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D



func _on_body_entered(body: Node2D) -> void:
	print("I BITE >:( 3")
	queue_free() #odebere brouka
	if body is CharacterBody2D:
		body.can_move = 0
		if x == 1:
			body.velocity.y = -300
			x = 0
	print("you died")
	await get_tree().create_timer(1.5).timeout
	y = 0
	
	if y == 0:
		get_tree().reload_current_scene()


func _on_ready() -> void:
	animated_sprite.play("default")
	animated_sprite.flip_h = true
