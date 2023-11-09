import pygame
from random import randint

display_w = 800
display_h = 600
score = 0
game_exit = False # Если false - то игра идет\
distance=0
distance_FINISH=3000


pygame.init()
game_font = pygame.font.Font('img/Pixel.ttf', 24)
game_display = pygame.display.set_mode((display_w, display_h))

class car:
    image = pygame.image.load('img/car.png')
    line = 0
    speed = 0
    car_y = 400
    visible = True
    
    def move(self):
        self.car_y -= self.speed
    
    def draw(self):
        self.move()
        if self.visible:
            game_display.blit(self.image,(335 + 75 * self.line ,self.car_y))
class police_car (car):
    image = pygame.image.load('img/car_police.png')
    car_y = 600
    speed = 10
    
class player_car(car):
    
    image = pygame.image.load('img/car.png')
    speed = 0
    speed_change = 2
    brakes = False
    fuel=100
    all_fuel=100
    hp=100
    all_hp=100
   
    
    def move_left(self):
        self.line = 0
    
    def move_right(self):
        self.line = 1
        
    def speed_Up(self):
        if back.speed + self.speed_change <= 30:
            back.speed += self.speed_change
    
    def speed_Down(self):
        if back.speed - self.speed_change >= 0:
            back.speed -= self.speed_change
     
    def move(self):
        global distance
        global fuel_w
        if self.brakes:
            self.speed_Down()
        self.car_y -= self.speed
        distance+=back.speed/10
        self.fuel-=back.speed/100+0.01
        self.game_over()
        self.win()
    def game_over(self):
        global stage,stages
        if (self.fuel<=0) or (self.hp<=0):
            player.change_brakes()
            music =pygame.mixer.music.load("img/over.mp3")
            
            if back.speed==0: 
                pygame.mixer.music.play(1)
                police.line = (self.line-1)*(-1)
                police.draw()
                if police.car_y<=450:
                    stage=stages[4]   
    def win(self):
        global distance,score
        global stage,stages
        if distance>=distance_FINISH:
            music =pygame.mixer.music.load("img/win.mp3")
            back.speed=0
            self.speed=20
            pygame.mixer.music.play(1)
            if self.car_y < -99:
                score+=500
                stage=stages[5]
    def change_brakes(self):
        self.brakes = not ( self.brakes )
    
class enemy_car(car):
    image = pygame.image.load('img/car_red1.png')
    speed = 5
    line = 0
    
    def __init__(self, speed, line):
        self.speed = speed
        self.line = line
    
    def move(self):
        global score
        if self.speed > 0:
                self.image = pygame.image.load('img/car_red1.png')
        else:
            self.image = pygame.image.load('img/car_red2.png')
            
        if self.car_y < -99:
            self.car_y = display_h
            if self.visible:
                score += 100
            self.reset()
            
        if self.car_y > display_h:
            self.car_y = -99 
            if self.visible:
                score += 100    
            self.reset()
            
        self.car_y -= self.speed - back.speed
        
        self.collide_check(player)
    
    def collide_check(self, car2):
        if self.visible :
            global score
            car_rect = self.image.get_rect().move((335 + 75 * self.line ,self.car_y))
            car2_rect = car2.image.get_rect().move((335 + 75 * car2.line ,car2.car_y))
            
            if car_rect.colliderect(car2_rect):
                score -= 200
                player.hp-=10
                self.visible = False
                
    def reset(self):
        
        speed = randint(5,25)
        direction = randint(1,2)
        line = randint(0,1)
        
        if direction == 2:
            speed *= -1
            
        self.speed = speed
        self.direction = direction
        self.line = line
        if randint(0,1) == 1:
            self.visible = True   
        else:
            self.visible = False  
        

class background:
    image = pygame.image.load('img/background.png')
    speed = 20
    background_y = 0
    
    def draw(self):
        self.background_y += self.speed
      
        
        
        game_display.blit(self.image,(0,self.background_y-2352))
        game_display.blit(self.image,(0,self.background_y))
                
        if self.background_y >= display_h:
            self.background_y = display_h - 2352
class bonus(car):
    car_y=-20
    
    def move(self):
        self.car_y+=back.speed
        if self.car_y > display_h:
                self.car_y = -99 
                self.reset()
        self.collide_check(player)
 
    def collide_check(self, car2):
        if self.visible :
            car_rect = self.image.get_rect().move((335 + 75 * self.line ,self.car_y))
            car2_rect = car2.image.get_rect().move((335 + 75 * car2.line ,car2.car_y))
            
            if car_rect.colliderect(car2_rect):
                self.visible = False    
                self.actions()
    def reset(self):
        line = randint(0,1)
        self.line=line
        if randint(0,4) == 1:
            self.visible = True   
        else:
            self.visible = False     
class bonus_fuel(bonus):
    image=pygame.image.load('img/fuel_item.png')

    def actions(self):
        if player.fuel+30>100:
            player.fuel=100
        else:
            player.fuel+=30
class bonus_hp(bonus): 
    image=pygame.image.load('img/hp_item.png')
    def actions(self):
        if player.hp+20>100:
            player.hp=100
        else:
            player.hp+=20    
