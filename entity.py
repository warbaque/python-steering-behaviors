import sfml as sf
import random
import settings
import utility


max_speed = settings.ENTITY_MAX_SPEED


class Entity(sf.Drawable):


	def __init__(self, position=None, color=None):

		sf.Drawable.__init__(self)

		self.shape = sf.CircleShape()
		self.shape.radius = settings.ENTITY_SIZE/2

		r = 55 + random.randrange(200)
		g = 55 + random.randrange(200)
		b = 55 + random.randrange(200)
		self.shape.fill_color = sf.Color(r, g, b, 50)
		self.shape.outline_color = sf.Color(r, g, b, 200)
		self.shape.outline_thickness = 1

		v_x = random.randrange(200) - 100
		v_y = random.randrange(200) - 100
		self.position = position
		self.velocity = sf.Vector2(v_x, v_y)

		self.line = sf.VertexArray(sf.PrimitiveType.LINES, 2)
		self.line[0].color = sf.Color(r, g, b, 200)
		self.line[1].color = sf.Color(r, g, b, 10)

		self.centre_of_mass = sf.Vector2()
		self.average_velocity = sf.Vector2()
		self.num_nearby_entities = 0


	def update(self, dt):

		speed = utility.length(self.velocity)
		if (speed > max_speed):
			self.velocity = utility.unit_vector(self.velocity) * max_speed
		self.position += self.velocity * dt.seconds
		self.centre_of_mass.x = 0
		self.centre_of_mass.y = 0
		self.average_velocity.x = 0
		self.average_velocity.y = 0
		self.num_nearby_entities = 0


	def draw(self, target, states):

		self.shape.position = self.position - self.shape.radius
		self.line[0].position = self.position
		self.line[1].position = self.position + self.velocity * 0.3
		target.draw(self.shape, states)
		target.draw(self.line, states)

	def scatter(self):

		self.position.x = random.randrange(settings.WIDTH)
		self.position.y = random.randrange(settings.HEIGHT)
		self.velocity.x = random.randrange(2 * max_speed) - max_speed
		self.velocity.y = random.randrange(2 * max_speed) - max_speed
