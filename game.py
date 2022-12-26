from random import seed, randint
import pygame
import sys
import os


# Tu definiujemy wszystkie parametry odpowiadające za wygląd gry. 
max_x = 1400
max_y = 800
text_factor = 17
one_frame_time = 75
duck_factor = 17
treat_factor = 15
ice_factor = 5
hardness_factor = 100000


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources\\bitmap\\duck.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(self.rect.w//duck_factor,self.rect.h//duck_factor))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 3*max_y//4
        pygame.display.set_icon(self.image)


class Treat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources\\bitmap\\burger.png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(self.rect.w//treat_factor,self.rect.h//treat_factor))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ice(pygame.sprite.Sprite):
    def __init__(self, which_ice, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load("resources\\bitmap\\ice1.png"))
        self.images.append(pygame.image.load("resources\\bitmap\\ice2.png"))
        self.images.append(pygame.image.load("resources\\bitmap\\ice3.png"))
        self.images.append(pygame.image.load("resources\\bitmap\\ice4.png"))
        self.images.append(pygame.image.load("resources\\bitmap\\ice5.png"))
        self.image = self.images[which_ice]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(self.rect.w//ice_factor,self.rect.h//ice_factor))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def up(obj, move_delta):
    # Poruszenie obiektu (sprite'u) w górę. 
    # move_delta - o ile przesuwamy obiekt jednorazowo
    #
    if obj.rect.y>42*max_y/100+move_delta:
        obj.rect.y-=move_delta


def down(obj, move_delta):
    # Poruszenie obiektu (sprite'u) w dół. 
    # move_delta - o ile przesuwamy obiekt jednorazowo
    #
    if obj.rect.y+obj.rect.h<max_y-move_delta:
        obj.rect.y+=move_delta


def right(obj, move_delta):
    # Poruszenie obiektu (sprite'u) w prawo. 
    # move_delta - o ile przesuwamy obiekt jednorazowo
    #
    if obj.rect.x+obj.rect.w<max_x-move_delta:
        obj.rect.x+=move_delta


def left(obj, move_delta):
    # Poruszenie obiektu (sprite'u) w lewo. 
    # move_delta - o ile przesuwamy obiekt jednorazowo
    #
    if obj.rect.x>-200:
        obj.rect.x-=move_delta


def main():
    # Główna funkcja programu - to tu zaczyna się uruchomienie gry.
    seed(42)

    time_delta = 0
    energy = 200
    hi_score = 0
    score = 0
    counter = 0
    started = False
    game_over = False
    
    pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    background = pygame.image.load("resources\\bitmap\\landscape.jpg")
    background = pygame.transform.scale(background,(max_x,max_y))

    sounds = []
    sounds.append(pygame.mixer.Sound('resources\\sounds\\11570__samplecat__squeak-duck6.wav'))
    sounds.append(pygame.mixer.Sound('resources\\sounds\\242664__reitanna__quack.wav'))

    #pygame.mixer.music.load('resources\\mjuzik.mp3')
    #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()/4)
    #pygame.mixer.music.play(-1)
    #music = True

    font = pygame.font.Font('resources\\font\\04B_30__.TTF', max_y // text_factor)
    text = font.render('This is Icy Duck!', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (max_x // 2 , max_y // 5)

    font_go1 = pygame.font.Font('resources\\font\\04B_30__.TTF', max_y // text_factor)
    text_go1 = font.render('GAME OVER', True, (255,255,255))
    textRect_go1 = text_go1.get_rect()
    textRect_go1.center = (max_x // 2 , max_y // 3)

    font_go2 = pygame.font.Font('resources\\font\\04B_30__.TTF', max_y // text_factor)
    text_go2 = font.render('YOU HAVE WON!', True, (255,255,255))
    textRect_go2 = text_go2.get_rect()
    textRect_go2.center = (max_x // 2 , max_y // 3)

    font_scores = pygame.font.Font('resources\\font\\04B_30__.TTF', max_y // text_factor // 2)

    screen = pygame.display.set_mode((max_x,max_y))
    pygame.display.set_caption("Icy Duck")

    all_sprites = pygame.sprite.Group()
    ice_sprites = pygame.sprite.Group()
    ice_blocks = []

    treats_sprites = pygame.sprite.Group()
    treats = []

    player = Player()
    all_sprites.add(player)

    for _ in range(35):
        current_sprite = Ice(randint(1,4), randint(50, max_x), randint(max_y // 100 * 45, max_y))
        while pygame.sprite.spritecollideany(current_sprite, all_sprites) is not None:
            current_sprite = Ice(randint(1, 4), randint(50, max_x), randint(max_y // 100 * 45, max_y))
        ice_blocks.append(current_sprite)
        all_sprites.add(current_sprite)
        ice_sprites.add(current_sprite)

    while True:
        counter += 1
        if (counter % (4 * hardness_factor) == 0) and (energy>1): energy -= 1
        if counter > 50 * hardness_factor:
            counter=0
            current_sprite = Treat(max_x, randint(max_y // 100 * 45, max_y))
            if pygame.sprite.spritecollideany(current_sprite, all_sprites) is None:
                treats.append(current_sprite)
                all_sprites.add(current_sprite)
                treats_sprites.add(current_sprite)

        if energy<200:
            move_delta = energy // 20 + 2
        else:
            move_delta = 12

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                started = True
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pass
                #if music:
                #    music = False
                #    pygame.mixer.music.stop()
                #else:
                #    music = True
                #    pygame.mixer.music.play(-1)

        time_delta += clock.tick()

        if time_delta > one_frame_time:
            time_delta = 0

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]: up(player, move_delta)
            if keys_pressed[pygame.K_DOWN]: down(player, move_delta)
            if keys_pressed[pygame.K_LEFT] and player.rect.x > move_delta: left(player, move_delta)
            if keys_pressed[pygame.K_RIGHT]:
                right(player, move_delta)
                if energy>1:
                    energy -= 1

            for_removal=[]
            for ice_block in ice_blocks:
                left(ice_block,randint(1,3))
                if ice_block.rect.x+ice_block.rect.w<0:
                    ice_block.kill()
                    for_removal.append(ice_block)
            for ice_block in for_removal:
                ice_blocks.remove(ice_block)
                current_sprite = Ice(randint(1, 4), max_x, randint(max_y // 100 * 45, max_y))
                while pygame.sprite.spritecollideany(current_sprite, all_sprites) is not None:
                    current_sprite = Ice(randint(1, 4), max_x, randint(max_y // 100 * 45, max_y))
                ice_blocks.append(current_sprite)
                all_sprites.add(current_sprite)
                ice_sprites.add(current_sprite)
                score += 10
                sounds[0].play()

            for_removal=[]
            for treat in treats:
                left(treat,randint(1,3))
                if treat.rect.x<-100:
                    treat.kill()
                    for_removal.append(treat)
            for treat in for_removal:
                treats.remove(treat)


            ice_collided = pygame.sprite.spritecollideany(player, ice_sprites)

            if ice_collided is not None:
                sounds[1].play()
                game_over = True

            treat_collided = pygame.sprite.spritecollideany(player, treats_sprites)

            if treat_collided is not None:
                sounds[0].play()
                score +=100
                energy +=50
                if energy>900: energy=900
                treat_collided.kill()
                treats.remove(treat_collided)

            if score >= 999950:
                score = 999999
                game_over = True

            text_scores = font_scores.render("ENERGY: "+"{0:03d}".format(energy)+
                                            " SCORE: "+"{0:06d}".format(score)+
                                            " HI SCORE: "+"{0:06d}".format(hi_score),
                                            True, (255, 255, 255))
            text_scoresRect = text_scores.get_rect()
            text_scoresRect.x = max_x - text_scoresRect.w - 20
            text_scoresRect.y = 20

            screen.fill((0,0,0))
            screen.blit(background,(0,0))
            if not started: screen.blit(text, textRect)
            if game_over:
                if score==999999:
                    screen.blit(text_go2, textRect_go2)
                else:
                    screen.blit(text_go1, textRect_go1)
            screen.blit(text_scores, text_scoresRect)
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.update()
            if game_over:
                for _ in range(999999):
                    for _ in range(100): pass
                if score > hi_score: hi_score = score
                score = 0
                counter = 0
                energy = 200
                game_over = False
                started = False
                player.rect.x = 10
                player.rect.y = randint(max_y // 2 + 20, max_y)
                while pygame.sprite.spritecollideany(player, ice_sprites) is not None:
                    player.rect.x = 10
                    player.rect.y = randint(max_y // 2 + 20, max_y)


if __name__ == "__main__":
    main()