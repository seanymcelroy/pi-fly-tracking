import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define radar parameters
center = (width // 2, height // 2)
radius = min(width, height) // 2 - 50
angle = 0
rotation_speed = 1

# Define slice parameters
slice_color = GREEN
slice_alpha = 255
slice_radius = radius
slice_width = 10

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the radar circle
    pygame.draw.circle(screen, GREEN, center, radius, 2)

    # Draw the spinning slice object
    start_angle = math.radians(angle)
    end_angle = math.radians(angle + 60)  # Adjust the angle to determine the size of the slice
    pygame.draw.arc(screen, (slice_color[0], slice_color[1], slice_color[2], slice_alpha),
                    (center[0] - slice_radius, center[1] - slice_radius, slice_radius * 2, slice_radius * 2),
                    start_angle, end_angle, slice_width)

    # Calculate the points to connect the ends of the arc to the center
    start_pos = (
        center[0] + int(slice_radius * math.cos(start_angle)),
        center[1] + int(slice_radius * math.sin(start_angle))
    )
    end_pos = (
        center[0] + int(slice_radius * math.cos(end_angle)),
        center[1] + int(slice_radius * math.sin(end_angle))
    )

    # Draw lines connecting the ends of the arc to the center
    pygame.draw.line(screen, slice_color, center, start_pos, slice_width)
    pygame.draw.line(screen, slice_color, center, end_pos, slice_width)

    # Update angle
    angle = (angle + rotation_speed) % 360

    # Update slice opacity
    slice_alpha -= 1
    if slice_alpha < 0:
        slice_alpha = 255

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
