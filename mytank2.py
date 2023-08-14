import random

import pygame
import keyboard

import colors
from settings import parametersmytank1 as pr1, parametersmytank2 as pr2
from map import Missile, Bonus


class MyTank2(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy, direction):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.direction = direction
        self.setImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.speed_abs = 32//2
        self.speed = (self.direction[0]*self.speed_abs, self.direction[1]*self.speed_abs)
        self.shot_timer = 0
        self.shot_delay = pr1.shot_delay
        self.tp_timer = 0
        self.tp_delay = pr2.tp_delay
        self.health = pr2.health
        self.armor = pr2.armor
        self.damage = pr2.damage
        self.missiles = pr2.missiles
        self.armor_missiles = pr2.armor_missiles
        self.money = pr2.money
        self.save_money = pr2.save_money
        self.explosion_resistance = pr2.explosion_resistance
        self.kills = pr2.kills
        self.eventkey = None
        self.shot_sound = pygame.mixer.Sound("sounds\\shot.wav")
        self.bonus_sound = pygame.mixer.Sound("sounds\\star.wav")
        self.time = 0
        self.fl = False
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_tanks.add(self)
        self.tank_game.all_mytanks.add(self)
        self.tank_game.all_mytanks2.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)

    def getMoney(self, money):
        self.money += money
        pr2.money += money

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
            Missile(self.tank_game, xy, self.direction, self.damage, "mytank2", colors.RED)

    def armorShot(self):
        if self.armor_missiles > 0:
            self.armor_missiles -= 1
            self.shot_sound.play()
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "armor", colors.ORANGE)

    def coldShot(self):
        if self.missiles > 0:
            self.missiles -= 1
            self.shot_sound.play()
            xy = (self.rect.center[0] + self.rect.width // 2 * self.direction[0],
                  self.rect.center[1] + self.rect.height // 2 * self.direction[1])
            Missile(self.tank_game, xy, self.direction, self.damage, "cold", colors.BLUE)


    def checkDynamite(self):
        tank_check = MyTank2(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        obstacles = pygame.sprite.spritecollide(tank_check, self.tank_game.all_dynamite, False)
        tank_check.kill()
        if len(obstacles) > 0:
            obstacles[0].bang()

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
            pr2.health += effects_dict["health"]
        if "damage" in effects_dict.keys():
            self.damage += effects_dict["damage"]
            pr2.damage += effects_dict["damage"]
        if "armor" in effects_dict.keys():
            self.armor += effects_dict["armor"]
            pr2.armor +=  effects_dict["armor"]
        if "missiles" in effects_dict.keys():
            self.missiles += effects_dict["missiles"]
            pr2.missiles += effects_dict["missiles"]
        if "money" in effects_dict.keys():
            self.money += effects_dict["money"]
            pr2.money += effects_dict["money"]
        if "explosion_resistance" in effects_dict.keys():
            self.explosion_resistance += effects_dict["explosion_resistance"]
            pr2.explosion_resistance += effects_dict["explosion_resistance"]
        self.bonus_sound.play()

    def checkCold(self, damage):
        self.health -= damage
        if self.health <= 0:
            for tank1 in self.tank_game.all_mytanks1:
                tank1.plusKills()
                pr1.kills += 1
                self.fl = False
            print("MyTank2 УБИТ!!!")
            self.drawBang(self)
            self.health = pr2.health
            self.armor = pr2.armor
            self.damage = pr2.damage
            self.missiles = pr2.missiles
            self.armor_missiles = pr2.armor_missiles
            self.kills = pr2.kills
            self.explosion_resistance = pr2.explosion_resistance
            self.rect.topleft = self.tank_game.getXY()
            if self.save_money > 0:
                self.save_money -= 1
                pr2.save_money -= 1
            else:
                for tank1 in self.tank_game.all_mytanks1:
                    tank1.getMoney(self.money)
                self.money = 0
                pr2.money = 0

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
                    for tank1 in self.tank_game.all_mytanks1:
                        tank1.plusKills()
                        pr1.kills += 1

                        self.fl = False
                    print("MyTank2 УБИТ!!!")
                    self.drawBang(self)
                    self.health = pr2.health
                    self.armor = pr2.armor
                    self.damage = pr2.damage
                    self.missiles = pr2.missiles
                    self.armor_missiles = pr2.armor_missiles
                    self.kills = pr2.kills
                    self.explosion_resistance = pr2.explosion_resistance
                    self.rect.topleft = self.tank_game.getXY()
                    if self.save_money > 0:
                        self.save_money -= 1
                        pr2.save_money -= 1
                    else:
                        for tank1 in self.tank_game.all_mytanks1:
                            tank1.getMoney(self.money)
                        self.money = 0
                        pr2.money = 0


    def drawParameters(self):
        font = pygame.font.SysFont("Segoe UI", self.tank_game.cell_size-5)

        tank_render = font.render("TANK2", True, colors.RED)
        self.tank_game.sc.blit(tank_render, (self.tank_game.cell_size * 43, self.tank_game.cell_size * 1))

        health_render = font.render(f"Здоровье: {self.health}", True, colors.RED)
        self.tank_game.sc.blit(health_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 2))

        armor_render = font.render(f"броня: {self.armor}", True, colors.RED)
        self.tank_game.sc.blit(armor_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 3))

        damage_render = font.render(f"Урон: {self.damage}", True, colors.RED)
        self.tank_game.sc.blit(damage_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 4))

        tp_render = font.render(f"Tp Time: {self.tp_delay - self.tp_timer}", True, colors.RED)
        self.tank_game.sc.blit(tp_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 5))

        explosion_resistance_render = font.render(f"взрыв. уст.: {self.explosion_resistance}", True, colors.RED)
        self.tank_game.sc.blit(explosion_resistance_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 6))

        missiles_render = font.render(f"снаряды: {self.missiles}", True, colors.RED)
        self.tank_game.sc.blit(missiles_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 7))

        kills_render = font.render(f"убито: {self.kills}", True, colors.RED)
        self.tank_game.sc.blit(kills_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 8))

        money_render = font.render(f"монет: {self.money}", True, colors.RED)
        self.tank_game.sc.blit(money_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 9))

        save_render = font.render(f"сохранений: {self.save_money}", True, colors.RED)
        self.tank_game.sc.blit(save_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 10))

        armor_missiles_render = font.render(f"мощн. снаряды: {self.armor_missiles}", True, colors.RED)
        self.tank_game.sc.blit(armor_missiles_render, (self.tank_game.cell_size * 42, self.tank_game.cell_size * 11))

    def plusKills(self):
        self.kills += 1

    def checkMove(self):
        tank_check = MyTank2(self.tank_game, self.rect.topleft, self.direction)
        tank_check.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        tank_check.rect.move_ip(tank_check.speed)
        obstacles = pygame.sprite.spritecollide(tank_check, self.tank_game.all_obstacles, False)
        tank_check.kill()
        if len(obstacles) > 2 or tank_check.rect.left < 0 or tank_check.rect.top < 0 or\
                tank_check.rect.right > self.tank_game.x_cells*self.tank_game.cell_size or tank_check.rect.bottom > self.tank_game.y_cells*self.tank_game.cell_size-1:
            return False
        else:
            return True

    def setImage(self):
        if self.direction == (-1, 0):
            self.image = pygame.image.load("images\\tank_yellow_left.png")#"images\\tank_yellow_left.png"
        elif self.direction == (0, 1):
            self.image = pygame.image.load("images\\tank_yellow_down.png")
        elif self.direction == (1, 0):
            self.image = pygame.image.load("images\\tank_yellow_right.png")
        elif self.direction == (0, -1):
            self.image = pygame.image.load("images\\tank_yellow_up.png")

    def updateShotTimer(self):
        if self.shot_timer > 0:
            self.shot_timer -= 1

    def checkShot(self):
        if self.shot_timer <= 0:
            self.shot_timer = self.shot_delay
            return True
        else:
            return False

    def updateTpTimer(self):
        if self.tp_timer > 0:
            self.tp_timer -= 1

    def checkTp(self):
        if self.tp_timer <= 0:
            self.tp_timer = self.tp_delay
            return True
        else:
            return False

    def calcDirection(self):
        if self.eventkey == pygame.K_KP4:
            self.direction = (-1, 0)
        elif self.eventkey == pygame.K_KP6:
            self.direction = (1, 0)
        elif self.eventkey == pygame.K_KP8:
            self.direction = (0, -1)
        elif self.eventkey == pygame.K_KP5:
            self.direction = (0, 1)
        self.setImage()

    def move(self):
        self.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        self.rect.move_ip(self.speed)

    def update(self, *args, **kwargs):
        if self.fl == True and self.tank_game.timer % 10 == 0:
            self.checkHit(100, "oh")
        else:
            self.speed_abs = 32//2


        if self.tank_game.timer % 1 == 0 and self.health < pr2.health and self.fl == False:
            self.health += 10

        if keyboard.is_pressed('/') and self.money > 0:
            self.speed_abs = 32 // 1
            self.time = self.tank_game.timer - 20
            self.money -= 1

        if self.time == self.tank_game.timer:
            self.speed_abs = 32 // 2
            self.time = 0

        if self.save_money < 0:
            self.save_money = 0
        self.drawParameters()
        self.updateShotTimer()
        self.updateTpTimer()
        for event in self.tank_game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP8\
                        or event.key == pygame.K_KP5 \
                        or event.key == pygame.K_KP4 \
                        or event.key == pygame.K_KP6\
                        or event.key == pygame.K_KP7\
                        or event.key == pygame.K_KP9:
                    self.eventkey = event.key
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_KP8\
                        or event.key == pygame.K_KP5 \
                        or event.key == pygame.K_KP4 \
                        or event.key == pygame.K_KP6\
                        or event.key == pygame.K_KP7\
                        or event.key == pygame.K_KP9:
                    self.eventkey = None

        self.calcDirection()
        if self.eventkey == pygame.K_KP7 and self.checkShot():
            self.shot()
        if keyboard.is_pressed("0") and self.checkShot():
            self.armorShot()
        if keyboard.is_pressed("-") and self.checkShot():
            self.coldShot()


        if self.checkMove() and self.fl == False:
            if self.eventkey == pygame.K_KP4 or self.eventkey == pygame.K_KP6 or self.eventkey == pygame.K_KP8 or \
                    self.eventkey == pygame.K_KP5:
                self.move()
                self.checkDynamite()
        self.processBonus()


        if keyboard.is_pressed("1"):
            self.image = pygame.image.load("images/hide.png")