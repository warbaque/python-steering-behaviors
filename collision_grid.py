import sfml as sf
import math


class Cell(object):


	def __init__(self):

		self.entities = []


	def add_entity(self, entity):

		self.entities.append(entity)


	def remove_entity(self, entity):

		self.entities.remove(entity)


	def clear(self):

		del self.entities[:]



class CollisionGrid(sf.Drawable):


	def __init__(self, width, height, cell_size):

		sf.Drawable.__init__(self)

		self.width = width
		self.height = height
		self.cell_size = cell_size

		self.cols = int(math.ceil((self.width / cell_size)))
		self.rows = int(math.ceil((self.height / cell_size)))

		self.cells = [[Cell() for _ in range(self.rows)] for _ in range(self.cols)]

		# Grid lines for drawing
		self.lines = sf.VertexArray(sf.PrimitiveType.LINES, 2*self.rows+2*self.cols)
		for x in range(self.cols):
			self.lines[2*x].position = (x*self.cell_size, 0)
			self.lines[2*x+1].position = (x*self.cell_size, self.height)
			self.lines[2*x].color = sf.Color(220, 220, 100, 50)
			self.lines[2*x+1].color = sf.Color(220, 220, 100, 50)
		for y in range(self.rows):
			self.lines[2*(y+self.cols)].position = (0, y*self.cell_size)
			self.lines[2*(y+self.cols)+1].position = (self.width, y*self.cell_size)
			self.lines[2*(y+self.cols)].color = sf.Color(220, 220, 100, 50)
			self.lines[2*(y+self.cols)+1].color = sf.Color(220, 220, 100, 50)


	def add_entity(self, entity):

		self.get_cell(entity.position).add_entity(entity)


	def remove_entity(self, entity):

		self.get_cell(entity.position).remove_entity(entity)


	def get_nearby_entities(self, entity, radius = None):

		if(not radius):
			radius = self.cell_size
		entities = []

		min_x = int((entity.position.x - radius) / self.cell_size)
		min_y = int((entity.position.y - radius) / self.cell_size)
		max_x = int(min_x + 2*radius/self.cell_size + 1)
		max_y = int(min_y + 2*radius/self.cell_size + 1)

		min_x = max(min_x, 0)
		min_y = max(min_y, 0)
		max_x = min(max_x, self.cols)
		max_y = min(max_y, self.rows)

		for y in range(min_y, max_y):
			for x in range(min_x, max_x):
				entities.extend(self.cells[x][y].entities)

		return entities


	def get_cell(self, position):

		return self.cells[int(position.x / self.cell_size)][int(position.y / self.cell_size)]


	def clear(self):

		[[c.clear() for c in cells] for cells in self.cells]


	def draw(self, target, states):

		target.draw(self.lines, states)
