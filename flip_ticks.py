import time,pygame,sys,locale
locale.setlocale(locale.LC_TIME,'')
pygame.init()

# gestion des arguments
SIZE = 100
BGCOLOR = 0x000000
FGCOLOR = 0xf0f0f0
exec(';'.join(sys.argv[1:]))

# chargements des fontes
FONT = pygame.font.Font('FreeMonoBold.ttf',SIZE)
FONTDATE = pygame.font.Font('FreeMonoBold.ttf',int(SIZE/7))

# init du display
SCREEN = pygame.display.set_mode(FONT.size('00 00 00'))
pygame.time.wait(100)
SCREEN.fill(BGCOLOR)
pygame.event.clear()
FGCOLOR = SCREEN.unmap_rgb(FGCOLOR)

# AFFI = surface du background, contient la date
# UP,DOWN = rects des moitiers sup et inf de l'afficheur
AFFI = pygame.Surface(FONT.size('00 00 00')).convert_alpha()
AFFIRECT = AFFI.get_rect()
UP = pygame.Rect(AFFIRECT.topleft,(AFFIRECT.width,AFFIRECT.centery-1))
BOTTOM = pygame.Rect((0,AFFIRECT.centery+1),AFFIRECT.bottomright)
del AFFIRECT

# maj du background au lancement et passage du minuit
# entierement redessiner car une fois par 24 heures ca mange pas de pain
def update_bg():
    AFFI.fill((0,0,0,0))
    TIME = time.localtime()

    X1,X0 = UP.width/16*5,UP.width/16*11
    Y0 = UP.bottom
    SHIFT = FONTDATE.get_height()/2
    for DATE,X,shift in ('%a',X1,-SHIFT),('%b',X0,-SHIFT),('%Y',X0,SHIFT),('%d',X1,SHIFT):
        STRDATE = time.strftime(DATE,TIME)
        DATERECT = pygame.Rect((0,0),FONTDATE.size(STRDATE))
        DATERECT.center = X,Y0
        DATERECT.move_ip(0,shift)
        AFFI.blit(FONTDATE.render(STRDATE,1,(20,0,0)),DATERECT.move(1,1))
        AFFI.blit(FONTDATE.render(STRDATE,1,(255,255,255)),DATERECT)

    FLIP = pygame.transform.scale(pygame.image.load('image4320.png'),FONT.size('0'))
    FLIP_W = FLIP.get_width()
    for i in 0,1,3,4,6,7:
        AFFI.blit(FLIP,(i*FLIP_W,0))
    del FLIP
    del FLIP_W

# maj de l'heure
def update_time(T):
    SCREEN.fill(BGCOLOR)
    SCREEN.blit(AFFI,(0,0))
    SCREEN.blit(FONT.render(T,1,(0,0,0)),(2,2))
    SCREEN.blit(FONT.render(T,1,FGCOLOR),(0,0))
    pygame.display.update(UP)
    pygame.time.wait(50)
    pygame.display.update(BOTTOM)

update_bg()

#  synchronisation

B = '00 00 00'
while  B != time.strftime('%H %M %S',time.localtime()):
    update_time(B)
    B = ''.join(map(lambda x,y: str((((x!=y)+int(x))%10)if y!=' ' else ' '),B,time.strftime('%H %M %S',time.localtime())))
    pygame.time.wait(50)
    if B == '00 00 00': update_bg()
update_time(B)
while  B == time.strftime('%H %M %S',time.localtime()): pass
#SCREEN.fill(BGCOLOR)
TICKS = pygame.time.get_ticks()+1000
# main loop

while not pygame.event.peek(pygame.QUIT):
    pygame.event.clear()
    T = time.strftime('%H %M %S',time.localtime())
    if T == '00 00 00': update_bg()
    update_time(T)
    pygame.time.delay(TICKS-pygame.time.get_ticks())
    TICKS += 1000
