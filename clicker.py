# Example file showing a circle moving on screen
import pygame
import random 
import math
import threading
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 360))
clock = pygame.time.Clock()
running = True
dt = 0

def modulate(num, dist):
    return ((num - 1) % dist ) + 1

timer = 0

pop_sfx = pygame.mixer.Sound("pop.wav")
pop_sfx.set_volume(0.5)
ding_sfx = pygame.mixer.Sound("Bell Ding.mp3")
ding_sfx.set_volume(0.5)

upgrade_icons = [pygame.image.load("trashpicker_bit.png").convert_alpha(), pygame.image.load("trashbin_bit.png").convert_alpha(), pygame.image.load("warning_bit.png").convert_alpha(), pygame.image.load("worker_bit.png").convert_alpha(), pygame.image.load("wte_bit.png").convert_alpha(), pygame.image.load("nets_bit.png").convert_alpha(), pygame.image.load("plant_bit.png").convert_alpha(), pygame.image.load("funds_bit.png").convert_alpha(), pygame.image.load("space_bit.png").convert_alpha()]
# trashpicker, bins, warnings, worker, waste-to-energy, nets, recycling plant, extra funds, rocket
upgrade_rect = [""] * len(upgrade_icons)
upgrade_unlocked = [False] * len(upgrade_icons)
upgrade_amounts = [0] * len(upgrade_icons)
upgrade_costs = [10, 100, 500, 1500, 5000, 10000, 50000, 125000, 1000000]

score = 0
amount_gained = 0

upgrade_txtcost = [""] * len(upgrade_icons)
upgrade_txtcost_rect = [""] * len(upgrade_icons)
upgrade_txtamnt = [""] * len(upgrade_icons)
upgrade_txtamnt_rect = [""] * len(upgrade_icons)

for x in range(0, len(upgrade_icons)):
    upgrade_icons[x] = pygame.transform.scale(upgrade_icons[x], (96, 96))
    upgrade_rect[x] = upgrade_icons[x].get_rect()

shop_uis = [pygame.image.load("shopUI_bit.png").convert_alpha(), pygame.image.load("shopUI-alt_bit.png").convert_alpha()]
shop_x = -379
shop_ui = shop_uis[0]
shop_ui = pygame.transform.scale(shop_ui, (416, 360))
shop_ui_active = False
shop_ui_rect = shop_ui.get_rect()

notif_sym = pygame.image.load("notification_bit.png").convert_alpha()
notif_sym = pygame.transform.scale(notif_sym, (34/2, 155/2))
notif_active = False
notif_sym = pygame.transform.rotozoom(notif_sym, -20, 1)

sym_image = pygame.image.load("symbol.png").convert_alpha()
sym_image = pygame.transform.scale(sym_image, (371/9, 360/9))

bg_source = pygame.image.load("checkerboard_bit.png").convert_alpha()
bg_source = pygame.transform.scale(bg_source, (750, 614))

bg_coords = 0

trash_list = [pygame.image.load("soda_bit.png").convert_alpha(), pygame.image.load("bottle_bit.png").convert_alpha(),pygame.image.load("plastic_bit.png").convert_alpha(),pygame.image.load("gold bar_bit.png").convert_alpha(),pygame.image.load("bag_bit.png").convert_alpha(),pygame.image.load("ball_bit.png").convert_alpha()]
scale_factor = 1.5
trash_list_res = [(145/scale_factor, 196/scale_factor), (107/scale_factor, 284/scale_factor), (313/scale_factor, 209/scale_factor),(313/scale_factor, 201/scale_factor),(247/scale_factor, 255/scale_factor),(157/scale_factor, 157/scale_factor)]
trash_list_index = 0

source_clicker_image = trash_list[trash_list_index]

click_obj_size = 1
click_obj_image = source_clicker_image
clicker_rotate = 0
click_obj_image = pygame.transform.rotate(click_obj_image, clicker_rotate)
click_obj_image = pygame.transform.scale(click_obj_image, trash_list_res[trash_list_index])
click_obj_rect = click_obj_image.get_rect()

gained_slash = pygame.image.load("slash_bit.png").convert_alpha()
gained_slash = pygame.transform.scale(gained_slash, (34/4, 75/4))

touching_upgrade = -1
up_descriptions = [["Trash Picker", "A spike tool that helps","you pick up more trash quicker.", "Increases score gained per click."],["Recycling Bin", "A place to throw things away.", "50 score per second."],["A warning sign", "A sign to tell people not to litter.", "100 score per second."], ["Community Service Worker", "Someone else to pick up the trash.", "500 score per second."],["Waste-To-Energy Plant", "Converts the trash", "into electricity.", "1000 score per second."],["Ocean Nets", "Nets to clean the trash", "out of the ocean.", "2500 score per second."],["Recycling Plant", "Converts the trash", "back into usuable things.", "5000 score per second."],["Extra Funds", "Some billionaire's private funds.", "Plus 0.1x multiplier to", "all productions."],["Rocket", "Send the trash into space.", "not our problem anymore. :P", "10000 score per second."]]

