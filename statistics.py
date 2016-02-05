import settings
import sfml as sf
import re
from collections import deque


UPDATES_PER_SECOND = 10

class Statistics(sf.Drawable):


	def __init__(self, font):

		sf.Drawable.__init__(self)

		self.time_per_text_update = sf.seconds(1/UPDATES_PER_SECOND)
		self.update_time = sf.seconds(0)
		self.num_frames = 0

		self.fps = deque([], UPDATES_PER_SECOND)
		self.t_update = deque([], UPDATES_PER_SECOND)
		self.t_render = deque([], UPDATES_PER_SECOND)

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

		self.help_text = sf.Text()
		self.help_text.font = font
		self.help_text.position = (settings.WIDTH-300, 5)
		self.help_text.character_size = 14
		self.help_text.color = sf.Color(220, 220, 100, 220)
		r = re.compile(r'(.+=) *sf\.Keyboard\.(.*)')
		with open("settings.py") as s:
			t = r.findall(s.read())
			t = '\n'.join(map(' '.join, t))
			self.help_text.string = "KEYBINDINGS:\n" + "------------\n" + t
		self.help = settings.HELP_ON


	def update_texts(self, dt):

		self.update_time += dt
		if (self.update_time >= self.time_per_text_update):

			self.update_time -= self.time_per_text_update
			self.fps.append(self.num_frames)
			fps = sum(self.fps)
			tpf = sum(self.t_render)/(1000*UPDATES_PER_SECOND)
			tpu = sum(self.t_update)/(1000*UPDATES_PER_SECOND)
			text = "FPS: {}\n".format(fps)
			text += "Time / frame: {:.3f} ms\n".format(tpf)
			text += "Time / update: {:.3f} ms\n".format(tpu)
			text += "Number of entities: {}\n".format(self.num_entities)
			text += "Collision checks: {}\n".format(self.collision_checks)
			self.text.string = text
			self.num_frames = 0

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


	def draw(self, target, states):

		target.draw(self.text, states)
		target.draw(self.settings_text, states)
		if self.help:
			target.draw(self.help_text, states)
