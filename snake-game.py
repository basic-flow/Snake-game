from tkinter import *
import random
import os

GAME_WIDTH = 1000
GAME_HEIGHT = 500
SPEED = 10
SPACE_SIZE = 10
BODY_PARTS = 3
SNAKE_COLOR = "#43eb34"
FOOD_COLOR = "red"
BACKGOUND_COLOR = "black"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y,x+SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0,int((GAME_WIDTH/SPACE_SIZE)-1))* SPACE_SIZE
        y = random.randint(0,int((GAME_HEIGHT/SPACE_SIZE)-1))* SPACE_SIZE
        self.coordinates = [x,y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR,tag="food")

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]
    
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down": 
        y += SPACE_SIZE   
    elif direction == "left":
        x -= SPACE_SIZE        
    elif direction == "right":
        x += SPACE_SIZE       
    
    snake.coordinates.insert(0,(x,y))
    
    square = canvas.create_rectangle(x,y, x+ SPACE_SIZE,y + SPACE_SIZE,fill = SNAKE_COLOR)
    
    snake.squares.insert(0, square)
    
    if x== food.coordinates[0] and y ==food.coordinates[1]:
        
        global score
        
        score += 1
        
        label.config(text="Score : {}".format(score))
        
        canvas.delete("food")
        
        food = Food()
        
    else:
        del snake.coordinates[-1]
    
        canvas.delete(snake.squares[-1])
    
        del snake.squares[-1]  
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn,snake,food)

def change_direction(new_directioon):
    global direction
    
    if new_directioon == 'left':
        if direction != 'right':
            direction = new_directioon
    elif new_directioon == 'right':
        if direction != 'left':
            direction = new_directioon
    elif new_directioon == 'up':
        if direction != 'down':
            direction = new_directioon
    elif new_directioon == 'down':
        if direction != 'up':
            direction = new_directioon

def check_collisions(snake):
    x,y = snake.coordinates[0]
    
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 100,font=('Arial',70), text='GAME OVER',fill='red',tag ='game')
    play_again_button = Button(
        window,
        text="Play Again",
        font=('Arial', 30),
        bg="red",  
        fg="black",   
        activebackground="red",  
        activeforeground="black",
        command=reset_game
    )
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 50,
        window=play_again_button,
        tag='play_again_button'
    )

def reset_game():
    global snake, food, score, direction
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)
    
def pulse_food():
    canvas.itemconfig("food", fill="yellow")
    window.after(200, lambda: canvas.itemconfig("food", fill=FOOD_COLOR))
    window.after(400, pulse_food)

window = Tk()
window.config(bg='black')
window.title("Snake game")
window.resizable(False,False)
try:
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "snake.png")
    if os.path.exists(icon_path):
        window.iconphoto(True, PhotoImage(file=icon_path))
    else:
        print("Icon file not found, using default icon")
except Exception as e:
    print(f"Could not load window icon: {e}")




score = 0
direction = 'down'

label = Label(window,fg='white',bg='black',text="Score : {}".format(score), font=('Arial',40))
label.pack()

canvas = Canvas(window, bg = BACKGOUND_COLOR, height=GAME_HEIGHT,width=GAME_WIDTH)
canvas.pack()


window.bind('<a>', lambda ebent: change_direction('left'))
window.bind('<d>', lambda ebent: change_direction('right'))
window.bind('<w>', lambda ebent: change_direction('up'))
window.bind('<s>', lambda ebent: change_direction('down'))



snake = Snake()
food = Food()
pulse_food()
next_turn(snake,food)

window.mainloop()