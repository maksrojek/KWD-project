import numpy as np
from Game import Game
import pygame
import time

pygame.init()
font = pygame.font.SysFont("monospace", 30, True)
surface = pygame.display.set_mode((860, 860))  # width x height
pygame.display.set_caption('GridWorld')
sleep_time = 0.01


def drawGridWorld(Q, field, player, action):
    surface.fill((0, 0, 0))
    wiersz = 0
    kolumna = 0
    offset = 10
    size = 200
    for pole in range(len(Q)):  # Y # pola pionowo
        if pole != 0 and (pole % len(Q[0]) == 0):
            wiersz += 1
            kolumna = 0
        x_cord = offset + offset * kolumna + kolumna * size
        y_cord = offset + offset * wiersz + wiersz * size
        # Field
        field_color = (189, 189, 189)
        if field[pole] == 'H':
            field_color = (33, 33, 33)
        if field[pole] == 'S':
            field_color = (255, 179, 0)
        if field[pole] == 'G':
            field_color = (118, 255, 3)
        pygame.draw.rect(surface, field_color, (x_cord, y_cord, size, size))
        # Player
        if pole == player:
            field_color = (3, 169, 244)
            pygame.draw.circle(surface, field_color, (
                int(round(x_cord + size / 2)), int(round(y_cord + size / 2))),
                               int(round(size / 2)))
        if action == 0:
            move_action = font.render("<", False, (255, 0, 0))
        if action == 1:
            move_action = font.render("\/", False, (255, 0, 0))
        if action == 2:
            move_action = font.render(">", False, (255, 0, 0))
        if action == 3:
            move_action = font.render("/\\", False, (255, 0, 0))

        surface.blit(move_action, (0, 0))
        # QMatrix

        color = (255, 255, 255)

        best = Q[pole].argmax()
        for i in range(4):
            if i == best:
                color = (255, 0, 0)
            x_label_cord = 0
            y_label_cord = 0
            if i == 0:  # left
                x_label_cord = x_cord
                y_label_cord = y_cord
                direction = 'left'
                # color = (0, 0, 255)  # blue

            if i == 1:  # down
                x_label_cord = x_cord
                y_label_cord = y_cord + size / 4
                direction = 'down'
                # color = (0, 255, 0)  # green

            if i == 2:  # right
                x_label_cord = x_cord
                y_label_cord = y_cord + size / 4 * 2
                direction = 'right'
                # color = (0, 255, 255)  # green blue

            if i == 3:  # up
                x_label_cord = x_cord
                y_label_cord = y_cord + size / 2 + size / 4
                direction = 'up'
                # color = (255, 0, 0)  # red

            label = font.render("{}:{}".format(direction, round(Q[pole][i], 3)), False,
                                color)
            surface.blit(label, (x_label_cord, y_label_cord))
        kolumna += 1
    pygame.display.update()
    time.sleep(sleep_time)


def simulate(num_episodes, penalty, probability, hole_penalty):
    rows = 4
    cols = 4
    field = ['S', 'F', 'F', 'F',
             'F', 'H', 'F', 'H',
             'F', 'F', 'F', 'H',
             'H', 'F', 'F', 'G'
             ]
    env = Game(field, rows, cols, penalty, hole_penalty, 1, probability)
    # Initialize table with all zeros
    Q = np.zeros([rows * cols, 4])
    alpha = .8
    y = .95
    reward_list = []
    for i in range(num_episodes):
        # Reset environment and get first new observation
        obsv = env.reset()
        # drawGridWorld(Q, field, obsv, 0)
        rewardAll = 0
        loop_counter = 0
        while loop_counter < 99:
            loop_counter += 1
            # Choose an action by greedily (with noise) picking from Q table
            action = np.argmax(Q[obsv, :] + np.random.randn(1, 4) * (1. / (i + 1)))
            # drawGridWorld(Q, field, obsv, action)
            # Get new state and reward from environment
            next_obsv, reward, done, info = env.step(action)
            # drawGridWorld(Q, field, next_obsv, action)
            # Update Q-Table with new knowledge
            Q[obsv, action] = Q[obsv, action] + alpha * (
                    reward + y * np.max(Q[next_obsv, :]) - Q[obsv, action])
            obsv = next_obsv

            if done:
                if reward == 1:
                    rewardAll += 1
                break
        reward_list.append(rewardAll)

    score = sum(reward_list) / num_episodes
    return score


if __name__ == '__main__':
    num_iterate = 100
    num_episodes = 2000
    hole_penalty = 0
    scores = [0, 0, 0, 0]
    for _ in range(num_iterate):
        scores[0] += simulate(num_episodes, 0, 0, hole_penalty)
        scores[1] += simulate(num_episodes, -0.04, 0.6, hole_penalty)
        scores[2] += simulate(num_episodes, 0, 0.6, hole_penalty)
        scores[3] += simulate(num_episodes, -0.04, 0, hole_penalty)
    scores = [s / num_iterate for s in scores]
    print(scores)
