#this spaggeti code was made by  @w4ssim23


import turtle
import random
import winsound


#considering this a constant so we make the work easier
Ground = -180

# Set up the screen
wn = turtle.Screen()
wn.title("Definitely not that chrome game")
wn.bgcolor("black")
wn.setup(width=800, height=400)
wn.tracer(0)


# Set up the player
player = turtle.Turtle()
player.penup()
player.goto(-320, Ground)
player.color("white")
player.speed(0)
player.shape("square")
player.dy = 0



#setting up the score bar
score = 0
scoreprinter = turtle.Turtle()
scoreprinter.speed(0)
scoreprinter.penup()
scoreprinter.color("white")
scoreprinter.hideturtle()
scoreprinter.goto(0,150)



#creat start text  
start_text = turtle.Turtle()
start_text.speed(0)
start_text.color("white")
start_text.penup()
start_text.goto(0,-110)
start_text.hideturtle()
start_text.write("\t      Welcome to the game!\n\nIn this project, I've tried to implement the basics\nof the turtle model to create a game similar to the\none in Google Chrome\n\nUse the space bar to jump!\n\n\n\n\n\t     Press Enter to continue.", align="center", font=("Courier", 16, "normal"))






# FUNCTIONS




#to creat a brick
def brick_creator(x : int, y : int):
    b = turtle.Turtle()
    b.penup()
    b.goto(x, y)
    b.color("red")
    b.speed(0)
    b.shape("square")
    b.shapesize(stretch_wid=3, stretch_len=1)
    return b




def ScoreDetector_creator(x : int, y : int):
    b = turtle.Turtle()
    b.penup()
    b.goto(x, y)
    b.hideturtle()
    b.speed(0)
    return b


def brick_generator(bricks_list : list , scoredetect : list):
    x = random.randint(600, 670)
    bricks_list.append(brick_creator(x , Ground))
    scoredetect.append(ScoreDetector_creator(x , Ground +60))
    wn.ontimer(lambda: brick_generator(bricks_list,scoredetect), 1500)


def brick_trash(bricks_list : list , scoredetect : list) :
    if bricks_list[0].xcor() < -400 :
        bricks_list[0].hideturtle()
        bricks_list.pop(0)
        scoredetect.pop(0)
    wn.ontimer(lambda: brick_trash(bricks_list,scoredetect), 1000)
    


#simple collision logic
def is_collision(player : turtle, brick : turtle) -> bool:
    return  ( brick.xcor() -10 <= player.xcor() <= brick.xcor() + 10   and  player.ycor() < brick.ycor() + 40) 

def score_added(player : turtle, score_detector : turtle) -> bool:
    return player.distance(score_detector) < 10


#to check if the player is on the ground
def on_the_ground(player : turtle):
    return player.ycor() <= Ground




#making the jumping logic and system
#took me alot of time to find a solution , almost gave up man

#gravity logic
def gravity(player : turtle):
    if not on_the_ground(player):
        player.dy -= 0.2


def gravity_glitch_fixing(player : turtle):
    if player.ycor() < Ground : 
        player.sety(Ground)
        player.dy = 0    


#jump logic
def jump(player : turtle):
    if on_the_ground(player):
        player.dy = 5
        winsound.PlaySound("jump.wav",winsound.SND_ASYNC)

def jumping(player : turtle):
    wn.listen()
    wn.onkeypress(lambda: jump(player), "space")





def close_game(score,best_score,score_printer) : #fix this shit
    if score > best_score:
        best_score = score
        save_best_score(best_score)
    player.hideturtle()
    for b in bricks :
        b.hideturtle()
    wn.update()
    score_printer.clear()
    score_printer.goto(0,-120)
    score_printer.write(f"   You lost ! :(\n\nYour score was : {score}\n\n\n  click to exit.",align=("center") , font=("Courier",24,"normal"))
    turtle.exitonclick()   







# Game loop
def game_loop(bricks_list , detectors_list , score,bestscore):
    wn.update()

    for b in bricks_list:
        if is_collision(player, b):
            close_game(score,bestscore,scoreprinter)

    for b in detectors_list :
        if score_added(player,b) :
            score += 1
            scoreprinter.clear()
            scoreprinter.write(f"Score : {score}             Best Score : {best_score} ",align=("center") , font=("Courier",24,"normal"))

    gravity(player)
    gravity_glitch_fixing(player)

    player.sety(player.ycor() + player.dy)

    for brick in bricks_list:
        brick.setx(brick.xcor() - 2)

    for detect in detectors_list:
        detect.setx(detect.xcor() - 2)

    wn.ontimer(lambda: game_loop(bricks_list , detectors_list , score , best_score), 10)


def save_best_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def load_best_score():
    try:
        with open("score.txt", "r") as file:
            best_score = int(file.read())
            return best_score
    except :
        return 0






# Create a list of bricks
bricks = []
detectors = []
best_score = load_best_score()





def start_game():
    start_text.clear()
    scoreprinter.write(f"Score : {score}             Best Score : {best_score} ",align=("center") , font=("Courier",24,"normal"))  
    brick_generator(bricks, detectors)
    brick_trash(bricks, detectors)  
    jumping(player)
    game_loop(bricks, detectors, score,best_score)



wn.listen()
wn.onkeypress(start_game, "Return")
turtle.done()







