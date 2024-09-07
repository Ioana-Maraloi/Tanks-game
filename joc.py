import sys
import time
import pygame
import pygame_menu
import math
pygame.init()
a = pygame.display.get_desktop_sizes()
screen_width = a[0][0]
screen_height = a[0][1]
screen_height -= 55
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.font.init()

# COLORS:
color_red = (255, 0, 0)
color_white = (255, 255, 255)
color_blue = (0, 0, 128)
color_lightblue = (0, 0, 255)
color_yellow = (255, 255, 0)
color_green = (0, 200, 0)
color_pink = (255, 192, 203)
color_purple = (160, 32, 240)
color_black = (0, 0, 0)
run = True

# calculating the coordonates so that the rectangle is in the middle:
rectangle_height = 600
rectangle_length = 1000
wall_thickness = 5
rectangle_y = (screen_height - rectangle_height) / 2
rectangle_x = (screen_width - rectangle_length) / 2
rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_length, rectangle_height)
# calculating the dimensions of the window that is displayed if someone wins
win_rectangle_length = screen_width / 4
win_rectangle_height = screen_height / 4
win_rectangle_x = screen_width / 2 - win_rectangle_length / 2
win_rectangle_y = screen_height / 2 - win_rectangle_height / 2
win_rectangle = pygame.Rect(win_rectangle_x, win_rectangle_y, win_rectangle_length, win_rectangle_height)
# calculating the x and y coordonates of the two tanks
tank1_x= rectangle_x + 70 + 75 / 2
tank1_y =rectangle_y + 500 + 75 / 2
tank2_x = rectangle_x + 900 + 75 / 2
tank2_y = rectangle_y + 70 + 75 / 2
# i declared a few fonts that will be used later
system_font = pygame.font.get_default_font()
fontBig = pygame.font.SysFont(system_font, 100, False, True)
fontMedium = pygame.font.SysFont(system_font, 50)
fontWinner = pygame.font.SysFont(system_font, 120, False, True)
fontItalic = pygame.font.SysFont(system_font, 70, False, True)
cool_font = pygame_menu.font.FONT_DIGITAL
player1_name = ""
player2_name = ""
def set_name1(value):
    global player1_name
    player1_name = value
def set_name2(value):
    global player2_name
    player2_name = value
