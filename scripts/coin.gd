extends Area2D

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var label: Label = $"../../Player/Camera2D/Label"

func _ready() -> void:
	animated_sprite.animation_finished.connect(on_konec)

func _on_body_entered(body: Node2D) -> void:
	GlobalVar.i += 1
	label.text = str(GlobalVar.i) 
	animated_sprite.play("despawn")

func on_konec() -> void:
	if animated_sprite.animation == "despawn":
		queue_free()
