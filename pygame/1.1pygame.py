import pygame
import sys
import random

class Fireball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = pygame.transform.smoothscale(pygame.image.load('REQUIREMENTS/fireball.webp'), (30, 30))
        self.speed = 8

class Screen:
    pygame.init()
    pygame.display.set_caption('ANGRY BIRDS ' )
    icon = pygame.image.load('REQUIREMENTS/logo.png')
    pygame.display.set_icon(icon)

    def __init__(self) :
        self.screen = pygame.display.set_mode((1000, 750))
        self.frames = pygame.time.Clock()
        self.hero_speed = 7
        self.game_active = True
        self.space_key_pressed = False
        self.enemy_count_bool=True
    
    def reset(self):
        self.enemies_list = []
        self.fireballs = []

        #speed of falling enemy
        self.speed = 1
        
        #used to increment the enemy counter
        self.score = 0

        self.life = 3
        self.enemy_count = 3

    def create_enemy(self):
        enemy_x = random.randint(100, 900)
        enemy_y = 50
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 100, 100)

        enemies_image = pygame.image.load('REQUIREMENTS/latest.webp')
        enemies_image = pygame.transform.smoothscale(enemies_image, (100, 100))
        enemy_image = pygame.transform.smoothscale(enemies_image.copy(), (100, 100))

        self.enemies_list.append({"rect": enemy_rect, "image": enemy_image})

    def music(self):
        pygame.mixer.music.load("REQUIREMENTS/angry-bird-theme-song.mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

    def hero(self):
        hero_x = 450
        hero_y = 600
        self.hero_rect = pygame.Rect(hero_x, hero_y, 100, 100)

        self.hero_image = pygame.image.load('REQUIREMENTS/hero.png')
        self.hero_image = pygame.transform.smoothscale(self.hero_image, (110, 150))

    def shoot(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not self.space_key_pressed:
            fire_x = self.hero_rect.x + 40
            fire_y = self.hero_rect.y
            self.space_key_pressed = True
            self.fireballs.append(Fireball(fire_x, fire_y))
        elif not keys[pygame.K_SPACE]:
            self.space_key_pressed = False

        for fireball in self.fireballs:
            fireball.rect.y -= fireball.speed

        self.fireballs = [fireball for fireball in self.fireballs if fireball.rect.y >= 0]

    def screen_setup(self):
        self.test_font = pygame.font.Font('REQUIREMENTS/font_file.ttf', 50)
        self.font_surface = self.test_font.render('ANAND ANGRY BIRDS', True, 'brown')
        self.SCORE = pygame.font.Font('REQUIREMENTS/font_file.ttf', 20)
        self.life1 = self.SCORE.render(f'    .life :: {self.life}', True, 'black')
        self.score1 = self.SCORE.render(f'SCORE :: {self.score}', True, 'black')
        self.on_screen_background = pygame.image.load('REQUIREMENTS/BACKGROUNDS.webp')
        self.on_screen_radio = pygame.image.load('REQUIREMENTS/radio (1).png')
        self.sr=pygame.image.load('REQUIREMENTS/lastscreen.webp')
        self.sr=pygame.transform.smoothscale(self.sr,(300,100))

        self.game_over = pygame.font.Font('REQUIREMENTS/font_file.ttf', 80)

        self.endblack = pygame.image.load('REQUIREMENTS/endblack.webp')
        self.endblack = pygame.transform.smoothscale(self.endblack, (1000,750))
        self.reload_react=pygame.Rect(450,450,100,100)

    def while_t(self):
        self.screen_setup()
        self.hero()
        self.music()

        #create number of enmies for the starting
        for i in range(self.enemy_count):  
            self.create_enemy()

        while True:
            if self.game_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                #hero movement right or left
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and self.hero_rect.x > 0:
                    self.hero_rect.x -= self.hero_speed
                if keys[pygame.K_d] and self.hero_rect.x < 900:
                    self.hero_rect.x += self.hero_speed
                
                #level increase the level when score reaches to multiple of 10
                if self.score % 10 == 0 and self.score > 0:
                    if not self.k:
                        self.enemy_count += 1
                        self.speed+=0.1
                        self.create_enemy()
                        self.k = True
                if self.score % 10 != 0:
                    self.k = False

                self.score1 = self.SCORE.render(f'SCORE :: {self.score}', True, 'black')
                self.screen.blit(self.on_screen_background, (0, 0))
                self.screen.blit(self.on_screen_radio, (20, 200))
                self.screen.blit(self.font_surface, (300, 70))
                self.shoot()

                # display all the enemy
                for enemy in self.enemies_list:
                    self.screen.blit(enemy["image"], enemy["rect"])

                # display all fireballs
                for fireball in self.fireballs:
                    self.screen.blit(fireball.image, fireball.rect)

                self.screen.blit(self.hero_image, self.hero_rect)
                self.screen.blit(self.score1, (10, 10))
                self.screen.blit(self.life1, (10, 30))

                #check wheather the bullet is hit or not and also check that the bullet is hit from hero
                for enemy in self.enemies_list:
                    enemy["rect"].y += self.speed

                    if enemy["rect"].colliderect(self.hero_rect):
                        self.life -= 1
                        if self.life == 0:
                            self.game_active = False

                    for fireball in self.fireballs:
                        if enemy["rect"].colliderect(fireball.rect):
                            self.score += 1
                            self.fireballs.remove(fireball)
                            enemy["rect"].y = 0
                            enemy["rect"].x = random.randint(100, 900)

                    if enemy["rect"].y == 750:
                        self.life -= 1
                        enemy["rect"].y = 0
                        enemy["rect"].x = random.randint(100, 900)

                self.life1 = self.SCORE.render(f'    .life :: {self.life}', True, 'black')

                #ends the game when life become 0
                if self.life == 0:
                    self.game_active = False

                pygame.display.update()
                #frame rate of the game
                self.frames.tick(100)
                
            else:
                 
                self.screen.blit(self.on_screen_background, (0, 0))
                self.screen.blit(self.on_screen_radio, (20, 200))
                self.screen.blit(self.endblack, (0,0))
                self.screen.blit(self.sr,(350,600))
                self.ENDSCORE = pygame.font.Font('REQUIREMENTS/font_file.ttf', 50)
                self.endscore = self.ENDSCORE.render(f'SCORE :: {self.score}', True, 'black')
                self.screen.blit(self.endscore, (390, 620))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if pygame.mouse.get_pressed()[0]:
                    if self.reload_react.collidepoint(pygame.mouse.get_pos()):
                        self.reset()
                        self.game_active=True
                        for i in range(self.enemy_count):  
                            self.create_enemy()

                pygame.display.update()
                self.frames.tick(100)

if __name__ == '__main__':
    k = Screen()
    k.reset() 
    k.while_t()