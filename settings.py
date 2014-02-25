import sfml as sf


TIME_PER_FRAME = sf.seconds(1/60)

WIDTH = 1280
HEIGHT = 720
CELL_SIZE = 100

ENTITY_SIZE = 20
ENTITY_MAX_SPEED = 100
INITIAL_ENTITIES = 35

attractive_mouse = False
scary_mouse = False

boid_sight_radius = 100
desired_separation = 50
max_steering_force = 500

separation = 0.1
alignment = 0.1
cohesion = 0.1
