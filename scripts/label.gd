extends Label


func _on_area_2d_body_entered(body: Node2D) -> void:
	queue_free()
