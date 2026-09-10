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

INFO_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("Arial", 16, bold= True)
SMALL_FONT = pygame.font.SysFont("Arial", 14, bold= True)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 48, bold= True)

SETTINGS_BUTTON = pygame.Rect(WIDTH - 95, 10, 85, 30)
SETTINGS_PANEL = pygame.Rect(180, 85, 440, 430)
COLOR_OPTIONS = [
    ("Red", "red"),
    ("White", "white"),
    ("Blue", "blue"),
    ("Green", "green"),
    ("Yellow", "yellow"),
    ("Purple", "purple"),
    ("Orange", "orange"),
    ("Black", "black"),
]
INFO_BAR_COLOR_OPTIONS = [option for option in COLOR_OPTIONS if option[1] != "black"]
BACKGROUND_COLOR_OPTIONS = [
    ("Navy", pygame.Color(0,25,40)),
    ("Blue", "blue"),
    ("Green", "green"),
    ("Purple", "purple"),
    ("Gray", "gray"),
    ("White", "white"),
]

def get_default_settings():
    return {
        "color1": "red",
        "color2": "white",
        "outline": "black",
        "background": pygame.Color(0,25,40),
        "info_bar": "white",
        "spawn_rate": TARGET_INCREMENT,
        "target_size": 30,
        "lives": 10,
    }

#make a Target class that will have all the behavior and functionality for the onscreen targets
class Target:
    GROWTH_RATE = 0.2 #how fast the target grows - again we can use sliders in a future update
    RING_PATTERN = (
        ("outline", 1.0),
        ("color1", 0.90),
        ("outline", 0.85),
        ("color2", 0.80),
        ("outline", 0.75),
        ("color1", 0.60),
        ("outline", 0.55),
        ("color2", 0.40),
        ("outline", 0.35),
        ("color2", 0.30),
    )

    def __init__(self, x, y): #x,y are the positions to place the target
        self.x = x
        self.y = y
        self.size = 0 #radius of target
        self.grow = True

    def update(self, target_size):
        if self.size + self.GROWTH_RATE >= target_size: #we need to begin shrinking
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win, settings):
        #Draw from largest to smallest so each black ring becomes an outline between sections.
        for color_key, scale in self.RING_PATTERN:
            pygame.draw.circle(win, settings[color_key], (self.x, self.y), self.size * scale)

    def collide(self, x, y):
       dis = math.sqrt( (self.x - x)**2 + (self.y - y)**2)
       return dis <= self.size

#create the main program loop
def draw(win, targets, settings):
    #you need to clear the screen then draw the objects on it and update the display, and we do this every frame - frame by frame rendering
    win.fill(settings["background"])

    for target in targets:
        target.draw(win, settings)



def format_time(seconds):
    milliseconds = math.floor(int(seconds * 1000 % 1000) / 100)
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f'{minutes: 02d} : {seconds: 02d} : {milliseconds: 02d}'

def draw_info_bar(win, elapsed_time, target_hits, misses, settings, settings_open):
    pygame.draw.rect(win, settings["info_bar"], (0,0, WIDTH, INFO_BAR_HEIGHT))
    hits_per_second = target_hits / elapsed_time if elapsed_time > 0 else 0
    lives_remaining = max(0, settings["lives"] - misses)

    labels = [
        (f'Time: {format_time(elapsed_time)}', 5),
        (f'Hits: {target_hits}', 160),
        (f'Speed: {hits_per_second:.2f}/s', 235),
        (f'Misses: {misses}', 355),
        (f'Lives: {lives_remaining}', 455),
        ('Esc/Space: Restart', 545),
    ]

    for text, x in labels:
        label = LABEL_FONT.render(text, True, 'black')
        y = (INFO_BAR_HEIGHT - label.get_height()) // 2
        win.blit(label, (x, y))

    button_color = "lightblue" if settings_open else "lightgray"
    pygame.draw.rect(win, button_color, SETTINGS_BUTTON, border_radius=4)
    pygame.draw.rect(win, "black", SETTINGS_BUTTON, 2, border_radius=4)
    button_label = SMALL_FONT.render("Settings", True, "black")
    button_x = SETTINGS_BUTTON.centerx - button_label.get_width() // 2
    button_y = SETTINGS_BUTTON.centery - button_label.get_height() // 2
    win.blit(button_label, (button_x, button_y))