mainFont = pygame.font.Font("Schluber.ttf", 50)
subtitleFont = pygame.font.Font("Schluber.ttf", 25)
upgradeFont = pygame.font.Font("Schluber.ttf", 25)
descFont = pygame.font.Font("Schluber.ttf", 20)

def unlockUpgrades():
    for x in range(0, len(upgrade_icons)):
        if upgrade_unlocked[x] == False and score >= upgrade_costs[x]/2 and upgrade_amounts[x] == 0:
            global notif_active
            if shop_ui_active == False:
                notif_active = True
            upgrade_unlocked[x] = True

def perSecond(scoreTimer):
    while scoreTimer.is_set():
        global score
        global amount_gained
        amount_gained = 0
        amount_gained += round(50 * upgrade_amounts[1] * (upgrade_amounts[7]/10+1))
        amount_gained += round(100 * upgrade_amounts[2] * (upgrade_amounts[7]/10+1))
        amount_gained += round(500 * upgrade_amounts[3] * (upgrade_amounts[7]/10+1))
        amount_gained += round(1000 * upgrade_amounts[4] * (upgrade_amounts[7]/10+1))
        amount_gained += round(2500 * upgrade_amounts[5] * (upgrade_amounts[7]/10+1))
        amount_gained += round(5000 * upgrade_amounts[6] * (upgrade_amounts[7]/10+1))
        amount_gained += round(10000 * upgrade_amounts[8] * (upgrade_amounts[7]/10+1))
        score += amount_gained
        time.sleep(1)

scoreTimer = threading.Event()
scoreTimer.set()

ts = threading.Thread(target=perSecond, args=(scoreTimer,))
ts.start()

