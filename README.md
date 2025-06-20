# Python OpenGL Maze Game from Zero

Author: Dmytro Chesniuk

## Description

- 3D Maze Escape is a third-person perspective puzzle game built using Python, Pygame, and OpenGL. The player navigates through a series of 3D mazes with the objective of reaching the yellow goal cube while avoiding blue walls. 
The game features smooth camera control, level progression, and atmospheric lighting to enhance the immersive experience.

## Key Features

- 3D Maze Rendering: The game uses OpenGL to draw the maze with cubes, each colored to represent walls, the player, and the goal.
- Each level is defined in a .txt file, where: 0 = empty space, 1 = wall, 2 = goal
- Victory & Loss Sounds: Sound effects play when the player reaches the goal or restarts the level, increasing game feedback and immersion.
- Reset & Exit Options: Players can restart the current level using the R key or exit the game with Esc.

## Controls

- W, A, S, D: Move the player forward, left, backward, and right.
- Mouse: Look around / rotate the camera.
- R: Reset current level.
- ESC: Unlock cursor and make mouse visible (pause-like behavior).
