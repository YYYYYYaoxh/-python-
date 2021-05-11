import time

import pygame

from sprites import *
from collide_plant import *


class Main(object):
    def __init__(self):
        """初始化"""
        pygame.init()
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("植物大战僵尸 by YXH")
        # 创建菜单
        self.menu = pygame.image.load("./images/menu/Surface.png")
        self.one = pygame.image.load("./images/menu/1.png")
        self.two = pygame.image.load("./images/menu/2.png")
        self.three = pygame.image.load("./images/menu/3.png")
        self.four = pygame.image.load("./images/menu/4.png")
        self.five = pygame.image.load("./images/menu/5.png")
        self.six = pygame.image.load("./images/menu/6.png")
        self.help = pygame.image.load("./images/menu/Help.png")
        # 设置时钟
        self.clock = pygame.time.Clock()
        # 定义循环次数量更换图片以制造动画效果
        self.index = 0
        # 音乐初始化
        pygame.mixer.init()
        pygame.mixer.music.load('./music/Crazy Dave IN-GAME.mp3')
        self.lose_sound = pygame.mixer.Sound("./music/lose_sound.wav")
        self.zombie_coming_sound = pygame.mixer.Sound("./music/zombie_coming.wav")
        pygame.mixer.music.play()
        # 字体渲染
        self.sun_num1 = 1000
        self.sun_front = pygame.font.SysFont('arial', 20)
        self.sun_num = self.sun_front.render(str(self.sun_num1), True, (0, 0, 0))
        # 鼠标位置捕获
        self.x, self.y = pygame.mouse.get_pos()
        # 创建事件
        pygame.time.set_timer(SUN_EVENT, 10000)
        pygame.time.set_timer(BULLET_EVENT, 1000)
        pygame.time.set_timer(ZOMBIE_EVENT, 8000)
        pygame.time.set_timer(FLOWER_SUN_EVENT, 1000)
        # 创建精灵
        self.__create_sprite()
        self.choose = 0
        # 创建暂停变量
        self.pause = False
        # 加载暂停按钮的图片
        self.pause_image = pygame.image.load("./images/game_pause_nor.png").convert_alpha()
        self.pause_image_rect = self.pause_image.get_rect()
        # 加载暂停时的图片
        self.pause_images = pygame.image.load("./images/pause.png").convert_alpha()
        # 加载僵尸进屋时的失败图片
        self.lose_image = pygame.image.load("./images/GameOver.png").convert_alpha()
        # 定义一个变量区分游戏是否失败
        self.isLose = False
        # 定义一个变量以使第一个僵尸出现时，播放音效
        self.coming = 0

    def start_game(self):
        """游戏开始程序"""
        while True:
            # 设置帧率
            self.clock.tick(FRAME)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__collide_cheek()
            # 位置更新
            self.__sprite_update()
            # 调用update（）方法
            pygame.display.update()

    def __create_sprite(self):
        """精灵创建"""
        self.BG = pygame.image.load("./images/Background.jpg").convert_alpha()
        self.Card_Slot = pygame.image.load("./images/cardSlot.png") .convert_alpha()
        self.card_peashooter = Card("./images/cards/card_peashooter.png")
        self.card_sunflower = Card("./images/cards/card_sunflower.png")
        self.card_wall_nut = Card("./images/cards/card_wallnut.png")
        self.Peashooter_group = pygame.sprite.Group()
        self.Sunflower_group = pygame.sprite.Group()
        self.WallNut_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.sun_group = pygame.sprite.Group()
        self.zombie_group = pygame.sprite.Group()

    def __event_handler(self):
        """事件监听"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出事件
                self.__game_over()
            if event.type == SUN_EVENT:
                # 太阳掉落
                sun = Sun(10)
                self.sun_group.add(sun)
            if event.type == BULLET_EVENT:
                # 豌豆射手发射子弹
                for sprite in self.Peashooter_group:
                    bullet = Bullet(sprite.rect, 983)
                    self.bullet_group.add(bullet)
            if event.type == FLOWER_SUN_EVENT:
                # 太阳花生产太阳
                for self.sprite in self.Sunflower_group:
                    now = time.time()
                    if now - self.sprite.last_time >= 8:
                        sun = Sun(0)
                        sun.rect.x = self.sprite.rect.x + 20
                        sun.rect.y = self.sprite.rect.y + 30
                        self.sun_group.add(sun)
                        self.sprite.last_time = now
            if event.type == ZOMBIE_EVENT:
                self.coming += 1
                if self.coming == 1:
                    self.zombie_coming_sound.play()
                # 僵尸出现
                zombie = Zombie()
                list_y = (100, 200, 300, 400, 500)
                zombie.rect.centery = random.choice(list_y)
                self.zombie_group.add(zombie)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标事件
                self.pressed_key = pygame.mouse.get_pressed()
                if self.pressed_key[0] == 1:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    if 1354 <= x <= 1390 and 4 <= y <= 39 and self.pause is False:
                        # 用鼠标控制游戏的暂停与开始
                        self.pause = True
                    elif self.pause is True and 549 <= x <=722 and 371 <= y <= 391:
                        self.pause = False
                    # y=133 220 337 420 513
                    # x= 307 370 448 543 633 707 787 862 935
                    # 254, 85 983, 570
                    # x =252 337 411 499 578 660 739 819 894 978
                    # y =82 176 274 376 467 569
                    # 判断是否点击了植物卡片
                    if 275 <= x <= 275 + self.card_peashooter.rect.width and \
                            10 <= y <= 10 + self.card_peashooter.rect.height:
                        self.choose = 1
                    elif 325 < x <= 325 + self.card_sunflower.rect.width and \
                            10 <= y <= 10 + self.card_sunflower.rect.height:
                        self.choose = 2
                    elif 380 < x <= 380 + self.card_wall_nut.rect.width and \
                            10 <= y <= 10 + self.card_wall_nut.rect.height:
                        self.choose = 3
                    elif 254 <= x <= 983 and 85 <= y <= 570:
                        # 将x，y 的值定义到地图的可以种植植物的边框中,
                        map_size_x = [252, 337, 411, 499, 578, 660, 739, 819, 894, 978]
                        map_size_y = [82, 176, 274, 376, 467, 569]
                        for i in range(10):
                            if map_size_x[i] <= x <= map_size_x[i+1]:
                                x = (map_size_x[i] + map_size_x[i+1])/2
                        for i in range(6):
                            if map_size_y[i] <= y <= map_size_y[i+1]:
                                y = (map_size_y[i] + map_size_y[i+1])/2
                        if self.sun_num1 >= 50:
                            if self.choose == 1:
                                # 创建植物
                                peashooter = Peashooter()
                                # 定义植物坐标——鼠标位置
                                peashooter.rect.centerx = x
                                peashooter.rect.centery = y
                                # 判断当前位置是否有植物：
                                if (plant_cheek(peashooter, self.Peashooter_group) and
                                        plant_cheek(peashooter, self.Sunflower_group) and
                                        plant_cheek(peashooter, self.WallNut_group)):
                                    # 添加植物到精灵组
                                    self.Peashooter_group.add(peashooter)
                                    # 重置choose恢复鼠标
                                    self.choose = 0
                                    # 扣除分数
                                    self.sun_num1 -= 100
                                else:
                                    self.choose = 0

                            elif self.choose == 2:
                                now_time = time.time()
                                sunflower = Sunflower(now_time)
                                sunflower.rect.centerx = x
                                sunflower.rect.centery = y
                                # 判断当前位置是否有植物：
                                if (plant_cheek(sunflower, self.Peashooter_group) and
                                        plant_cheek(sunflower, self.Sunflower_group) and
                                        plant_cheek(sunflower, self.WallNut_group)):
                                    self.Sunflower_group.add(sunflower)
                                    self.choose = 0
                                    # 扣除分数
                                    self.sun_num1 -= 50
                                else:
                                    self.choose = 0
                            elif self.choose == 3:
                                wall_nut = WallNut()
                                wall_nut.rect.centerx = x
                                wall_nut.rect.centery = y
                                # 判断当前位置是否有植物：
                                if (plant_cheek(wall_nut, self.Peashooter_group) and
                                        plant_cheek(wall_nut, self.Sunflower_group) and
                                        plant_cheek(wall_nut, self.WallNut_group)):
                                    self.WallNut_group.add(wall_nut)
                                    self.choose = 0
                                    # 扣除分数
                                    self.sun_num1 -= 50
                                else:
                                    self.choose = 0
                        if self.choose == 0:
                            pass

                    for sprite in self.sun_group:
                        # 判断是否点击了太阳，收集了太阳
                        if (sprite.rect.x <= x <= sprite.rect.x + sprite.rect.width and
                                sprite.rect.y <= y <= sprite.rect.y + sprite.rect.height):
                            self.sun_num1 += 50
                            sprite.kill()
            if event.type == pygame.KEYDOWN:
                # 用键盘控制游戏的暂停与开始
                print(event.key)
                if event.key == 27:
                    self.pause = not self.pause
                elif event.key == 13 and self.pause is True:
                    self.pause = not self.pause

    def __collide_cheek(self):
        """碰撞检测"""
        # 判断僵尸是否遇到了植物
        # 若遇到了植物，则开启攻击状态
        zombie_collide(self.Peashooter_group, self.zombie_group)
        zombie_collide(self.WallNut_group, self.zombie_group)
        zombie_collide(self.Sunflower_group, self.zombie_group)
        # 判断遇到植物的僵尸眼前的植物是否已经死亡
        # 若植物已经死亡，则僵尸恢复行走状态
        for zombie in self.zombie_group:
            a = pygame.sprite.spritecollide(zombie, self.Peashooter_group, False)
            b = pygame.sprite.spritecollide(zombie, self.WallNut_group, False)
            c = pygame.sprite.spritecollide(zombie, self.Sunflower_group, False)
            if len(a) == 0 and len(b) == 0 and len(c) == 0 and zombie.isMeet is True:
                zombie.isMeet = False

        # 判断子弹是否遇到僵尸，若遇到僵尸则子弹消失并且僵尸血量减少
        for zombie in self.zombie_group:
            for bullet in self.bullet_group:
                if zombie.isAlive is True:
                    if pygame.sprite.collide_mask(zombie, bullet):
                        s = pygame.sprite.spritecollide(zombie, self.bullet_group, True)
                        if len(s) > 0:
                            zombie.energy -= 10
                            s.clear()

        # 判断是否有僵尸到达房屋位置
        for zombie in self.zombie_group:
            if zombie.rect.x <= 150:
                self.isLose = True
                self.lose_sound.play()

    def __sprite_update(self):
        """精灵绘制以及位置更新"""
        if self.isLose is not True:
            if self.pause is not True:
                self.screen.blit(self.BG, (0, 0))

                self.Peashooter_group.update(self.index)
                self.Peashooter_group.draw(self.screen)

                self.Sunflower_group.update(self.index)
                self.Sunflower_group.draw(self.screen)

                self.WallNut_group.update(self.index)
                self.WallNut_group.draw(self.screen)

                self.bullet_group.update(self.index)
                self.bullet_group.draw(self.screen)

                self.sun_group.update(self.index)
                self.sun_group.draw(self.screen)

                self.zombie_group.update(self.index)
                self.zombie_group.draw(self.screen)

                self.screen.blit(self.Card_Slot, (200, 0))
                self.screen.blit(self.sun_num, (218, 62))
                self.screen.blit(self.card_peashooter.image, (275, 10))
                self.screen.blit(self.card_sunflower.image, (325, 10))
                self.screen.blit(self.card_wall_nut.image, (380, 10))
                self.screen.blit(self.pause_image, (SCREEN_RECT.right - 50, 0))
                self.sun_front = pygame.font.SysFont('arial', 20)
                self.sun_num = self.sun_front.render(str(self.sun_num1), True, (0, 0, 0))
                self.index += 1
            else:
                self.screen.blit(self.pause_images, (400, 100))
        else:

            self.screen.blit(self.lose_image, (SCREEN_RECT.centerx - 200, SCREEN_RECT.centery - 200))

    @staticmethod
    def __game_over():
        """控制游戏程序结束"""
        pygame.mixer.quit()
        pygame.quit()
        exit()


if __name__ == "__main__":
    Game = Main()
    Game.start_game()
