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

		for event in self.window.events:

			if (type(event) is sf.CloseEvent):
				self.window.close()

			elif (type(event) is sf.MouseButtonEvent and event.pressed):
				self.entities.append(Entity(event.position))

			elif (type(event) is sf.KeyEvent and event.pressed):

				if (event.code is sf.Keyboard.ESCAPE):
					self.window.close()

				elif (event.code is sf.Keyboard.D):
					for e in self.entities:
						e.scatter()


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
					f.velocity -= d * (settings.desired_separation/distance - 1) * settings.separation
					s.velocity += d * (settings.desired_separation/distance - 1) * settings.separation

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
