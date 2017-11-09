from __future__ import division, print_function, absolute_import, unicode_literals
import math
import operator
import types
from math import atan2, sin, cos, floor, ceil
import random
import collections

def limit(vector, lim):
    if abs(vector) > lim:
        vector.normalize()
        vector *= lim

_use_slots = True


_enable_swizzle_set = False

# Requires class to derive from object.
if _enable_swizzle_set:
    _use_slots = True

class _EuclidMetaclass(type):
    def __new__(cls, name, bases, dct):
        if _use_slots:
            return type.__new__(cls, name, bases + (object,), dct)
        else:
            del dct['__slots__']
            return types.ClassType.__new__(types.ClassType, name, bases, dct)
__metaclass__ = _EuclidMetaclass


class Vector2(object):
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __copy__(self):
        return self.__class__(self.x, self.y)

    copy = __copy__

    def __repr__(self):
        return 'Vector2(%.4f, %.4f)' % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return self.x == other[0] and self.y == other[1]

    def __neq__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0 or self.y != 0

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __setitem__(self, key, value):
        l = [self.x, self.y]
        l[key] = value
        self.x, self.y = l

    def __iter__(self):
        return iter((self.x, self.y))

    def __getattr__(self, name):
        try:
            return tuple([(self.x, self.y)['xy'.index(c)] for c in name])
        except ValueError:
            raise AttributeError(name)

    if _enable_swizzle_set:
        def __setattr__(self, name, value):
            if len(name) == 1:
                object.__setattr__(self, name, value)
            else:
                try:
                    l = [self.x, self.y]
                    for c, v in map(None, name, value):
                        l['xy'.index(c)] = v
                    self.x, self.y = l
                except ValueError:
                    raise AttributeError(name)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x,
                           self.y + other.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(self.x + other[0],
                           self.y + other[1])
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other[0]
            self.y += other[1]
        return self

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x,
                           self.y - other.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(self.x - other[0],
                           self.y - other[1])

    def __rsub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(other.x - self.x,
                           other.y - self.y)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return Vector2(other.x - self[0],
                           other.y - self[1])

    def __mul__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(self.x * other,
                       self.y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        assert type(other) in (int, long, float)
        self.x *= other
        self.y *= other
        return self

    def __div__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.div(self.x, other),
                       operator.div(self.y, other))

    def __rdiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.div(other, self.x),
                       operator.div(other, self.y))

    def __floordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.floordiv(self.x, other),
                       operator.floordiv(self.y, other))

    def __rfloordiv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.floordiv(other, self.x),
                       operator.floordiv(other, self.y))

    def __truediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.truediv(self.x, other),
                       operator.truediv(self.y, other))

    def __rtruediv__(self, other):
        assert type(other) in (int, long, float)
        return Vector2(operator.truediv(other, self.x),
                       operator.truediv(other, self.y))

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    __pos__ = __copy__

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    magnitude = __abs__

    def clear(self):
        self.x = 0
        self.y = 0

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        d = self.magnitude()
        if d:
            self.x /= d
            self.y /= d
        return self

    def normalized(self):
        d = self.magnitude()
        if d:
            return Vector2(self.x / d, self.y / d)
        return self.copy()

    def dot(self, other):
        assert isinstance(other, Vector2)
        return self.x * other.x + self.y * other.y

    def cross(self):
        return Vector2(self.y, -self.x)

    def reflect(self, normal):
        # assume normal is normalized
        assert isinstance(normal, Vector2)
        d = 2 * (self.x * normal.x + self.y * normal.y)
        return Vector2(self.x - d * normal.x, self.y - d * normal.y)

