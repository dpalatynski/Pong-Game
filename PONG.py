########################
#
#  PONG GAME
#
# % D Pałatyński
#
#######################

import pygame
from pygame.locals import *
import sys
from pygame import *
import random
import time

#   PARAMETRY GRY:

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT) #Rozmiar ekranu
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100 #Rozmiary paletki
#Piłka generuje się losowo w połowie szerokości ekranu na tych pozycjach: (w odpowiednich miejscach jest użyte random.choice()
BALL_RANDOM_GENERATE = [SCREEN_HEIGHT/5,4 *SCREEN_HEIGHT/5,3 * SCREEN_HEIGHT/5, 2*SCREEN_HEIGHT/5, 1 * SCREEN_HEIGHT/5, 7* SCREEN_HEIGHT/10, 3 * SCREEN_HEIGHT/10, SCREEN_HEIGHT/10, 9* SCREEN_HEIGHT/10]
POINTS_TO_WIN = 5 #punkty do wygranej

GREY = (128,128,128)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK =(0,0,0)

global PADDLE_PLAYER_COLOR
global PADDLE_ENEMY_COLOR
global GAME_MODE

PADDLE_PLAYER_COLOR = WHITE #zmienna odpowiedzialna za kolor: - paletki gracza
PADDLE_ENEMY_COLOR = WHITE # - paletki przeciwnika
GAME_MODE = 0 # 0 - Singleplayer 1 - Multiplayer

screen = pygame.display.set_mode(SCREEN_SIZE)  #tworzymy ekran
pygame.display.set_caption("PONG GAME") #tytuł gry
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

mixer.init() #przygotowujemy dźwięki
bouncefx = mixer.Sound("bounce.wav")
scorefx = mixer.Sound("score.wav")
funnyfx = mixer.Sound("funny.wav")
correctfx = mixer.Sound("correct.wav")
wrongfx = mixer.Sound("wrong.wav")

#   KLASY OBIEKTÓW:

class Player():
    """
    Klasa gracza - obiekt po prawej stronie ekranu w kształcie prostokąta
    Ruch w zależności od naciśniętych klawiszy UP i DOWN, prędkość poruszania
    się paletki jest ustalona odgórnie jak i położenie początkowe. Wysokość
    i szerokość paletki obydwóch graczy jest ustalona w parametrach gry.
    Podcza gry multiplayer ten obiekt jest traktowany jako Player 2.
    """
    def __init__(self):
        self.x = SCREEN_WIDTH - 5 # zrobione w ten sposób, aby paletka "przylegała" do ściany (estetyka)
        self.y = SCREEN_HEIGHT/2
        self.speed = 4
        self.score = 0
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def points(self):
        if self.score == POINTS_TO_WIN: #jeżeli gracz zdobywa 5-ty punkt, punkty przeciwnika i gracza zerują sie na następną grę
            self.score = 0
            enemy.score = 0

    def movement(self):
        self.rect.center = (self.x, self.y)

        keys = pygame.key.get_pressed() #odpowiednia funkcjonalność przycisków i dodawanie współrzednej y (poruszanie się góra-dół) o wartość prędkości
        if keys[pygame.K_UP]:
            self.y -= self.speed
            if self.y > SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.y < 0:
                self.y = 0

        if self.rect.top <= 0: #paletka nie może uciec poza ekran
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def draw(self):
        pygame.draw.rect(screen, PADDLE_PLAYER_COLOR, self.rect) #rysujemy obiekt na oknie

    def scoreboardplayer(self):
        lyrics(str(player.score), 50 , 750, 40) #rysujemy ilość punktów w górnym rogu ekranu


