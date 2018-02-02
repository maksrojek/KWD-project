import random


class Game:
    stan = 0
    rows = 0
    cols = 0
    step_reward = 0
    hole_reward = 0
    win_reward = 0
    probability = 0
    field = []

    def __init__(self, field, rows, cols, step_reward, hole_reward, win_reward,
                 probability):
        self.field = field
        self.rows = rows
        self.cols = cols
        self.step_reward = step_reward
        self.hole_reward = hole_reward
        self.win_reward = win_reward
        self.probability = probability

    def step(self, action):
        reward = self.step_reward
        done = False
        info = False

        if random.random() <= self.probability:
            new_action = random.randint(0, 3)
            while action == new_action or (action - 2) % 4 == new_action:
                new_action = random.randint(0, 3)

            action = new_action

        if (action == 0) and ((self.stan % self.rows) != 0):
            self.stan -= 1
        if (action == 1) and (self.stan < ((self.rows - 1) * self.cols)):
            self.stan += self.cols
        if (action == 2) and ((self.stan % self.cols) != (self.cols - 1)):
            self.stan += 1
        if (action == 3) and (self.stan >= self.cols):
            self.stan -= self.cols

        if self.field[self.stan] == 'H':
            reward = self.hole_reward
            done = True

        if self.field[self.stan] == 'G':
            reward = self.win_reward
            done = True

        return self.stan, reward, done, info

    def reset(self):
        self.stan = 0
        return self.stan
