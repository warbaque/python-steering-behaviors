import settings
import sfml as sf


class Statistics(sf.Drawable):


	def __init__(self, font):

		sf.Drawable.__init__(self)

		self.update_time = sf.seconds(0)
		self.num_frames = 0

		self.text = sf.Text()
		self.text.font = font
		self.text.position = (5, 5)
		self.text.character_size = 14
		self.text.color = sf.Color(220, 220, 100, 220)

		self.settings_text = sf.Text()
		self.settings_text.font = font
		self.settings_text.position = (5, settings.HEIGHT-65)
		self.settings_text.character_size = 14
		self.settings_text.color = sf.Color(220, 220, 100, 220)

		self.num_entities = 0
		self.collision_checks = 0


	def update(self, dt):

		self.num_frames += 1
		self.update_time += dt

		if (self.update_time >= sf.seconds(0.1)):
			fps = int(self.num_frames / self.update_time.seconds)
			tps = int(self.update_time.microseconds / self.num_frames)
			text = "FPS: " + str(fps) + "\n"
			text += "Time / update: " + str(tps) + " us\n"
			text += "Number of entities: " + str(self.num_entities) + "\n"
			text += "Collision checks: " + str(self.collision_checks) + "\n"
			self.text.string = text

			text = "{:30} | {:30}\n{:30} | {:30} | {:30}\n{:30} | {:30} | {:30}\n".format(
				"Attractive mouse   : {}".format(settings.attractive_mouse),
				"Scary mouse        : {}".format(settings.scary_mouse),
				"Boid sight radius  : {}".format(settings.boid_sight_radius),
				"Desired Separation : {}".format(settings.desired_separation),
				"Max steering force : {}".format(settings.max_steering_force),
				"Separation factor  : {:.2f}".format(settings.separation),
				"Alignment factor   : {:.2f}".format(settings.alignment),
				"Cohesion factor    : {:.2f}".format(settings.cohesion))

			self.settings_text.string = text

			self.update_time -= sf.seconds(0.1)
			self.num_frames = 0


	def draw(self, target, states):

		target.draw(self.text, states)
		target.draw(self.settings_text, states)
