try:
    import sys
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class Player:
    def __init__(self, name, points=0):
        self.name = name
        self.points = points

    def __str__(self):
        return f"{self.name} has {self.points} points"

