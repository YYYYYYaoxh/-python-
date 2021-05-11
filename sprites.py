import pygame
import random

# 定义类

# 定义窗口常量
SCREEN_RECT = pygame.Rect(0, 0, 1400, 600)
# 定义帧率
FRAME = 20
# 定义事件常量
SUN_EVENT = pygame.USEREVENT + 1
BULLET_EVENT = pygame.USEREVENT + 2
ZOMBIE_EVENT = pygame.USEREVENT + 3
FLOWER_SUN_EVENT = pygame.USEREVENT + 4


class Card(object):
    """卡片精灵"""
    def __init__(self, image_name):
        self.image = pygame.image.load(image_name).convert_alpha()
        self.rect = self.image.get_rect()
        scale = 0.78
        self.image = pygame.transform.scale(self.image, (int(self.rect.width*scale), int(self.rect.height*scale)))


class Peashooter(pygame.sprite.Sprite):
    """豌豆射手"""
    def __init__(self):
        # 完成对豌豆射手的初始化
        super().__init__()
        self.image = pygame.image.load('./images/plants/Peashooter/Peashooter_0.png').convert_alpha()
        self.images = [pygame.image.load('./images/plants/Peashooter/Peashooter_{:d}.png'.format(i)).convert_alpha()
                       for i in range(13)]
        self.rect = self.images[0].get_rect()
        self.energy = 6 * 10
        self.zombie = set()

    def update(self, *args):
        self.image = self.images[args[0] % len(self.images)]
        if self.energy <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """子弹"""
    def __init__(self, num, bg_size):
        super().__init__()
        self.image = pygame.image.load("./images/bullets/peaBullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        # 定义子弹的初始化位置
        self.rect.left = num[0] + 45
        self.rect.top = num[1]
        # 地图边缘
        self.width = bg_size
        # 子弹速度默认
        self.speed = 5

    def update(self, *args):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.kill()


class Sunflower(pygame.sprite.Sprite):
    """太阳花"""
    def __init__(self, time):
        super().__init__()
        self.image = pygame.image.load('./images/plants/SunFlower/SunFlower_0.png').convert_alpha()
        self.images = [pygame.image.load('./images/plants/SunFlower/SunFlower_{:d}.png'.format(i)) for i in range(18)]
        self.rect = self.images[0].get_rect()
        self.sunflower_sun_group = pygame.sprite.Group()
        self.last_time = time
        self.energy = 4*10

    def update(self, *args):
        if self.energy > 0:
            self.image = self.images[args[0] % len(self.images)]
        else:
            self.kill()


class WallNut(pygame.sprite.Sprite):
    """坚果墙"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./images/plants/WallNut/WallNut_0.png').convert_alpha()
        self.images = [pygame.image.load('./images/plants/WallNut/WallNut_{:d}.png'. format(i)) for i in range(16)]
        self.rect = self.images[0].get_rect()
        self.energy = 30*10

    def update(self, *args):
        # 坚果墙在血量不同时有不一样的形态
        if self.energy >= 20*10:
            self.image = self.images[args[0] % len(self.images)]
        elif 10*10 <= self.energy < 20*10:
            self.image = pygame.image.load("./images/plants/WallNut/Wallnut_cracked1.png").convert_alpha()
            scale = 0.99
            self.image = pygame.transform.scale(self.image,
                                                (int(self.rect.width * scale), int(self.rect.height * scale)))
        elif 0 < self.energy < 10*10:
            self.image = pygame.image.load("./images/plants/WallNut/Wallnut_cracked2.png").convert_alpha()
            scale = 0.99
            self.image = pygame.transform.scale(self.image,
                                                (int(self.rect.width * scale), int(self.rect.height * scale)))
        elif self.energy <= 0:
            self.kill()


class Sun(pygame.sprite.Sprite):
    """太阳"""
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("./images/Sun/Sun_0.png").convert_alpha()
        self.images = [pygame.image.load("./images/Sun/Sun_{:d}.png". format(i)) for i in range(22)]
        self.rect = self.images[0].get_rect()
        # 利用随机模块控制太阳掉落的位置
        self.rect.x = random.randint(254, 983)
        # 太阳的最低点
        self.max_y = random.randint(85, 570)
        self.rect.y = 0
        # 利用速度控制太阳是否下落，若是太阳花产生的速度则为0
        self.speed = speed
        self.last_time = 0

    def update(self, *args):
        # 太阳在到达最低点前会移动
        if self.rect.y <= self.max_y:
            self.rect.y += self.speed
        # 太阳的旋转动画
        self.image = self.images[args[0] % len(self.images)]
        self.last_time += 1
        if self.last_time == 100:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 动画
        self.image = pygame.image.load("./images/Zombie/Zombie_0.png")
        self.images = [pygame.image.load("./images/Zombie/Zombie_{:d}.png".format(i))for i in range(22)]
        self.attack_images = [pygame.image.load("./images/Zombie/ZombieAttack_{:d}.png".format(i))for i in range(21)]
        self.die_images = [pygame.image.load("./images/Zombie/ZombieDie_{:d}.png".format(i)) for i in range(10)]
        # 位置
        self.rect = self.images[0].get_rect()
        self.rect.top = 25 + random.randrange(0, 4) * 125
        self.energy = 6 * 10
        self.rect.left = 1000
        self.speed = 2
        # 音效
        self.zombie_attack_sound = pygame.mixer.Sound("./music/zombie_attack_WallNut.wav")
        # die_times不是击中次数，是一项新指标，控制死亡动画显示时间
        self.die_times = 0
        # 利用isMeet来判断僵尸是否遇到植物从而切换状态
        self.isMeet = False
        # 判断僵尸是否存活
        self.isAlive = True

    def update(self, *args):
        if self.energy > 0:
            # energy就是生命值
            if self.isMeet:
                # 如果遇到僵尸吃植物，进入袭击模式
                self.image = self.attack_images[args[0] % len(self.attack_images)]
                self.zombie_attack_sound.play()
            else:
                # 否则就是正常模式
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > 150 and not self.isMeet:
                self.rect.left -= self.speed
        else:
            # 此时僵尸已经挂了，但要显示挂了的动画
            # 对应正好10张，所以die_times显示为20为界限
            self.isAlive = False
            if self.die_times < 20:
                self.image = self.die_images[self.die_times // 2]
                self.die_times += 1
            else:
                # 20次以后僵尸尸体保留一段时间，所以直接到30次是分界线
                if self.die_times > 30:
                    self.kill()
                else:
                    self.die_times += 1