def winning_function(color, whole_game):
    # if one of the tanks collides with a ball, the opponend wins
    # and a rectangle that says who wins is displayed
    global player1_name, player2_name
    pygame.draw.rect(screen, color, win_rectangle)
    # the second player is defined bt the color red and the first player by light blue
    if color == color_red:
        player2_rend = fontWinner.render(player2_name, True, color_white, None)
        x_position = win_rectangle_x + win_rectangle_length / 2 - len(player2_name) * 22
        screen.blit(player2_rend, (x_position, win_rectangle_y, win_rectangle_length, win_rectangle_height))
    elif color == color_lightblue:
        player1_rend = fontWinner.render(player1_name, True, color_white, None)
        x_position = win_rectangle_x + win_rectangle_length / 2 - len(player1_name) * 22
        screen.blit(player1_rend, (x_position , win_rectangle_y, win_rectangle_length, win_rectangle_height))
    # if no one got to 10 points, the game continues until someone reaches 10
    # if someone got to 10 points, that person wins the whole game
    if whole_game == False:
        wins_rend = fontBig.render("wins!", True, color_white, None)
        wins_x_pos = win_rectangle_x  + win_rectangle_length / 2 - len("wins!") * 18
        screen.blit(wins_rend, (wins_x_pos, win_rectangle_y + win_rectangle_height / 2, win_rectangle_length, win_rectangle_height // 2))
    else:
        wins_rend2 = fontItalic.render("wins the game!", True, color_white, None)
        wins_x_pos = win_rectangle_x + 10
        screen.blit(wins_rend2, (wins_x_pos, win_rectangle_y + win_rectangle_height / 2, win_rectangle_length, win_rectangle_height // 2))
# loading the pictures of the tanks and making them smaller
blue_tank = pygame.image.load("blue_tank.png")
red_tank = pygame.image.load("red_tank.png")
blue_tank = pygame.transform.scale(blue_tank, (50, 75))
red_tank = pygame.transform.scale(red_tank, (50, 75))
tank1 = pygame.transform.rotate(blue_tank, angle = 0)
# adding awesome arcade music in the background
awesome_sound = pygame.mixer.music.load("retro_music.mp3")
pygame.mixer.music.play()

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, angle):
        super().__init__()
        self.color = color
        self.angle = 0
        self.image = pygame.Surface([100, 100])
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x, self.y))
        if color == "blue":
            self.pic = pygame.transform.rotate(blue_tank, angle)
        elif color == "red":
            self.pic = pygame.transform.rotate(red_tank, angle)
    def update(self):
        if self.color == "blue":
            self.pic = pygame.transform.rotate(blue_tank, self.angle)
            self.rect = self.pic.get_rect(center = (self.x, self.y))
        if self.color == "red":
            self.pic = pygame.transform.rotate(red_tank, self.angle)
            self.rect = self.pic.get_rect(center = (self.x, self.y))
    def move_up(self):
        # if the angle is a multiple of pi/4, i move the tank directly
        # else, i calcultate sin and cos and update the x an y coordonates
        if self.angle == 0:
            self.y -= 0.5
        elif self.angle == 180:
            self.y += 0.5
        elif self.angle == 90:
            self.x -= 0.5   
        elif self.angle == 270:
            self.x += 0.5
        else:
            angle_radians = math.radians(self.angle)
            hypotenuse = 0.5
            sinus = abs(math.sin(angle_radians))
            cosinus = abs(math.cos(angle_radians))
            x_modif = sinus * hypotenuse
            y_modif = cosinus * hypotenuse
            # upper left (first quadrant):
            if self.angle > 0 and self.angle < 90:
                self.x -= x_modif
                self.y -= y_modif
            # lower left (second quadrant):
            elif self.angle > 90 and self.angle < 180:
                self.x -= x_modif 
                self.y += y_modif
            # lower right (third quadrant):
            elif self.angle > 180 and self.angle < 270:
                self.x += x_modif 
                self.y += y_modif
            # upper right (fourth quadrant):
            elif self.angle > 270 and self.angle < 360:
                self.x += x_modif
                self.y -= y_modif
    def move_down(self):
        # if the angle is a multiple of pi/4, i move the tank directly
        # else, i calcultate sin and cos and update the x an y coordonates
        if self.angle == 0:
            self.y += 0.5
        elif self.angle == 180:
            self.y -= 0.5
        elif self.angle == 90:
            self.x += 0.5   
        elif self.angle == 270:
            self.x -= 0.5
        else:
            angle_radians = math.radians(self.angle)
            hypotenuse = 0.5
            sinus = abs(math.sin(angle_radians))
            cosinus = abs(math.cos(angle_radians))
            x_modif = sinus * hypotenuse
            y_modif = cosinus * hypotenuse
            # upper left (first quadrant):
            if self.angle > 0 and self.angle < 90:
                self.x += x_modif
                self.y += y_modif
            # lower left (second quadrant):
            elif self.angle > 90 and self.angle < 180:
                self.x += x_modif 
                self.y -= y_modif
            # lower right (third quadrant):
            elif self.angle > 180 and self.angle < 270:
                self.x -= x_modif 
                self.y -= y_modif
            # upper right (fourth quadrant):
            elif self.angle > 270 and self.angle < 360:
                self.x -= x_modif
                self.y += y_modif
    def check_move_up(self):
        normal_move = True
        copy_x = self.x
        copy_y = self.y
        # before i make the move, i need to check if the tank will colide with any 
        # vertical/horizontal wall
        for vertical_wall in Vertical_Walls_group:
            coord_wall = vertical_wall.rect.center
            coord_x = coord_wall[0]
            coord_y = coord_wall[1]
            coord_top = vertical_wall.rect.midtop
            coord_top_y = coord_top[1]
            coord_bottom = vertical_wall.rect.midbottom
            coord_bottom_y = coord_bottom[1]
            # if the tank hits the wall on the long side,
            # i check the angle and the tank moves a little further away from the wall
            if self.y - 30 < coord_bottom_y and self.y + 30 > coord_top_y:
                if self.angle >= 0 and self.angle < 90:
                    if abs(self.x - 30 - coord_x) < 5:
                        self.x += 2
                        normal_move = False
                elif self.angle >= 90 and self.angle < 180:
                    if abs(self.x - 30 - coord_x) < 5:
                        self.x += 2
                        normal_move = False
                elif self.angle >= 180 and self.angle < 270:
                    if abs(self.x + 30 - coord_x) < 5:
                        self. x -= 2
                        normal_move = False
                elif self.angle >= 270 and self.angle < 360:
                    if abs(self.x + 30 - coord_x) < 5:
                        self.x -= 2
                        normal_move = False
            else:
                # if the tank is very close to the edge of a wall,
                # i check the angle and the tank moves a little further away from the small side
                if math.dist((self.x, self.y), (coord_bottom[0], 
                                                coord_bottom[1])) < 40 or math.dist((self.x, self.y), (coord_top[0], coord_top[1])) < 40:
                    normal_move = False
                    if self.angle >= 0 and self.angle < 90:
                        self.x = copy_x + 1
                        self.y = copy_y + 1
                    elif self.angle >= 90 and self.angle < 180:
                        self.x = copy_x + 1
                        self.y = copy_y - 1
                    elif self.angle >= 180 and self.angle < 270:
                        self.x = copy_x - 1
                        self.y = copy_y - 1
                    elif self.angle >= 270 and self.angle < 360:
                        self.x = copy_x - 1
                        self.y = copy_y + 1
        # i will check if the tank collides with a horizontal wall in a similar way as
        # i checked with a vertical wall
        for horizontal_wall in Horizontal_Walls_group:
            coord_wall = horizontal_wall.rect.center
            coord_y = coord_wall[1]
            coord_left = horizontal_wall.rect.midleft
            coord_left_x = coord_left[0]
            coord_right = horizontal_wall.rect.midright
            coord_right_x = coord_right[0]
            if self.x - 30 < coord_right_x and self.x + 30 > coord_left_x:
                # if the angle is upwards ( first or fourth quadrant)
                if self.angle >= 0 and self.angle < 90:
                    if abs(self.y - 30 - coord_y) < 5:
                        self.y += 2
                        normal_move = False
                elif self.angle > 270 and self.angle < 360:
                    if abs(self.y - 30 - coord_y) < 5:
                        self.y += 2
                        normal_move = False
                # if the angle is downwards ( second or third quadrant)
                elif self.angle >= 90 and self.angle < 180:
                    if abs(self.y + 30 - coord_y) < 5:
                        self.y -= 2
                        normal_move = False
                elif self.angle > 180 and self.angle < 270:
                    if abs(self.y + 30 - coord_y) < 5:
                        self.y -= 2
                        normal_move = False
            else:
                if math.dist((self.x, self.y), (coord_left[0], coord_left[1])) < 40 or math.dist((self.x, self.y), (coord_right[0], coord_right[1])) < 40:
                    normal_move = False
                    if self.angle >= 0 and self.angle < 90:
                        self.x = copy_x + 1
                        self.y = copy_y + 1
                    elif self.angle >= 90 and self.angle < 180:
                        self.x = copy_x + 1
                        self.y = copy_y - 1
                    elif self.angle >= 180 and self.angle < 270:
                        self.x = copy_x - 1
                        self.y = copy_y - 1
                    elif self.angle >= 270 and self.angle < 360:
                        self.x = copy_x - 1
                        self.y = copy_y + 1
        # if the tank didn`t meet any wall, normal_move = true and a 
        # simple move will be executed
        if normal_move:
            self.move_up()
    def check_move_down(self):
        # when the tank goes backwards, i still need to check if it hits any walls
        # i will check in a simmilar way as i checked for moving forwards
        normal_move = True
        copy_x = self.x
        copy_y = self.y
        for vertical_wall in Vertical_Walls_group:
            coord_wall = vertical_wall.rect.center
            coord_x = coord_wall[0]
            coord_top = vertical_wall.rect.midtop
            coord_top_y = coord_top[1]
            coord_bottom = vertical_wall.rect.midbottom
            coord_bottom_y = coord_bottom[1]
            if self.y - 30 < coord_bottom_y and self.y + 30 > coord_top_y:
                if self.angle >= 0 and self.angle < 90:
                    if abs(self.x + 30 - coord_x) < 5:
                        self.x -= 2
                        normal_move = False             
                elif self.angle > 90 and self.angle < 180:
                    if abs(self.x + 30 - coord_x) < 5:
                        self.x -= 2
                        normal_move = False
                elif self.angle > 180 and self.angle < 270:
                    if abs( self.x - 30 - coord_x) < 5: 
                        self. x += 2 
                        normal_move = False     
                elif self.angle > 270 and self.angle < 360:
                    if abs( self.x - 30 - coord_x) < 5: 
                        self.x += 2
                        normal_move = False
            else:
                if math.dist((self.x, self.y), (coord_bottom[0], coord_bottom[1])) < 40 or math.dist((self.x, self.y), (coord_top[0], coord_top[1])) < 40:
                    normal_move = False
                    if self.angle >= 0 and self.angle < 90:
                        self.x = copy_x - 1
                        self.y = copy_y - 1
                    elif self.angle >= 90 and self.angle < 180:
                        self.x = copy_x - 1
                        self.y = copy_y + 1
                    elif self.angle >= 180 and self.angle < 270:
                        self.x = copy_x + 1
                        self.y = copy_y + 1
                    elif self.angle >= 270 and self.angle < 360:
                        self.x = copy_x + 1
                        self.y = copy_y - 1
        for horizontal_wall in Horizontal_Walls_group:
            coord_wall = horizontal_wall.rect.center
            coord_y = coord_wall[1]
            coord_left = horizontal_wall.rect.midleft
            coord_left_x = coord_left[0]
            coord_right = horizontal_wall.rect.midright
            coord_right_x = coord_right[0]
            if self.x - 30 < coord_right_x and self.x + 30 > coord_left_x:
                # if the angle is upwards ( first or fourth quadrant)
                if self.angle >= 0 and self.angle < 90:
                    if abs(self.y + 35 - coord_y) < 5:
                        self.y -= 2
                        normal_move = False
                elif self.angle >= 270 and self.angle < 360:
                    if abs(self.y + 35 - coord_y) < 5:
                        self.y -= 2
                        normal_move = False
                # if the angle is downwards ( second or third quadrant)
                elif self.angle >= 90 and self.angle < 180:
                    if abs(self.y - 35 - coord_y) < 5:
                        self.y += 2
                        normal_move = False
                elif self.angle >= 180 and self.angle < 270:
                    if abs(self.y - 35 - coord_y) < 5:
                        self.y += 2
                        normal_move = False
            else:
                if math.dist((self.x, self.y), (coord_left[0], coord_left[1])) < 40 or math.dist((self.x, self.y), (coord_right[0], coord_right[1])) < 40:
                    normal_move = False
                    if self.angle >= 0 and self.angle < 90:
                        self.x = copy_x - 1
                        self.y = copy_y - 1
                    elif self.angle >= 90 and self.angle < 180:
                        self.x = copy_x - 1
                        self.y = copy_y + 1
                    elif self.angle >= 180 and self.angle < 270:
                        self.x = copy_x + 1
                        self.y = copy_y + 1
                    elif self.angle >= 270 and self.angle < 360:
                        self.x = copy_x + 1
                        self.y = copy_y - 1
        if normal_move:
            self.move_down()
tank1 = Tank(tank1_x, tank1_y, "blue", 0)
tank2= Tank(tank2_x, tank2_y, "red", 0)
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, color):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color_white)
        self.image.set_colorkey(color_white)
        self.direction = direction
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.birth = time.time()
        self.rect = self.image.get_rect( center = (pos_x, pos_y))
        pygame.draw.circle(self.image, color_pink, (10, 10), radius = 3, width = 3)
    def update(self):
        global tank1
        global tank2
        global player1_score, player2_score
        for vertical_wall in Vertical_Walls_group:
                coord_wall = vertical_wall.rect.center
                coord_x = coord_wall[0]
                coord_top = vertical_wall.rect.midtop
                coord_top_y = coord_top[1]
                coord_bottom = vertical_wall.rect.midbottom
                coord_bottom_y = coord_bottom[1]
                if self.pos_y < coord_bottom_y and self.pos_y > coord_top_y:
                    if abs(self.pos_x - coord_x) < 10:
                        if self.direction == 90:
                            self.direction = 270
                        elif self.direction == 270:
                            self.direction = 90
                        else:
                            self.direction = 360 - self.direction
            # if a ball collides with a horizontal wall
        for horizontal_wall in Horizontal_Walls_group:
                coord_wall = horizontal_wall.rect.center
                coord_y = coord_wall[1]
                coord_left = horizontal_wall.rect.midleft
                coord_left_x = coord_left[0]
                coord_right = horizontal_wall.rect.midright
                coord_right_x = coord_right[0]
                if self.pos_x > coord_left_x and self.pos_x < coord_right_x:
                    if abs(self.pos_y - coord_y) < 10: 
                        # first and second quadrant
                        if self.direction >= 0 and self.direction < 180:
                            self.direction = 180 - self.direction
                        # third quadrant
                        elif self.direction >= 180 and self.direction < 270:
                            reduction = self.direction - 180
                            self.direction = 360 - reduction
                        # fourth quadrant
                        elif self.direction >= 270 and self.direction <= 360:
                            reduction = self.direction - 270
                            self.direction = 180 + 90 - reduction
        if time.time() - self.birth > 1:
            if math.dist((self.pos_x, self.pos_y), (tank1.x, tank1.y)) < 30:
                self.kill()
                Ball_group.empty()
                tank1.kill()
                player2_score += 1
                if player2_score >= 10:
                    winning_function(color_red, True)
                else:
                    winning_function(color_red, False)
            if math.dist((self.pos_x, self.pos_y), (tank2.x, tank2.y)) < 30:
                self.kill()
                Ball_group.empty()
                tank2.kill()
                player1_score += 1
                if player1_score >= 10:
                    winning_function(color_lightblue, True)
                else:
                    winning_function(color_lightblue, False)
        if self.direction == 0:
            self.pos_y -= 0.5
        elif self.direction == 180:
            self.pos_y += 0.5
        elif self.direction == 90:
            self.pos_x -= 0.5
        elif self.direction == 270:
            self.pos_x += 0.5
        else:
            change_x = abs(math.sin(math.radians(self.direction)) / 2)
            change_y = abs(math.cos(math.radians(self.direction)) / 2)
            if self.direction > 0 and self.direction < 90:
                self.pos_x -= change_x
                self.pos_y -= change_y
            if self.direction > 90 and self.direction < 180:
                self.pos_x -= change_x
                self.pos_y += change_y
            if self.direction > 180 and self.direction < 270:
                self.pos_x += change_x
                self.pos_y += change_y
            if self.direction > 270 and self.direction < 360:
                self.pos_x += change_x
                self.pos_y -= change_y
        self.rect = self.image.get_rect( center = (self.pos_x, self.pos_y))
        pygame.draw.circle(self.image, color_pink, (10, 10), radius = 3, width = 3)
    def delete(self):
        if time.time() - self.birth > 5.0:
            self.kill()
         
