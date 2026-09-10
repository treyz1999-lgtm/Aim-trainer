import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #initialize a pygame window
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400 #this is how fast we want the targets to appear; update in the future to allow for UI sliders
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30
BG_COLOR = pygame.Color(0,25,40) #this might be adjustable by the user in the future as well

#make a Target class that will have all the behavior and functionality for the onscreen targets
class Target:
    MAX_SIZE = 30 #this is how large the target can grow to - will likely make this adjustable via a slider or something in the future
    GROWTH_RATE = 0.2 #how fast the target grows - again we can use sliders in a future update
    COLOR1 = "red" #what color we want it to be
    COLOR2 = "white"
    OUTLINE = "black"
    RINGS = (
        (OUTLINE, 1.0),
        (COLOR1, 0.90),
        (OUTLINE, 0.85),
        (COLOR2, 0.80),
        (OUTLINE, 0.75),
        (COLOR1, 0.60),
        (OUTLINE, 0.55),
        (COLOR2, 0.40),
        (OUTLINE, 0.35),
        (COLOR2, 0.30),
    )

    def __init__(self, x, y): #x,y are the positions to place the target
        self.x = x
        self.y = y
        self.size = 0 #radius of target
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: #we need to begin shrinking
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        #Draw from largest to smallest so each black ring becomes an outline between sections.
        for color, scale in self.RINGS:
            pygame.draw.circle(win, color, (self.x, self.y), self.size * scale)

    def collide(self, x, y):
       dis = math.sqrt( (self.x - x)**2 + (self.y - y)**2)
       return dis <= self.size

#create the main program loop
def draw(win, targets):
    #you need to clear the screen then draw the objects on it and update the display, and we do this every frame - frame by frame rendering
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    pygame.display.update()




def main():
    run = True
    targets = [] #store all the target objects
    clock = pygame.time.Clock() #fixed frame rate

    target_hits = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) #trigger the event every x ms

    while run:
        clock.tick(60)
        click = False #if the user clicks we set this to true
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get(): #loop through all events occurring
            if event.type == pygame.QUIT:
                run = False
                break # this lets you actually click the x button and close the app

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING) #this will ensure the targets do not appear off the screen
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)  #new target object
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks +=1

        #update targets before you draw them
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target) #clean up for performance
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_hits += 1

        draw(WIN, targets)

    pygame.quit()


if __name__ == "__main__":
    main()
