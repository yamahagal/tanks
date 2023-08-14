import random

import pygame
import keyboard

import colors
from settings import parametersmytank1 as pr1, parametersmytank2 as pr2
from map import Missile, Armor, Bonus, Brick, Bonus2


class MyTank1(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy, direction):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.direction = direction
        self.setImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.speed_abs = 32 // 2
        self.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        self.shot_timer = 0
        self.shot_delay = pr1.shot_delay
        self.move_timer = 0
        self.move_delay = 5
        self.tp_timer = 0
        self.tp_delay = pr1.tp_delay
        self.health = pr1.health
        self.armor = pr1.armor
        self.damage = pr1.damage
        self.missiles = pr1.missiles
        self.armor_missiles = pr1.armor_missiles
        self.money = pr1.money
        self.save_money = pr1.save_money
        self.explosion_resistance = pr1.explosion_resistance
        self.kills = pr1.kills
        self.eventkey = None
        self.shot_sound = pygame.mixer.Sound("sounds\\shot.wav")
        self.bonus_sound = pygame.mixer.Sound("sounds\\star.wav")
        self.time = 0
        self.fl = False
        self.sheld = False
        self.tp_x = 10 * self.tank_game.cell_size
        self.tp_y = 10 * self.tank_game.cell_size
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_tanks.add(self)
        self.tank_game.all_mytanks.add(self)
        self.tank_game.all_mytanks1.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)

    def write(self):
        with open('settings/params1.txt', 'w') as file:
            # записываем параметры в файл
            s = ""
            s += f'health={pr1.health}\n'
            s += f'armor={pr1.armor}\n'
            s += f'damage={pr1.damage}\n'
            s += f'missiles={pr1.missiles}\n'
            s += f'money={pr1.money}\n'
            s += f'save_money={pr1.save_money}\n'
            s += f'tp_delay={pr1.tp_delay}\n'
            s += f'explosion_resistance={pr1.explosion_resistance}\n'
            s += "#f"

            file.write(s)

    def getMoney(self, money):
        self.money += money
        pr1.money += money

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

    def getTopLeft(self):
        return self.rect.topleft

    def shot(self):
        if self.missiles > 0:
            self.missiles -= 1
            self.shot_sound.play()
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "mytank1", colors.RED)

    def coldShot(self):
        if self.missiles > 0:
            self.missiles -= 1
            self.shot_sound.play()
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "cold", colors.BLUE)

    def armorShot(self):
        if self.armor_missiles > 0:
            self.armor_missiles -= 1
            self.shot_sound.play()
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "armor", colors.ORANGE)

    def processBonus(self):
        bonuses = pygame.sprite.spritecollide(self, self.tank_game.all_bonus, False)
        if len(bonuses) > 0:
            for bonus in bonuses:
                self.applyBonus(bonus.getEffects())
                bonus.kill()
                if bonus.two == 1:
                    Bonus(self.tank_game)
            return True
        else:
            return False

    def getXY(self):
        while True:
            x_c = []
            for x in range(0, self.tank_game.x_cells * self.tank_game.cell_size, self.tank_game.cell_size):
                x_c.append(x)

            x_rect = random.choice(x_c)

            y_c = []
            for y in range(0, (self.tank_game.y_cells - 1) * self.tank_game.cell_size, self.tank_game.cell_size):
                y_c.append(y)

            y_rect = random.choice(y_c)

            sprites_xy = []
            for sprite in self.tank_game.all_sprites:
                sprites_xy.append(sprite.rect.topleft)
            if (x_rect, y_rect) not in sprites_xy:
                return (x_rect, y_rect)

    def applyBonus(self, effects_dict):
        print(effects_dict)
        if "health" in effects_dict.keys():
            self.health += effects_dict["health"]
            pr1.health += effects_dict["health"]
        if "damage" in effects_dict.keys():
            self.damage += effects_dict["damage"]
            pr1.damage += effects_dict["damage"]
        if "armor" in effects_dict.keys():
            self.armor += effects_dict["armor"]
            pr1.armor += effects_dict["armor"]
        if "missiles" in effects_dict.keys():
            self.missiles += effects_dict["missiles"]
            pr1.missiles += effects_dict["missiles"]
        if "money" in effects_dict.keys():
            self.money += effects_dict["money"]
            pr1.money += effects_dict["money"]
        if "explosion_resistance" in effects_dict.keys():
            self.explosion_resistance += effects_dict["explosion_resistance"]
            pr1.explosion_resistance += effects_dict["explosion_resistance"]

        self.bonus_sound.play()

    def checkCold(self, damage):
        self.health -= damage
        if self.health <= 0:
            for tank2 in self.tank_game.all_mytanks2:
                tank2.plusKills()
                pr1.kills += 1
                self.fl = False
            print("MyTank1 УБИТ!!!")
            self.drawBang(self)
            self.health = pr1.health
            self.armor = pr1.armor
            self.damage = pr1.damage
            self.missiles = pr1.missiles
            self.armor_missiles = pr1.armor_missiles
            self.kills = pr1.kills
            self.explosion_resistance = pr1.explosion_resistance
            self.rect.topleft = self.tank_game.getXY()
            if self.save_money > 0:
                self.save_money -= 1
                pr1.save_money -= 1
            else:
                for tank2 in self.tank_game.all_mytanks2:
                    tank2.getMoney(self.money)
                self.money = 0
                pr1.money = 0

    def checkHit(self, damage, owner):
        if owner == "cold":
            self.fl = True
        elif owner == "oh" or owner == "armor":

            self.checkCold(damage)
        else:
            self.tp_timer = self.tp_delay
            in_damage = damage - self.armor
            if in_damage > 0:
                self.health -= in_damage
                if self.health <= 0:
                    for tank2 in self.tank_game.all_mytanks2:
                        tank2.plusKills()
                        pr2.kills += 1
                        self.fl = False
                    print("MyTank1 УБИТ!!!")
                    self.drawBang(self)
                    self.health = pr1.health
                    self.armor = pr1.armor
                    self.damage = pr1.damage
                    self.missiles = pr1.missiles
                    self.armor_missiles = pr1.armor_missiles
                    self.kills = pr1.kills
                    self.explosion_resistance = pr1.explosion_resistance
                    self.rect.topleft = self.tank_game.getXY()
                    if self.save_money > 0:
                        self.save_money -= 1
                        pr1.save_money -= 1
                    else:
                        for tank2 in self.tank_game.all_mytanks2:
                            tank2.getMoney(self.money)
                        self.money = 0
                        pr1.money = 0

    def drawParameters(self):
        font = pygame.font.SysFont("Segoe UI", self.tank_game.cell_size - 5)

        tank_render = font.render("TANK1", True, colors.RED)
        self.tank_game.sc.blit(tank_render, (self.tank_game.cell_size * 33, self.tank_game.cell_size * 1))

        health_render = font.render(f"здоровье: {self.health}", True, colors.RED)
        self.tank_game.sc.blit(health_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 2))

        armor_render = font.render(f"броня: {self.armor}", True, colors.RED)
        self.tank_game.sc.blit(armor_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 3))

        damage_render = font.render(f"Урон: {self.damage}", True, colors.RED)
        self.tank_game.sc.blit(damage_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 4))

        tp_render = font.render(f"Tp Time: {self.tp_delay - self.tp_timer}", True, colors.RED)
        self.tank_game.sc.blit(tp_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 5))

        explosion_resistance_render = font.render(f"взрыв. уст.: {self.explosion_resistance}", True, colors.RED)
        self.tank_game.sc.blit(explosion_resistance_render,
                               (self.tank_game.cell_size * 32, self.tank_game.cell_size * 6))

        missiles_render = font.render(f"снаряды: {self.missiles}", True, colors.RED)
        self.tank_game.sc.blit(missiles_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 7))

        kills_render = font.render(f"убито: {self.kills}", True, colors.RED)
        self.tank_game.sc.blit(kills_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 8))

        money_render = font.render(f"монет: {self.money}", True, colors.RED)
        self.tank_game.sc.blit(money_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 9))

        save_render = font.render(f"сохранений: {self.save_money}", True, colors.RED)
        self.tank_game.sc.blit(save_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 10))

        armor_missiles_render = font.render(f"мощн. снаряды: {self.armor_missiles}", True, colors.RED)
        self.tank_game.sc.blit(armor_missiles_render, (self.tank_game.cell_size * 32, self.tank_game.cell_size * 11))

    def plusKills(self):
        self.kills += 1

    def checkMove(self):
        tank_check = MyTank1(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        obstacles = pygame.sprite.spritecollide(tank_check, self.tank_game.all_obstacles, False)
        tank_check.kill()
        if len(obstacles) > 2:  # or tank_check.rect.left < 0 or tank_check.rect.top < 0 or\tank_check.rect.right > x_cells*cell_size or tank_check.rect.bottom > y_cells*cell_size-1:
            return False
        else:
            return True

    def checkDynamite(self):
        tank_check = MyTank1(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        obstacles = pygame.sprite.spritecollide(tank_check, self.tank_game.all_dynamite, False)
        tank_check.kill()
        if len(obstacles) > 0:
            obstacles[0].bang()

    def getMissilesXY(self):
        for missile in self.tank_game.all_missiles:
            if missile.rect.center[1] < self.rect.center[1] and missile.direction == (0, 1):
                if missile.rect.center[0] == self.rect.center[0] or missile.rect.center[0] == self.rect.left or \
                        missile.rect.center[0] == self.rect.right:
                    print("опасно")
                    if self.checkTp():
                        self.rect.topleft = self.tank_game.getXY()

            if missile.rect.center[1] > self.rect.center[1] and missile.direction == (0, -1):
                if missile.rect.center[0] == self.rect.center[0] or missile.rect.center[0] == self.rect.left or \
                        missile.rect.center[0] == self.rect.right:
                    print("опасно")
                    if self.checkTp():
                        self.rect.topleft = self.tank_game.getXY()

            if missile.rect.center[0] < self.rect.center[0] and missile.direction == (1, 0):
                if missile.rect.center[1] == self.rect.center[1] or missile.rect.center[1] == self.rect.left or \
                        missile.rect.center[1] == self.rect.right:
                    print("опасно")
                    if self.checkTp():
                        self.rect.topleft = self.tank_game.getXY()

            if missile.rect.center[0] > self.rect.center[0] and missile.direction == (-1, 0):
                if missile.rect.center[1] == self.rect.center[1] or missile.rect.center[1] == self.rect.left or \
                        missile.rect.center[1] == self.rect.right:
                    print("опасно")
                    if self.checkTp():
                        self.rect.topleft = self.tank_game.getXY()

    def setImage(self):
        if self.direction == (-1, 0):
            self.image = pygame.image.load("images\\tank_green_left.png")
        elif self.direction == (0, 1):
            self.image = pygame.image.load("images\\tank_green_down.png")
        elif self.direction == (1, 0):
            self.image = pygame.image.load("images\\tank_green_right.png")
        elif self.direction == (0, -1):
            self.image = pygame.image.load("images\\tank_green_up.png")  # "images\\tank_green_up.png"

    def updateShotTimer(self):
        if self.shot_timer > 0:
            self.shot_timer -= 1

    def updateMoveTimer(self):
        if self.move_timer > 0:
            self.move_timer -= 1

    def checkShot(self):
        if self.shot_timer <= 0:
            self.shot_timer = self.shot_delay
            return True
        else:
            return False

    def updateTpTimer(self):
        if self.tp_timer > 0:
            self.tp_timer -= 2

    def checkTp(self):
        if self.tp_timer <= 0:
            self.tp_timer = self.tp_delay
            return True
        else:
            return False

    def calcDirection(self):
        if self.eventkey == pygame.K_LEFT:
            self.direction = (-1, 0)
        elif self.eventkey == pygame.K_RIGHT:
            self.direction = (1, 0)
        elif self.eventkey == pygame.K_UP:
            self.direction = (0, -1)
        elif self.eventkey == pygame.K_DOWN:
            self.direction = (0, 1)
        self.setImage()

    def move(self):
        self.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        self.rect.move_ip(self.speed)

    def setBlock(self):
        if self.direction == (-1, 0):
            Armor(self.tank_game, ((self.rect.topleft[0] + self.tank_game.cell_size) / 32, (self.rect.topleft[1]) / 32))
        elif self.direction == (1, 0):
            Armor(self.tank_game, ((self.rect.topleft[0] - self.tank_game.cell_size) / 32, (self.rect.topleft[1]) / 32))
        elif self.direction == (0, -1):
            Armor(self.tank_game, ((self.rect.topleft[0]) / 32, (self.rect.topleft[1] + self.tank_game.cell_size) / 32))
        elif self.direction == (0, 1):
            Armor(self.tank_game, ((self.rect.topleft[0]) / 32, (self.rect.topleft[1] - self.tank_game.cell_size) / 32))

    def getTpPlace(self):

        if keyboard.is_pressed("f"):
            self.tp_x -= self.tank_game.cell_size
        elif keyboard.is_pressed("h"):
            self.tp_x += self.tank_game.cell_size
        elif keyboard.is_pressed("t"):
            self.tp_y -= self.tank_game.cell_size
        elif keyboard.is_pressed("g"):
            self.tp_y += self.tank_game.cell_size

        cell = pygame.Rect(self.tp_x, self.tp_y, self.tank_game.cell_size, self.tank_game.cell_size)
        pygame.draw.rect(self.tank_game.sc, colors.RED, cell, 1)

        if keyboard.is_pressed("."):
            self.rect.topleft = (self.tp_x, self.tp_y)

    def update(self, *args, **kwargs):
        if self.fl == True and self.tank_game.timer % 10 == 0:
            self.checkHit(100, "oh")
        else:
            self.speed_abs = 32 // 2

        # self.getMissilesXY()

        if keyboard.is_pressed('p') and self.money > 0:
            self.speed_abs = 32 // 1
            self.time = self.tank_game.timer - 20
            self.money -= 1

        if self.time == self.tank_game.timer:
            self.speed_abs = 32 // 2
            self.time = 0

        if self.tank_game.timer % 1 == 0 and self.health < pr1.health and self.fl == False:
            self.health += 10

        if self.save_money < 0:
            self.save_money = 0
        self.drawParameters()
        self.updateShotTimer()
        self.updateTpTimer()
        for event in self.tank_game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN \
                        or event.key == pygame.K_LEFT \
                        or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_SPACE:
                    self.eventkey = event.key
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN \
                        or event.key == pygame.K_LEFT \
                        or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_SPACE:
                    self.eventkey = None

        self.calcDirection()
        if self.eventkey == pygame.K_SPACE and self.checkShot():
            self.shot()
        if keyboard.is_pressed("c") and self.checkShot():
            self.coldShot()
        if keyboard.is_pressed("v") and self.checkShot():
            self.armorShot()

        self.getTpPlace()

        if keyboard.is_pressed("a"):
            print(self.tp_x, self.tp_y)
            for s in self.tank_game.all_sprites:
                if s.rect.topleft == (self.tp_x / self.tank_game.cell_size, self.tp_y / self.tank_game.cell_size):
                    s.kill()
            Armor(self.tank_game, (self.tp_x / self.tank_game.cell_size, self.tp_y / self.tank_game.cell_size))

        if keyboard.is_pressed("x"):
            print(self.tp_x, self.tp_y)
            for s in self.tank_game.all_sprites:
                if s.rect.topleft == (self.tp_x, self.tp_y):
                    s.kill()
            Brick(self.tank_game, (self.tp_x / self.tank_game.cell_size, self.tp_y / self.tank_game.cell_size))

        if keyboard.is_pressed("d"):
            print(self.tp_x, self.tp_y)
            for s in self.tank_game.all_sprites:
                if s.rect.topleft == (self.tp_x, self.tp_y):
                    s.kill()
            Bonus2(self.tank_game, (self.tp_x, self.tp_y))

        if keyboard.is_pressed("z"):
            print(self.tp_x, self.tp_y)
            for sprite in self.tank_game.all_sprites:
                if sprite.rect.topleft == (self.tp_x, self.tp_y):
                    sprite.kill()

        if self.checkMove() and self.fl == False:
            if self.eventkey == pygame.K_LEFT or self.eventkey == pygame.K_RIGHT or self.eventkey == pygame.K_UP or \
                    self.eventkey == pygame.K_DOWN:
                self.move()
                self.checkDynamite()

        self.processBonus()

        if keyboard.is_pressed("ctrl"):
            self.image = pygame.image.load("images/mine.png")
