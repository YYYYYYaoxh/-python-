import pygame

# 储存一些关于植物的方法


def plant_cheek(a,b):
    cheek = pygame.sprite.spritecollide(a, b, False)
    if len(cheek) == 0:
        return True
    else:
        return False


def zombie_collide(plant_group, zombie_group):
    for zombie in zombie_group:
        for peashooter in plant_group:
            if pygame.sprite.collide_mask(zombie, peashooter):
                if zombie.rect.y <= peashooter.rect.y:
                    zombie.isMeet = True
                    peashooter.energy -= 1