class Enemy():
    """
    Klasa przeciwnika (lub podczas gry multiplayer - Player 1) obiekt po
    lewej stronie ekranu w kształcie prostokąta. Jeżeli rozgrywka jest
    singleplayer za poruszanie odpowiada komputer, który w funkcji movement
    ma określone warunki jak powinien się poruszać w zależności od położenia
    piłeczki.
    Jeżeli gra jest multiplayer ten obiekt jest traktowany jak
    Player 1 i użytkowik steruje nim używając klawiszy W i S.

    AI - jeżeli prędkość piłki jest w skierowana w stronę gracza, paletka przeciwnika
    jest kierowana mniej więcej na środek wysokości ekranu, co pozwoli zapewnić
    lepszy start do odebrania piłki. W innym wypadku paletka podąża za piłką.

    Player 1 - Gracz steruje przyciskami W, aby ruszyć paletką do góry, natomiast
    S, aby paletkę skierować do dołu.
    """
    def __init__(self):
        self.x = 5  # zrobione w ten sposób, aby paletka "przylegała" do ściany (estetyka)
        self.y = SCREEN_HEIGHT/2
        self.speed = 4
        self.score = 0
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def points(self):
        if self.score == POINTS_TO_WIN: #jeżeli przeciwnik zdobywa 5-ty punkt, punkty przeciwnika i gracza zerują sie na następną grę
            self.score = 0
            player.score = 0


    def movement(self):
        self.rect.center = (self.x, self.y)
        if GAME_MODE == 1: #Opcja multiplayer - Player 1 steruje odpowiednio W i S góra-dół
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.y -= self.speed
            elif keys[pygame.K_s]:
                self.y += self.speed

            if self.rect.top <= 0: #waruneka by paletka nie uciekła poza ekran
                self.rect.top = 0
            elif self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        else: #Opcja Singleplayer
                if ball.speed_x >= 0: #Pierwszy warunek, jeżeli prędkość piłeczki jest dodatnia (czyli leci w prawą stronę na gracza) to
                    if self.rect.top == SCREEN_HEIGHT/2 - 50 :  #paletka ustawia się mniej więcej na środku
                        self.y = self.y
                    elif self.rect.top < SCREEN_HEIGHT/2 - 50:
                        self.y += self.speed/2
                    else:
                        self.y -= self.speed/2
                else:   #W tym miejscu prędkość piłeczki jest skierowana do paletki klasy Enemy
                    if self.rect.top <= 0: #na początku standardowy warunek, aby paletka nie uciekła poza ekran
                        self.rect.top = 0
                    elif self.rect.bottom >= SCREEN_HEIGHT:
                        self.rect.bottom = SCREEN_HEIGHT

                    if ball.rect.top < self.rect.top:  #cała sztuczna inteligencja jest opisana w tych linijkach, polega na tym,
                        self.y -= self.speed           #że są analizowane obiekty typu pygame.rect i w zależności od wzajemnego położenia
                    elif ball.rect.bottom > self.rect.bottom:
                        self.y += self.speed            #góry i dołu obiektów ball i tej klasy przeciwnika ruch wykonywany jest w odpowiednią stronę
                                                        # aby paletka podążąła za piłką

    def draw(self):
        pygame.draw.rect(screen, PADDLE_ENEMY_COLOR, self.rect)  #rysujemy obiekt na oknie

    def scoreboardenemy(self):
        lyrics(str(enemy.score), 50 , 50, 40) #rysujemy ilość punktów w górnym rogu ekranu

