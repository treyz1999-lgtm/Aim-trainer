import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #initialize a pygame window
pygame.display.set_caption("Aim Trainer")

#create the main program loop
def main():
    run = True
    while run:
        for event in pygame.event.get(): #loop through all events occurring
            if event.type == pygame.QUIT:
                run = False
                break # this lets you actually click the x button and close the app

    pygame.quit()


if __name__ == "__main__":
    main()