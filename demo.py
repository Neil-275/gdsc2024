import pygame
import random
import math

pygame.init()

maxW,maxH=900,720   
screen= pygame.display.set_mode((maxW,maxH))

pygame.display.set_caption("demo")
# icon= pygame.image.load('img/logo.png')
# pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf',28)
fontI= pygame.font.Font('freesansbold.ttf',24)

#background
background=pygame.image.load("rsrc/intersection.jpeg")
background= pygame.transform.scale(background, (maxW, maxH))
light_img= pygame.image.load("rsrc/light.png")
light_img= pygame.transform.scale(light_img,(60,90))
red_img=  pygame.image.load("rsrc/red.png")
red_img= pygame.transform.scale(red_img,(35,30))
green_img= pygame.image.load("rsrc/green.png")
green_img= pygame.transform.scale(green_img,(30,32))

n_xemay=3
n_xehoi=2
n_xetai=1
xe_img=[[],[],[]]

for i in range(0,n_xemay):
    tmp= pygame.image.load(f"rsrc/xemay_{i}.png")
    xe_img[0].append(pygame.transform.scale(tmp, (32,40)))
for i in range(0,n_xehoi):
    tmp=pygame.image.load(f"rsrc/xehoi_{i}.png")
    xe_img[1].append(pygame.transform.scale(tmp, (40,69)))
for i in range(0,n_xetai):
    tmp= pygame.image.load(f"rsrc/xetai_{i}.png")
    xe_img[2].append(pygame.transform.scale(tmp, (42,100)))


light_pos=[[322,598,527,266],[111,154,545,473]]
count_pos=[[350,627,556,294],[177,220,610,536]]
color_pos=[[335,611,541,278],[125,169,559,487]]
#Timer
start_time = pygame.time.get_ticks()
current_time = 0
countdown_duration=4
cur_light_id=3

def updateDisplay(State,x,y):
    screen.blit(State,(x,y))

class Light:
    def __init__(self) -> None:
        self.time=0
        self.id=0
        self.countdown_second=countdown_duration
    def displayCountdown(self,id): #id= 0:4
        global cur_light_id,countdown_duration
        if (cur_light_id==id):
            self.countdown_second = (countdown_duration * 1000 - current_time) // 1000
            if self.countdown_second <= 0:
                self.countdown_second = 0
                res=calGST()
                print(res)
                cur_light_id= (cur_light_id+1)%4
                countdown_duration+=res
                self.countdown_second=countdown_duration
            countdown_text = font.render(str(self.countdown_second), True, (250,250,250))
            updateDisplay(green_img,color_pos[0][id],color_pos[1][id])
        else:
             countdown_text = font.render("--", True, (250,250,250))
             updateDisplay(red_img,color_pos[0][id],color_pos[1][id])
        text_rect = countdown_text.get_rect(center=(count_pos[0][id],count_pos[1][id]))
        screen.blit(countdown_text, text_rect)

di=[[0,-1,0,1],[1,0,-1,0]]
next_coming_lane=[0,0,0,0]
starting_point=[[[380,418],[1150,1150],[458,496],[-150,-150]],[[-150,-150],[243,300],[900,900],[366,424]]]
stopline=[[383,595,524,312],[134,243,580,476]]
angle=[180,90,0,-90]
number_of_lanes=4

def calGST():
    global vehicles
    res=0
    for vehicle in vehicles:
        if ((cur_light_id+1)%4 == vehicle.direction):
            res+= vehicle.type*(vehicle.velocity+1)
    res=int(res/number_of_lanes)+3
    print(res)
    return min(99,res)

class Vehicle:
    def __init__(self,i,direction):
        self.img=pygame.transform.rotate(xe_img[i][0],angle[direction])
        self.type=i #0,1,2
        self.velocity=0.3
        self.direction=direction
        self.x=0
        self.y=0
        
    def run():
        for vehicle in vehicles:
            
            if vehicle.direction == cur_light_id:
                vehicle.x+= vehicle.velocity*di[0][vehicle.direction]
                vehicle.y+= vehicle.velocity*di[1][vehicle.direction]
            
            if ((vehicle.direction==0 and (vehicle.y+vehicle.img.get_height()<= stopline[1][0]-10 or vehicle.y+vehicle.img.get_height() > stopline[1][0]+10))\
                or (vehicle.direction==1 and (vehicle.x>= stopline[0][1]+10 or vehicle.x< stopline[0][1]-10))\
                or (vehicle.direction==2 and (vehicle.y>= stopline[1][2]+10 or vehicle.y< stopline[1][2]-10))\
                or (vehicle.direction==3 and (vehicle.x+vehicle.img.get_width()<= stopline[0][3]-10 or vehicle.x+vehicle.img.get_width() > stopline[0][3]+10)))\
                and not isCollide(vehicle):
                vehicle.x+= vehicle.velocity*di[0][vehicle.direction]
                vehicle.y+= vehicle.velocity*di[1][vehicle.direction]
            if vehicle.x<-500 or vehicle.x> 1500 or vehicle.y>1000 or vehicle.y<-500 :
                vehicles.remove(vehicle)
    def resize(self):
        None
    def randomVehicle(direction):
        global vehicles
        random_number = random.randint(0, 2)
        vehicle = Vehicle(random_number,direction)
        vehicle.x= starting_point[0][direction][next_coming_lane[direction]]
        vehicle.y= starting_point[1][direction][next_coming_lane[direction]]
        print(vehicle.x,vehicle.y)
        next_coming_lane[direction]= (next_coming_lane[direction]+1)%2
        vehicles.append(vehicle)

def isCollide(v):
    global vehicles
    ok=0
    a,b=v.x,v.y
    tmp_x,tmp_y=0,0
    min_dis=10000
    tt=0
    if (v.direction==0 and v.y+v.img.get_height() > stopline[1][0]+10)\
        or (v.direction==1 and  v.x< stopline[0][1]-10)\
        or (v.direction==2 and v.y< stopline[1][2]-10)\
        or (v.direction==3 and v.x+v.img.get_width() > stopline[0][3]+10):
        return 0
    for vehicle in vehicles:
        x= vehicle.x
        y=vehicle.y
        if (x==a and y==b):
            continue
        if (x!=a and y!=b):
            continue
        dis=abs(a-x)+abs(b-y)
        if dis<min_dis: 
            min_dis=dis
            tt=max(vehicle.img.get_height(),vehicle.img.get_width())
    return min_dis-tt<13
running= True
light= Light()
vehicles= []


while running:
    screen.fill((4,4,4))
    screen.blit(background,(0,0))    
    for event in pygame.event.get():
        if  event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button pressed
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Mouse position:", mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Vehicle.randomVehicle(0)
            elif event.key == pygame.K_RIGHT:
                Vehicle.randomVehicle(1)
            elif event.key == pygame.K_DOWN:
                Vehicle.randomVehicle(2)
            elif event.key == pygame.K_LEFT:
                Vehicle.randomVehicle(3)
    Vehicle.run()
    current_time = pygame.time.get_ticks() - start_time
    
    
    for i in range(4):
        updateDisplay(light_img,light_pos[0][i],light_pos[1][i])
        light.displayCountdown(i)
    for vehicle in vehicles:
        updateDisplay(vehicle.img,vehicle.x,vehicle.y)
    pygame.display.update()
