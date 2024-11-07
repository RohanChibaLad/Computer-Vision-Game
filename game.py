import pygame
import sys
import random
import cv2
import mediapipe as mp

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)

# Screen dimensions
WIDTH, HEIGHT = 1280, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
pygame.display.set_caption("Simple Pygame Window")

# Colors
# Base Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Combo Colours
GREY = (155, 155, 155)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (155, 0, 255)
ORANGE = (255, 155, 0)
TEAL = (0, 255, 155)
BROWN = (131, 61, 23)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)
LIVES_RED = (181, 18, 1)

# Colours for Combo
COMBO_COLOURS = [
    BROWN,
    RED,
    ORANGE,
    YELLOW,
    GREEN,
    TEAL,
    CYAN,
    BLUE,
    PURPLE,
    INDIGO,
    VIOLET,
    PINK,
]

# Camera Initialisation
video = cv2.VideoCapture(1) #Camera index may change, was 1 for me in testing, maybe 0 if you need to use it
if not video.isOpened():
    print("Unable to open camera")

# Handtracking
mpHands = mp.solutions.hands
mpDrawing = mp.solutions.drawing_utils
hands = mpHands.Hands(max_num_hands=2)

# Class for the fruit objects
class Fruit():
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        self.name = "Fruit"
        self.initial_speed = initial_speed  # Initial speed of the fruit
        self.speed = initial_speed  # Current speed of the fruit
        self.xSpeed = random.choice([-1, 1])  # Direction of the fruit
        self.width, self.height = width, height
        self.maxHeight = random.randint(HEIGHT // 4, HEIGHT // 2)  # Height of the fruit
        #self.rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT, width, height)  # Random position
        self.falling = False  # Flag to indicate if the fruit is falling
        self.acceleration = -0.045  # Acceleration due to gravity
        self.frozen = False  # Determines if the fruit is frozen or not
        self.visible = True  # Used to show whether we should draw the fruit or not
        self.hit = False  # If the fruits been hit or not
        self.netActivated = netActivated  # If the net is active or not

        self.x = random.randint(0, WIDTH - 20)
        self.y = HEIGHT

    def update(self):
        if not self.frozen or self.hit:  # Only move if it isn't frozen or if it's been hit
            self.rect.x += self.xSpeed
            if not self.falling:
                # Move the fruit up until it reaches its maximum height
                if self.rect.y >= self.maxHeight:
                    self.rect.y -= self.speed
                    self.speed += self.acceleration  # Decrease speed as it reaches the apex
                else:
                    self.falling = True  # Change direction once it reaches max height
                    self.speed -= self.acceleration  # Reset speed for falling motion
            else:
                if not self.netActivated or self.hit:  # If the safety net is not activated
                    self.rect.y += self.speed
                    self.speed -= self.acceleration
                else:  # If the safety net is activated
                    if self.rect.bottom < HEIGHT - 100 or self.hit:  # If the fruit is above the net
                        self.rect.y += self.speed
                        self.speed -= self.acceleration
                    else:  # If the fruit is on or below the net
                        if self.hit:
                            self.frozen = False
                            self.speed = self.initial_speed
                        self.rect.y = HEIGHT - 100 - self.height
                        self.speed = 0
                        self.xSpeed = 0
                        self.frozen = True

        # print(self.rect.top)
        # print(self.maxHeight)

class Apple(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated)
        self.colour = GREEN
        self.fruit = "Apple"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 600, 1650, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)

class Orange(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated)
        self.colour = ORANGE
        self.fruit = "Orange"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 600, 0, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 2300, 1650, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)

class Banana(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated)
        self.colour = YELLOW
        self.fruit = "Banana"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 550, 1100, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 550, 1100, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(WHITE)
class Strawberry(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated=False)
        self.colour = GREY
        self.fruit = "Strawberry"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 1100, 550, 600, 550)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 1650, 1100, 600, 550)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)