class Ball():
    """
    Klasa piłki - obiekt rysowany jako koło o promieniu 5 na obszarze gry.
    Początkowa prędkość względem osi OX jest wybierana losowo, co oznacza,
    że nie ma ustalone który z graczy zaczyna rozgrywkę. Piłka zawsze pojawia
    się na środku szerokości ekranu, aczkolwiek miejsce pojawienia się względem
    wysokości jest losowe i wszystko możliwości zawierają się w liście
    BALL_RANDOM_GENERATE.

    Informacje o poruszaniu się piłeczki klasy Ball:

        Piłka może przyśpieszać, aczkolwiek zastrzeżone jest, że piłka
        nie osiągnie większej prędkości niż 7, bo wtedy jest hamowana
        do 7. Pozwoli to przeprowadzić lepszą rozgrywkę z komputerem (piłka nie
        zacznie przyspieszać w pewnym momencie w ogromnie duży sposób, ponieważ
        stosowany jest odpowiedni mnożnik w zalezności od miejsca odbicia się od paletki)
         oraz ułatwia to pokonanie Komputera

        #1 - Kolizja ze ścianą górną lub dolną - piłka zmienia prędkość
        względem osi OY na przeciwną

        #2 - Kolizja ze ścianami bocznymi.
        Obiek klasy piłka jest generowany od początku z określoną prędkością
        zwróconą w stronę tego gracza, który zdobył punkt. Miejsce pojawienia
        się piłeczki (współrzędna wysokości) jest losowo wybierana. Dodany zostaje
        punkt odpowiedniemi graczowi + efekty dźwiękowe.
        Jeżeli ilość punktów jest równa ilości punktów do wygrania, to
        puszczana jest muzyka zwycięstwa/porażki, pojawia się ekran z odpowiednim
        napisem (w zależności od wyboru trybu gry i zwycięstwa lub porażki).
        Wszystkie obiekty generują się od nowa (poprzednia gra wylatuje
        z pamięci to pozwala wrócić do menu głównego i rozpocząć nową rozgrywkę).

        #3 - Kolizja z paletką - jest określana na podstawie funkcji wbudowanej
        colliderect, która sprawdza czy obiekty piłki i odpowiednich graczy
        nie kolidują ze sobą. Podczas odbicia piłeczka nabiera prędkości x i y,
        predkość y ustalana jest stała. Odbicie piłki na górze, sprawi, że piłeczka
        poleci do góry, a odbicie piłeczki dolną częścią paletki sprawi, że
        piłeczka zostanie odbita na dół. W zależności od miejsca odbicia się
        piłeczki na paletce gracza/przeciwnika, nabiera ona różnych prędkościch
        względem osi OX i OY.
    """
    def __init__(self):
        self.x = SCREEN_WIDTH/2
        self.y = random.choice(BALL_RANDOM_GENERATE)
        self.speed_x = random.choice([-4,4])
        self.speed_y = 4
        self.size = 5
        self.rect = pygame.Rect(self.x-self.size,self.y-self.size,self.size*2, self.size*2)

    def movement(self):
        if self.speed_x >= 7:   #zablokowanie możliwości przyśpieszenia piłeczki do większej wartości niż 7 lub odpowiednio -7
            self.speed_x = 7
        if self.speed_x <= -7:
            self.speed_x = -7

        self.x += self.speed_x  #zmiana współrzędnych o wartość prędkości
        self.y += self.speed_y

        self.rect.center = (self.x, self.y)

        #1 - kolizja ze ścianą górną lub dolną (piłka nie przyśpiesza, jej prędkość po prostu zmienia znak na przeciwny)
        if self.rect.top <= 1: #dla estetyki piłka odbije się odrobinę wcześniej o 1
            self.speed_y *= -1
        elif self.rect.bottom >= SCREEN_HEIGHT - 1:
            self.speed_y *= -1
        #print(self.speed_x,self.speed_y)    <------- można zaobserwować jak zmienia się prędkośc po określonym odbiciu

        #2 - kolizja ze ścianą przy klasie Player() - z wyłączeniem odbicia się od paletki (tzn. jeden z graczy traci punkt)
        if self.rect.right >= SCREEN_WIDTH:
            self.__init__()  #generujemy piłkę jeszcze raz od środka
            self.speed_x = -4 #nadajemy jej odpowiednią prędkośc
            enemy.score += 1 #dodajemy punkt
            if enemy.score < POINTS_TO_WIN: #Sprawdzamy, czy koniec gry + odpowiednia muzyka
                if GAME_MODE ==0:
                    wrongfx.play()
                else:
                    correctfx.play()
            else:
                enemy.__init__()  # koniec gry, w takim razie kasujemy wartości przypisane tym obiektom (tzn. tworzymy nowe po prostu) - aby
                player.__init__()  #po przejściu do menu i ponownego zaczęcia gry nie zacząć przez przypddek w miejscu, gdzie pozostała paletka
                ball.__init__()
                if GAME_MODE ==0: #w zależności od trybu gry wyświetlamy odpowiedni napis
                    funnyfx.play()
                    winner("Enemy wins!",115)
                else:
                    scorefx.play()
                    winner("Player 1 wins!",50)

        #2 - kolizja ze ściną przy klasie Enemy()  - z wyłączeniem odbicia się od paletki (tzn. jeden z graczy traci punkt) - analogiznie jak wyżej, tylko
        elif self.rect.left <= 0:   #wartości pozmieniane tak, aby piłka generowała się w drugą stronę i punkty zostają przypisane drugiemu graczowi
            self.__init__()
            self.speed_x = 4
            player.score += 1
            if player.score < POINTS_TO_WIN:
                correctfx.play()
            else:
                enemy.__init__()
                player.__init__()
                ball.__init__()
                scorefx.play()
                if GAME_MODE ==0:
                    winner("You win!",115)
                else:
                    winner("Player 2 wins!",50)

        #3 - kolizja z paletką (odbicie piłeczki) z Player() i Enemy() - czyli jak piłeczka się odbija od paletki (wzory)
        if self.rect.colliderect(player.rect): #najpierw sprawdzamy, czy zachodzi kolizja
            n = player.rect.center[1] #wpsółrzędna y obiektu gracza, przypisana do zmiennej n
            if self.y < n * 0.9: # w zależności od współrzędnej y piłeczki, zmiennej n i określonych warunków jak w if/elifach piłeczka odbija się w określony
                self.speed_x *= -1.2   #sposób, z zachowaniem tego, że jak odbija się od górnej czesci paletki to leci do góry, inaczej do dołu
                self.speed_y = -5
            elif self.y >= n * 0.9 and self.y < n:
                self.speed_x *= -1.1
                self.speed_y = -4
            elif self.y >= n and self.y < 1.1 * n:
                self.speed_x *= -1.1
                self.speed_y = 4
            else:
                self.speed_x *= -1.2
                self.speed_y = 5
            bouncefx.play() #dźwiek odbicia

        if self.rect.colliderect(enemy.rect): #analogicznie jak przy kolizji z Player()
            n = enemy.rect.center[1]
            if self.y < n * 0.9:
                self.speed_x *= -1.2
                self.speed_y = -5
            elif self.y >= n * 0.9 and self.y < n:
                self.speed_x *= -1.1
                self.speed_y = -4
            elif self.y >= n and self.y < 1.1 * n:
                self.speed_x *= -1.1
                self.speed_y = 4
            else:
                self.speed_x *= -1.2
                self.speed_y = 5
            bouncefx.play()

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x),int(self.y)), self.size)

