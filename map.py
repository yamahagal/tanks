import random

import pygame

import colors

class Missile(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy, direction, damage, owner, color):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.Surface((2, 2))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.center = (xy[0]+self.direction[0]*(self.rect.width//2), xy[1]+self.direction[1]*(self.rect.height//2))
        self.speed_abs = 30
        self.damage = damage
        self.owner = owner
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_missiles.add(self)
        self.tank_game.all_not_tnt.add(self)

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

    def checkHit(self):
        bricks_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_bricks, False)
        if len(bricks_to_kill) > 0:
            for brick in bricks_to_kill:
                self.drawBang(brick)
                brick.kill()
            if self.owner != "super":
                self.kill()

        armors_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_armors, False)
        if len(armors_to_kill) > 0:
            for armor in armors_to_kill:
                armor.checkHit(self.damage)
                self.kill()


        base1_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_base1, False)
        if len(base1_to_kill) > 0:
            for base1 in base1_to_kill:
                base1.checkHit(self.damage)
            if self.owner != "super":
                self.kill()

        base2_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_base2, False)
        if len(base2_to_kill) > 0:
            for base2 in base2_to_kill:
                base2.checkHit(self.damage)
            if self.owner != "super":
                self.kill()

        tanks_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_tanks, False)
        if len(tanks_to_kill) > 0:
            for tank in tanks_to_kill:
                tank.checkHit(self.damage, self.owner)
                self.drawBang(tank)
            if self.owner != "super":
                self.kill()


        dynamite_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_dynamite, False)
        if len(dynamite_to_kill) > 0:
            for dynamite in dynamite_to_kill:
                dynamite.bang()
                self.drawBang(dynamite)
            if self.owner != "super":
                self.kill()

        bonuses_to_kill = pygame.sprite.spritecollide(self, self.tank_game.all_bonus, False)
        if len(bonuses_to_kill) > 0:
            for bonus in bonuses_to_kill:
                bonus.checkHit()
                self.drawBang(bonus)
            if self.owner != "super":
                self.kill()

    def update(self, *args, **kwargs):
        self.speed = (self.direction[0] * self.speed_abs, self.direction[1] * self.speed_abs)
        self.rect.move_ip(self.speed)
        self.checkHit()
        if self.rect.center[0] < 0 or self.rect.center[0] > self.tank_game.x_cells*self.tank_game.cell_size or \
            self.rect.center[1] < 0 or self.rect.center[1] > self.tank_game.y_cells*self.tank_game.cell_size:
            self.kill()