while running:
    click_obj_image = source_clicker_image
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            scoreTimer.clear()
            running = False
        elif shop_ui_active == False:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and click_obj_rect.collidepoint(mouse_x, mouse_y):
                if trash_list_index == 3:
                    score += (1 + upgrade_amounts[0]) * 3
                else:
                    score += 1 + upgrade_amounts[0]
                pop_sfx.play()
                click_obj_size = 0.8
                trash_list_index = random.randint(0, len(trash_list)-1)
                source_clicker_image = trash_list[trash_list_index]
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and click_obj_rect.collidepoint(mouse_x, mouse_y):
                click_obj_size = 1.2
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and shop_ui_rect.collidepoint(mouse_x, mouse_y) and mouse_x <= 50:
                shop_ui_active = True
                notif_active = False
                shop_ui = shop_uis[1]
                shop_ui = pygame.transform.scale(shop_ui, (416, 360))
        elif shop_ui_active == True:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and shop_ui_rect.collidepoint(mouse_x, mouse_y):
                if mouse_x >= 360:
                    shop_ui_active = False
                    shop_ui = shop_uis[0]
                    shop_ui = pygame.transform.scale(shop_ui, (416, 360))
                else:
                    for x in range(0, len(upgrade_icons)):
                        if upgrade_unlocked[x] == True and score >= round(upgrade_costs[x] * (1.15**upgrade_amounts[x])) and upgrade_rect[x].collidepoint(mouse_x, mouse_y):
                            score -= round(upgrade_costs[x] * (1.15**upgrade_amounts[x]))
                            upgrade_amounts[x] += 1
                            ding_sfx.play()

    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#94bfff")

    unlockUpgrades()

    if shop_ui_active == True:
        shop_x += 0.2 * (0 - shop_x)
        touching_upgrade = -1
        for x in range(0, len(upgrade_icons)):
            if upgrade_unlocked[x] == True and upgrade_rect[x].collidepoint(mouse_x, mouse_y):
                touching_upgrade = x
                break
    else:
        shop_x += 0.2 * (-379 - shop_x)

    click_obj_size += 0.2 * (1 - click_obj_size)
    click_obj_image = pygame.transform.scale(click_obj_image, (trash_list_res[trash_list_index][0] * click_obj_size, trash_list_res[trash_list.index(source_clicker_image)][1] * click_obj_size))
    
    clicker_rotate = math.sin(timer/50) * 10
    click_obj_image = pygame.transform.rotozoom(click_obj_image, clicker_rotate, 1)

    click_obj_rect = click_obj_image.get_rect()
    click_obj_rect.topleft = (screen.get_width() / 2 - click_obj_image.width/2, screen.get_height() / 2- click_obj_image.height/2)

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    scoreText_surface = mainFont.render(str(score), True, "#C5E7F1")
    scoreText_rect = scoreText_surface.get_rect()
    scoreText_rect.center = (screen.get_width() - (5 + scoreText_rect.width/2), 35)

    amntGained_surface = subtitleFont.render(f"{str(amount_gained)}  s", True, "#C5E7F1")
    amntGained_rect = amntGained_surface.get_rect()
    amntGained_rect.center = (screen.get_width() - (5 + amntGained_rect.width/2), 35+amntGained_rect.height)

    screen.blit(bg_source, (bg_coords-67, bg_coords-67))

    if (bg_coords > 67):
        bg_coords = 0
    else:
        bg_coords += 0.5

    screen.blit(click_obj_image, (screen.get_width() / 2 - click_obj_image.width/2, screen.get_height() / 2- click_obj_image.height/2))

    screen.blit(shop_ui, (shop_x, 0))
    if (notif_active == True):
        screen.blit(notif_sym, (shop_x + shop_ui_rect.width - 30, screen.get_height()/2 - 70))

    for x in range(0, len(upgrade_icons)):
        if upgrade_unlocked[x] == True:
            screen.blit(upgrade_icons[x], ((shop_x + (114 * (modulate((x+1), 3) - 1))) + 10, ((math.ceil(3*((x+1)/9))-1) * 106) + 25))
            upgrade_rect[x] = upgrade_icons[x].get_rect()
            upgrade_rect[x].topleft = ((shop_x + (114 * (modulate((x+1), 3) - 1))) + 10, ((math.ceil(3*((x+1)/9))-1) * 106) + 25)
            if score >= round(upgrade_costs[x] * (1.15**upgrade_amounts[x])):
                upgrade_txtcost[x] = upgradeFont.render(str(round(upgrade_costs[x] * (1.15**upgrade_amounts[x]))), True, "#00FF2A")
            else:
                upgrade_txtcost[x] = upgradeFont.render(str(round(upgrade_costs[x] * (1.15**upgrade_amounts[x]))), True, "#FF0000")
            upgrade_txtcost_rect[x] = upgrade_txtcost[x].get_rect()
            upgrade_txtcost_rect[x].midright = ((shop_x + (114 * (modulate((x+1), 3) - 1))) + 112, ((math.ceil(3*((x+1)/9))-1) * 106) + 121)

            upgrade_txtamnt[x] = upgradeFont.render(f"x{str(upgrade_amounts[x])}", True, "#C5E7F1")
            upgrade_txtamnt_rect[x] = upgrade_txtamnt[x].get_rect()
            upgrade_txtamnt_rect[x].midleft = ((shop_x + (114 * (modulate((x+1), 3) - 1))) + 5, ((math.ceil(3*((x+1)/9))-1) * 106) + 121)

            screen.blit(upgrade_txtcost[x], upgrade_txtcost_rect[x])
            screen.blit(upgrade_txtamnt[x], upgrade_txtamnt_rect[x])

    screen.blit(scoreText_surface, scoreText_rect)
    screen.blit(amntGained_surface, amntGained_rect)
    screen.blit(gained_slash, (480-26, amntGained_rect.y+1))
    screen.blit(sym_image, (screen.get_width() - (sym_image.width + scoreText_rect.width + 10), sym_image.height/4))
    if touching_upgrade != -1:
        if modulate(touching_upgrade+1, 3) == 1:
            pygame.draw.rect(screen, "#397C9B", (mouse_x, mouse_y+20, 260, 100))
        elif modulate(touching_upgrade+1, 3) == 2:
            pygame.draw.rect(screen, "#397C9B", (mouse_x-100, mouse_y+20, 260, 100))
        elif modulate(touching_upgrade+1, 3) == 3:
            pygame.draw.rect(screen, "#397C9B", (mouse_x-200, mouse_y+20, 260, 100))
        y_offset = 0
        for x in range(0, len(up_descriptions[touching_upgrade])):
            upgrade_desc = descFont.render(str(up_descriptions[touching_upgrade][x]), True, "#B9E4FA")
            upgrade_desc_rect = upgrade_desc.get_rect()
            if modulate(touching_upgrade+1, 3) == 1:
                upgrade_desc_rect.topleft=(mouse_x+5, mouse_y+25+y_offset)
            elif modulate(touching_upgrade+1, 3) == 2:
                upgrade_desc_rect.topleft=(mouse_x-95, mouse_y+25+y_offset)
            elif modulate(touching_upgrade+1, 3) == 3:
                upgrade_desc_rect.topleft=(mouse_x-195, mouse_y+25+y_offset)
            screen.blit(upgrade_desc, upgrade_desc_rect)
            y_offset += 21

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()