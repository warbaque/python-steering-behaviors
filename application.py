import sys
import random
import settings
import utility
import sfml as sf
from statistics import Statistics
from entity import Entity
from collision_grid import CollisionGrid


time_per_frame = settings.TIME_PER_FRAME

width = settings.WIDTH
height = settings.HEIGHT
cell_size = settings.CELL_SIZE


class Application(object):

	def __init__(self):

		font = sf.Font.from_file("media/fonts/UbuntuMono-R.ttf")
		self.statistics = Statistics(font)

		window_settings = sf.window.ContextSettings()
		window_settings.antialiasing_level = 8
		self.window = sf.RenderWindow(
			sf.VideoMode(width, height),
			"Steering Behaviors For Autonomous Characters",
			sf.Style.DEFAULT, window_settings)
		self.window.vertical_synchronization = False

		self.entities = []
		self.grid = CollisionGrid(width, height, cell_size)


	def run(self):

		clock = sf.Clock()
		time_since_last_update = sf.seconds(0)
		for i in range(settings.INITIAL_ENTITIES):
			self.entities.append(Entity(sf.Vector2(
				random.randrange(width),
				random.randrange(height))))

		while self.window.is_open:

			dt = clock.restart()
			time_since_last_update += dt

			while time_since_last_update > time_per_frame:

				time_since_last_update -= time_per_frame

				self.process_events()

				self.update_grid()
				self.handle_collision()
				self.grid.clear()
				self.update(time_per_frame)

			self.statistics.update(dt)
			self.render()


	def process_events(self):

		def close():
			self.window.close()

		def toggle_attractive_mouse():
			settings.attractive_mouse = not settings.attractive_mouse

		def toggle_scary_mouse():
			settings.scary_mouse = not settings.scary_mouse

		def scatter_boids():
			for e in self.entities:
				e.scatter()

		def increase_boid_sight_radius():
			settings.boid_sight_radius += 10

		def decrease_boid_sight_radius():
			settings.boid_sight_radius -= 10

		def increase_desired_separation():
			settings.desired_separation += 10

		def decrease_desired_separation():
			settings.desired_separation -= 10

		def increase_max_steering_force():
			settings.max_steering_force += 10

		def decrease_max_steering_force():
			settings.max_steering_force -= 10

		def increase_separation_factor():
			settings.separation += 0.1

		def decrease_separation_factor():
			settings.separation -= 0.1

		def increase_alignment_factor():
			settings.alignment += 0.1

		def decrease_alignment_factor():
			settings.alignment -= 0.1

		def increase_cohesion_factor():
			settings.cohesion += 0.1

		def decrease_cohesion_factor():
			settings.cohesion -= 0.1

		actions = {
			sf.Keyboard.ESCAPE : close,
			settings.toggle_attractive_mouse : toggle_attractive_mouse,
			settings.toggle_scary_mouse : toggle_scary_mouse,
			settings.scatter_boids : scatter_boids,
			settings.increase_boid_sight_radius : increase_boid_sight_radius,
			settings.decrease_boid_sight_radius : decrease_boid_sight_radius,
			settings.increase_desired_separation : increase_desired_separation,
			settings.decrease_desired_separation : decrease_desired_separation,
			settings.increase_max_steering_force : increase_max_steering_force,
			settings.decrease_max_steering_force : decrease_max_steering_force,
			settings.increase_separation_factor : increase_separation_factor,
			settings.decrease_separation_factor : decrease_separation_factor,
			settings.increase_alignment_factor : increase_alignment_factor,
			settings.decrease_alignment_factor : decrease_alignment_factor,
			settings.increase_cohesion_factor : increase_cohesion_factor,
			settings.decrease_cohesion_factor : decrease_cohesion_factor
		}


		for event in self.window.events:

			if (type(event) is sf.CloseEvent):
				close()

			elif (type(event) is sf.MouseButtonEvent and event.pressed):
				self.entities.append(Entity(event.position))

			elif (type(event) is sf.KeyEvent and event.pressed):
				try:
					actions.get(event.code)()
				except TypeError:
					pass


	def update(self, dt):

		for e in self.entities:
			e.update(dt)
			if (e.position.x < 0):
				e.position.x += width
			elif (e.position.x > width):
				e.position.x -= width
			if (e.position.y  < 0):
				e.position.y += height
			elif (e.position.y > height):
				e.position.y -= height


	def render(self):

		self.window.clear()
		for e in self.entities:
			self.window.draw(e)
		self.window.draw(self.grid)
		self.window.draw(self.statistics)
		self.window.display()


	def update_grid(self):

		for e in self.entities:
			self.grid.add_entity(e)


	def handle_collision(self):

		self.statistics.num_entities = len(self.entities)
		self.statistics.collision_checks = 0

		for f in self.entities:

			self.grid.remove_entity(f)
			nearby_boids = self.grid.get_nearby_entities(f,
				settings.boid_sight_radius)


			if (settings.scary_mouse):
				d = sf.Mouse.get_position(self.window) - f.position
				distance = utility.length(d)
				if (distance < settings.ENTITY_SIZE * 10):
					steer = d * (settings.ENTITY_SIZE * 10/distance - 1)
					if (utility.length(steer) > settings.max_steering_force):
						steer = utility.unit_vector(steer) * settings.max_steering_force
					f.velocity -= steer


			if (settings.attractive_mouse):
				f.centre_of_mass += sf.Mouse.get_position(self.window)
				f.num_nearby_entities += 1


			for s in nearby_boids:
				self.statistics.collision_checks += 1

				d = s.position - f.position
				distance = utility.length(d)

				if (distance < settings.boid_sight_radius):
					f.centre_of_mass += s.position
					s.centre_of_mass += f.position
					f.average_velocity += s.velocity
					s.average_velocity += f.velocity
					f.num_nearby_entities += 1
					s.num_nearby_entities += 1

					# SEPARATE
					if (distance < settings.desired_separation):
						steer = d * (settings.desired_separation/distance - 1) * settings.separation
						if (utility.length(steer) > settings.max_steering_force):
							steer = utility.unit_vector(steer) * settings.max_steering_force
						f.velocity -= steer
						s.velocity += steer

			if (not f.num_nearby_entities):
				continue

			# COHERE
			desired = f.centre_of_mass / f.num_nearby_entities - f.position
			d = utility.length(desired)
			if (d < 65):
				desired *= d/15
			else:
				desired *= 65/15
			steer = desired-f.velocity
			if (utility.length(steer) > settings.max_steering_force):
				steer = utility.unit_vector(steer) * settings.max_steering_force
			f.velocity += steer * settings.cohesion

			# ALIGN
			steer = f.average_velocity / f.num_nearby_entities
			if (utility.length(steer) > settings.max_steering_force):
				steer = utility.unit_vector(steer) * settings.max_steering_force
			f.velocity += steer * settings.alignment


if __name__ == "__main__":

	app = Application()
	app.run()