class Watermelon(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated)
        self.colour = PINK
        self.fruit = "Watermelon"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 3400, 0, 600, 550)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 1650, 550, 600, 550)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)


class Mango(Fruit):
    def __init__(self, initial_speed, width, height, netActivated=False):  # Initalizes the object
        super().__init__(initial_speed, width, height, netActivated)
        self.colour = BROWN
        self.fruit = "Mango"
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/fruits.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 550, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def updateImage(self):
        self.image = get_image(self.sprite_sheet, 0, 1650, 600, 550)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)


# Class for the bomb object
class Bomb():
    def __init__(self, initial_speed, invisible=False, netActivated=False):  # Initalizes the object
        self.name = "Bomb"
        self.colour = RED  # Colour of the rectangle
        self.initial_speed = initial_speed  # Initial speed of the fruit
        self.speed = initial_speed  # Current speed of the fruit
        self.xSpeed = random.choice([-1, 1])  # Direction of the fruit
        self.width, self.height = 50, 50
        self.maxHeight = random.randint(HEIGHT // 4, HEIGHT // 2)  # Height of the fruit
        #self.rect = pygame.Rect(random.randint(0, WIDTH - 20), HEIGHT, 50, 50)  # Random position
        self.falling = False  # Flag to indicate if the fruit is falling
        self.acceleration = -0.045  # Acceleration due to gravity
        self.frozen = False  # Shows whether the bomb is frozen or not
        self.visible = True  # Tell us whether we should draw it or not
        self.invisible = invisible  # Used for the powerup
        # IMAGE
        self.sprite_sheet = pygame.image.load("Images/bomb.png").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 256, 256)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale down to match bomb size
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20)
        self.rect.y = HEIGHT

    def update(self):  # Updates the position of the fruit
        if not self.frozen:  # If its not frozen, move it
            self.rect.x += self.xSpeed
            if not self.falling:
                # Move the fruit up until it reaches its maximum height
                if self.rect.y >= self.maxHeight:
                    self.rect.y -= self.speed
                    self.speed += self.acceleration  # Decrease speed as it reaches the apex
                else:
                    self.falling = True  # Change direction once it reaches max height
                    self.speed -= self.acceleration  # Reset speed for falling motion
            else:
                # Move the fruit down off the screen
                self.rect.y += self.speed
                self.speed -= self.acceleration  # Increase speed as it falls due to gravity


