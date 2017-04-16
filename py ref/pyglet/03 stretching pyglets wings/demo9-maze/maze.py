from math import sqrt
from random import randint
from creature import Ghost
from data import all_ghosts
from room import Room
from shape import Shape

minRoomLen = 2
maxRoomLen = 8
scale = 64

class Maze(object):

    def __init__(self):
        self.rooms = []
        self.shape = None
        self.creatures = []
        self.size = 0

    def create(self, width, height, numRooms):
        self.generate_rooms(width, height, numRooms)
        self.generate_shape()
        self.generate_ghosts()
        self.size = sqrt(width * width + height * height)

    def generate_rooms(self, width, height, numRooms):
        for _ in range(numRooms):
            if len(self.rooms) == 0:
                roomStart = (
                    (randint(0, width) - width/2) * scale,
                    (randint(0, height) - height/2) * scale, )
            else:
                prevRoom = self.rooms[randint(0, len(self.rooms)-1)]
                if randint(0, 1) == 0:
                    roomStart = prevRoom.start
                else:
                    roomStart = prevRoom.end
            roomLength = randint(minRoomLen, maxRoomLen)
            roomDirection = (0, 0)
            while roomDirection == (0, 0):
                roomDirection = (randint(-1, +1), randint(-1, +1))
            roomEnd = (
                roomStart[0] + roomDirection[0] * roomLength * scale,
                roomStart[1] + roomDirection[1] * roomLength * scale, )

            room = Room(roomStart, roomEnd)
            self.rooms.append(room)

    def generate_shape(self):
        for room in self.rooms:
            room.make_shape()
        self.shape = Shape([room.shape for room in self.rooms])

    def generate_ghosts(self):
        for room in self.rooms:
            ghost_shape = all_ghosts[randint(0, len(all_ghosts)-1)]
            ghost = Ghost(ghost_shape, room.start, room.angle)
            ghost.room = room
            self.creatures.append(ghost)

    def update(self, dt):
        for ghost in self.creatures:
            ghost.update(dt)

