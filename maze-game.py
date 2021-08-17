import turtle
import math
import random
 
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Runner")
wn.setup(700,700)
wn.tracer(0,0)

# turtle.shapesize(20,20)
images = ["images/winning_pic.gif", "images/blood.gif", "images/door.gif", "images/ghost_right.gif", "images/ghost_left.gif", "images/treasure.gif", "images/wall.gif", "images/spider_left.gif", "images/spider_right.gif", "images/skeleton_left.gif", "images/skeleton_right.gif", "images/glob_left.gif", "images/glob_right.gif", "images/zombie_left.gif", "images/zombie_right.gif", "images/machine_left.gif", "images/machine_right.gif", "images/bullet_horizontal.gif", "images/bullet_vertical.gif"]
for image in images:
    turtle.register_shape(image)

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        # self.color("white")
        self.penup()
        self.speed(0)

class Draw_Score(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("gold")
        self.penup()
        self.goto(-30, 310)

    def update_treasure(self, score):
        player.gold += score
        self.hideturtle()
        self.clear()
        self.write("Gold: {}".format(player.gold), move=False, align="left", font=("Arial", 24, "normal"))
 
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("images/ghost_right.gif")
        # self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.direction = "right"
 
    def go_up(self):
        self.direction = "up"
        x = self.xcor()
        y = self.ycor() + 20
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_down(self):
        self.direction = "down"
        x = self.xcor()
        y = self.ycor() - 20
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_right(self):
        self.direction = "right"
        self.shape("images/ghost_right.gif")
        x = self.xcor() + 20
        y = self.ycor() 
        if (x,y) not in walls:
            self.goto(x, y)
 
    def go_left(self):
        self.direction = "left"
        self.shape("images/ghost_left.gif")
        x = self.xcor() - 20
        y = self.ycor() 
        if (x,y) not in walls:
            self.goto(x, y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 20:
            return True
        else:
            return False

    def bullet_shoot(self):
        bullet = Bullet(self)
        if bullet.direction == "up":
            bullet.shape("images/bullet_vertical.gif")
            dx = 0
            dy = 20
        elif bullet.direction == "down":
            bullet.shape("images/bullet_vertical.gif")
            dx = 0
            dy = -20
        elif bullet.direction == "left":
            bullet.shape("images/bullet_horizontal.gif")
            dx = -20
            dy = 0
        elif bullet.direction == "right":
            bullet.shape("images/bullet_horizontal.gif")
            dx = 20
            dy = 0
        else:
            dx = 0
            dy = 0

        def keep_shooting():
            move_to_x = bullet.xcor() + dx
            move_to_y = bullet.ycor() + dy

            enemy_hit = False
            if (move_to_x, move_to_y) not in walls:
                for enemy in enemies:
                    if bullet.is_collision(enemy):
                        enemy_hit = True
                        pen.shape("images/blood.gif")
                        pen.goto(enemy.xcor(), enemy.ycor())
                        pen.stamp()
                        enemy.destroy()
                        enemies.remove(enemy)
                    enemy.speed(0)
                    bullet.speed(0)
            else:
                bullet.destroy()
                return
        
            if enemy_hit == True:
                bullet.destroy()
                return

            bullet.showturtle()
            bullet.goto(move_to_x, move_to_y)
            turtle.ontimer(keep_shooting, t=100)
        keep_shooting()

class Bullet(turtle.Turtle):
    def __init__(self, player):
        turtle.Turtle.__init__(self)
        self.penup() 
        self.setpos(player.pos())
        self.direction = player.direction
        self.speed(0)
        self.hideturtle()

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        opposites = {"up": "horizontal", "down": "horizontal", "left": "vertical", "right": "vertical"}

        print(distance)
        if (distance < 21 and (self.xcor() == other.xcor() or self.ycor() == other.ycor())):
            print("hit")
            # or (opposites[other.direction] != opposites[self.direction] and distance < 100)
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

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

class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.enemy = random.choice(["spider", "skeleton", "glob", "zombie", "machine"])
        string = "images/enemyToFight_left.gif".replace("enemyToFight", self.enemy)
        self.shape(string)
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 20
        elif self.direction == "down":
            dx = 0
            dy = -20
        elif self.direction == "left":
            self.shape("images/enemyToFight_left.gif".replace("enemyToFight", self.enemy))
            dx = -20
            dy = 0
        elif self.direction == "right":
            self.shape("images/enemyToFight_right.gif".replace("enemyToFight", self.enemy))
            dx = 20
            dy = 0
        else:
            dx = 0
            dy = 0

        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(100, 300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

levels=[""]
 
level_1 = [
         "XXDXXXXXXXXXXXXXXXXXXXXXXXXXXX",
         "XXP XXXXXXXXXXXX      E XXXXXX",
         "XX  XXXXXXXXXXXX XX XXX XXXXXX",
         "XX          EXXX XX XXX XXXXXX",
         "X     XXXXXXXXXX XX XXX XXXXXX",
         "X  X XXXXX    E  XX XX   XXXXX",
         "X  X  XXXX XXXXX            EX",
         "X  XX    X XXXXX XXXXXE  XXX X",
         "X  XX XXXX XXXXX XXXXXX XXXX X",
         "X  XX    E XXXXX XXXXXX XXXX X",
         "X  XXXX XXXXXXXX        XXXX X",
         "X E   X XXXXXXXXXXXXXXXXXXXX X",
         "X     X     E      XX    E   X",
         "XXXXXXX XXXXXXXXXXXXX XXXXX  X",
         "XXXXXXX XXXXXXXXXXXXX XXXXX  X",
         "XXXTXXX    E       XX XXXXXE X",
         "XXX XXX XXXXXXXXXXXXX     XXXX",
         "XXX XXX X    E  E   XXXXX XXXX",
         "XXX XXX X       E   E    EXXXX",
         "XXX XXX X XX XXXXXXXXXXXX    X",
         "XXX XXX X XX    X     E   XX X",
         "XXX XXXXX XXXXXXXXX XXXXX XX X",
         "X X        E     XX XXXXX    X",
         "X XXXXXXXXXXXXXX XXXXXXXXXXXXX",
         "X    E                 E   XXX",
         "XXX XXXXXXXXXXXXXXXXXXXXXXXXXX",
         "XXX                       XXXX",
         "XXX XXXXXXXXXXXXXXXXXXXXX   EX",
         "XXX        E     XXXXXXXX    X",
         "XXXXXXXXXXXXXXXXTXXXXXXXXXXXXX"]
 
levels.append(level_1)
 
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            char=level[y][x]
            screen_x = -288 + (x*20)
            screen_y = 288 - (y*20)
            if char=="X":
                pen.shape("images/wall.gif")
                pen.goto(screen_x,screen_y)
                pen.stamp()
                walls.append((screen_x,screen_y))
            if char=='P':
                player.goto(screen_x,screen_y)
            if char == 'T':
                treasures.append(Treasure(screen_x, screen_y))
            if char == 'E':
                enemies.append(Enemy(screen_x, screen_y))
            if char == 'D':
                pen.shape("images/door.gif")
                pen.goto(screen_x,screen_y)
                pen.stamp()
                walls.append((screen_x,screen_y))
 
pen = Pen()
player = Player()
score = Draw_Score()
score.update_treasure(0)
walls = []
treasures = []
enemies = []
setup_maze(levels[1])
 
#Keyboard Binding
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.bullet_shoot, "space")

# draw_score()
 
wn.tracer(0,0)
 
def end_game():
    pen.hideturtle()
    pen.clear() 
    player.hideturtle()
    for treasure in treasures:
        treasure.destroy()
        # treasure.clear()
    for enemy in enemies:
        enemy.destroy()
        # enemy.clear()

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            score.update_treasure(treasure.gold)
            treasure.destroy()
            treasures.remove(treasure)

    for enemy in enemies:
        if player.is_collision(enemy):
            end_game()
            score.clear()
            score.goto(-75, 0)
            pen.shape("images/winning_pic.gif")
            pen.goto(-125, 15)
            pen.showturtle()
            score.write("Player Dies!", move=False, align="left", font=("Arial", 24, "normal"))

    if player.gold == 200:
        score.clear()
        score.goto(-75, 0)
        end_game()
        score.write("Player Wins!", move=False, align="left", font=("Arial", 24, "normal"))
        pen.shape("images/winning_pic.gif")
        pen.goto(-125, 15)
        pen.showturtle()
    wn.update()