# Class for the game instance
class Game:
    def __init__(self):
        # Init function
        # Initialises the variables needed in displaying the combo and score
        # Also initialises the things needed for calculating in updating
        self.font = pygame.font.SysFont("Arial", 32)
        self.font2 = pygame.font.SysFont("Arial", 16)
        # Default values
        self.score = 0
        self.comboCounter = 0
        self.comboMultiplier = 1
        self.comboText = 'Combo: ' + str(self.comboCounter)
        self.multiplierText = ''
        self.double = False
        self.lives = 10

    def updateCombo(self, hit):
        # Updates the combo based on whether True or False is passed in
        if hit:
            # If a fruit is hit, it adds 1 to the counter
            # The multiplier increases every 20 consecutive hits ~ 13 levels with a different color for each level
            self.comboCounter += 1
            if self.comboCounter > 1:
                self.comboMultiplier = min(self.comboCounter // 10 + 1, len(COMBO_COLOURS))
            self.multiplierText = 'x' + str(self.comboMultiplier)
        else:
            # If they have missed a fruit, resets everything
            self.comboCounter = 0
            self.comboMultiplier = 1
            self.multiplierText = ''

        self.comboText = 'Combo: ' + str(self.comboCounter)

    def updateScore(self, val):
        # Updates the score with the value sent
        print(self.comboMultiplier)
        if self.double:
            self.score += val * self.comboMultiplier * 2
        else:
            self.score += val * self.comboMultiplier

    def displayScore(self):
        score_text = 'Score: ' + str(self.score)
        textSurface = self.font.render(score_text, True, WHITE)
        textRect = textSurface.get_rect()
        textRect.midtop = (WIDTH // 2, 30)
        drawTextWithOutline(self.font, score_text, WHITE, GREY, textRect.left, textRect.top)

    def displayCombo(self):
        combo_text = 'Combo: ' + str(self.comboCounter)
        textSurface = self.font.render(combo_text, True, WHITE)
        textRect = textSurface.get_rect()
        textRect.midtop = (WIDTH // 2, 80)
        drawTextWithOutline(self.font, combo_text, WHITE, GREY, textRect.left, textRect.top)

        if self.comboCounter == 0:
            multiplier_text = self.multiplierText
            color = BROWN
        else:
            multiplier_text = self.multiplierText
            color = COMBO_COLOURS[min(self.comboMultiplier, len(COMBO_COLOURS) - 1)]

        textSurface = self.font2.render(multiplier_text, True, color)
        textRect = textSurface.get_rect()
        textRect.midbottom = (WIDTH // 2, 110)
        drawTextWithOutline(self.font2, multiplier_text, color, GREY, textRect.left, textRect.top)

    def displayLives(self):
        lives_text = 'Lives Left: ' + str(self.lives)
        textSurface = self.font.render(lives_text, True, WHITE)
        textRect = textSurface.get_rect()
        textRect.midtop = (WIDTH * 3.5 // 4, 30)
        drawTextWithOutline(self.font, lives_text, WHITE, GREY, textRect.left, textRect.top)

# Parent class for powerups
class Powerups():
    def __init__(self, time):
        self.name = "Powerup"
        self.active = False
        self.width, self.height = 50, 50
        #self.rect = pygame.Rect(random.randint(0, WIDTH - 20), 0, self.width, self.height)  # Random position
        self.startTime = time
        self.currentTime = time
        self.teleport_timer = 0
        self.teleport_interval = 1000
        self.last_teleport_time = 0
        self.visible = True  # Shows whether we should draw the powerup or not

        self.x = random.randint(0, WIDTH - 20)
        self.y = HEIGHT // 4

    def updateTime(self, time):
        self.currentTime = time

    def activate(self):  # Activates the powerup
        self.active = True
        self.visible = False  # No longer draw the powerup on the screen

    def deactivate(self):  # Deactivates the powerup
        self.active = False

    def update(self):
        if not self.active:  # Powerups only move around if they havnt been activated yet
            current_time = pygame.time.get_ticks()

            # Teleport if enough time has elapsed since the last teleport
            if current_time - self.last_teleport_time >= self.teleport_interval:
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                self.rect.y = random.randint(0, HEIGHT - self.rect.height)
                self.last_teleport_time = current_time  # Update last teleport time


class Freeze(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "Freeze"
        self.colour = TEAL
        #Image
        self.sprite_sheet = pygame.image.load("Images/powerups.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 1000, 1000)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Invisibility(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "Invisibility"
        self.colour = WHITE
        # Image
        self.sprite_sheet = pygame.image.load("Images/bombPowerup.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 1920, 1536)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class DoublePoints(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "Double Points"
        self.colour = YELLOW
        # Image
        self.sprite_sheet = pygame.image.load("Images/powerups.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 900, 900, 1000, 1000)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class SafetyNet(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "Safety Net"
        self.colour = GREY
        self.netVisible = False
        # Image
        self.sprite_sheet = pygame.image.load("Images/powerups.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 900, 1000, 1000)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def drawNet(self, screen):
        self.visible = True
        self.rect = pygame.Rect(0, HEIGHT - 100, WIDTH, 30)
        self.colour = WHITE
        pygame.draw.rect(screen, self.colour, self.rect)  # Draws where the hands are on the screen
        # Image
        self.sprite_sheet = pygame.image.load("Images/net.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 1920, 1440)
        self.image = pygame.transform.scale(self.image, (WIDTH, 30))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 100


class TimeSlow(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "Time Slow"
        self.colour = BROWN
        # Image
        self.sprite_sheet = pygame.image.load("Images/powerups.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 900, 0, 1000, 1000)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RegenLives(Powerups):  # Child of powerup class
    def __init__(self, time):
        super().__init__(time)
        self.type = "RegenLives"
        self.colour = LIVES_RED
        # Image
        self.sprite_sheet = pygame.image.load("Images/heart.jpg").convert_alpha()
        self.image = get_image(self.sprite_sheet, 0, 0, 5000, 5000)
        self.image = pygame.transform.scale(self.image, (75, 75))  # Scale down to match bomb size
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Knife():
    def __init__(self):
        #  Knife
        self.knifeSheet = pygame.image.load("Images/knife.jpg").convert_alpha()
        self.knife = get_image(self.knifeSheet, 0, 0, 1920, 1440)
        self.knife = pygame.transform.scale(self.knife, (75, 75))  # Scale down to match bomb size
        self.knife.set_colorkey(WHITE)
        self.rect = self.knife.get_rect()

    def drawKnife(self, center):
        self.rect.center = center
        SCREEN.blit(self.knife, self.rect.center)

def get_image(sheet, x, y, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    return image

def draw_countdown(seconds):
    font = pygame.font.SysFont("Arial", 72)
    textSurface = font.render(str(seconds), True, WHITE)
    textRect = textSurface.get_rect()
    textRect.midtop = (WIDTH // 2, HEIGHT // 2)
    drawTextWithOutline(font, seconds, WHITE, BLACK, textRect.left, textRect.top)

def drawTextWithOutline(font, text, textColour, outlineColour, x, y):
    textSurface = font.render(str(text), True, textColour)
    outlineSurface = font.render(str(text), True, outlineColour)

    # Create a slightly larger rectangular surface for the outline
    outline_rect = outlineSurface.get_rect()
    outline_rect.inflate_ip(2, 2)  # Increase the size by 2 pixels on each side

    # Create a surface with a transparent background
    surface = pygame.Surface(outline_rect.size, pygame.SRCALPHA)

    # Draw the outline text first
    surface.blit(outlineSurface, (0, 0))

    # Draw the actual text on top of the outline
    surface.blit(textSurface, (2, 2))  # Offset by 2 pixels for the outline

    SCREEN.blit(surface, (x, y))

def game():
    clock = pygame.time.Clock()  # Initialises the clock
    game = Game()  # Instance of the game
    knife = Knife()
    items = []  # List to store fruit objects
    exploded = False
    powerupCount = 0
    startTime, currentTime = 0, 0  # Used later for powerups
    invisible = False
    netActivated = False
    slow = False  # Used to see if the slow powerup is activated or not
    bg = pygame.image.load("Images/gameBG.jpg")
    bg = pygame.transform.scale(bg, (1280, 800))  # Scale down to match bomb size
    countdown = 5

    # Countdown loop
    while countdown > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(bg, (0, 0))
        # Draw countdown
        draw_countdown(countdown)
        pygame.display.flip()

        # Wait for 1 second
        pygame.time.wait(1000)

        countdown -= 1

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capturing frames
        success, frame = video.read()
        if not success:
            print("Error: Unable to capture frames from the camera.")

        if success:
            # Resize the frame to a smaller size
            frame = cv2.resize(frame, (380, 216))  # New size: 190x108
            # Convert the frame to RGB (Pygame uses RGB)
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Flipping the frame
            flippedFrame = cv2.flip(rgbFrame, 1)

            tracking = hands.process(flippedFrame)

            # Used for finding center postion
            xCentre = 0
            yCentre = 0
            numLandmarks = 0

            # Stores the center coordinates
            handCenters = []

            if tracking.multi_hand_landmarks:
                handCenters = []  # Resets for each frame
                for hand_landmarks in tracking.multi_hand_landmarks:
                    # Reset center coordinates for each hand
                    xCentre = 0
                    yCentre = 0
                    numLandmarks = 0

                    # Converting hand landmarks to pixels
                    for landmark in hand_landmarks.landmark:
                        xCoordinate, yCoordinate = landmark.x, landmark.y

                        # Setting the boundaries of the landmarks
                        xCoordinate = max(0.0, min(1.0, xCoordinate))
                        yCoordinate = max(0.0, min(1.0, yCoordinate))

                        # Pixel Conversion
                        xPixel = round(xCoordinate * rgbFrame.shape[1])
                        yPixel = round(yCoordinate * rgbFrame.shape[0])

                        # Increment the center coordinates
                        xCentre += xPixel
                        yCentre += yPixel
                        numLandmarks += 1

                    # Converting to pixels
                    if numLandmarks > 0:
                        # Calculate the average center position
                        xCentre = round(xCentre / numLandmarks)
                        yCentre = round(yCentre / numLandmarks)

                        # Convert center coordinates to pixel positions relative to the pygame window
                        pixelX = int((xCentre / 380) * WIDTH)  # 190 is the width of the resized frame
                        pixelY = int((yCentre / 216) * HEIGHT)  # 108 is the height of the resized frame

                        handCenters.append((pixelX, pixelY))

                        # print("Center of the hand (pixels): (", pixel_x, ", ", pixel_y, ")")

                        # Draw landmarks on the flipped frame
                        mpDrawing.draw_landmarks(flippedFrame, hand_landmarks, mpHands.HAND_CONNECTIONS)

        # Convert the frame to Pygame surface
        frame_surface = pygame.image.frombuffer(flippedFrame.tobytes(), (380, 216), 'RGB')

        # Clear the screen
        #SCREEN.fill(BLACK)
        SCREEN.blit(bg, (0, 0))


        # Draw the camera feed in the upper left corner
        SCREEN.blit(frame_surface, (10, 10))  # Position the camera feed at (10, 10)
        # SCREEN.blit(text, textRect) # Score

        # Create new fruit objects every few frames
        if pygame.time.get_ticks() % 60 == 0:
            chance = random.randint(1, 101)  # Random chance for a powerup
            powerup = random.randint(1, 9)
            if game.comboMultiplier % 1:  # Each time its a new combo multiplier give them a powerup
                if powerupCount < 3:
                    powerupCount += 1
                    if powerup == 1:
                        items.append(Freeze(pygame.time.get_ticks()))
                    elif powerup == 2:
                        items.append(DoublePoints(pygame.time.get_ticks()))
                    elif powerup == 3:
                        items.append(SafetyNet(pygame.time.get_ticks()))
                    elif powerup == 4:
                        items.append(Invisibility(pygame.time.get_ticks()))
                    elif powerup == 5:
                        items.append(TimeSlow(pygame.time.get_ticks()))
                    elif powerup == 6:
                        items.append(RegenLives(pygame.time.get_ticks()))



            elif chance <= 10:  # 10% chance for a powerup to randomly spawn
                if powerupCount < 3:
                    powerupCount += 1
                    if powerup == 1:
                        items.append(Freeze(pygame.time.get_ticks()))
                    elif powerup == 2:
                        items.append(DoublePoints(pygame.time.get_ticks()))
                    elif powerup == 3:
                        items.append(SafetyNet(pygame.time.get_ticks()))
                    elif powerup == 4:
                        items.append(Invisibility(pygame.time.get_ticks()))
                    elif powerup == 5:
                        items.append(TimeSlow(pygame.time.get_ticks()))

            # Percentage based for what fruit appears, some are more common and worth less, some are less common and worth more
            chance = random.randint(1, 101)
            if 0 < chance <= 15:
                if netActivated:
                    items.append(Apple(8, 70, 70, True))
                elif slow:
                    items.append(Apple(4, 70, 70, False))
                elif slow and netActivated:
                    items.append(Apple(4, 70, 70, True))
                else:
                    items.append(Apple(8, 70, 70))
            elif 15 < chance <= 30:
                if netActivated:
                    items.append(Orange(8, 70, 70, True))
                elif slow:
                    items.append(Orange(4, 70, 70, False))
                elif slow and netActivated:
                    items.append(Orange(4, 70, 70, True))
                else:
                    items.append(Orange(8, 70, 70))
            elif 30 < chance <= 45:
                if netActivated:
                    items.append(Banana(8, 70, 70, True))
                elif slow:
                    items.append(Banana(4, 70, 70, False))
                elif slow and netActivated:
                    items.append(Banana(4, 70, 70, True))
                else:
                    items.append(Banana(8, 70, 70))
            elif 45 < chance <= 55:
                if netActivated:
                    items.append(Watermelon(8, 100, 100, True))
                elif slow:
                    items.append(Watermelon(4, 100, 100, False))
                elif slow and netActivated:
                    items.append(Watermelon(4, 100, 100, True))
                else:
                    items.append(Watermelon(8, 100, 100))
            elif 55 < chance <= 65:
                if netActivated:
                    items.append(Mango(8, 30, 60, True))
                elif slow:
                    items.append(Mango(4, 30, 60, False))
                elif slow and netActivated:
                    items.append(Mango(4, 30, 60, True))
                else:
                    items.append(Mango(8, 30, 60))
            elif 65 < chance <= 70:
                if netActivated:
                    items.append(Strawberry(8, 20, 20, True))
                elif slow:
                    items.append(Strawberry(4, 20, 20, False))
                elif slow and netActivated:
                    items.append(Strawberry(4, 20, 20, True))
                else:
                    items.append(Strawberry(8, 20, 20))
            else:
                if invisible:  # Make any newly spawned bombs invisible if they need to be
                    items.append(Bomb(8, True))
                elif netActivated:
                    items.append((Bomb(8, False, True)))
                elif netActivated and invisible:
                    items.append((Bomb(8, True, True)))
                elif slow:
                    items.append((Bomb(4, False, False)))
                elif slow and invisible:
                    items.append((Bomb(4, True, False)))
                elif slow and invisible and netActivated:
                    items.append((Bomb(4, True, True)))
                else:
                    items.append(Bomb(8))

        game.displayScore()  # Displays the score on the screen
        game.displayCombo()  # Displays the combo counter on the screen
        game.displayLives()

        # Iterate over hand centers
        for center in handCenters:
            pygame.draw.circle(SCREEN, CYAN, center, 5)  # Draws where the hands are on the screen
            #knife.drawKnife(center)

        # Update and draw all fruit objects
        for item in items:  # Loops through the fruits
            if item.name == "Powerup":  # If the item is a powerup
                # Update the powerup time
                currentTime = pygame.time.get_ticks()
                item.updateTime(currentTime)

                if (item.currentTime - item.startTime) >= 10000:  # If the time difference is greater than 10 seconds
                    # Deactive powerup and remove
                    item.deactivate()
                    items.remove(item)
                    powerupCount = 0

                    # Unfreeze the items
                    if item.type == "Freeze":
                        for item in items:
                            if item.name != "Powerup":
                                item.frozen = False

                    # Make bombs visible again
                    elif item.type == "Invisible":
                        for item in items:
                            if item.name == "Bomb":
                                item.invisible = False
                                invisible = False

                    # Deactivate double points
                    elif item.type == "Double Points":
                        game.double = False

                    # Deactivate the net
                    elif item.type == "Safety Net":
                        item.netVisible = False
                        item.visible = False
                        for item in items:
                            if item.name != "Powerup":
                                item.netActivated = False
                                item.speed = item.initial_speed
                                item.frozen = False
                                netActivated = False

                    # Deactivate the time slow
                    elif item.type == "Time Slow":
                        slow = False
                        for item in items:
                            if item.name != "Powerup":
                                item.speed = item.initial_speed * 2



            if item.visible:
                item.update()  # Updates the item on the screen
                SCREEN.blit(item.image, item.rect)

                if item.name == "Powerup" and item.type == "Safety Net":
                    if item.netVisible:
                        item.drawNet(SCREEN)

            # Used to see if the hands are over objects or not
            handInside = False
            handEntered = False
            handExited = False

            # Iterate over hand centers
            for center in handCenters:
                pygame.draw.circle(SCREEN, CYAN, center, 5)
                #knife.drawKnife(center)

                # Check if any hand is over the rectangle
                if item.rect.x < center[0] < item.rect.x + item.width and item.rect.y < center[
                    1] < item.rect.y + item.height:
                    if item.name == "Fruit":  # If its a fruit
                        item.updateImage()
                        item.frozen = False  # Fruit is no longer frozen
                        item.falling = True
                        if item.visible == True and item.hit == False:  # Temporary condition, but if its a fruit and not white, then it hasnt been hit yet
                            game.updateCombo(True)  # if the item name is a fruit, then they have hit a fruit so update the combo counter
                            item.hit = True  # It has been hit
                            # Temporary actions just to test code and interactions with the rectangles
                            if item.fruit == "Apple" or item.fruit == "Orange" or item.fruit == "Banana":  # Basic/more common fruit so less points
                                game.updateScore(10)  # Updates the score
                            elif item.fruit == "Mango" or item.fruit == "Watermelon":  # Slightly rarer points, so double the points
                                game.updateScore(20)  # Updates the score
                            else:
                                # Much more points for the rarest fruit
                                game.updateScore(50)  # Updates the score

                    elif item.name == "Powerup":  # If its a powerup
                        # Activate the power up and get the time it started
                        item.colour = WHITE
                        item.activate()
                        item.startTime = pygame.time.get_ticks()
                        startTime = pygame.time.get_ticks()
                        currentTime = pygame.time.get_ticks()

                        # If it was the freeze power up, freeze everything
                        if item.type == "Freeze":
                            for item in items:
                                if item.name != "Powerup":
                                    item.frozen = True

                        # If it was the invisible power up, make bombs invisible
                        elif item.type == "Invisibility":
                            for item in items:
                                if item.name == "Bomb":
                                    item.invisible = True

                        # If its a DP powerup, then set double to true
                        elif item.type == "Double Points":
                            game.double = True

                        # If its a safety net activate it
                        elif item.type == "Safety Net":
                            item.netVisible = True  # Set the net to be visible
                            item.drawNet(SCREEN)  # Begin drawing it on screen

                            # Set the net to be active for each fruit so it has the right movement
                            for item in items:
                                if item.name != "Powerup":
                                    item.netActivated = True
                                    netActivated = True

                        # if its a time slow, slow the speed of the fruit/bombs
                        elif item.type == "Time Slow":
                            slow = True
                            for item in items:
                                if item.name != "Powerup":
                                    item.speed = item.initial_speed // 2

                        elif item.type == "Regen Lives":  # Adds two lives
                            game.lives += 2


                    else:  # If its not a fruit
                        if item.invisible == False and item.visible == True:
                            item.frozen = False  # Unfreeze it as its been hit
                            item.visible = False  # Make it invisible as its a bomb
                            if not (item.colour == BLACK):  # If it hasnt been hit
                                item.colour = BLACK  # Indicates its been hit
                                game.updateScore(-5)  # Updates the score
                                game.updateCombo(False)  # Resets the combo counter
                                exploded = True
                                game.lives -= 1

                    if exploded:
                        for item in items:
                            item.visible = False
                            if item.name == "Powerup":
                                powerupCount = 0
                            items.remove(item)
                        exploded = False

                    break  # Exit the loop. Allows both hands to change colour

            # Remove fruit objects that have fallen off the screen
            if item.rect.y > HEIGHT:
                if item.name == "Fruit" and item.hit != True:  # If its a fruit and hasnt been hit
                    game.updateCombo(False)  # Resets the combo counter
                    game.lives -= 1
                items.remove(item)  # Removes it from the list

        if game.lives < 0:
            running = False

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()
