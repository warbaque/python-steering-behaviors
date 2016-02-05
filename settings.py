import sfml as sf


# STATIC VALUES

TIME_PER_UPDATE = sf.seconds(1/60)

WIDTH = 1280
HEIGHT = 720
CELL_SIZE = 60

ENTITY_SIZE = 20
ENTITY_MAX_SPEED = 100
INITIAL_ENTITIES = 50

HELP_ON = True


# DEFAULT FLOCKING PARAMETERS

attractive_mouse = False
scary_mouse = False

boid_sight_radius = 60
desired_separation = 50
max_steering_force = 80

separation = 0.2
alignment = 0.1
cohesion = 0.1


# KEYBINDINGS
toggle_help                 = sf.Keyboard.F1
delete_entities             = sf.Keyboard.DELETE
toggle_attractive_mouse     = sf.Keyboard.A
toggle_scary_mouse          = sf.Keyboard.S
scatter_boids               = sf.Keyboard.D
decrease_boid_sight_radius  = sf.Keyboard.NUM1
increase_boid_sight_radius  = sf.Keyboard.Q
decrease_desired_separation = sf.Keyboard.NUM2
increase_desired_separation = sf.Keyboard.W
decrease_max_steering_force = sf.Keyboard.NUM3
increase_max_steering_force = sf.Keyboard.E
decrease_separation_factor  = sf.Keyboard.NUM4
increase_separation_factor  = sf.Keyboard.R
decrease_alignment_factor   = sf.Keyboard.NUM5
increase_alignment_factor   = sf.Keyboard.T
decrease_cohesion_factor    = sf.Keyboard.NUM6
increase_cohesion_factor    = sf.Keyboard.Y