class Vertical_Walls(pygame.sprite.Sprite):
    def __init__(self, length, color, x, y):
        super().__init__()
        self.image = pygame.Surface((wall_thickness, length))
        self.image.fill(color)
        if color == color_white:
            self.image.set_colorkey(color_white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Horizontal_Walls(pygame.sprite.Sprite):
    def __init__(self, length, color, x, y):
        super().__init__()
        self.image = pygame.Surface((length, wall_thickness))
        self.image.fill(color)
        if color == color_white:
            self.image.set_colorkey(color_white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
# defining the borders of the map
upper_wall = Horizontal_Walls( rectangle_length, color_white, rectangle_x, rectangle_y + 50)
lower_wall = Horizontal_Walls(rectangle_length, color_white, rectangle_x, rectangle_y + rectangle_height)
left_wall = Vertical_Walls(rectangle_height - 50, color_white, rectangle_x, rectangle_y + 55)
right_wall = Vertical_Walls(rectangle_height - 50, color_white, rectangle_x + rectangle_length - 5, rectangle_y + 50)
# additional walls to create a maze
middle_1_height = (rectangle_height - 250) / 3
middle_x = rectangle_x + rectangle_length / 2
middle_wall_1 = Vertical_Walls(middle_1_height, color_black, middle_x, rectangle_y + 50)
middle_2_y = rectangle_y + middle_1_height + 150
middle_wall_2 = Vertical_Walls(middle_1_height, color_black, middle_x, middle_2_y)
middle_3_y = rectangle_y + 2 * middle_1_height + 250
middle_wall_3 = Vertical_Walls(middle_1_height, color_black, middle_x, middle_3_y)
wall1_y = rectangle_y + 4 * rectangle_height / 5
# blue side
hwall_blue_1 = Horizontal_Walls(rectangle_length / 4, color_black, rectangle_x, wall1_y)
vwall_1x = rectangle_x + rectangle_length / 3 + 50
vwall_blue_1 = Vertical_Walls(rectangle_height / 3, color_black, vwall_1x, wall1_y - 80)
wall_vert_y = wall1_y - 150
vwall_blue_2 = Vertical_Walls(150, color_black, rectangle_x + 100, wall_vert_y)
vwall_blue_3 = Horizontal_Walls(100, color_black, rectangle_x + 200, wall_vert_y + 50)
vwall_blue_rect1 = Vertical_Walls(50, color_black, rectangle_x + 295, wall_vert_y )
vwall_blue_rect2 = Vertical_Walls(50, color_black, rectangle_x + 200, wall_vert_y )
hwall_blue_rect1 = Horizontal_Walls(100, color_black, rectangle_x + 200, wall_vert_y)
hwall_blue_rect2 = Horizontal_Walls(100, color_black, rectangle_x, rectangle_y + 50 + middle_1_height)
middle_left = rectangle_x + rectangle_length / 4
middle_x = rectangle_x + rectangle_length / 2
middle_y = rectangle_y + rectangle_height / 2
hwall_blue_2 = Horizontal_Walls(104, color_black, middle_x - 100, rectangle_y + 50 + middle_1_height)
vwall_blue_4 = Vertical_Walls(180, color_black, middle_left - 50, rectangle_y + 50)
vwall_blue_5= Vertical_Walls(100, color_black, middle_x - 100, rectangle_y + 50 + middle_1_height)
hwall_blue_3 = Horizontal_Walls(100, color_black, rectangle_x + 150, middle_y - 70)
vwall_blue_6 = Vertical_Walls(50, color_black, middle_left + 100, rectangle_y + 50)
# red side
wall_2_y = rectangle_y + rectangle_height / 5 + 50
wall_2_x = middle_x + 100
hwall_red_1 = Horizontal_Walls(rectangle_length / 5, color_black, wall_2_x, wall_2_y)
hwall_red_2 = Horizontal_Walls(100, color_black, wall_2_x + 100 + rectangle_length / 5, wall_2_y)
wall_2vert_y = rectangle_y + 50
vwall_red_1 = Vertical_Walls(rectangle_height / 3, color_black, middle_x + 100, wall_2vert_y)
vwall_red_2 = Vertical_Walls(100, color_black, wall_2_x + rectangle_length / 5 + 100, wall_2_y)
hwall_red_3 = Horizontal_Walls(100, color_black, wall_2_x + 100 + rectangle_length / 5, wall_2_y + 100)
hwall_red_4 = Horizontal_Walls(80, color_black, wall_2_x + 120, wall_2_y + 100)
hwall_red_5 = Horizontal_Walls(rectangle_length / 4, color_black, middle_x, wall1_y)
hwall_red_6 = Horizontal_Walls(150, color_black, wall_2_x, middle_y + 100)
vwall_red_3 = Vertical_Walls(200, color_black, wall_2_x + rectangle_length / 5 + 60, rectangle_y + rectangle_height - 200 )
hwall_red_7 = Horizontal_Walls(50, color_black, rectangle_x + rectangle_length - 50, rectangle_y + rectangle_height - 200)
vwall_red_4 = Vertical_Walls(60, color_black, wall_2_x + 50, middle_y + 40)
vwall_red_5 = Vertical_Walls(50, color_black, wall_2_x + 200, wall_2_y + 100)
Vertical_Walls_group = pygame.sprite.Group()
Vertical_Walls_group.add(right_wall, left_wall)
Horizontal_Walls_group = pygame.sprite.Group()
Vertical_Walls_group.add(middle_wall_1, middle_wall_2, middle_wall_3)
Horizontal_Walls_group.add(upper_wall, lower_wall)
# additional walls:
# walls on the blue side:
Horizontal_Walls_group.add(hwall_blue_1, hwall_blue_2, hwall_blue_3)
Vertical_Walls_group.add(vwall_blue_1, vwall_blue_2, vwall_blue_3)
Vertical_Walls_group.add(vwall_blue_4, vwall_blue_5, vwall_blue_6)
Vertical_Walls_group.add(vwall_blue_rect1, vwall_blue_rect2)
Horizontal_Walls_group.add(hwall_blue_rect1, hwall_blue_rect2)
# red side:
Horizontal_Walls_group.add(hwall_red_1, hwall_red_2, hwall_red_3)
Horizontal_Walls_group.add(hwall_red_4, hwall_red_5, hwall_red_6, hwall_red_7)
Vertical_Walls_group.add(vwall_red_1, vwall_red_2, vwall_red_3)
Vertical_Walls_group.add(vwall_red_4, vwall_red_5)

player1_score = 0
player2_score = 0
Ball_group = pygame.sprite.Group()
def game(ratio_1, ratio_2):
    global player1_score, player2_score
    global tank1_x, tank1_y, tank2_x, tank2_y, rectangle_x, rectangle_y
    run = True
    clock = pygame.time.Clock()
    tank1 = Tank(tank1_x, tank1_y, "blue", 0)
    tank2= Tank(tank2_x, tank2_y, "red", 0)
    Tanks_group = pygame.sprite.Group()
    Tanks_group.add(tank1)
    Tanks_group.add(tank2)
    while run:
        copy_tank1_x = tank1.x
        copy_tank1_y = tank1.y
        copy_tank2_x = tank2.x
        copy_tank2_y = tank2.y
        copy_score1 = player1_score
        copy_score2 = player2_score
        screen.fill(color_black)
        pygame.draw.rect(screen, color_white, rectangle)
        screen.fill(color_white, rectangle)
        # the rectangles where the score is displayed
        # the dimensions of the rectangles are calculated in the match function (atios)
        rectangle_score1 = pygame.Rect(rectangle_x, rectangle_y, ratio_1 , 50)
        rectangle_score2 = pygame.Rect(rectangle_x + ratio_1, rectangle_y, ratio_2, 50)
        pygame.draw.rect(screen, color_lightblue, rectangle_score1)
        pygame.draw.rect(screen, color_red, rectangle_score2)
        # the name of the game and of the players are 
        # displayed at the top of the rectangle 
        title = fontMedium.render("tanks", True, color_white, None)
        player1 = fontMedium.render(player1_name, True, color_white, None)
        player2 = fontMedium.render(player2_name, True, color_white, None)
        # as well as the score of each player
        score1 = str(player1_score)
        score2 = str(player2_score)
        score1_rend = fontMedium.render(score1, True, color_white, None)
        score2_rend = fontMedium.render(score2, True, color_white, None)
        # the first player`s name and score will be displayed in the left side of the rectangle
        # while the second`s is in the right side
        screen.blit(title, (rectangle_x + rectangle_length/2 - 40, rectangle_y))
        screen.blit(player1, rectangle_score1)
        screen.blit(score1_rend, (rectangle_x + len(player1_name) * 25, rectangle_y))
        screen.blit(score2_rend, (rectangle_x + rectangle_length - len(player2_name) * 25 - 30, rectangle_y))
        screen.blit(player2, (rectangle_x + rectangle_length - len(player2_name) * 25, rectangle_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player1_score = -1
                run = False
        keys = pygame.key.get_pressed()
        # moves for the red tank (tank number 2):
        # the second tank is moved by the arrow keys
        if keys[pygame.K_UP]:
            tank2.check_move_up()
        if keys[pygame.K_DOWN]:
            tank2.check_move_down()
        if keys[pygame.K_RIGHT]:
            tank2.angle -= 1
        if keys[pygame.K_LEFT]:
            tank2.angle += 1
        if keys[pygame.K_SPACE]:
            ball = Ball(tank2.x, tank2.y, tank2.angle, color_blue)
            Ball_group.add(ball)
        # moves for the blue tank (tank number 1):
        # the first tank is moved by the wasd keys
        if keys[pygame.K_w]:
            tank1.check_move_up()
        if keys[pygame.K_s]:
            tank1.check_move_down()
        if keys[pygame.K_d]:
            tank1.angle -= 1
        if keys[pygame.K_a]:
            tank1.angle += 1
        if keys[pygame.K_t]:
            ball = Ball(tank1.x, tank1.y, tank1.angle, color_blue)
            Ball_group.add(ball)
        if keys[pygame.K_ESCAPE]:
            run = False
            player1_score = -1
        # making sure the angles remain in [0, 360)
        if tank1.angle >= 360:
          tank1.angle %= 360
        if tank1.angle < 0:
            tank1.angle = 360 + tank1.angle
        if tank2.angle >= 360:
            tank2.angle %= 360
        if tank2.angle < 0:
            tank2.angle = 360 + tank2.angle
        # if the tanks get too close 
        if math.dist((tank1.x, tank1.y), (tank2.x, tank2.y)) < 70:
            tank1.x = copy_tank1_x - 0.1
            tank1.y = copy_tank1_y - 0.1
            tank2.x = copy_tank2_x - 0.1
            tank2.y = copy_tank2_y - 0.1
            tank1.rect = tank1.pic.get_rect(center = (tank1.x, tank1.y))
            tank2.rect = tank2.pic.get_rect(center = (tank2.x, tank2.y))
        # updating and drawing the walls, tanks and balls
        Vertical_Walls_group.draw(screen)
        Horizontal_Walls_group.draw(screen)
        for ball in Ball_group:
            ball.delete()
        Tanks_group.update()
        Ball_group.update()
        Ball_group.draw(screen)
        if copy_score1 == player1_score and copy_score2 == player2_score:
            run =True
        else:
            run = False
            if player1_score - copy_score1 > 1:
                player1_score = copy_score1 + 1
            if player2_score - copy_score2 > 1:
                player2_score = copy_score2 + 1
        # displaying the pictures of the tanks
        if run == True:
            screen.blit(tank1.pic, tank1.rect)
            screen.blit(tank2.pic, tank2.rect)
        pygame.display.update()
        clock.tick(250)
    # if someone wins, the winning rectangle will be displayed for 2 seconds before
    # the game continues
    time.sleep(2)
def match():
    global player1_score
    global player2_score
    run = True
    ratio_1 = ratio_2 = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # if the the players have the same score, the top bar will be half blue, half red
        if player1_score == player2_score:
            ratio_1 = 1/2 * rectangle_length
            ratio_2 = 1/2 * rectangle_length
        # if a player didn`t score yet, the top bar will be displayed in the color of the opponent
        elif player1_score == 0 and player2_score != 0:
            ratio_1 = 0
            ratio_2 = rectangle_length
        elif player2_score == 0 and player1_score != 0:
            ratio_1 = rectangle_length
            ratio_2 = 0
        else:
        # else, i calculate the proportions and the lengths of those two rectangles
            total = player1_score + player2_score
            ratio_1 = player1_score * rectangle_length / total
            ratio_2 = player2_score * rectangle_length / total
        game(ratio_1, ratio_2)
        if player1_score == -1:
            run = False
        if player1_score >= 10:
            run = False
        if player2_score >= 10:
            run = False
    time.sleep(2)
def loading_menu():
    loading_menu = pygame_menu.Menu("TANKS", 1000, 600, True, 
                                    theme = pygame_menu.themes.THEME_BLUE)
    bara = loading_menu.add.progress_bar("loading", default = 0, 
                                         font_color = color_black, font_name = cool_font, 
                                         progress_text_align = pygame_menu.locals.ALIGN_CENTER,
                                         progress_text_font_color = color_black)
    start_time = pygame.time.get_ticks()
    duration = 2000
    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        progress = min(100, (elapsed_time / duration) * 100)
        bara.set_value(progress)
        loading_menu.update(pygame.event.get())
        loading_menu.draw(screen)
        pygame.display.flip()
        if elapsed_time >= duration:
            break
    bara.set_value(100)
    loading_menu.add.button("start game!", match, font_name = cool_font)
    loading_menu.add.button("undo", start_the_game, font_name = cool_font)
    loading_menu.mainloop(screen)  
def start_the_game():
    # a menu for introducing the names of the players
    start_menu = pygame_menu.Menu("players:", 1000, 600, True, 
                                  theme = pygame_menu.themes.THEME_BLUE, 
                                  rows = 3, columns = 3)
    # getting the names of the first player
    start_menu.add.text_input("player 1:", maxchar= 7, maxwidth=20, onchange= set_name1,
                              font_name = cool_font, font_size = 20)
    image_path_wasd = "wasd_keyboard.png"
    start_menu.add.image(image_path=image_path_wasd, scale=(0.5, 0.5))
    start_menu.add.none_widget()
    start_menu.add.none_widget()    
    tank_picture = "tank.png"
    start_menu.add.image(image_path=tank_picture, scale = (0.25, 0.25))
    start_menu.add.button("done!",loading_menu, font_name = cool_font, font_size = 20)
    # getting the name of the second player
    start_menu.add.text_input("player 2:", maxchar=7, maxwidth=20, onchange=set_name2,
                              font_name = cool_font, font_size = 20)
    image_path_arrows = "keyboard.png"
    start_menu.add.image(image_path=image_path_arrows, scale = (0.5, 0.5))
    start_menu.mainloop(screen)
def explain_rules():
    # a menu for explaining the rules and for credits for the pictures   
    rules_menu = pygame_menu.Menu("rules", 1000, 600, True, theme = pygame_menu.themes.THEME_SOLARIZED)
    rules_menu.add.label("the first player controls the blue tank with the wasd keys", 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_lightblue, font_size = 30)
    rules_menu.add.label("the second player controls the red tank with the arrow keys",
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_lightblue, font_size = 30)
    rules_menu.add.label('they shoot using the "t" and space key', 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_lightblue, font_size = 30)
    rules_menu.add.label("the balls bounce of the walls and dissapear after 5 seconds ", 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_lightblue, font_size = 30)
    rules_menu.add.label("first one to kill the other player 10 times wins!!", 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_lightblue, font_size = 30)
    rules_menu.add.label('credits for the pictures: "https://www.flaticon.com/free-icons/soldier"', 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_blue, font_size = 20)
    rules_menu.add.label("tank icons created by Marz Gallery - Flaticon", 
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_blue, font_size = 20)
    rules_menu.add.label('"https://www.flaticon.com/free-icons/wasd" Wasd icons created by Freepik-Flaticon',
                         align = pygame_menu.locals.ALIGN_CENTER, font_color = color_blue, font_size = 20,
                         underline = True)
    rules_menu.add.button("return to main menu", main_menu)
    rules_menu.mainloop(screen)
def main_menu():
    menu = pygame_menu.Menu("welcome", 1000, 600, True, theme = pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label("Tanks", font_size = 100, font_color = color_blue, font_name = cool_font)
    menu.add.label("made by Ioana Maraloi", font_size = 20, font_color = color_lightblue, font_name = cool_font)
    menu.add.none_widget()
    menu.add.button('play', start_the_game, font_name = cool_font)
    menu.add.button('explain rules', explain_rules, font_name = cool_font)
    menu.add.button('quit', pygame_menu.events.EXIT, font_name = cool_font)
    menu.mainloop(screen)
main_menu()
pygame.font.quit()
pygame.quit()