import sfml as sf
import math


def length(vector):
	return math.sqrt(vector.x * vector.x + vector.y * vector.y)


def unit_vector(vector):
	return vector / length(vector)
