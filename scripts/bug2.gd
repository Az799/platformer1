extends Area2D


@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var label: Label = $"../../Player/Camera2D/Label"


#func _on_body_entered(body: Node2D) -> void:
#	print("no bug :< 2")
#	queue_free() #odebere brouka
	

func _on_ready() -> void:
	animated_sprite.play("default")
	animated_sprite.flip_h = false