# FUNKCJE, KTÓRE SĄ ODPOWIEDZIALNE ZA ZMIENNE GLOBALNE
#te funkcje, są mi potrzebne, aby przechowywać informacje/wartości, które można konfigurować podczas gry, ich przeznaczenie jest opisane w nazwie funkcji
def paddleforplayergreen():
    global PADDLE_PLAYER_COLOR
    PADDLE_PLAYER_COLOR = GREEN

def paddleforplayerred():
    global PADDLE_PLAYER_COLOR
    PADDLE_PLAYER_COLOR = RED

def paddleforplayerblue():
    global PADDLE_PLAYER_COLOR
    PADDLE_PLAYER_COLOR = BLUE

def paddleforplayerwhite():
    global PADDLE_PLAYER_COLOR
    PADDLE_PLAYER_COLOR = WHITE

def paddleforenemygreen():
    global PADDLE_ENEMY_COLOR
    PADDLE_ENEMY_COLOR = GREEN

def paddleforenemyred():
    global PADDLE_ENEMY_COLOR
    PADDLE_ENEMY_COLOR = RED

def paddleforenemyblue():
    global PADDLE_ENEMY_COLOR
    PADDLE_ENEMY_COLOR = BLUE

def paddleforenemywhite():
    global PADDLE_ENEMY_COLOR
    PADDLE_ENEMY_COLOR = WHITE

def singleplayer():
    global GAME_MODE
    GAME_MODE = 0

def multiplayer():
    global GAME_MODE
    GAME_MODE = 1

#   FUNKCJE POMOCNICZE ORAZ MENU

def quitgame():
    """Funkcja jest wywoływana podczas naciskania przycisku "Quit a game" w game_intro"""
    pygame.display.quit()
    exit()

def text_objects(text, font, color):
    """
    Funkcja odpowiedzialna, za tekst, który jest pisany odpowiednim kolorem,
    odpowiednio ustawiony do funkcji button
    text - podawany w cudzysłowach tekst, który ma się wyświetlić
    font - czcionka tekstu
    color - kolor podany w RGB tekstu
    """
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def lyrics(message, size, x,y, color=WHITE):
    """Funkcja odpowiedzialna za generowanie tekstu, który wyświetla się w
    różnych miejscach w menu i podmenu. Używany w wielu funkcjach, które tworzą
    całe strony tekstu, np. zasady gry
    message - tekst, który ma zostać wyświetlony
    size - rozmiar tekstu
    x,y - współrzędne tekstu
    color - domyślnie biały, można zmieniać, podawać w RGB"""
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(message, largeText,color)
    TextRect.center = (x,y)
    screen.blit(TextSurf,TextRect)

