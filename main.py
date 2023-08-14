import random
import time
import json

import pygame
import pygame_menu
import keyboard
import colorama

import colors
from settings import parametersmytank1 as pr1, parametersmytank2 as pr2
from tank1 import Tank1
from tank2 import Tank2
from mytank1 import MyTank1
from mytank2 import MyTank2

from map import Missile, Armor, Brick, Bonus, Dynamite


class TankGame:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # важно прописать до pygame.init()
        pygame.init()

        # checkPassword()

        self.FPS = 30
        self.cell_size = 32
        self.x_cells = 30
        self.y_cells = 20
        self.timer = 13500

        self.sc = pygame.display.set_mode((self.x_cells * (self.cell_size + 20), self.y_cells * (self.cell_size + 4)))
        pygame.display.set_caption('танчики')
        self.clock = pygame.time.Clock()

        self.start_sound = pygame.mixer.Sound("sounds\\level_start.mp3")

        self.all_sprites = pygame.sprite.Group()
        self.all_not_tnt = pygame.sprite.Group()
        self.all_missiles = pygame.sprite.Group()
        self.all_bricks = pygame.sprite.Group()
        self.all_armors = pygame.sprite.Group()
        self.all_dynamite = pygame.sprite.Group()
        self.all_base1 = pygame.sprite.Group()
        self.all_base2 = pygame.sprite.Group()
        self.all_blocks = pygame.sprite.Group()
        self.all_tanks = pygame.sprite.Group()
        self.all_tank1 = pygame.sprite.Group()
        self.all_tank2 = pygame.sprite.Group()
        self.all_mytanks = pygame.sprite.Group()
        self.all_mytanks2 = pygame.sprite.Group()
        self.all_mytanks1 = pygame.sprite.Group()
        self.all_bad = pygame.sprite.Group()
        self.all_obstacles = pygame.sprite.Group()
        self.all_bonus = pygame.sprite.Group()

        # self.readIn1()
        # self.readIn2()
        self.checkPlay()

        self.game_running = False
        self.player = 1

        self.menu = self.createMenu()

    def createMenu(self):
        menu = pygame_menu.Menu("Магазин", self.x_cells * (self.cell_size + 20), self.y_cells * (self.cell_size + 4),
                                theme=pygame_menu.themes.THEME_BLUE)
        menu.add.selector('игрок', [('MyTank1', 1), ('MyTank2', 2)], onchange=self.choosePlayer)
        menu.add.button('старт', self.startTheGame)
        menu.add.button('урон - 15 монет', self.getDamage)
        menu.add.button('здоровье - 10 монет', self.getHealth)
        menu.add.button('броня - 10 монет', self.getArmor)
        menu.add.button('взрывоустойчивесть - 15 монет', self.getExplosionResistance)
        menu.add.button('снаряды - 10 монет', self.getMissiles)
        menu.add.button('мощные снаряды - 5 монет', self.getMissilesArmor)
        menu.add.button('время телепортации - 10 монет', self.getTpTime)
        menu.add.button('ускоренная стрельба - 10 монет', self.getShotTime)
        menu.add.button('сохранение монет - 1 монета', self.getSaveMoney)
        image = pygame_menu.BaseImage(image_path="images/case.png", )
        menu.add.banner(image, self.test)
        return menu

    def test(self):
        cost = 1
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    r1 = random.randint(0, 92)
                    if r1 <= 70:
                        print(colorama.Style.RESET_ALL + "обычный")
                        tank1.money -= cost
                    elif r1 > 70 and r1 <= 80:
                        print(colorama.Fore.GREEN + "необычный")
                        tank1.money -= cost
                        tank1.money += 2
                    elif r1 > 80 and r1 <= 87:
                        print(colorama.Fore.BLUE + "редкий")
                        tank1.money -= cost
                        tank1.money += 4
                    elif r1 > 87 and r1 <= 90:
                        print("\033[35m" + "эпический")
                        tank1.money -= cost
                        tank1.money += 8
                    elif r1 > 90 and r1 <= 92:
                        print(colorama.Fore.RED + "легендарный")
                        tank1.money -= cost
                        tank1.money += 16
                    print(colorama.Style.RESET_ALL)


        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    r = random.randint(0, 92)
                    if r <= 70:
                        print(colorama.Style.RESET_ALL + "обычный")
                        tank2.money -= cost
                    elif r > 70 and r <= 80:
                        print(colorama.Fore.GREEN + "необычный")
                        tank2.money -= cost
                        tank2.money += 2
                    elif r > 80 and r <= 87:
                        print(colorama.Fore.BLUE + "редкий")
                        tank2.money -= cost
                        tank2.money += 4
                    elif r > 87 and r <= 90:
                        print("\033[35m" + "эпический")
                        tank2.money -= cost
                        tank2.money += 8
                    elif r > 90 and r <= 92:
                        print(colorama.Fore.RED + "легендарный")
                        tank2.money -= cost
                        tank2.money += 16
                        print(colorama.Style.RESET_ALL)

    def checkPassword(self):
        i1 = int(input("введите пароль из цифр: "))
        i2 = float(input("введите цифру: "))

        t = time.localtime(time.time())
        if i1 != t.tm_min or i2 != t.tm_min / 2:
            print("неправильный пароль")
            exit()

    def readIn1(self):
        with open('settings/params1.txt', 'r') as file:
            file.seek(0)
            for line in file:
                if 'health' in line:
                    pr1.health = int(line.split('=')[1])
                if 'armor' in line:
                    pr1.armor = int(line.split('=')[1])
                if 'damage' in line:
                    pr1.damage = int(line.split('=')[1])
                if 'missiles' in line:
                    pr1.missiles = int(line.split('=')[1])
                if 'armor_missiles' in line:
                    pr1.armor_missiles = int(line.split('=')[1])
                if 'money' in line:
                    pr1.money = int(line.split('=')[1])
                if 'save_money' in line:
                    pr1.save_money = int(line.split('=')[1])
                if 'tp_delay' in line:
                    pr1.tp_delay = int(line.split('=')[1])
                if 'explosion_resistance' in line:
                    pr1.explosion_resistance = int(line.split('=')[1])

    def readIn2(self):
        with open('settings/params2.txt', 'r') as file:
            file.seek(0)
            for line in file:
                if 'health' in line:
                    pr2.health = int(line.split('=')[1])
                if 'armor' in line:
                    pr2.armor = int(line.split('=')[1])
                if 'damage' in line:
                    pr2.damage = int(line.split('=')[1])
                if 'missiles' in line:
                    pr2.missiles = int(line.split('=')[1])
                if 'armor_missiles' in line:
                    pr2.armor_missiles = int(line.split('=')[1])
                if 'money' in line:
                    pr2.money = int(line.split('=')[1])
                if 'save_money' in line:
                    pr2.save_money = int(line.split('=')[1])
                if 'tp_delay' in line:
                    pr2.tp_delay = int(line.split('=')[1])
                if 'explosion_resistance' in line:
                    pr2.explosion_resistance = int(line.split('=')[1])

    def checkPlay(self):
        file = None
        try:
            file = open("settings/play_count", 'r', encoding="utf-8")
            r = int(file.read())
        finally:
            file.close()

        file1 = None
        try:
            file1 = open("settings/play_count", 'w', encoding="utf-8")
            if r < 100:
                file1.write(str(r + 1))
            else:
                file1.write(str(100))
                print("лимит исчерпан")
                exit()
        finally:
            file1.close()

    def createMap(self):
        name = input("введите назвение карты: ")
        try:
            if name == "s":
                with open('map/blocks.txt', "r") as json_file:
                    blocks = json.load(json_file)
                    for xy in blocks.get("armors"):
                        Armor(self, xy)
                    for xy in blocks.get("bricks"):
                        Brick(self, xy)

            else:
                with open('map/' + name + '_blocks.txt', "r") as json_file:
                    blocks = json.load(json_file)
                    for xy in blocks.get("armors"):
                        Armor(self, xy)
                    for xy in blocks.get("bricks"):
                        Brick(self, xy)

            print("карта загружена")
            MyTank1(self, self.getXY(), (0, 1))
            MyTank2(self, self.getXY(), (0, 1))
        except FileNotFoundError:
            print("такой карты нет")
            self.createMap()

    def getXY(self):
        while True:
            x_c = []
            for x in range(0, self.x_cells * self.cell_size, self.cell_size):
                x_c.append(x)

            x_rect = random.choice(x_c)

            y_c = []
            for y in range(0, (self.y_cells - 1) * self.cell_size, self.cell_size):
                y_c.append(y)

            y_rect = random.choice(y_c)

            sprites_xy = []
            for sprite in self.all_sprites:
                sprites_xy.append(sprite.rect.topleft)
            if (x_rect, y_rect) not in sprites_xy:
                return (x_rect, y_rect)

    def drawGrid(self):
        for x in range(self.x_cells):
            for y in range(self.y_cells + 1):
                cell = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.sc, colors.WHITE, cell, 1)

    def pressProcessing(self):

        def killAll():
            for tank in self.all_bad:
                tank.kill()
            for brick in self.all_bricks:
                brick.kill()
            for armor in self.all_armors:
                armor.kill()
            for bonus in self.all_bonus:
                bonus.kill()
            for missile in self.all_missiles:
                missile.kill()
            for dynamite in self.all_dynamite:
                dynamite.kill()

        if keyboard.is_pressed('r'):
            for sprite in self.all_sprites:
                sprite.kill()
            self.createMap()

        if keyboard.is_pressed("esc"):
            self.saveMap()

        if keyboard.is_pressed('f1'):
            Tank1(self, self.getXY(), (0, 1))
        if keyboard.is_pressed('f2'):
            Tank2(self, self.getXY(), (0, 1))

        if keyboard.is_pressed('9'):
            for tank2 in self.all_mytanks2:
                if tank2.checkTp():
                    tank2.rect.topleft = self.getXY()

        if keyboard.is_pressed('s + h'):
            self.game_running = False

        if keyboard.is_pressed('n'):
            for tank1 in self.all_mytanks1:
                if tank1.checkTp():
                    tank1.rect.topleft = self.getXY()

        if keyboard.is_pressed('b'):
            for tank1 in self.all_mytanks1:
                if tank1.checkTp():
                    tank1.rect.topleft = (35 * self.cell_size, 10 * self.cell_size)

        if keyboard.is_pressed('enter'):
            for tank1 in self.all_mytanks1:
                if tank1.checkTp() and tank1.money > 0:
                    tank1.money -= 1
                    for tank2 in self.all_mytanks2:
                        tank1.direction = tank2.direction

                        top_left1 = (tank2.getTopLeft()[0], tank2.getTopLeft()[1] - self.cell_size)
                        top_left2 = (tank2.getTopLeft()[0], tank2.getTopLeft()[1] + self.cell_size)
                        top_left3 = (tank2.getTopLeft()[0] + self.cell_size, tank2.getTopLeft()[1])
                        top_left4 = (tank2.getTopLeft()[0] - self.cell_size, tank2.getTopLeft()[1])
                        for block in self.all_blocks:
                            if tank2.direction == (0, 1):
                                tank1.rect.topleft = top_left1
                            elif tank2.direction == (0, -1):
                                tank1.rect.topleft = top_left2
                            elif tank2.direction == (1, 0):
                                tank1.rect.topleft = top_left4
                            elif tank2.direction == (-1, 0):
                                tank1.rect.topleft = top_left3
                            if tank1.rect.topleft[0] <= 0 or tank1.rect.topleft[1] <= 0:
                                tank1.rect.topleft = self.getXY()
                            if tank1.rect.topleft == block.rect.topleft:
                                block.kill()

        if keyboard.is_pressed('alt'):
            for tank1 in self.all_mytanks1:

                if tank1.money > 0 and tank1.missiles > 0 and tank1.checkShot():
                    tank1.money -= 1
                    tank1.shot_sound.play()

                    xy = (tank1.rect.center[0] + tank1.rect.width // 2 * tank1.direction[0],
                          tank1.rect.center[1] + tank1.rect.height // 2 * tank1.direction[1])
                    Missile(self, xy, tank1.direction, 1000 ** 1000, "super",
                            colors.YELLOW)

        if keyboard.is_pressed('3'):
            for tank2 in self.all_mytanks2:
                if tank2.money > 0 and tank2.missiles > 0 and tank2.checkShot():
                    tank2.money -= 1
                    tank2.shot_sound.play()
                    xy = (tank2.rect.center[0] + tank2.rect.width // 2 * tank2.direction[0],
                          tank2.rect.center[1] + tank2.rect.height // 2 * tank2.direction[1])
                    Missile(self, xy, tank2.direction, 1000 ** 1000, "super", colors.YELLOW)

        if keyboard.is_pressed('+'):
            for tank2 in self.all_mytanks2:
                if tank2.checkTp() and tank2.money > 0:
                    tank2.money -= 1
                    for tank1 in self.all_mytanks1:
                        tank2.direction = tank1.direction

                        top_left1 = (tank1.getTopLeft()[0], tank1.getTopLeft()[1] - self.cell_size)
                        top_left2 = (tank1.getTopLeft()[0], tank1.getTopLeft()[1] + self.cell_size)
                        top_left3 = (tank1.getTopLeft()[0] + self.cell_size, tank1.getTopLeft()[1])
                        top_left4 = (tank1.getTopLeft()[0] - self.cell_size, tank1.getTopLeft()[1])
                        for block in self.all_blocks:
                            if tank1.direction == (0, 1):
                                tank2.rect.topleft = top_left1
                            elif tank1.direction == (0, -1):
                                tank2.rect.topleft = top_left2
                            elif tank1.direction == (1, 0):
                                tank2.rect.topleft = top_left4
                            elif tank1.direction == (-1, 0):
                                tank2.rect.topleft = top_left3
                            # if tank2.rect.topleft[0] <= 0 or tank2.rect.topleft[1] <= 0 or:
                            #     tank2.rect.topleft = getXY()

                            if tank2.rect.topleft[0] < 0 or tank2.rect.topleft[0] > self.x_cells * self.cell_size or \
                                    tank2.rect.topleft[1] < 0 or tank2.rect.topleft[1] > self.y_cells * self.cell_size:
                                tank2.rect.topleft = self.getXY()

                            if tank2.rect.topleft == block.rect.topleft:
                                block.kill()

        if keyboard.is_pressed('m + 2'):
            MyTank2(self, self.getXY(), (0, 1))
        if keyboard.is_pressed('m + 1'):
            MyTank1(self, self.getXY(), (0, 1))

        if keyboard.is_pressed(','):
            Bonus(self)
        if keyboard.is_pressed('delete'):
            killAll()

        if keyboard.is_pressed('shift + l'):
            Dynamite(self, self.getXY())

    def choosePlayer(self, value, x):
        self.player = value[0][1]
        print(self.player)

    def getDamage(self):
        cost = 15
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if keyboard.is_pressed("ctrl"):
                    if tank1.money >= cost:
                        num = tank1.money // cost
                        tank1.damage += (1000 * num)
                        tank1.money -= (cost * num)
                        pr1.damage += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank1.money >= cost:
                        tank1.damage += 1000
                        tank1.money -= cost
                        pr1.damage += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if keyboard.is_pressed("ctrl"):
                    if tank2.money >= cost:
                        num = tank2.money // cost
                        tank2.damage += (1000 * num)
                        tank2.money -= (cost * num)
                        pr2.health += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank2.money >= cost:
                        tank2.damage += 1000
                        tank2.money -= cost
                        pr2.damage += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

    def getHealth(self):
        cost = 10
        if self.player == 1:

            for tank1 in self.all_mytanks1:
                if keyboard.is_pressed("ctrl"):
                    if tank1.money >= cost:
                        num = tank1.money // cost
                        tank1.health += (1000 * num)
                        tank1.money -= (cost * num)
                        pr1.health += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank1.money >= cost:
                        tank1.health += 1000
                        tank1.money -= cost
                        pr1.health += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if keyboard.is_pressed("ctrl"):
                    if tank2.money >= cost:
                        num = tank2.money // cost
                        tank2.health += (1000 * num)
                        tank2.money -= (cost * num)
                        pr2.health += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank2.money >= cost:
                        tank2.health += 1000
                        tank2.money -= cost
                        pr2.health += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

    def getArmor(self):
        cost = 10
        if self.player == 1:
            for tank1 in self.all_mytanks1:

                if keyboard.is_pressed("ctrl"):
                    if tank1.money > cost:
                        num = tank1.money // cost
                        tank1.armor += (1000 * num)
                        tank1.money -= (cost * num)
                        pr1.armor += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank1.money >= cost:
                        tank1.armor += 1000
                        tank1.money -= cost
                        pr1.armor += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if keyboard.is_pressed("ctrl"):
                    if tank2.money > cost:
                        num = tank2.money // cost
                        tank2.armor += (1000 * num)
                        tank2.money -= (cost * num)
                        pr2.armor += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank2.money >= cost:
                        tank2.armor += 1000
                        tank2.money -= cost
                        pr2.armor += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

    def getExplosionResistance(self):
        cost = 15
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    tank1.explosion_resistance += 1000
                    tank1.money -= cost
                    pr1.explosion_resistance += 1000
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    tank2.explosion_resistance += 1000
                    tank2.money -= cost
                    pr2.explosion_resistance += 1000
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def getMissiles(self):
        cost = 10
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if keyboard.is_pressed("ctrl"):
                    if tank1.money >= cost:
                        num = tank1.money // cost
                        tank1.missiles += (1000 * num)
                        tank1.money -= (cost * num)
                        pr1.missiles += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank1.money >= cost:
                        tank1.missiles += 1000
                        tank1.money -= cost
                        pr1.missiles += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if keyboard.is_pressed("ctrl"):
                    if tank2.money >= cost:
                        num = tank2.money // cost
                        tank2.missiles += (1000 * num)
                        tank2.money -= (cost * num)
                        pr1.missiles += (1000 * num)
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)
                else:
                    if tank2.money >= cost:
                        tank2.missiles += 1000
                        tank2.money -= cost
                        pr1.missiles += 1000
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "недостаточно монет!")
                        print(colorama.Style.RESET_ALL)

    def getMissilesArmor(self):
        cost = 5
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    tank1.armor_missiles += 10
                    tank1.money -= cost
                    pr1.armor_missiles += 10
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    tank2.armor_missiles += 10
                    tank2.money -= cost
                    pr2.armor_missiles += 10
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def getSuperLot(self):
        cost = 100
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    tank1.missiles += 600
                    tank1.armor += 600
                    tank1.health += 600
                    tank1.damage += 600
                    tank1.explosion_resistance += 600
                    tank1.money -= cost
                    pr1.missiles += 600
                    pr1.armor += 600
                    pr1.health += 600
                    pr1.damage += 600
                    pr1.explosion_resistance += 600
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    tank2.missiles += 600
                    tank2.armor += 600
                    tank2.health += 600
                    tank2.damage += 600
                    tank2.explosion_resistance += 600
                    tank2.money -= cost
                    pr2.missiles += 600
                    pr2.armor += 600
                    pr2.health += 600
                    pr2.damage += 600
                    pr2.explosion_resistance += 600
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def getTpTime(self):
        cost = 10
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    if tank1.tp_delay > 20:
                        tank1.tp_delay -= 10
                        tank1.money -= cost
                        pr1.tp_delay -= 10
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "минимальный уровень задержки телепортации - 20")
                        print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    if tank2.tp_delay > 20:
                        tank2.tp_delay -= 10
                        tank2.money -= cost
                        pr2.tp_delay -= 10
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)

                    else:
                        print(colorama.Fore.RED, "минимальный уровень задержки телепортации - 20")
                        print(colorama.Style.RESET_ALL)

                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def getShotTime(self):
        cost = 10
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    if tank1.shot_delay > 2:
                        tank1.shot_delay -= 1
                        tank1.money -= cost
                        pr1.shot_delay -= 1
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "минимальный уровень задержки cтельбы - 2")
                        print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    if tank2.shot_delay > 2:
                        tank2.shot_delay -= 1
                        tank2.money -= cost
                        pr2.shot_delay -= 1
                        print(colorama.Fore.GREEN, "покупка совершена")
                        print(colorama.Style.RESET_ALL)
                    else:
                        print(colorama.Fore.RED, "минимальный уровень задержки cтельбы - 2")
                        print(colorama.Style.RESET_ALL)

                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def getSaveMoney(self):
        cost = 1
        if self.player == 1:
            for tank1 in self.all_mytanks1:
                if tank1.money >= cost:
                    tank1.save_money += 1
                    tank1.money -= cost
                    pr1.save_money += 1

                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)
        elif self.player == 2:
            for tank2 in self.all_mytanks2:
                if tank2.money >= cost:
                    tank2.save_money += 1
                    tank2.money -= cost
                    pr2.save_money += 1
                    print(colorama.Fore.GREEN, "покупка совершена")
                    print(colorama.Style.RESET_ALL)
                else:
                    print(colorama.Fore.RED, "недостаточно монет!")
                    print(colorama.Style.RESET_ALL)

    def startTheGame(self):
        self.game_running = True

    def write1(self):
        with open('settings/params1.txt', 'w') as file:
            # записываем параметры в файл
            file.write(f'health={pr1.health}\n')
            file.write(f'armor={pr1.armor}\n')
            file.write(f'damage={pr1.damage}\n')
            file.write(f'missiles={pr1.missiles}\n')
            file.write(f'armor_missiles={pr1.armor_missiles}\n')
            file.write(f'money={pr1.money}\n')
            file.write(f'save_money={pr1.save_money}\n')
            file.write(f'tp_delay={pr1.tp_delay}\n')
            file.write(f'shot_delay={pr1.shot_delay}\n')
            file.write(f'explosion_resistance={pr1.explosion_resistance}\n')

    def write2(self):
        with open('settings/params2.txt', 'w') as file:
            # записываем параметры в файл
            file.write(f'health={pr2.health}\n')
            file.write(f'armor={pr2.armor}\n')
            file.write(f'damage={pr2.damage}\n')
            file.write(f'missiles={pr2.missiles}\n')
            file.write(f'armor_missiles={pr2.armor_missiles}\n')
            file.write(f'money={pr2.money}\n')
            file.write(f'save_money={pr2.save_money}\n')
            file.write(f'tp_delay={pr2.tp_delay}\n')
            file.write(f'shot_delay={pr2.shot_delay}\n')
            file.write(f'explosion_resistance={pr2.explosion_resistance}\n')

    def playGame(self, events):
        if self.timer % 100 == 0:
            print(self.timer)
        self.timer -= 1
        if self.timer <= 0:
            s1 = 0
            s2 = 0
            for tank1 in self.all_mytanks1:
                s1 = tank1.kills
            for tank2 in self.all_mytanks2:
                s2 = tank2.kills

            if s1 < s2:
                print("TANK2 победил")
            elif s1 > s2:
                print("TANK1 победил")
            else:
                print("ничья")

            self.write1()
            self.write2()
            exit()

        if len(self.all_bonus) < 10:
            Bonus(self)

        self.pressProcessing()
        self.sc.fill(colors.BLACK)
        self.all_sprites.draw(self.sc)
        self.all_sprites.update(events=events)

        # drawGrid()

    def saveMap(self):
        name = input("Введите назвение карты: ")
        bricks = []
        for brick in self.all_bricks:
            bricks.append((brick.rect.topleft[0] // self.cell_size, brick.rect.topleft[1] // self.cell_size))

        armors = []
        for armor in self.all_armors:
            armors.append((armor.rect.topleft[0] // self.cell_size, armor.rect.topleft[1] // self.cell_size))

        blocks_dict = {"armors": armors, "bricks": bricks}

        with open("map/" + name + '_blocks.txt', "w") as file:
            json.dump(blocks_dict, file)

    def main(self):
        self.createMap()
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.write1()
                    self.write2()
                    exit()

            if self.game_running:
                self.playGame(self.events)
            else:
                self.menu.update(self.events)
                self.menu.draw(self.sc)
                self.events = None
                for tank1 in self.all_mytanks1:
                    font1 = pygame.font.SysFont("Segoe UI", self.cell_size - 5)
                    money_render1 = font1.render(f"TANK1 - {tank1.money} монет", True, colors.RED)
                    self.sc.blit(money_render1, (self.cell_size * 33, self.cell_size * 1))
                for tank2 in self.all_mytanks2:
                    font2 = pygame.font.SysFont("Segoe UI", self.cell_size - 5)
                    money_render2 = font2.render(f"TANK2 - {tank2.money} монет", True, colors.RED)
                    self.sc.blit(money_render2, (self.cell_size * 33, self.cell_size * 2))
            pygame.display.update()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    TankGame().main()

