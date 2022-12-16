import pygame
from datetime import datetime
import random

class ItRains:
    def __init__(self):
        pygame.init()

        # game window related
        pygame.display.set_caption("Rain of Coins")
        self.width = 600
        self.height = 800
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font_large = pygame.font.SysFont("Arial", 50)
        self.font_medium = pygame.font.SysFont("Arial", 27)
        self.font_small = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()

        # robot
        self.robot = pygame.image.load("robot.png")
        self.direction = 0
        self.speed = 6
        self.normal_speed = 6
        self.fast_speed = 18
        self.slow_speed = 2

        # coins
        self.coin = pygame.image.load("coin.png")
        self.coin_speed = 5

        #monsters
        self.monster = pygame.image.load("monster.png")

        self.new_game()
        self.main_loop()

    def new_game(self):
        self.game_over = False
        
        # robot
        self.x = self.width / 2 - self.robot.get_width() / 2
        self.y = self.height - self.robot.get_height()

        # cois
        self.falling_coins = []
        self.collected_coins = 0

        # monsters
        self.falling_monsters = []
        self.monster_spawn_rate = 200
        self.monster_speed = 5

        self.difficulty_timestamp = 0 # time when difficulty was last increased
        
        self.game_start_time = datetime.now()
        self.game_finish_time = None

    def main_loop(self):
        while True:
            self.check_events()

            if not self.game_over:
                # move the robot
                self.x += self.direction * self.speed
                if self.x < 0:
                    self.x = 0
                if self.x > self.width - self.robot.get_width():
                    self.x = self.width - self.robot.get_width()

                # spawn new coins
                i = random.randint(1, 200)
                if 1 <= i <=2:
                    x = random.randint(0, self.width - self.coin.get_width())
                    y = 0 - self.coin.get_height()
                    self.falling_coins.append([x, y])

                # spawn new monsters
                i = random.randint(1, self.monster_spawn_rate)
                if 1 <= i <=2:
                    x = random.randint(0, self.width - self.monster.get_width())
                    y = 0 - self.monster.get_height()
                    self.falling_monsters.append([x, y])

                # handle existing coins
                for c in self.falling_coins[:]:
                    # move coins downwards
                    c[1] += self.coin_speed
                    
                    # remove coins that are out of bounds
                    if c[1] >= self.height:
                        self.falling_coins.remove(c)
                        continue

                    # collect coins that touch the robot
                    if c[1] + self.coin.get_height() >= self.height - self.robot.get_height():
                        if c[0] < self.x + self.robot.get_width() and c[0] + self.coin.get_width() > self.x:
                            self.falling_coins.remove(c)
                            self.collected_coins += 1

                # handle existing monsters
                for m in self.falling_monsters[:]:
                    # move monsters downwards
                    m[1] += self.monster_speed
                    
                    # remove monsters that are out of bounds
                    if m[1] >= self.height:
                        self.falling_monsters.remove(m)

                    # check if player touches any monsters
                    if m[1] + self.monster.get_height() >= self.height - self.robot.get_height() / 2:
                        if m[1] < self.height - self.robot.get_height() / 2:
                            if m[0] <= self.x + self.robot.get_width() / 2 <= m[0] + self.monster.get_width():
                                self.game_over = True
                                self.game_finish_time = datetime.now() - self.game_start_time

                # make the game more difficult
                time = datetime.now() - self.game_start_time
                seconds = time.seconds
                seconds += 31
                if seconds % 30 == 0 and seconds != 0 and seconds != self.difficulty_timestamp:
                    self.monster_spawn_rate = self.monster_spawn_rate * 0.8 // 1
                    self.difficulty_timestamp = seconds

            self.draw_window()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = -1
                if event.key == pygame.K_RIGHT:
                    self.direction = 1
                if event.key == pygame.K_LSHIFT:
                    self.speed = self.fast_speed
                if event.key == pygame.K_LCTRL:
                    self.speed = self.slow_speed
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if self.direction == -1:
                        self.direction = 0
                if event.key == pygame.K_RIGHT:
                    if self.direction == 1:
                        self.direction = 0
                if event.key == pygame.K_LSHIFT:
                    self.speed = self.normal_speed
                if event.key == pygame.K_LCTRL:
                    self.speed = self.normal_speed

            if self.game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # pressing restart button
                    if (self.width - 130) / 2 <= event.pos[0] <= (self.width - 130) / 2 + 130:
                        if self.height / 2 + 70 <= event.pos[1] <= self.height / 2 + 70 + 50:
                            self.new_game()

            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill((30, 30, 30))

        # robot
        self.window.blit(self.robot, (self.x, self.y))
        pygame.draw.circle(self.window, (0, 0, 0), (self.x + self.robot.get_width() / 2, self.y + self.robot.get_height() / 2 + 6), 7)
        pygame.draw.circle(self.window, (0, 0, 255), (self.x + self.robot.get_width() / 2, self.y + self.robot.get_height() / 2 + 6), 5)

        # coins
        for c in self.falling_coins[:]:
            self.window.blit(self.coin, (c[0], c[1]))

        # monsters
        for m in self.falling_monsters[:]:
            self.window.blit(self.monster, (m[0], m[1]))

        # timer
        if not self.game_over:
            time = datetime.now() - self.game_start_time
            minutes = time.seconds // 60
            seconds = time.seconds - time.seconds // 60 * 60
            text = self.font_large.render(f"{minutes:02}:{seconds:02}", True, (255, 0, 0))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, 50))

        # coin counter
        if not self.game_over:
            text = self.font_large.render(str(self.collected_coins), True, (255, 255, 0))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, 110))

        if self.game_over:
            # game over base rectangle
            pygame.draw.rect(self.window, (50, 50, 50), ((self.width - 500) / 2, (self.height - 350) / 2, 500, 350), 0, 5)

            # tip
            text = self.font_small.render(f"Tip: try using ctrl and shift while playing.", True, (255, 255, 255))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - 300))
        
            # game over text
            text = self.font_large.render(f"Game over!", True, (255, 0, 0))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - 140))

            # coins text
            text = text = self.font_medium.render(f"Coins: {self.collected_coins}", True, (255, 255, 255))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - 50))

            # time text
            minutes = self.game_finish_time.seconds // 60
            seconds = self.game_finish_time.seconds - self.game_finish_time.seconds // 60 * 60
            text = text = self.font_medium.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - 10))

            # score text
            seconds = self.game_finish_time.seconds
            score = self.collected_coins * 12 + seconds * 12
            text = text = self.font_medium.render(f"Score: {score:06}", True, (255, 255, 255))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 + 30))

            # restart button
            pygame.draw.rect(self.window, (0, 150, 0), ((self.width - 130) / 2, self.height / 2 + 90, 130, 50), 0, 5)
            text = self.font_medium.render(f"Restart", True, (255, 255, 255))
            self.window.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 + 97))


        pygame.display.flip()


if __name__ == "__main__":
    ItRains()