def draw_game_over(win, elapsed_time, target_hits, misses, settings, settings_open):
    draw(win, [], settings)
    draw_info_bar(win, elapsed_time, target_hits, misses, settings, settings_open)

    game_over_label = GAME_OVER_FONT.render('Game Over', True, 'white')
    message_label = LABEL_FONT.render('Press Esc or Space to restart', True, 'white')

    game_over_x = (WIDTH - game_over_label.get_width()) // 2
    game_over_y = (HEIGHT - game_over_label.get_height()) // 2 - 30
    message_x = (WIDTH - message_label.get_width()) // 2
    message_y = game_over_y + game_over_label.get_height() + 15

    win.blit(game_over_label, (game_over_x, game_over_y))
    win.blit(message_label, (message_x, message_y))
    pygame.display.update()


def reset_game():
    return {
        "targets": [],
        "target_hits": 0,
        "clicks": 0,
        "misses": 0,
        "start_time": time.time(),
        "game_over": False,
        "end_time": None,
        "pause_start": None,
    }


def set_spawn_timer(settings):
    pygame.time.set_timer(TARGET_EVENT, settings["spawn_rate"])


def pause_game(game_state):
    if game_state["pause_start"] is None:
        game_state["pause_start"] = time.time()
    pygame.time.set_timer(TARGET_EVENT, 0)


def resume_game(game_state, settings):
    if game_state["pause_start"] is not None:
        game_state["start_time"] += time.time() - game_state["pause_start"]
        game_state["pause_start"] = None

    if not game_state["game_over"]:
        set_spawn_timer(settings)


def get_color_label(color, options):
    for label, option_color in options:
        if color == option_color:
            return label
    return str(color)


def get_next_color(color, options):
    color_values = [option_color for _, option_color in options]
    if color not in color_values:
        return color_values[0]

    current_index = color_values.index(color)
    return color_values[(current_index + 1) % len(color_values)]


def get_color_controls():
    return [
        ("color1", "Color 1", COLOR_OPTIONS, pygame.Rect(410, 160, 150, 28)),
        ("color2", "Color 2", COLOR_OPTIONS, pygame.Rect(410, 200, 150, 28)),
        ("outline", "Outline", COLOR_OPTIONS, pygame.Rect(410, 240, 150, 28)),
        ("background", "Background", BACKGROUND_COLOR_OPTIONS, pygame.Rect(410, 280, 150, 28)),
        ("info_bar", "Info Bar", INFO_BAR_COLOR_OPTIONS, pygame.Rect(410, 320, 150, 28)),
    ]


def get_slider_controls():
    return [
        ("spawn_rate", "Spawn Rate", 100, 2000, 50, "ms", pygame.Rect(390, 380, 160, 8)),
        ("target_size", "Target Size", 10, 80, 1, "px", pygame.Rect(390, 420, 160, 8)),
        ("lives", "Lives", 1, 20, 1, "", pygame.Rect(390, 460, 160, 8)),
    ]


def get_slider_value(mouse_x, slider_rect, min_value, max_value, step):
    percent = (mouse_x - slider_rect.left) / slider_rect.width
    percent = max(0, min(1, percent))
    value = min_value + percent * (max_value - min_value)
    value = round(value / step) * step
    return int(max(min_value, min(max_value, value)))


def draw_settings_panel(win, settings):
    pygame.draw.rect(win, "white", SETTINGS_PANEL, border_radius=6)
    pygame.draw.rect(win, "black", SETTINGS_PANEL, 2, border_radius=6)

    title = LABEL_FONT.render("Settings", True, "black")
    win.blit(title, (SETTINGS_PANEL.x + 20, SETTINGS_PANEL.y + 18))

    hint = SMALL_FONT.render("Changing a setting restarts the game", True, "black")
    win.blit(hint, (SETTINGS_PANEL.x + 20, SETTINGS_PANEL.y + 42))

    for key, label_text, options, rect in get_color_controls():
        label = LABEL_FONT.render(label_text, True, "black")
        win.blit(label, (SETTINGS_PANEL.x + 35, rect.y + 5))

        pygame.draw.rect(win, settings[key], rect, border_radius=4)
        pygame.draw.rect(win, "black", rect, 2, border_radius=4)
        text_color = "white" if settings[key] == "black" else "black"
        value_label = SMALL_FONT.render(get_color_label(settings[key], options), True, text_color)
        value_x = rect.centerx - value_label.get_width() // 2
        value_y = rect.centery - value_label.get_height() // 2
        win.blit(value_label, (value_x, value_y))

    for key, label_text, min_value, max_value, step, unit, rect in get_slider_controls():
        value = settings[key]
        label = LABEL_FONT.render(f"{label_text}: {value}{unit}", True, "black")
        win.blit(label, (SETTINGS_PANEL.x + 35, rect.y - 10))

        pygame.draw.rect(win, "gray", rect, border_radius=4)
        percent = (value - min_value) / (max_value - min_value)
        knob_x = rect.left + int(percent * rect.width)
        knob = pygame.Rect(0, 0, 14, 24)
        knob.center = (knob_x, rect.centery)
        pygame.draw.rect(win, "lightblue", knob, border_radius=4)
        pygame.draw.rect(win, "black", knob, 2, border_radius=4)