class BoidSwarm(object):

    def __init__(self,width, size, cell_w):
        self.boids = []  # list of all the boids

        divs_height = int(floor(size/cell_w))
        divs_width = int(floor(width/cell_w))
        self.divisions_width = divs_width
        self.divisions_height = divs_height
        self.cell_width = cell_w

        self.cell_table = {}
        self.num_cells = divs_height*divs_width
        for i in range(divs_height):
            for j in range(divs_width):
                # use deque for fast appends of several deque
                self.cell_table[(i, j)] = collections.deque()

    def cell_num(self, x, y):
        """Forces units into border cells if they hit an edge"""
        i = int(floor(x / self.cell_width))
        j = int(floor(y / self.cell_width))
        # deal with boundary conditions
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        if j >= self.divisions_height:
            j = self.divisions_height-1  # zero indexing
        if i >= self.divisions_width:
            i = self.divisions_width-1  # zero indexing
        return (j, i)

    def find_cell_containing(self, x, y):
        """returns the cell containing a position x,y"""
        return self.cell_table[self.cell_num(x, y)]

    def find_near(self, x, y, influence_range):
        """return objects within radius influence_range of point x,y"""
        if influence_range == 0:
            _nearObjects = self.find_cell_containing(x, y)
        elif influence_range <= self.cell_width:
            _nearObjects = self.find_neighbour_cells(x, y)
        else:
            ext = ceil(influence_range/self.cell_width)
            _nearObjects = self.find_extended(x, y, ext)

        return _nearObjects

    def find_neighbour_cells(self, x, y):
        return self.cell_table[self.cell_num(x, y)]

    def find_extended(self, x, y, d):
        I, J = self.cell_num(x, y)
        d = int(d)
        group = collections.deque()
        for i in range(I-d, I+d):
            for j in range(J-d, J+d):
                #if (i, j) in self.cell_table:
                if (i >= 0 and j >=0 and j < self.divisions_width and i < self.divisions_height):
                    if (self.cell_table[(i,j)]):
                        group.extend(self.cell_table[(i, j)])  # merge deque
        return group

    def rebuild(self):
        for cell in self.cell_table.values():
            cell.clear()
        for b in self.boids:
            c = self.find_cell_containing(b.position.x, b.position.y)
            c.append(b)