def draw_ui():
    global distance_FINISH
    global distance
    
    text_image = game_font.render("SCORE : " + str(score), True, (255,255,255))
    game_display.blit(text_image,(10,10))
    
    #Dist_text="DISTANCE: {:.0f}".format(distance)
    #text_image = game_font.render(Dist_text, True, (255,255,255))
    #game_display.blit(text_image,(10,60))    
    
    pygame.draw.rect(game_display,(200,200,210),(0,display_h-15,display_w,10))
    dist_w=distance/distance_FINISH
    pygame.draw.rect(game_display,(225,75,75),(0,display_h-15,display_w*dist_w,10))
    game_display.blit(pygame.image.load('img/fuel_icon.png'),(10,60))
    
    fuel_w=player.fuel/player.all_fuel
    if fuel_w>=0:
        pygame.draw.rect(game_display,(225,75,75),(50,90,95*fuel_w,10))
    hp_w=player.hp/player.all_hp
    game_display.blit(pygame.image.load('img/hp_icon.png'),(10,120))
    if hp_w>=0:
        pygame.draw.rect(game_display,(225,75,75),(50,150,95*hp_w,10))
# глобальные переменные будут здесь

back = background()
player = player_car()
fuelb=bonus_fuel()
hp=bonus_hp()
enemies = []
police=police_car()
stages=['start_menu','game','game_menu','pre_game_over','game_over','win']
stage=stages[0]
for i in range(2):
    speed = randint(5,25)
    
    #direction = randint(1,2)
    direction = i + 1
    line = i
    
    if direction == 2:
        speed *= -1
        
    enemies.append(enemy_car(speed,line))
    

# здесь можно смело поменять название
pygame.display.set_caption('Hot race 0.1')
clock = pygame.time.Clock()
pos=[]
def process_keyboard(event):
    global stage,stages,game_exit,hp,fuel,score,distance,score,distance_FINISH
   # print(event)
    if stage =='start_menu':
        pos=pygame.mouse.get_pos()
        x=pos[0]
        y=pos[1]
        #print(x,y)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button== 1:
               #print(1)
                
                #print(pos)
                
                if (x>=365)and(x<=425):
                    if (y>=400)and(y<=425):
                        stage=stages[1]
                if (x>=370)and(x<=420):
                    if (y>=440)and(y<=460):   
                        game_exit = True
    elif stage =='game':
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_UP:
                player.speed_Up()
            if event.key == pygame.K_DOWN:
                player.speed_Down() 
            if event.key == pygame.K_SPACE:
                player.change_brakes() 
            print(event.key)
            if event.key == 27:
                stage=stages[0]
            
    elif (stage =='game_over')or(stage =='win'):
       
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button== 1:
               #print(1)
                pos=pygame.mouse.get_pos()
                #print(pos)
                x=pos[0]
                y=pos[1]
                if (x>=50)and(x<=140):
                    if (y>=500)and(y<=525):
                        player.hp=100
                        player.fuel=100
                        back.speed=20
                        distance=0
                        score=0
                        distance_FINISH+=500
                        stage=stages[1]
                if (x>=700)and(x<=750):
                    if (y>=500)and(y<=525):   
                        game_exit = True        
            
   

# самая важная функция в ней все и происходит
def game_loop(update_time):
    global game_exit

    while not game_exit:
        
        # обработка пришедших событий
        for event in pygame.event.get():
            #print(event)
            process_keyboard(event)
            if event.type == pygame.QUIT:
                game_exit = True
                
        # на этом уровне должна происходить отрисовка

        # нарисовать машинку
        # нарисовать фон
        if stage=='game':
            back.draw()
            player.draw()
            fuelb.draw()
            hp.draw()
            for enemy in enemies:
                enemy.draw()
            draw_ui()
            
        elif stage=='game_over':
            pygame.draw.rect(game_display,(0,0,0),(0,0,display_w,display_h))
            text_image = game_font.render("game over " , True, (255,255,255))
            game_display.blit(text_image,(display_w/2.5,display_h/2))
            text_image = game_font.render("YOU SCORE : " + str(score), True, (255,255,255))
            game_display.blit(text_image,(display_w/2.5,display_h/1.5)) 
            text_image = game_font.render("restart  " , True, (255,255,255))
            game_display.blit(text_image,(50,500))  
            text_image = game_font.render("exit  " , True, (255,255,255))
            game_display.blit(text_image,(700,500))             
        elif stage=='win':
            pygame.draw.rect(game_display,(0,0,0),(0,0,display_w,display_h))
            text_image = game_font.render("you win " , True, (255,255,255))
            game_display.blit(text_image,(display_w/2.5,display_h/2))
            text_image = game_font.render("YOU SCORE : " + str(score), True, (255,255,255))
            game_display.blit(text_image,(display_w/2.5,display_h/1.5))  
            text_image = game_font.render("start  " , True, (255,255,255))
            game_display.blit(text_image,(50,500))  
            text_image = game_font.render("exit  " , True, (255,255,255))
            game_display.blit(text_image,(700,500))  
            
        elif stage=='start_menu':
            pos1=pygame.mouse.get_pos()
            x1=pos1[0]
            y1=pos1[1]
            game_display.blit(pygame.image.load('img/title.png'),(0,0))
            game_display.blit(pygame.image.load('img/title_cursor.png'),(x1-10,y1-10))
            pygame.mixer.music.load("img/game.mp3")
            pygame.mixer.music.play(1)            
        pygame.display.update()
        clock.tick(update_time)
        
        

game_loop(30)
pygame.quit()