def handle_settings_event(event, settings):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for key, _, options, rect in get_color_controls():
            if rect.collidepoint(event.pos):
                settings[key] = get_next_color(settings[key], options)
                return True

    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
        if event.type == pygame.MOUSEMOTION and not event.buttons[0]:
            return False

        for key, _, min_value, max_value, step, _, rect in get_slider_controls():
            if rect.inflate(20, 24).collidepoint(event.pos):
                new_value = get_slider_value(event.pos[0], rect, min_value, max_value, step)
                if settings[key] != new_value:
                    settings[key] = new_value
                    return True

    return False


def main():
    run = True
    clock = pygame.time.Clock() #fixed frame rate
    settings = get_default_settings()
    game_state = reset_game()
    settings_open = False

    set_spawn_timer(settings) #trigger the event every x ms

    while run:
        clock.tick(60)
        click = False #if the user clicks we set this to true
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get(): #loop through all events occurring
            if event.type == pygame.QUIT:
                run = False
                break # this lets you actually click the x button and close the app

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                game_state = reset_game()
                if settings_open:
                    pause_game(game_state)
                else:
                    set_spawn_timer(settings)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if SETTINGS_BUTTON.collidepoint(event.pos):
                    settings_open = not settings_open
                    if settings_open:
                        pause_game(game_state)
                    else:
                        resume_game(game_state, settings)
                    continue

                if settings_open:
                    settings_changed = handle_settings_event(event, settings)
                    if settings_changed:
                        game_state = reset_game()
                        pause_game(game_state)
                    continue

                click = True
                game_state["clicks"] +=1

            if settings_open and event.type == pygame.MOUSEMOTION:
                settings_changed = handle_settings_event(event, settings)
                if settings_changed:
                    game_state = reset_game()
                    pause_game(game_state)

            if event.type == TARGET_EVENT and not game_state["game_over"] and not settings_open:
                spawn_padding = max(TARGET_PADDING, settings["target_size"])
                x = random.randint(spawn_padding, WIDTH - spawn_padding) #this will ensure the targets do not appear off the screen
                y = random.randint(INFO_BAR_HEIGHT + spawn_padding, HEIGHT - spawn_padding)
                target = Target(x, y)  #new target object
                game_state["targets"].append(target)

        if game_state["game_over"]:
            elapsed_time = game_state["end_time"]
        elif settings_open and game_state["pause_start"] is not None:
            elapsed_time = game_state["pause_start"] - game_state["start_time"]
        else:
            elapsed_time = time.time() - game_state["start_time"]

        #update targets before you draw them
        if not game_state["game_over"] and not settings_open:
            for target in game_state["targets"][:]:
                target.update(settings["target_size"])

                if target.size <= 0:
                    game_state["targets"].remove(target) #clean up for performance
                    game_state["misses"] += 1
                    continue

                if click and target.collide(*mouse_pos):
                    game_state["targets"].remove(target)
                    game_state["target_hits"] += 1

        if game_state["misses"] >= settings["lives"] and not game_state["game_over"]:
            game_state["game_over"] = True
            game_state["end_time"] = elapsed_time
            game_state["targets"] = []
            pygame.time.set_timer(TARGET_EVENT, 0)

        if settings_open:
            draw(WIN, [], settings)
            draw_info_bar(
                WIN,
                elapsed_time,
                game_state["target_hits"],
                game_state["misses"],
                settings,
                settings_open,
            )
            draw_settings_panel(WIN, settings)
            pygame.display.update()
        elif game_state["game_over"]:
            draw_game_over(
                WIN,
                elapsed_time,
                game_state["target_hits"],
                game_state["misses"],
                settings,
                settings_open,
            )
        else:
            draw(WIN, game_state["targets"], settings)
            draw_info_bar(
                WIN,
                elapsed_time,
                game_state["target_hits"],
                game_state["misses"],
                settings,
                settings_open,
            )
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