def button(txt,x,y,w,h,ic,ac,action=None):
    """
    Funkcja, która najpierw pobiera współrzedne myszki oraz współrzędne miejsca,
    które użytkownik nacisnał, następnie rysuje na ekranie przycisk i zmienia
    jego kolor w zależności czy kursor znajduje się nad przyciskiem czy poza przyciskiem
    txt - tekst, który pojawia sie na przycisku
    x,y - współrzędne
    w,h - szerokość i długość
    ic - kolor przycisku, kiedy kursor nie jest nad przyciskiem
    ac - kolor przycisku, kiedy kursor jest nad przyciskiem
    action - akcja, czyli działanie, które zostanie wykonane, po nacisnięciu przycisku
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesanbold.ttf",20)
    textSurf, textRect = text_objects(txt, smallText, BLACK)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def buttonbacktomenu():
    """
    Przycisk, który pojawia się w odpowiednich częściach i podstronach MENU,
    pozwalający na natychmiastowe przejście do menu głównego
    """
    button("BACK TO MENU!", SCREEN_WIDTH/2 - 75, 5 * SCREEN_HEIGHT/6, 150, 50, WHITE, GREY,action = game_intro)

def stopagame():
    """
    Funkcja, która odpowiedzialna jest za zakończenie rozgrywki, ale nie
    wychodzi z programu, tylko wraca do menu głównego kasując informacje o
    dotychczasowej rozgrywce
    """
    player.__init__()
    enemy.__init__()
    ball.__init__()
    game_intro()

def finishgame():
    """Przyciski, które pozwalają podczas pauzy zakończyć rozgrywkę i przenieść się
    do menu głównego lub wyjść całkowicie z gry."""
    button("Exit", SCREEN_WIDTH/2 - 75, 5 * SCREEN_HEIGHT/6, 160, 70, WHITE, GREY,action = quitgame)
    button("Back to menu", SCREEN_WIDTH/2 - 75, 4 * SCREEN_HEIGHT/6 , 160,70,WHITE,GREY,action=stopagame)


def winner(text,size):
    """
    Funkcja, generuje napis na całym oknie gry, używana jest do informacji końcowej
    podczas gry, który z zawodników wygrał. Współrzędne pojawienia się tekstu są ustalone
    z góry w tej funkcji.
    text - tekst informacji, kto wygrał
    size - wielkość tekstu
    """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        screen.fill(BLACK)
        lyrics(text, size, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150)

        buttonbacktomenu()
        pygame.display.update()
        clock.tick(15)


def about():
    """Podstrona menu, w której zawarte są informacje o autorze, można do niej wejść
    klikając odpowiedni przycisk w game_intro. Można przejść z tej strony do game_intro
    używając odpowiednio przycisku."""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        screen.fill(BLACK)
        lyrics("Author: D Pałatyński",30,SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30)
        lyrics("Year of production: 2018",30,SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)

        buttonbacktomenu()
        pygame.display.update()
        clock.tick(15)

def settings():
    """Podstrona menu, w która jest odpowiedzialna za konfiguracje gry, można wybrać
    kolor paletki gracza jak i kolor paletki przeciwnika (ewentualnie drugiego gracza).
    Jedną z dodatkowych możliwości jest wybranie typu gry (mode) pomiędzy grą
    przeciwko komputerowi lub przeciwko drugiego graczowi. Obecnie wybrana wartość
    pojawia się nad przyciskami, w zależności od spełnionych warunków (ifów na dole,
    które są uzależnione od zmiennych globalnych i przechowywane do momentu wyłączenia
    programu) pojawia się określony tekst, np. "Current mode: Singleplayer" itp.
    Po naciśnięciu na określony przycisk włączana jest funkcja (action w button), która
    zmienia określone parametry (kolor paletki gracza, kolor paletki przeciwnika
    oraz tryb gry)"""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        screen.fill(BLACK)

        if GAME_MODE ==0:
            lyrics("Choose the color of your enemy paddle:",15, 180,50)
        else:
            lyrics("Choose the color of the first player paddle:",15, 180,50)
        button("GREEN",100,200, 100, 50, GREEN, GREY,action=paddleforenemygreen)
        button("RED", 100, 300, 100, 50, RED, GREY,action=paddleforenemyred)
        button("BLUE", 100, 400, 100, 50, BLUE, GREY,action=paddleforenemyblue)
        button("WHITE", 100, 100, 100, 50, WHITE, GREY,action=paddleforenemywhite)
        if PADDLE_ENEMY_COLOR == WHITE:
            lyrics("Current color: WHITE", 15, 150, 70)
        elif PADDLE_ENEMY_COLOR == RED:
            lyrics("Current color: RED", 15, 150, 70,RED)
        elif PADDLE_ENEMY_COLOR == GREEN:
            lyrics("Current color: GREEN", 15, 150, 70,GREEN)
        elif PADDLE_ENEMY_COLOR == BLUE:
            lyrics("Current color: BLUE", 15, 150, 70, BLUE)

        lyrics("Mode: ",15, 400,180)
        button("Singleplayer", 350, 250, 100, 50, WHITE, GREY,action=singleplayer)
        button("Multiplayer", 350, 350, 100, 50, WHITE, GREY,action=multiplayer)
        if GAME_MODE == 0:
            lyrics("Current mode: Singleplayer",15, 400, 200)
        elif GAME_MODE == 1:
            lyrics("Current mode: Multiplayer",15, 400, 200)

        if GAME_MODE ==0:
            lyrics("Choose the color of your paddle:",15, 630,50)
        else:
            lyrics("Choose the color of the second player paddle:",15, 630,50)
        button("GREEN",600,200, 100, 50, GREEN, GREY,action=paddleforplayergreen)
        button("RED", 600, 300, 100, 50, RED, GREY,action=paddleforplayerred)
        button("BLUE", 600, 400, 100, 50, BLUE, GREY,action=paddleforplayerblue)
        button("WHITE", 600, 100, 100, 50, WHITE, GREY,action=paddleforplayerwhite)
        if PADDLE_PLAYER_COLOR == WHITE:
            lyrics("Current color: WHITE", 15, 650, 70)
        elif PADDLE_PLAYER_COLOR == RED:
            lyrics("Current color: RED", 15, 650, 70,RED)
        elif PADDLE_PLAYER_COLOR == GREEN:
            lyrics("Current color: GREEN", 15, 650, 70,GREEN)
        elif PADDLE_PLAYER_COLOR == BLUE:
            lyrics("Current color: BLUE", 15, 650, 70, BLUE)

        buttonbacktomenu()
        pygame.display.update()
        clock.tick(15)

def rules():
    """Podstrona menu, w której zawarte są zasady gry"""
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        screen.fill(BLACK)
        lyrics("Control the right paddle using keyboard. Use UP to move the paddle up",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 150)
        lyrics(" and DOWN to move the paddle down.",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 120)
        lyrics("Points are scored when your opponent misses the ball.",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 90)
        lyrics("First player to reach 5 points wins the game.",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 60)
        lyrics("If you play on two players mode, the second player is on the left side.",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        lyrics("Use W to move up, and S to move down.",20,SCREEN_WIDTH/2,SCREEN_HEIGHT/2 + 30)
        lyrics("If you want to pause the game, press P.",20, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60)

        buttonbacktomenu()
        pygame.display.update()
        clock.tick(15)


def pause():
    """Podczas gry po wcisnięcicu przez użytkownika przycisku P włączana jest pauza,
    następuje stop w rozgrywce i pojawia się napis "PAUSED", aby kontynuować grę,
    trzeba nacisnąć na przycisk "Continue", który wyświetla się na środku ekranu.
    Ewentualnie można od razu wyjść z gry klikając na przycisk "Finish the game"."""
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                normal_game()

        lyrics("PAUSED", 115, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150)
        pygame.display.update()
        button("Continue",SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 ,160,70,WHITE,GREY,action=normal_game)
        finishgame()

def game_intro():
    """Funkcja, która tworzy menu główne gry, z tej podstrony można odpowiednio:
        Start a game - zacząć rozgrywkę z określoną konfiguracją
        Exit - zamknąć grę
        Rules - przeczytać zasady gry
        About - dowiedzieć się informacji o autorze
        Settings - wybrać odpowiednią dla siebie konfigurację"""
    screen.fill(BLACK)
    pygame.display.update()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
        lyrics("PONG GAME", 115, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150)
        pygame.display.update()

        button("Start a game",160,250,160,70,WHITE,GREY,action=normal_game)
        button("Exit", 480,250,160,70,WHITE,GREY,action=quitgame)
        button("Rules",125,450,100,50,WHITE,GREY,action=rules)
        button("About",350,450,100,50,WHITE,GREY,action=about)
        button("Settings",575,450,100,50,WHITE,GREY,action=settings)


        pygame.display.update()
        clock.tick(15)

def normal_game():
    """Rozgrywka właściwa, w tym miejscu, są wywoływane wszystkie funkcje związane
    z klasami obiektów takich jak Player, Enemy i Ball. Funkcja włącza się po nacisnięciu
    przycisku "Start a game" w menu głównym"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pause()

        ball.movement()
        player.movement()
        enemy.movement()
        screen.fill(BLACK)
        ball.draw()
        player.draw()
        player.scoreboardplayer()
        player.points()
        enemy.draw()
        enemy.scoreboardenemy()
        enemy.points()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    #Stworzenie obiektów określonych klas oraz uruchomienie menu
    player = Player()
    enemy = Enemy()
    ball = Ball()
    game_intro()