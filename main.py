#Imports
import pygame
from pygame import mixer
from regex import R

pygame.init()

#Color params
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
red = (255, 0, 0)
gold = (212, 175, 155)
cyan = (0, 255, 255)

#Screen params
WIDTH = 1400
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 28)

#Time params
fps = 60
timer = pygame.time.Clock()
instruments = 6
beats = 8
bpm = 240

#Game params
playing = True
active_length = 0
active_beat = 1
beat_changed = True

#Other variables
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

#Loading sounds
hi_hat = mixer.Sound('./sounds/hi_hat.WAV')
snare = mixer.Sound('./sounds/snare.WAV')
bass = mixer.Sound('./sounds/kick.WAV')
crash = mixer.Sound('./sounds/crash.wav')
clap = mixer.Sound('./sounds/clap.wav')
floor = mixer.Sound('./sounds/tom.WAV')

#Functions
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i==0:
                hi_hat.play()
            elif i==1:
                snare.play()
            elif i==2:
                bass.play()
            elif i==3:
                crash.play()
            elif i==4:
                clap.play()
            elif i==5:
                floor.play()

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    colors = [gray, white, gray]
    boxes = []
    
    #Hi Hat
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))
    #Snare
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    #Bass Drum
    bass_drum_text = label_font.render('Bass Drum', True, white)
    screen.blit(bass_drum_text, (30, 230))
    #Crash
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330))
    #Clap
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    #Floor Tom
    floor_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_text, (30, 530))

    #Creating the instruments grid
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i+1)*100), (200, (i+1)*100), 3)

    #Creating the boxes grid
    for i in range(beats):
        for j in range(instruments):
            
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            
            rect_x_ini = i*(WIDTH-200)//beats + 200
            rect_y_ini = j*100
            rect_width = (WIDTH-200)//beats
            rect_height = (HEIGHT-200)//instruments

            rect = pygame.draw.rect(screen, color, [rect_x_ini+5, rect_y_ini+5, rect_width - 10, rect_height - 10], 0, 3)
            pygame.draw.rect(screen, gold, [rect_x_ini, rect_y_ini, rect_width, rect_height], 5, 5)
            pygame.draw.rect(screen, black, [rect_x_ini, rect_y_ini, rect_width, rect_height], 2, 5)
            
            boxes.append((rect, (i,j)))

        active = pygame.draw.rect(screen, cyan, [beat*(WIDTH-200)//beats + 200, 0, ((WIDTH-200)//beats), instruments*100], 5, 3)

    return boxes

#Main game loop
run = True

while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in boxes:
                if box[0].collidepoint(event.pos):
                    coords = box[1]
                    clicked[coords[1]][coords[0]] *= -1

    beat_length = 3600/bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True
       
    pygame.display.flip()

pygame.quit()