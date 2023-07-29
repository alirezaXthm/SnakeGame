from tkinter import *
import random

WIDTH = 600
HEIGHT = 600
SPEED = 5000
SPACE = 30
BODY_PARTS = 3
SNAKE_COLOR = '#24d671'
BAIT_COLOR = '#d62468'
BACKGROUND_COLOR = '#1c1e1f'


class Snake():
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE, y+SPACE, fill = SNAKE_COLOR, tag='snake')
            self.squares.append(square)


class Bait():
    def __init__(self):
        x = (random.randint(0, WIDTH/SPACE-1)) * SPACE
        y = (random.randint(0, HEIGHT/SPACE-1)) * SPACE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x+SPACE, y+SPACE , fill=BAIT_COLOR, tag = 'bait')


def next_turn(snake, bait):
    x, y = snake.coordinates[0]
    if direction == 'up':
        y -= SPACE
    elif direction == 'down':
        y += SPACE
    elif direction == 'left':
        x -= SPACE
    elif direction == 'right':
        x += SPACE
    print(x,y, x+SPACE, y+SPACE)

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x,y, x+SPACE, y+SPACE, fill = SNAKE_COLOR)
    print()
    snake.squares.insert(0, square)

    
    if x == bait.coordinates[0] and y == bait.coordinates[1]:
        global score
        score += 1
        
        score_label.config(text=f'Score:{score}')
        
        canvas.delete('bait')
        
        bait = Bait()

    else:
        
        snake.coordinates.pop(-1)
        canvas.delete(snake.squares[-1])
        snake.squares.pop(-1)

    
    if check_collisions(snake):
        game_over()
        
    else:
        window.after(SPEED, next_turn, snake, bait)




def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= WIDTH:
        return True
    if y < 0 or y >= HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(300, 100, font=('consolas', 50), text='GAME OVER', fill = 'red', tag='game_over')


window = Tk()
window.title("Dumb Snake")
window.resizable(False, False)
window_width = WIDTH
window_height = HEIGHT
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


canvas = Canvas(window, bg = BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

score = 0
direction = 'down'

score_label = Label(window, text = f"Score:{score}", font=('airal', 20))
score_label.pack()

snake = Snake()
bait = Bait()

next_turn(snake, bait)

window.mainloop()