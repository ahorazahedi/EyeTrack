import pygame
import random
import cv2
import os
import time

url = 'http://192.168.1.107:8080/shot.jpg'

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

bgColor = (255, 255, 255)
dotColor = (0, 0, 0)
dotSize = 10
update_interval = 2000
image_capture_delay = 1000

logged_positions = []
running = True
counter = 0

myTime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def random_coordinates():
    return random.uniform(-1, 1), random.uniform(-1, 1)

last_update_time = pygame.time.get_ticks()
image_capture_time = None

output_directory = f"{myTime}"
os.makedirs(output_directory, exist_ok=True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    current_time = pygame.time.get_ticks()

    if current_time - last_update_time >= update_interval:
        last_update_time = current_time
        screen.fill(bgColor)

        random_x, random_y = random_coordinates()

        screen_width, screen_height = pygame.display.get_surface().get_size()
        pos_x = int((random_x + 1) * screen_width / 2)
        pos_y = int((random_y + 1) * screen_height / 2)

        logged_positions.append((random_x, random_y))

        pygame.draw.circle(screen, dotColor, (pos_x, pos_y), dotSize)
        pygame.display.flip()

        if image_capture_time is not None and current_time - image_capture_time >= image_capture_delay:
            capture = cv2.VideoCapture(url)
            ret, frame = capture.read()
            capture.release()

            image_filename = os.path.join(output_directory, f"cpt_{counter}.jpg")
            cv2.imwrite(image_filename, frame)
            counter += 1

    if image_capture_time is None:
        image_capture_time = current_time + image_capture_delay 
pygame.quit()


with open(f"{myTime}.txt", "w") as file:
    for position in logged_positions:
        file.write(f"{position[0]}, {position[1]}\n")
