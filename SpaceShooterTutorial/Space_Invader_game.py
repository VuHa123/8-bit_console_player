import pygame, sys
import random
import time
   

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")
#load imgae
red_space_ship = pygame.image.load("SpaceShooterTutorial/assets/pixel_ship_red_small.png").convert()
green_space_ship = pygame.image.load("SpaceShooterTutorial/assets/pixel_ship_green_small.png").convert()
blue_space_ship = pygame.image.load("SpaceShooterTutorial/assets/pixel_ship_blue_small.png").convert()
#player player
yellow_space_ship = pygame.image.load("SpaceShooterTutorial/assets/pixel_ship_yellow.png").convert()
#lasers
red_laser = pygame.image.load("SpaceShooterTutorial/assets/pixel_laser_red.png").convert()
green_laser = pygame.image.load("SpaceShooterTutorial/assets/pixel_laser_green.png").convert()
blue_laser = pygame.image.load("SpaceShooterTutorial/assets/pixel_laser_blue.png").convert()
yellow_laser = pygame.image.load("SpaceShooterTutorial/assets/pixel_laser_yellow.png").convert()
#load background
bg = pygame.image.load("SpaceShooterTutorial/assets/background-black.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    #ham giói hạn laser trong khung hình game
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    #ham va cham
    def collision(self, obj):
        return collide(self, obj)
class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.laser.remove(laser)
    #hồi chiêu
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    #tao hàm bắn
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    #hàm lấy chiều rộng của tàu
    def get_width(self):
        return self.ship_img.get_width()
    #hàm lấy chiều cao của tàu
    def get_height(self):
        return self.ship_img.get_height()
  
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        # hiệu ứng va chạm, sử dụng mask cho phép va chạm pixel
        # xác định mặt nạ
        self.mask = pygame.mask.from_surface(self.ship_img)
        # cho biết vị trí của pixel và vị trí không có trong
        # hình ảnh để xác định có va chạm pixel hay không
        self.max_health = health
    #kiểm tra người chơi có bắn trúng kẻ thù hay không
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, screen):
        super().draw(screen)
        self.healthbar(screen)
        
    def healthbar(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class EnemyShip(Ship):
    COLOR_MAP = {
                "red" : (red_space_ship, red_laser),
                "green": (green_space_ship, green_laser), 
                "blue": (blue_space_ship, blue_laser)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #hàm kiểu tra xem có sự chồng lấp giữa 2 đối tượng không
    
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.Font('04b_19/04B_19__.TTF', 40)
    lost_font = pygame.font.Font('04b_19/04B_19__.TTF', 60)

    enemies =[]
    wave_lenght = 5 # số lượng kẻ thù
    enemy_vel = 1 # tốc độ của kẻ thù
    #biến vận tốc
    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 
    #vẽ lại màn hình trò chơi sau mỗi lần
    def redraw_window():
        screen.blit(bg, (0,0))
        #viết text
        lives_label = main_font.render(f"Lives:{lives}", 1, (255,255, 255))#tham số 1 có tác dụng làm chữ mượt hơn
        level_label = main_font.render(f"Livel: {level}", 1,  (255, 255, 255))
        #hiển thị lên màn hình
        screen.blit(lives_label, (10,10))
        screen.blit(level_label, (WIDTH - level_label.get_width() -10, 10))
        for enemy in enemies:
            enemy.draw(screen)
        
        player.draw(screen)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            screen.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        # tạo hiệu ứng người chơi bắn laser vào kẻ thù
        if lives <= 0 or player.health <= 0:
            lost =True
            lost_count +=1 
            if lost:
                if lost_count > FPS * 3: #nếu thua, trong khoảng FPS * 3 sẽ thoát game
                    run = False
                else:
                    continue
        #tao hiệu ứng kẻ thù di chuyển xuống
        if len(enemies) == 0: #khi hết kẻ thù thì level của người chơi tăng lên 1
            level += 1
            wave_lenght += 5
            for i in range(wave_lenght):
                enemy = EnemyShip(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red",  "blue", "green"]))
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        #kiểm tra xem người chơi nhấn phím nào trên bàn phím để thực hiện hành động tương ứng
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # di chuyển sang trái
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # di chuyển sang phải
            player.x += player_vel
        if keys[pygame.K_w] and player.y -player_vel > 0: # di chuyển lên trên
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # di chuyển xuống dưới 
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        player.move_lasers(-laser_vel, enemies)
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        screen.blit(bg, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu()
