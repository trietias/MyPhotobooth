import gphoto2 as gp
import pygame, sys, time, os
from pygame.locals import *
import cv2
import cups
import numpy as np
from imutils.video import WebcamVideoStream
from PIL import Image

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
photo_size = 1500, 996
p1_loc = 237, 1255
p2_loc = 1863, 1255
p3_loc = 1863, 150
running = False
state = 0
picture_state = 0
counter_state = 4
p1 = ''
p2 = ''
p3 = ''
p1_cap = 0
p2_cap = 0
p3_cap = 0
time_since_last_picture = 0

conn = cups.Connection()

def curTime():
    millis = int(round(time.time() * 1000))
    return millis


def captureImage():
    updateWeb()
    context = gp.Context()
    gp.Camera()
    C = gp.Camera()

    filename = 'Photoboothphoto_' + str(curTime()) + '.jpg'
    cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
    print("Captured " + cap.folder + "/" + cap.name)
    file = C.file_get(cap.folder, cap.name, gp.GP_FILE_TYPE_NORMAL)
    gp.gp_file_save(file, filename)
    return filename


def photoSession():
    p1 = captureImage()
    time.sleep(2)
    p2 = captureImage()
    time.sleep(2)
    p3 = captureImage()
    time.sleep(2)

    template = Image.open('template.png')
    botLeft = Image.open(p1)
    botRight = Image.open(p2)
    topRight = Image.open(p3)
    botLeft = botLeft.resize(photo_size)
    botRight = botRight.resize(photo_size)
    topRight = topRight.resize(photo_size)

    template.paste(botLeft, p1_loc)
    template.paste(botRight, p2_loc)
    template.paste(topRight, p3_loc)
    template.show()


def updateWeb():
    frame = camera.read()

    screen.fill([0, 0, 0])
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

pygame.init()

flags = FULLSCREEN | DOUBLEBUF
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), flags)
screen.set_alpha(None)
font = pygame.font.Font('Bodoni/TrueType/Bodoni-11-Bold.ttf', 120)
effect = pygame.mixer.Sound('beep.wav')
clock = pygame.time.Clock()

camera = WebcamVideoStream(src=0).start()

context = gp.Context()
gp.Camera()
C = gp.Camera()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    state = 1
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

        if state == 0:
            # Do nothing for now
            a = 1
        elif state == 1:
            if picture_state == 0:
                if p1_cap == 0:
                    if counter_state == 4:
                        time_since_last_picture = curTime()
                        effect.play()
                        counter_state = 3
                    elif counter_state == 0:
                        filename = 'Photoboothphoto_' + str(curTime()) + '.jpg'
                        try:
                            cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                        except gp.GPhoto2Error:
                            time.sleep(1)
                            cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                        print("Captured " + cap.folder + "/" + cap.name)
                        file = C.file_get(cap.folder, cap.name, gp.GP_FILE_TYPE_NORMAL)
                        gp.gp_file_save(file, filename)
                        p1 = filename
                        p1_cap = 1
                        counter_state = 4
                        picture_state = 1
                    else:
                        if curTime() - time_since_last_picture >= 1000:
                            effect.play()
                            counter_state -= 1
                            time_since_last_picture = curTime()
            elif picture_state == 1:
                if (os.path.isfile(p1)):
                    if p2_cap == 0:
                        if counter_state == 4:
                            time_since_last_picture = curTime()
                            effect.play()
                            counter_state = 3
                        elif counter_state == 0:
                            filename = 'Photoboothphoto_' + str(curTime()) + '.jpg'
                            try:
                                cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                            except gp.GPhoto2Error:
                                time.sleep(1)
                                cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                            print("Captured " + cap.folder + "/" + cap.name)
                            file = C.file_get(cap.folder, cap.name, gp.GP_FILE_TYPE_NORMAL)
                            gp.gp_file_save(file, filename)
                            p2 = filename
                            p2_cap = 1
                            counter_state = 4
                            picture_state = 2
                        else:
                            if curTime() - time_since_last_picture >= 1000:
                                effect.play()
                                counter_state -= 1
                                time_since_last_picture = curTime()

                else:
                    continue
            elif picture_state == 2:
                if (os.path.isfile(p2)):
                    if p3_cap == 0:
                        if counter_state == 4:
                            time_since_last_picture = curTime()
                            effect.play()
                            counter_state = 3
                        elif counter_state == 0:
                            filename = 'Photoboothphoto_' + str(curTime()) + '.jpg'
                            try:
                                cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                            except gp.GPhoto2Error:
                                time.sleep(1)
                                cap = C.capture(gp.GP_CAPTURE_IMAGE, context)
                            print("Captured " + cap.folder + "/" + cap.name)
                            file = C.file_get(cap.folder, cap.name, gp.GP_FILE_TYPE_NORMAL)
                            gp.gp_file_save(file, filename)
                            p3 = filename
                            p3_cap = 1
                            counter_state = 4
                            picture_state = 3
                        else:
                            if curTime() - time_since_last_picture >= 1000:
                                effect.play()
                                counter_state -= 1
                                time_since_last_picture = curTime()
                else:
                    continue
            elif picture_state == 3:
                template = Image.open('template.png')
                botLeft = Image.open(p1)
                botRight = Image.open(p2)
                topRight = Image.open(p3)
                botLeft = botLeft.resize(photo_size)
                botRight = botRight.resize(photo_size)
                topRight = topRight.resize(photo_size)

                fName = 'Combined_' + str(curTime()) + '.png'
                template.paste(botLeft, p1_loc)
                template.paste(botRight, p2_loc)
                template.paste(topRight, p3_loc)
                template.save(fName)
                time.sleep(1)
                conn.printFile('Canon_SELPHY_CP1300',fName,'',{})
                state = 0
                picture_state = 0
                p1 = ''
                p2 = ''
                p3 = ''
                p1_cap = 0
                p2_cap = 0
                p3_cap = 0

        else:
            updateWeb()

        updateWeb()
        if counter_state < 4 and counter_state > 0:
            counter = font.render(str(int(counter_state)), True, pygame.Color('white'))
            text_rect = counter.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            screen.blit(counter, text_rect)
        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
        screen.blit(fps, (50, 50))
        clock.tick(60)
        pygame.display.update()

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()

