import turtle
import math
 
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Runner")
wn.setup(700,700)
wn.tracer(0,0)

# turtle.shapesize(20,20)
turtle.register_shape("images/ghost_right.gif")
turtle.register_shape("images/ghost_left.gif")
turtle.register_shape("images/treasure.gif")
turtle.register_shape("images/wall.gif")
 
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape(("images/wall.gif"))
        # self.color("white")
        self.penup()
        self.speed(0)

class Score(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("gold")
        self.penup()
        self.goto(-30, 310)

    def update_treasure(self, score):
        self.hideturtle()
        self.clear()
        self.write("Gold: {}".format(score), move=False, align="left", font=("Arial", 24, "normal"))
 
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("images/ghost_right.gif")
        # self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 0
 
    def go_up(self):
        x = self.xcor()
        y = self.ycor() + 20
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_down(self):
        x = self.xcor()
        y = self.ycor() - 20
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_right(self):
        self.shape("images/ghost_right.gif")
        x = self.xcor() + 20
        y = self.ycor() 
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_left(self):
        self.shape("images/ghost_left.gif")
        x = self.xcor() - 20
        y = self.ycor() 
        if (x,y) not in walls:
            self.goto(x, y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("images/treasure.gif")
        # self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

levels=[""]
 
level_1 = [
         "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "XXP XXXXXXXXXXXX        XXXXXX",
         "XX  XXXXXXXXXXXX XX XXX XXXXXX",
         "XX           XXX XX XXX XXXXXX",
         "X     XXXXXXXXXX XX XXX XXXXXX",
         "X XX XXXXX       XX XX   XXXXX",
         "X XX  XXXX XXXXX             X",
         "X XXX    X XXXXX XXXXX   XXX X",
         "X XXX XXXX XXXXX XXXXXX XXXX X",
         "X XXX      XXXXX XXXXXX XXXX X",
         "X XXXXX XXXXXXXX        XXXX X",
         "X XXXXX XXXXXXXXXXXXXXXXXXXX X",
         "      X            XX        X",
         " XXXXXX XXXXXXXXXXXXX XXXXXXXX",
         "XXXXXXX XXXXXXXXXXXXX XXXXXXXX",
         "XXXTXXX            XX XXXXXXXX",
         "XXX XXX XXXXXXXXXXXXX     XXXX",
         "XXX XXX XXXXXXXXXXXXXXXXX XXXX",
         "XXX XXX X                 XXXX",
         "XXX XXX X XX XXXXXXXXXXXX    X",
         "XXX XXX X XX    X         XX X",
         "XXX XXXXX XXXXXXXXX XXXXX XX X",
         "X X              XX XXXXX    X",
         "X XXXXXXXXXXXXXX XXXXXXXXXXXXX",
         "X                XXXXXXXXXXXXX",
         "XXX XXXXXXXXXXXXXXXXXXXXXXXXXX",
         "XXX                       XXXX",
         "XXX XXXXXXXXXXXXXXXXXXXXX XXXX",
         "XXX              XXXXXXXX XXXX",
         "XXXXXXXXXXXXXXXX XXXXXXXXXXXXX"]
 
levels.append(level_1)
 
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            char=level[y][x]
            screen_x = -288 + (x*20)
            screen_y = 288 - (y*20)
            if char=="X":
                pen.goto(screen_x,screen_y)
                pen.stamp()
                walls.append((screen_x,screen_y))
            if char=='P':
                player.goto(screen_x,screen_y)
            if char == 'T':
                treasures.append(Treasure(screen_x, screen_y))
 
pen = Pen()
player = Player()
score = Score()
score.update_treasure(0)
walls = []
treasures = []
setup_maze(levels[1])
 
#Keyboard Binding
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

# def draw_score(pen, score):
#     pen.color("blue")
#     # pen.hideturtle()
#     # pen.goto(-50, 350)
#     # if isinstance(score, str):
#     #     pen.clear()
#     pen.goto(-350, 0)
#     pen.write("{}".format(score), move=False, align="left", font=("Arial", 24, "normal"))

# draw_score()
 
# wn.tracer(0,0)
 
while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            score.update_treasure(player.gold)
            treasure.destroy()
            treasures.remove(treasure)

    wn.update()