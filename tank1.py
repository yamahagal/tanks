import random

import pygame

import colors
from map import Missile, Bonus


class Tank1(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy, direction):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.direction = direction
        self.setImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.speed_abs = 32//4
        self.speed = (self.direction[0]*self.speed_abs, self.direction[1]*self.speed_abs)
        self.shot_timer = 0
        self.shot_delay = 2
        self.health = 10000
        self.armor = 5000
        self.damage = 20000
        self.missiles = 10000
        self.explosion_resistance = 0
        self.dead = 0
        self.enemy = None
        self.move_xy = None
        self.shot_sound = pygame.mixer.Sound("sounds\\shot.wav")
        self.bonus_sound = pygame.mixer.Sound("sounds\\star.wav")
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_tanks.add(self)
        self.tank_game.all_tank1.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_bad.add(self)
        self.tank_game.all_not_tnt.add(self)

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

    def getTopLeft(self):
        return self.rect.topleft

    def getEnemy(self, enemy):
        if len(enemy) > 0:
            if self.enemy == None:
                if len(enemy.sprites())>1:
                    self.enemy = enemy.sprites()[0]
                else:
                    self.enemy = enemy.sprites()[0]
            if enemy.has([self.enemy]):
                if len(enemy.sprites()) > 1:
                    self.enemy = enemy.sprites()[0]
                else:
                    self.enemy = enemy.sprites()[0]
            return self.enemy

    def drawParameters(self):
        font = pygame.font.SysFont("Segoe UI", 10)
        score_render = font.render(f"Здоровье: {self.health+self.armor}, взр. уст.: {self.explosion_resistance} Урон: {self.damage}"
                                   f", снаряды: {self.missiles}", 1, colors.RED)
        self.tank_game.sc.blit(score_render, (self.rect.topleft[0]-70, self.rect.topleft[1]-20))

    def shot(self):
        if self.missiles > 0:
            self.missiles -= 1
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "tank1", colors.RED)
            self.shot_sound.play()

    def processBonus(self):
        bonuses = pygame.sprite.spritecollide(self, self.tank_game.all_bonus, False)
        if len(bonuses) > 0:
            for bonus in bonuses:
                self.applyBonus(bonus.getEffects())
                bonus.kill()
                Bonus(self.tank_game)
            return True
        else:
            return False

    def applyBonus(self, effects_dict):
        print(effects_dict)
        if "health" in effects_dict.keys():
            self.health += effects_dict["health"]
        if "damage" in effects_dict.keys():
            self.damage += effects_dict["damage"]
        if "armor" in effects_dict.keys():
            self.armor += effects_dict["armor"]
        if "missiles" in effects_dict.keys():
            self.missiles += effects_dict["missiles"]
        if "explosion_resistance" in effects_dict.keys():
            self.explosion_resistance += effects_dict["explosion_resistance"]
        self.bonus_sound.play()

    def checkHit(self, damage, owner):
        self.foundEnemy(owner)
        k = self.health/(self.health+self.armor)
        dh = round(damage*k)
        self.health -= dh
        self.armor -= (damage-dh)
        if self.health <= 0:
            self.drawBang(self)
            self.kill()
            for my_tank in self.tank_game.all_mytanks:
                my_tank.plusKills()


    def foundEnemy(self, owner):
        if owner == "mytank1":
            self.getEnemy(self.tank_game.all_mytanks1)
        elif owner == "mytank2":
            self.getEnemy(self.tank_game.all_mytanks2)


    def checkMove(self):
        tank_check = Tank1(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        obstacles = pygame.sprite.spritecollide(tank_check, self.tank_game.all_obstacles, False)
        tank_check.kill()
        if len(obstacles) > 2 or tank_check.rect.left < 0 or tank_check.rect.top < 0 or\
                tank_check.rect.right > self.tank_game.x_cells*self.tank_game.cell_size or tank_check.rect.bottom > self.tank_game.y_cells*self.tank_game.cell_size-1:
            return False
        else:
            return True

    def checkArmors(self, xy):
        a = pygame.sprite.Sprite()
        a.image = pygame.Surface((1, 1))
        a.rect = a.image.get_rect()
        a.rect.topleft = xy
        armors = pygame.sprite.spritecollide(a, self.tank_game.all_armors, False)
        if len(armors) > 0 or xy[0] < 0 or xy[1] < 0 or\
                xy[0] > self.tank_game.x_cells*self.tank_game.cell_size or xy[1] > self.tank_game.y_cells*self.tank_game.cell_size-1:
            return False
        else:
            return True

    def checkBrick(self):
        tank_check = Tank1(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        bricks = pygame.sprite.spritecollide(tank_check, self.tank_game.all_bricks, False)
        tank_check.kill()
        if len(bricks) > 0 or tank_check.rect.left < 0 or tank_check.rect.top < 0 or \
                tank_check.rect.right > self.tank_game.x_cells * self.tank_game.cell_size or tank_check.rect.bottom > self.tank_game.y_cells * self.tank_game.cell_size - 1:
            return False
        else:
            return True

    def checkBonus(self):
        bonuses = pygame.sprite.spritecollide(self, self.tank_game.all_bonus, False)
        if len(bonuses) > 0:
            for bonus in bonuses:
                bonus.kill()
                #Bonus(self.tank_game)

            return True
        else:
            return False

    def setImage(self):
        if self.direction == (-1, 0):
            self.image = pygame.image.load("images\\tank_gray_left.png")
        elif self.direction == (0, 1):
            self.image = pygame.image.load("images\\tank_gray_down.png")
        elif self.direction == (1, 0):
            self.image = pygame.image.load("images\\tank_gray_right.png")
        elif self.direction == (0, -1):
            self.image = pygame.image.load("images\\tank_gray_up.png")

    def updateShotTimer(self):
        if self.shot_timer > 0:
            self.shot_timer -= 1

    def checkShot(self):
        if self.shot_timer <= 0:
            self.shot_timer = self.shot_delay
            return True
        else:
            return False

    def chooseField(self):
        moves = []
        moves_checked = []
        moves_distance = []
        min_distance = 0
        moves_xy_min = []

        xy = self.rect.topleft
        moves.append((xy[0]+self.tank_game.cell_size, xy[1]))
        moves.append((xy[0]-self.tank_game.cell_size, xy[1]))
        moves.append((xy[0], xy[1]+self.tank_game.cell_size))
        moves.append((xy[0], xy[1]-self.tank_game.cell_size))
        enemy = self.getEnemy(self.tank_game.all_mytanks1)
        if enemy != None:
            enemy_xy = enemy.getTopLeft()

            for xy in moves:
                if self.checkArmors(xy):
                    moves_checked.append(xy)

            for xy in moves_checked:
                moves_distance.append(self.getDistance(enemy_xy, xy))
            min_distance = min(moves_distance)

            for i, d in enumerate(moves_distance):
                if d == min_distance:
                    moves_xy_min.append(moves_checked[i])
            self.move_xy = random.choice(moves_xy_min)

        else:
            self.move_xy = None

    def calcDirection(self):
        xy = self.move_xy
        if xy != None:
            if xy[1] < self.rect.topleft[1]:
                self.direction = (0, -1)
            if xy[1] > self.rect.topleft[1]:
                self.direction = (0, 1)
            if xy[0] < self.rect.topleft[0]:
                self.direction = (-1, 0)
            if xy[0] > self.rect.topleft[0]:
                self.direction = (1, 0)
            self.setImage()

    def getDistance(self, xy1, xy2):
        return abs(xy1[1] - xy2[1]) + abs(xy1[0] - xy2[0])

    def move(self):
        self.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        self.rect.move_ip(self.speed)

    def needShot(self):
        # напротив меня противник
        enemy = self.getEnemy(self.tank_game.all_mytanks1)
        if enemy != None:
            enemy_xy = enemy.getTopLeft()
            xy = self.rect.topleft
            if self.direction[0] != 0 and xy[1] <= enemy_xy[1]+self.tank_game.cell_size//2 and xy[1] >= enemy_xy[1]-self.tank_game.cell_size//2:
                if self.direction == (-1, 0) and enemy_xy[0] < xy[0]:
                    return True
                elif self.direction == (1, 0) and enemy_xy[0] > xy[0]:
                    return True

            elif self.direction[1] != 0 and xy[0] <= enemy_xy[0] + self.tank_game.cell_size // 2 and xy[0] >= enemy_xy[0] - self.tank_game.cell_size // 2:
                if self.direction == (0, -1) and enemy_xy[1] < xy[1]:
                    return True
                elif self.direction == (0, 1) and enemy_xy[1] > xy[1]:
                    return True

            # перед танком кирпич который мешает
            if not self.checkMove():
                return True

        return False

    def drawMoveXY(self):
        if self.move_xy != None:
            cell = pygame.Rect(self.move_xy[0], self.move_xy[1], self.tank_game.cell_size, self.tank_game.cell_size)
            pygame.draw.rect(self.tank_game.sc, colors.RED, cell, 1)

    def getMissilesXY(self):
        for missile in self.tank_game.all_missiles:
            if missile.rect.center[1] < self.rect.center[1] and missile.direction == (0, 1):
                if missile.rect.center[0] == self.rect.center[0] or missile.rect.center[0] == self.rect.left or missile.rect.center[0] == self.rect.right:
                    print("опасно")
                    self.direction = random.choice([(-1, 0), (1, 0)])
                    self.setImage()
                    if self.checkMove():
                        self.move()
                        self.move()
                        self.move()
                        self.move()
                    self.chooseField()
                    self.calcDirection()

            if missile.rect.center[1] > self.rect.center[1] and missile.direction == (0, -1):
                if missile.rect.center[0] == self.rect.center[0] or missile.rect.center[0] == self.rect.left or missile.rect.center[0] == self.rect.right:
                    print("опасно")
                    self.direction = random.choice([(-1, 0), (1, 0)])
                    self.setImage()
                    if self.checkMove():
                        self.move()
                        self.move()
                        self.move()
                        self.move()
                    self.chooseField()
                    self.calcDirection()

            if missile.rect.center[0] < self.rect.center[0] and missile.direction == (1, 0):
                if missile.rect.center[1] == self.rect.center[1] or missile.rect.center[1] == self.rect.left or missile.rect.center[1] == self.rect.right:
                    print("опасно")
                    self.direction = random.choice([(0, 1), (0, -1)])
                    self.setImage()
                    if self.checkMove():
                        self.move()
                        self.move()
                        self.move()
                        self.move()
                    self.chooseField()
                    self.calcDirection()

            if missile.rect.center[0] > self.rect.center[0] and missile.direction == (-1, 0):
                if missile.rect.center[1] == self.rect.center[1] or missile.rect.center[1] == self.rect.left or missile.rect.center[1] == self.rect.right:
                    print("опасно")
                    self.direction = random.choice([(0, 1), (0, -1)])
                    self.setImage()
                    if self.checkMove():
                        self.move()
                        self.move()
                        self.move()
                        self.move()
                    self.chooseField()
                    self.calcDirection()

    def update(self, *args, **kwargs):

        self.drawParameters()
        self.updateShotTimer()
        if self.move_xy == self.rect.topleft or self.move_xy == None:
            self.chooseField()
            self.calcDirection()
        self.drawMoveXY()
        if self.checkShot() and self.needShot():
            self.shot()

        self.getMissilesXY()
        self.setImage()

        if self.checkMove():
            self.move()

        self.processBonus()