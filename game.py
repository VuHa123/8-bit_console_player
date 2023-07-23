import pygame, sys, random
# Tao ham floor chay lien tuc
def draw_floor():
    screen.blit(floor, (floor_x_pos,650))
    screen.blit(floor, (floor_x_pos +432,650))
# ham tao ong
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # phai tao khoi xung quanh ong giong chim de neu xay ra va cham pygame co the nhan biet
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))#toa do x, y bang mot nua chieu dai va rong cua game
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos -650))# -650 de khoang trong cho chim qua ong tren va ong duoi
    return bottom_pipe, top_pipe
# ham di chuyen ong
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5 #lay ong dc tao ra va di chuyen ve ben trai
    return pipes
#tao ham hien thi ong
def drawn_pipe(pipes):
    for pipe in pipes:
        #cach de dao nguoc ong phia tren
        if pipe.bottom >= 600:#neu ong lon hon chieu dai của so game thi nó sẽ biet đó là ống ở dưới
            screen.blit(pipe_surface,pipe)
        else:
            #lat nguoc ong
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)#tham so truyen vao lan luot la: hinh anh muon lat, lat theo truc Ox(neu truyen vao la True), lat theo truc Oy(neu truyen vao la True)
            screen.blit(flip_pipe, pipe)
#ham xử lý va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rec.colliderect(pipe):#neu hcn bao quanh con chim cham voi hcn bao quanh ong thi:
            hit_sound.play()
            return False
        #xu ly khi con chim o ngoai man hinhf
        if bird_rec.top <= -75 or bird_rec.bottom >= 650:
            return False
    return True
# tao hieu ung chim cui len cui xuong(xoay chim)
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*4, 1.5)
    return new_bird
# tao hieu ung dap canh cho chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rec = new_bird.get_rect(center = (100, bird_rec.centery))
    return new_bird, new_bird_rec
#hien thi diem
def score_display(game_state):
    if game_state == 'main game': #game dang chay chi hien thi diem 
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rec = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rec)
    if game_state == 'game over': #game ket thuc se hien thi diem cuoi cung va diem cao nhat
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rec = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rec)

        high_score_surface = game_font.render(f' High Score:{int(score)}', True, (255, 255, 255))
        high_score_rec = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rec)
#cap nhat diem
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size =- 16, channels=2, buffer=521)#chinh gai tri am thanh ve thich hop voi pygame
pygame.init()
screen=pygame.display.set_mode((432, 768))
# Tốc độ game
clock = pygame.time.Clock()
#he thong tinh diem
game_font = pygame.font.Font('04b_19/04B_19__.TTF', 40)
#Tao bien tro choi 
# tao background cho game, thêm tham số convert để python load ảnh nhanh hơn(nó chuyển sang một dạng khác để python dễ dàng đọc hơn(matran))
background = pygame.image.load("assets/background-night.png").convert()
# tăng kích thước size ảnh background
background = pygame.transform.scale2x(background)
# tao chan nen trong background va tang kich thuoc
floor = pygame.image.load("assets/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# chèn chim
bird_down = pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
bird_mid = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_up = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rec = bird.get_rect(center = (100, 384)) #tạo hình chữ nhật xung quanh con chim, đặt con chim ở chính giữa, cách Ox 100, cách Oy bằng nửa chiều cao của cửa sổ game
#để tạo ra một con chim có thể bay thì ta thêm trọng lực cho chim
#tao timer cho bird dap canh
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
gravity = 0.15
#tạo biến cho sự di chuyển của chim
bird_movement = 0
#tao bien de ket thuc: khi chim o ngoai man hinh
game_active = True
#bien diem so
score = 0
high_score = 0
#tạo ống 
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# de ong xuat hien trong 1 khoang thoi gian nhat dinh
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)#1200: sau 1.2s se tao ong moi
#tao ong ben tren voi do dai ngau nhien
pipe_height = [200, 250, 300, 400]
#Tao man hinh ket thuc
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rec = game_over_surface.get_rect(center=(216, 384))
#chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#while loop cua tro choi
while True:
    for event in pygame.event.get():
        #tạo phím để người chơi ấn vào thì thoát game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #tương tác trên bàn phím
        if event.type == pygame.KEYDOWN:
            # Tạo hiệu ứng bay lên
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =- 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True#khi ma game ket thuc thi mk nhan tiep space no se kich hoat lai game
                game_active = True
                pipe_list.clear()
                bird_rec.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rec = bird_animation()

    # hiển thị phím tắt đó ra màn hình
    screen.blit(background, (0, 0))
    if game_active:
        #chim
        bird_movement += gravity# con chim càng di chuyển thì trong lực càng tăng
        # con chim di chuyển xuống dưới, tức cả hình chứ nhật cx di chuyến xg dưới
        rotated_bird = rotate_bird(bird)
        bird_rec.centery += bird_movement
        screen.blit(rotated_bird, bird_rec)
        game_active=check_collision(pipe_list)
        #ong
        pipe_list = move_pipe(pipe_list)#lay tat ca cac ong duoc tao ra roi di chuyen sau do tra lai pipe_list moi
        drawn_pipe(pipe_list)
        score += 0.01#bay cang lau diem cang cao
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rec)
        high_score = update_score(score, high_score)
        score_display('game over')
    #san
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = -0
    pygame.display.update()
    clock.tick(100)