#!/usr/bin/env python2
# Import libraries
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
    import pygame, math, random, sys, menu, settings
    from pygame.locals import *
except:
    import pygame, math, random, sys, menu, settings
    from pygame.locals import *

def play():
    cnt = 0
    dec = False
    timeForPower = False
    powerSent = False
    powercords = []
    freezePower = False
    freezeTimer = 10
    # Set the width and height of the window
    width, height = int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)
    # Create the window
    screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    # Initialize the joystick module
    pygame.joystick.init()
    # Check if there are any joysticks
    joystick_count = pygame.joystick.get_count()
    # If there are any joysticks, initialize the first one, else quit the joystick module
    if joystick_count:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        JS = True
        # Set joystick position
        if JS:
            stick0 = "right"
    else:
        pygame.joystick.quit()
        JS = False
    # Set pressed keys
    keys = [False, False, False, False]
    JSkeys = [False, False, False, False]
    # Set player position
    playerpos=[100,100]
    # Make an list for the accuracy
    acc=[0,0]
    # Make an list for where the arrows are
    arrows=[]
    # Set the timer for spawning badgers
    badtimer=100
    badtimer1=0
    # Make an list for where the badgers are
    badguys=[[800,100]]
    # Set your health value
    healthvalue=194
    # Set the wait times
    waitforexit=0
    waitforarrows=0
    waitforballoons=0
    waitforballoons2=2
    # Set displaying balloon on/off
    balloon1display = False
    balloon2display = False
    # Set start ticks
    startticks = pygame.time.get_ticks()
    # Initialize the mixer (for sound)
    pygame.mixer.init()
    # Set title
    pygame.display.set_caption("Galaxy Wars")
    
    # Load images
    # Load the players image
    player = pygame.image.load("resources/images/dude.png")
    # Load the power image
    power = pygame.image.load("resources/images/power.png")
    # Load the background image
    bgmain = pygame.image.load("resources/images/starfield.png")
    sunred = pygame.image.load("resources/images/SunRed.png")
    # Load the image of the castles
    castle = pygame.image.load("resources/images/castle.png")
    # Load the image for the arrows
    arrow = pygame.image.load("resources/images/bullet.png")
    # Load the image for the badgers
    badguyimg1 = pygame.image.load("resources/images/badguy.png")
    badguyimg = badguyimg1
    # Load the overlays
    greenoverlay = pygame.image.load("resources/images/greenoverlay.png")
    redoverlay = pygame.image.load("resources/images/redoverlay.png")
    # Load the healthbar images
    healthbar = pygame.image.load("resources/images/healthbar.png")
    health = pygame.image.load("resources/images/health.png")
    # Load the text balloons
    balloon1 = pygame.image.load("resources/images/balloon1.png")
    balloon2 = pygame.image.load("resources/images/balloon2.png")
    
    # Load audio
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    # Set the audio volume
    hit.set_volume(0.15)
    enemy.set_volume(0.15)
    shoot.set_volume(0.15)
    # Set the background music
    pygame.mixer.music.load('resources/audio/background.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.30)
    
    # Set positions
    castle1 = (0,height/16)
    castle2 = (0,height/3.5)
    castle3 = (0,height/2)
    castle4 = (0,height/1.4)

    # Set display mode
    prevFS = settings.getFullscreen()
    if settings.getFullscreen() == True:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    elif settings.getFullscreen() == False:
        screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    # Keep looping through
    running = 1
    exitcode = 0
    while running:
        print acc[0]
        # Set display mode if changed
        if prevFS != settings.getFullscreen():
            if settings.getFullscreen() == True:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
                prevFS = settings.getFullscreen()
            elif settings.getFullscreen() == False:
                screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
                prevFS = settings.getFullscreen()

        # Set joystick buttons, if there are any
        if JS:
            buttonUP = joystick.get_button(4)
            buttonRIGHT = joystick.get_button(5)
            buttonDOWN = joystick.get_button(6)
            buttonLEFT = joystick.get_button(7)
            buttonX = joystick.get_button(14)
            stick0a = joystick.get_axis(0)
            stick0b = joystick.get_axis(1)
            
        # Check for stick0's position
        if JS:
            if stick0a <= -0.5 and stick0b <= -0.5:
                stick0 = "leftup"
            elif stick0a <= -0.5 and stick0b >= 0.5:
                stick0 = "leftdown"
            elif stick0a >= 0.5 and stick0b <= -0.5:
                stick0 = "rightup"
            elif stick0a >= 0.5 and stick0b >= 0.5:
                stick0 = "rightdown"
            elif stick0a <= -0.5:
                stick0 = "left"
            elif stick0a >= 0.5:
                stick0 = "right"
            elif stick0b <= -0.5:
                stick0 = "up"
            elif stick0b >= 0.5:
                stick0 = "down"
            
        badtimer-=1
        # Clear the screen before drawing it again
        screen.fill(0)
        # Draw the background
        screen.blit(bgmain, (0, 0))
        screen.blit(sunred, (width // 2, 0))
        # Draw the castles
        screen.blit(castle, castle1)
        screen.blit(castle, castle2)
        screen.blit(castle, castle3)
        screen.blit(castle, castle4)
        # Set player position and rotation

        if JS == False:
            position = pygame.mouse.get_pos()
            angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
            playerrot = pygame.transform.rotate(player, 360-angle*57.29)
            playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
            screen.blit(playerrot, playerpos1)
        elif JS == True:
            if stick0 == "left":
                playerrot = pygame.transform.rotate(player, 180)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "right":
                playerrot = pygame.transform.rotate(player, 0)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "up":
                playerrot = pygame.transform.rotate(player, 90)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "down":
                playerrot = pygame.transform.rotate(player, 270)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "leftup":
                playerrot = pygame.transform.rotate(player, 135)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "leftdown":
                playerrot = pygame.transform.rotate(player, 225)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "rightup":
                playerrot = pygame.transform.rotate(player, 45)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)
            elif stick0 == "rightdown":
                playerrot = pygame.transform.rotate(player, 315)
                playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
                screen.blit(playerrot, playerpos1)

        
        # Draw arrows
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*20
            vely=math.sin(bullet[0])*20
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>width or bullet[2]<-64 or bullet[2]>height:
                arrows.pop(index)
            index+=1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                screen.blit(arrow1, (projectile[1], projectile[2]))
        # Draw badguys
        if badtimer==0:
            badheight1 = height/9.6
            badheight2 = height/1.1
            badheight = random.randint(int(badheight1), int(badheight2))
            badguys.append([width, badheight])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
        index=0
        for badguy in badguys:
            if badguy[0]<-64:
                badguys.pop(index)
            if freezePower is False:
                badguy[0]-=7
                if cnt < 30 and dec is False:
                    badguy[1] += 7
                    cnt += 1
                else:
                    dec = True
                    cnt -= 1
                    badguy[1] -= 7
                    if cnt is 0:
                        dec = False
            # Attack castle
            badrect=pygame.Rect(badguyimg.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= random.randint(5,20)
                badguys.pop(index)
            # Check for collisions
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0]+=1
                    if acc[0] % 5 == 0:
                        print "yo man"
                        timeForPower = True
                    else:
                        timeForPower = False
                    badguys.pop(index)
                    arrows.pop(index1)
                index1+=1
            # Next bad guy
            index+=1
        # Draw badgers
        for badguy in badguys:
            screen.blit(badguyimg, badguy)

        # Draw power if score  = 0 mod 5
        
        if powerSent:
            powercords[0] -= 7
            screen.blit(power, powercords)
            if powercords[0] < 0:
                powerSent = False

        if timeForPower and powerSent == False:
            powerheight1 = height/9.6
            powerheight2 = height/1.1
            powerheight = random.randint(int(powerheight1), int(powerheight2))
            powercords = [width, powerheight]
            print "powerSent"
            powerSent = True
            timeForPower = False
            screen.blit(power, powercords)

        if freezePower:
            freezeTimer += 10
            if freezeTimer > 1000:
                freezePower = False
                freezeTimer = 0
        # Check if power is Taken
        if powerSent:
            powerRect = pygame.Rect(power.get_rect())
            playerRect = pygame.Rect(player.get_rect())
            powerRect.top = powercords[1]
            powerRect.left = powercords[0]
            playerRect.top = playerpos[1]
            playerRect.left = playerpos[0]
            if powerRect.colliderect(playerRect):
                freezePower = True
                print "Collision Detected"
                powerSent = False
        # Draw clock
        font = pygame.font.Font("freesansbold.ttf", 24)
        survivedtext = font.render(str((90000-pygame.time.get_ticks()+startticks)/60000)+":"+str((90000-pygame.time.get_ticks()+startticks)/1000%60).zfill(2), True, (0,0,0))
        textRect = survivedtext.get_rect()
        textRect.topright=[width-5, 5]
        screen.blit(survivedtext, textRect)
        # Draw health bar
        screen.blit(healthbar, (5,5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1+8,8))
        # Loop through the events
        for event in pygame.event.get():
            # Check if the event is the X button 
            if event.type==pygame.QUIT:
                # If it is stop the music and go back to the main menu
                pygame.mixer.music.stop()
                menu.launch()
            if event.type == pygame.KEYDOWN:
                # Move up
                if event.key==K_w:
                    keys[0]=True
                elif event.key==K_UP:
                    keys[0]=True
                # Move left
                elif event.key==K_a:
                    keys[1]=True
                elif event.key==K_LEFT:
                    keys[1]=True
                # Move down
                elif event.key==K_s:
                    keys[2]=True
                elif event.key==K_DOWN:
                    keys[2]=True
                # Move right
                elif event.key==K_d:
                    keys[3]=True
                elif event.key==K_RIGHT:
                    keys[3]=True
                # Quit by pressing escape
                elif event.key==K_ESCAPE:
                    pygame.mixer.music.stop()
                    menu.launch()
                # Fullscreen by pressing F4
                elif event.key==K_F4:
                    settings.changeFullscreen()
                elif event.key==pygame.K_SPACE:
                    if waitforarrows == 0:
                        shoot.play()
                        position=pygame.mouse.get_pos()
                        acc[1]+=1
                        arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
                        # Set wait time for arrows in frames
                        waitforarrows=15
                        if waitforballoons2:
                            waitforballoons2-=1
                        else:
                            # Choose balloon
                            balloonnr = random.randint(1, 2)
                            if balloonnr == 1:
                                balloon1display = True
                            elif balloonnr == 2:
                                balloon2display = True
                            waitforballoons2=2
            if event.type == pygame.KEYUP:
                # Move up
                if event.key==pygame.K_w:
                    keys[0]=False
                elif event.key==pygame.K_UP:
                    keys[0]=False
                # Move left
                elif event.key==pygame.K_a:
                    keys[1]=False
                elif event.key==pygame.K_LEFT:
                    keys[1]=False
                # Move down
                elif event.key==pygame.K_s:
                    keys[2]=False
                elif event.key==pygame.K_DOWN:
                    keys[2]=False
                # Move right
                elif event.key==pygame.K_d:
                    keys[3]=False
                elif event.key==pygame.K_RIGHT:
                    keys[3]=False
        if waitforarrows:
            waitforarrows-=1
            waitforballoons = waitforarrows
        # Display balloon
        if waitforballoons:
            waitforballoons-=1
            if balloon1display:
                screen.blit(balloon1, (playerpos[0]+10, playerpos[1]-60))
            elif balloon2display:
                screen.blit(balloon2, (playerpos[0]+10, playerpos[1]-60))
        else:
            balloon1display = False
            balloon2display = False
    
        # Check if there are any joysticks
        if JS:
            # Check if UP is pressed
            if buttonUP:
                JSkeys[0]=True
            # Check if RIGHT is pressed
            elif buttonRIGHT:
                JSkeys[3]=True
            # Check if DOWN is pressed
            elif buttonDOWN:
                JSkeys[2]=True
            # Check if LEFT is pressed
            elif buttonLEFT:
                JSkeys[1]=True
            else:
                JSkeys[0]=False
                JSkeys[1]=False
                JSkeys[2]=False
                JSkeys[3]=False
            # Check of X is pressed
            if buttonX:
                if waitforarrows == 0:
                    shoot.play()
                    acc[1]+=1
                    if stick0 == "left":
                        arrows.append([3,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "right":
                        arrows.append([0,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "up":
                        arrows.append([-1.5,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "down":
                        arrows.append([1.5,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "leftup":
                        arrows.append([-2.25,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "leftdown":
                        arrows.append([2.25,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "rightup":
                        arrows.append([-0.75,playerpos1[0]+32,playerpos1[1]+32])
                    elif stick0 == "rightdown":
                        arrows.append([0.75,playerpos1[0]+32,playerpos1[1]+32])
                    # Set wait time for arrows in frames
                    waitforarrows=15
                    if waitforballoons2:
                        waitforballoons2-=1
                    else:
                        # Choose balloon
                        balloonnr = random.randint(1, 2)
                        if balloonnr == 1:
                            balloon1display = True
                        elif balloonnr == 2:
                            balloon2display = True
                        waitforballoons2=2        
        # Move player
        # Up
        if keys[0]:
            playerpos[1]-=5
        # Down
        elif keys[2]:
            playerpos[1]+=5
        # Left
        if keys[1]:
            playerpos[0]-=5
        # Right
        elif keys[3]:
            playerpos[0]+=5
        # Move player with JoyStick
        # Up
        if JSkeys[0]:
            playerpos[1]-=5
        # Down
        elif JSkeys[2]:
            playerpos[1]+=5
        # Left
        if JSkeys[1]:
            playerpos[0]-=5
        # Right
        elif JSkeys[3]:
            playerpos[0]+=5
    
        # Win/Lose check
        # Win
        if (pygame.time.get_ticks()-startticks)>=90000:
            running=0
            exitcode=1
        # Lose
        if healthvalue<=0:
            running=0
            exitcode=0
        if acc[1]!=0:
            accuracy=acc[0]*1.0/acc[1]*100
        else:
            accuracy=0
        # Flip the display
        pygame.display.flip()
    # Stop the music
    pygame.mixer.music.stop()
    # Win/lose display        
    # Lose
    if exitcode==0:
        # Initialize the font
        pygame.font.init()
        # Set font
        font = pygame.font.Font("freesansbold.ttf", 24)
        bigfont = pygame.font.Font("freesansbold.ttf", 48)
        # Render text
        gameover = bigfont.render("Game over!", True, (255,0,0))
        gameoverRect = gameover.get_rect()
        gameoverRect.centerx = screen.get_rect().centerx
        gameoverRect.centery = screen.get_rect().centery-24
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        # Draw red overlay
        for x in range(width/redoverlay.get_width()+1):
            for y in range(height/redoverlay.get_height()+1):
                screen.blit(redoverlay,(x*100,y*100))
        # Draw text
        screen.blit(gameover, gameoverRect)
        screen.blit(text, textRect)
    # Win
    else:
        # Initialize the font
        pygame.font.init()
        # Set font
        font = pygame.font.Font("freesansbold.ttf", 24)
        bigfont = pygame.font.Font("freesansbold.ttf", 48)
        # Render text
        youwin = bigfont.render("You win!", True, (0,255,0))
        youwinRect = youwin.get_rect()
        youwinRect.centerx = screen.get_rect().centerx
        youwinRect.centery = screen.get_rect().centery-24
        text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery+24
        # Draw green overlay
        for x in range(width/greenoverlay.get_width()+1):
            for y in range(height/greenoverlay.get_height()+1):
                screen.blit(greenoverlay,(x*100,y*100))
        # Draw text
        screen.blit(youwin, youwinRect)
        screen.blit(text, textRect)
    # Exit automatic when the game is stopped
    while 1:
        waitforexit+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if waitforexit == 1000:
            menu.launch()
        # Update the screen
        pygame.display.flip()
