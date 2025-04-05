extends CharacterBody2D
@onready var label_2: Label = $Camera2D/Label2

var ROLLSPEED = 0
const SPEED = 130.0
const JUMP_VELOCITY = -300.0
var can_move = 1 #y/n
var x = 1 #y/n
@onready var label: Label = $Camera2D/Label


@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _physics_process(delta: float) -> void:
	var direction = Input.get_axis("A","D") * can_move
	
	# Add the gravity.
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Handle jump.
	if Input.is_action_just_pressed("SPACEBAR") and is_on_floor():
		velocity.y = JUMP_VELOCITY
		
	# Roll xd + idle not idleing fix
	if Input.is_action_pressed("SHIFT") and not direction == 0:
		animated_sprite.play("roll")
		ROLLSPEED = 50
	else:
		ROLLSPEED = 0
	
	#Movement
	if direction:
		velocity.x = direction * (SPEED + ROLLSPEED) 
	else:
		velocity.x = 0
		
	if direction == 0:
		if is_on_floor():
			animated_sprite.play("idle")
		
	
	if direction < 0 and not Input.is_action_pressed("SHIFT"):
		animated_sprite.play("run")
		
	if direction > 0 and not Input.is_action_pressed("SHIFT"):
		animated_sprite.play("run")
	
	#left/right looking
	if direction < 0:
		animated_sprite.flip_h = true
	if direction > 0:
		animated_sprite.flip_h = false
	
	#death trigger
	if can_move == 0:
		x = 0 #turns off jump animationD
		animated_sprite.play("death")
		collision_layer = 0 #fall thru terrain + to pod tim taky, ale docela to mluvi samo za sebe
		collision_mask = 0
		
	#fall
	if not is_on_floor() and not direction == 0 and x == 1: # x turns off jump animation if ded
		if velocity.y > 100:
			animated_sprite.play("fall")
	
		if velocity.y < 100: 
			animated_sprite.play("jump")
	
	#druhej jump protoze proste pri normalni chuzi to nic nedela *sipka nahoru*
	if direction == 0 and not is_on_floor() and x == 1: # x turns off jump animation if ded
		if velocity.y > 100:
			animated_sprite.play("fall")
	
		if velocity.y < 100: 
			animated_sprite.play("jump")
	
	if GlobalVar.logedin:
		label_2.text = str(GlobalVar.username)
	move_and_slide()

	if Input.is_action_pressed("ESCAPE"):
		get_tree().change_scene_to_file("res://scenes/menu.tscn")