class Boid(object):

    influence_range = 90
    minsep = 25.0
    max_force = 20.0
    max_speed = 150.0
    drag = 0.9
    cohesion_strength = 1.1
    align_strength = 0.9
    sep_strength = 2.0
    wall_strength = 50.0

    # Get and set the speed as a scalar
    def _get_speed(self):
        return abs(self.velocity)

    def _set_speed(self, s):
        if abs(self.velocity) == 0:
            self.velocity = Vector2(random.uniform(-1,1), random.uniform(-1,1))

        self.velocity.normalize()
        self.velocity *= s

    speed = property(_get_speed, _set_speed)

    # get and set the rotation as an angle
    def _get_rotation(self):
        return atan2(self.velocity.y, self.velocity.x)

    def _set_rotation(self, r):
        old_speed = self.speed
        # set the direction as a unit vector
        self.velocity.x = cos(r)
        self.velocity.y = sin(r)

        self.speed = old_speed

    rotation = property(_get_rotation, _set_rotation)

    def __init__(self, x, y):
        """ create a new boid at x,y """
        self.neighbors = 0

        self.position = Vector2(x, y)
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(random.uniform(-self.max_speed, self.max_speed),
                                random.uniform(-self.max_speed, self.max_speed))

    def __repr__(self):
        return 'id %d' % self.id

    def borders(self, top, bottom, left, right):

        if (self.position.x > 0):
            self.position.x = (self.position.x)%right
        else :
            self.position.x = right+self.position.x

        if (self.position.y > 0):
            self.position.y = (self.position.y)%top
        else :
            self.position.y = top+self.position.y

    def update(self, t):
        """
        Method to update position by computing displacement from velocity and acceleration
        """
        self.position += (self.velocity * t + 0.5*self.acceleration*t**2)
        self.velocity += self.acceleration * t
        limit(self.velocity, self.max_speed)

    # Calculation variables for interact method - init once instead of on each call
    _sep_f = Vector2(0, 0)
    _align_f = Vector2(0, 0)
    _cohes_sum = Vector2(0, 0)
    forceWall = Vector2(0,0)

    def interact(self, actors, wallForce=0):

        self._sep_f.clear()
        self._align_f.clear()
        self._cohes_sum.clear()
        self.forceWall.clear()

        count = 0
        self.neighbors = len(actors)

        for other in actors:
            # vector pointing from neighbors to self
            diff = self.position - other.position
            d = abs(diff)

            # Only perform on "neighbor" actors, i.e. ones closer than arbitrary
            # dist or if the distance is not 0 (you are yourself)
            if 0 < d < self.influence_range:
                count += 1

                #diff.normalize()
                if d < self.minsep:
                    #diff /= d  # Weight by distance
                    self._sep_f += diff*(self.minsep/d)
                else :
                    self._sep_f += diff/d

                self._cohes_sum += other.position  # Add position

                # Align - add the velocity of the neighbouring actors, then average
                self._align_f += other.velocity

        if count > 0:
            # calc the average direction (normed avg velocity)
            self._align_f /= count
            # self._align_f.normalize()
            # self._align_f *= self.max_speed
            self._align_f -= self.velocity
            #limit(self._align_f, self.max_force)

            # calc the average position and calc steering vector towards it
            self._cohes_sum /= count
            cohesion_f = (self._cohes_sum-self.position)
            #cohesion_f = self.steer(self._cohes_sum, True)

            self._sep_f *= self.sep_strength
            self._align_f *= self.align_strength
            cohesion_f *= self.cohesion_strength

            # finally add the velocities
            sum = self._sep_f + cohesion_f + self._align_f
        if (wallForce):
            leftDist = self.position.x
            rightDist = 1300 - leftDist
            floorDist = self.position.y
            UpDist = 700 - floorDist
            if (floorDist >= 0 and floorDist <= 80 ):
                self.forceWall = Vector2(0,10)*(80.0/floorDist - 1)
            if (UpDist >=0 and UpDist <= 80):
                self.forceWall = self.forceWall + Vector2(0,-1)*(80.0/UpDist - 1)
            if (leftDist >=0 and leftDist <= 80):
                self.forceWall = self.forceWall + Vector2(10,0)*(80.0/leftDist - 1)
            if (rightDist >=0 and rightDist <= 80):
                self.forceWall = self.forceWall + Vector2(-1,0)*(80.0/rightDist - 1)


        self.forceWall *= self.wall_strength
        if (count > 0 ):
            sum = sum + self.forceWall
        else :
            sum = self.forceWall
            print (sum)
        self.acceleration = sum

    def steer(self, desired, slowdown=False):
        desired -= self.position
        d = abs(desired)
        # If the distance is greater than 0, calc steering (otherwise return zero vector)
        if d > 0:
            desired.normalize()
            if slowdown and (d < self.minsep):
                desired *= self.max_speed*d / self.minsep
            else:
                desired *= self.max_speed

            steer = desired - self.velocity
            limit(steer, self.max_force)
        else:
            steer = Vector2(0, 0)
        return steer

class FlockSimulation(object):

    """
    Ties the BoidSwarm with the boids.
    boidswarm just holds the data, boids know how to interact with each
    other. This class keeps the two separated
    """

    def __init__(self, starting_units=100, field_width=1200, field_size = 700):
        """
        """
        self.swarm = BoidSwarm(field_width,field_size, 20)  # /2
        self.field_width = field_width
        self.field_size = field_size
        self.pad = 80 # use to keep boids inside the play field

        for i in range(starting_units):
            b = Boid(random.uniform(self.pad, self.field_width-self.pad),
                     random.uniform(self.pad, self.field_size-self.pad))
            self.swarm.boids.append(b)
        self.swarm.rebuild()
        self._cumltime = 0  # calculation var

    def update(self, dt):
        """dt is in seconds"""
        for b in self.swarm.boids:
            close_boids = self.swarm.find_near(b.position.x, b.position.y, b.influence_range)
            b.interact(close_boids,1)
            b.update(dt)
            height = self.field_size
            width = self.field_width
            b.borders(height, 0, 0, width)  # keep the boids inside the borders
        # rebuild the swarm once we've updated all the positions
        self.swarm.rebuild()