class Brick(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.image.load("images\\block_brick.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (xy[0]*self.tank_game.cell_size,  xy[1]*self.tank_game.cell_size)
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_bricks.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

class Armor(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.image.load("images\\block_armor.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (xy[0]*self.tank_game.cell_size,  xy[1]*self.tank_game.cell_size)
        self.health = 1000000000
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_armors.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

    def checkHit(self, damage):
        self.drawParameters()
        self.health -= damage
        if self.health <= 0:
            self.drawBang(self)
            self.kill()

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

    def drawParameters(self):
        font = pygame.font.SysFont("Segoe UI", 10)
        score_render = font.render(f"{self.health}", 1, colors.RED)
        self.tank_game.sc.blit(score_render, (self.rect.topleft[0], self.rect.topleft[1]-20))

class Bonus(pygame.sprite.Sprite):
    def __init__(self, tank_game):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.health = 0
        self.damage = 0
        self.armor = 0
        self.missiles = 0
        self.coin = 0
        self.explosion_resistance = 0
        self.image = pygame.image.load("images\\bonus_time.png")
        self.chooseEffect()
        self.setImage()
        self.two = 1
        self.rect = self.image.get_rect()
        self.rect.topleft = self.getXY()
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_bonus.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

    def checkHit(self):
        self.drawBang(self)
        self.kill()

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

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

    def chooseEffect(self):
        effect = random.choice(['health', 'armor', 'coin'])#, 'damage' , 'missiles'
        if effect == 'health':
            self.health = 100
        elif effect == 'damage':
            self.damage = 100
        elif effect == 'armor':
            self.armor = 100
        elif effect == 'missiles':
            self.missiles = 100
        elif effect == 'coin':
            self.coin = 1
        elif effect == 'explosion_resistance':
            self.explosion_resistance = 1

        super_effect2 = random.randint(0, 90)
        if super_effect2 == 1:
            self.coin = 50


        # super_effect = random.choice(['super', 'bad', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'])
        # if super_effect == 'super':
        #     self.health = 100
        #     self.damage = 100
        #     self.armor = 100
        #     self.missiles = 100
        #     self.explosion_resistance = 1
        # elif super_effect == 'bad':
        #     self.health = -100
        #     self.damage = -100
        #     self.armor = -100
        #     self.explosion_resistance = 0

    def setImage(self):
        if self.armor == 100 and self.health == 100 and self.damage == 100 and self.missiles == 100 and self.explosion_resistance == 1\
                or self.armor == -100 and self.health == -100 and self.damage == -100 and self.explosion_resistance == 0:
            self.image = pygame.image.load("images\\bonus_super.png")
        elif self.armor == 100:
            self.image = pygame.image.load("images\\bonus_helmet.png")
        elif self.coin == 50:
            self.image = pygame.image.load("images\\bonus_super_coin.png")
        elif self.health == 100:
            self.image = pygame.image.load("images\\bonus_health.png")
        elif self.missiles == 100:
            self.image = pygame.image.load("images\\bonus_missiles.png")
        elif self.damage == 100:
            self.image = pygame.image.load("images\\bonus_b.png")
        elif self.explosion_resistance == 1:
            self.image = pygame.image.load("images\\bonus_explosion_resistance.png")
        elif self.coin == 1:
            self.image = pygame.image.load("images\\bonus_coin.png")

    def getEffects(self):
        effects = {"health": self.health, "damage": self.damage, "armor": self.armor, "money": self.coin, "missiles": self.missiles, "explosion_resistance": self.explosion_resistance}
        return effects

class Bonus2(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.health = 0
        self.damage = 0
        self.armor = 0
        self.missiles = 0
        self.coin = 50
        self.explosion_resistance = 0
        self.image = pygame.image.load("images\\bonus_time.png")
        self.setImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.two = 2
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_bonus.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

    def checkHit(self):
        self.drawBang(self)
        self.kill()


    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)


    def setImage(self):
        if self.armor == 100 and self.health == 100 and self.damage == 100 and self.missiles == 100 and self.explosion_resistance == 1\
                or self.armor == -100 and self.health == -100 and self.damage == -100 and self.explosion_resistance == 0:
            self.image = pygame.image.load("images\\bonus_super.png")
        elif self.armor == 100:
            self.image = pygame.image.load("images\\bonus_helmet.png")
        elif self.coin == 50:
            self.image = pygame.image.load("images\\bonus_super_coin.png")
        elif self.health == 100:
            self.image = pygame.image.load("images\\bonus_health.png")
        elif self.missiles == 100:
            self.image = pygame.image.load("images\\bonus_missiles.png")
        elif self.damage == 100:
            self.image = pygame.image.load("images\\bonus_b.png")
        elif self.explosion_resistance == 1:
            self.image = pygame.image.load("images\\bonus_explosion_resistance.png")
        elif self.coin == 1:
            self.image = pygame.image.load("images\\bonus_coin.png")

    def getEffects(self):
        effects = {"health": self.health, "damage": self.damage, "armor": self.armor, "money": self.coin, "missiles": self.missiles, "explosion_resistance": self.explosion_resistance}
        return effects

class Dynamite(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.image.load("images\\mine.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = self.tank_game.getXY()
        self.round = random.randint(64, 256)
        self.damage = 10000
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_dynamite.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_blocks.add(self)

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)


    def bang(self):
        self.kill()

        # for bonus in all_bonus:
        #     if bonus.rect.topleft[0]>=self.rect.topleft[0]-self.round and bonus.rect.topleft[0]<=self.rect.topleft[0]+self.round:
        #         if bonus.rect.topleft[1]>=self.rect.topleft[1]-self.round and bonus.rect.topleft[1]<=self.rect.topleft[1]+self.round:
        #             self.drawBang(bonus)
        #             bonus.kill()

        for dynamite in self.tank_game.all_dynamite:
            if dynamite.rect.topleft[0]>=self.rect.topleft[0]-self.round and dynamite.rect.topleft[0]<=self.rect.topleft[0] +self.round:
                if dynamite.rect.topleft[1]>=self.rect.topleft[1]-self.round and dynamite.rect.topleft[1]<=self.rect.topleft[1] +self.round:
                    self.drawBang(dynamite)
                    dynamite.bang()

        for tank in self.tank_game.all_tanks:
            if tank.rect.topleft[0]>=self.rect.topleft[0]-self.round and tank.rect.topleft[0]<=self.rect.topleft[0] +self.round:
                if tank.rect.topleft[1]>=self.rect.topleft[1]-self.round and tank.rect.topleft[1]<=self.rect.topleft[1] +self.round:
                    if tank.explosion_resistance <= 0:
                        tank.checkHit(self.damage, "k")
                    else:
                        tank.explosion_resistance -= 1

        for brick in self.tank_game.all_bricks:
            if brick.rect.topleft[0]>=self.rect.topleft[0]-self.round and brick.rect.topleft[0]<=self.rect.topleft[0]+self.round:
                if brick.rect.topleft[1]>=self.rect.topleft[1]-self.round and brick.rect.topleft[1]<=self.rect.topleft[1]+self.round:
                    self.drawBang(tank)
                    brick.kill()

        for armor in self.tank_game.all_armors:
            if armor.rect.topleft[0]>=self.rect.topleft[0]-self.round and armor.rect.topleft[0]<=self.rect.topleft[0]+self.round:
                if armor.rect.topleft[1]>=self.rect.topleft[1]-self.round and armor.rect.topleft[1]<=self.rect.topleft[1]+self.round:
                    armor.checkHit(self.damage)

class Base1(pygame.sprite.Sprite):
    def __init__(self, tank_game, xy):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.image.load("images\\base.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.health = 50000
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_base1.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

    def checkHit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.drawBang(self)
            self.kill()
            print("tank1 проиграл")


    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)

class Base2(pygame.sprite.Sprite):
    def __init__(self, tank_game):
        pygame.sprite.Sprite.__init__(self)
        self.tank_game = tank_game
        self.image = pygame.image.load("images\\base.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (29*self.tank_game.cell_size,  9*self.tank_game.cell_size)
        self.health = 50000
        self.tank_game.all_sprites.add(self)
        self.tank_game.all_base2.add(self)
        self.tank_game.all_obstacles.add(self)
        self.tank_game.all_not_tnt.add(self)
        self.tank_game.all_blocks.add(self)

    def checkHit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.drawBang(self)
            self.kill()
            print("tank2 проиграл")

    def drawBang(self, obg):
        cell = pygame.Rect(obg.rect.topleft[0], obg.rect.topleft[1], self.tank_game.cell_size, self.tank_game.cell_size)
        img2 = pygame.image.load("images\\bang2.png")
        self.tank_game.sc.blit(img2, cell)
