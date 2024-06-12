import pygame
import screeninfo
class DATA:
    BOSSSPEED = 10
    for m in screeninfo.get_monitors():
        SIZE = [m.width,m.height]
    @staticmethod
    def moveTo(ax,ay,bx,by,speed=5):
        
        steps_number = int(max(abs(bx-ax),abs(by-ay)))
        if (steps_number==0):
            return [ax,ay]
        stepx = float(bx-ax)/steps_number
        stepy = float(by-ay)/steps_number
        return [int(ax + stepx*speed), int(ay + stepy*speed)]
    
class Boss:
    def __init__(self,x,y):
        self.windows = []
        self.poses = [
            [0,0],
            [DATA.SIZE[0]/2,0],
            [0,DATA.SIZE[1]],
            [DATA.SIZE[0],0],
            [0,DATA.SIZE[1]/2],
            DATA.SIZE
        ]
        self.current_pos = 0
        self.end_pos = self.poses[self.current_pos]
        print(self.end_pos)
        for i in range(5):
            self.windows.append(pygame.Window("",(180,180),(x,y)))
            self.windows[i].always_on_top = True
    def update(self):
        last_wind = "None"
        for i in self.windows:
            i.get_surface().fill("black")
            pos = i.position
            if last_wind!="None":
                if pygame.Vector2.distance_to(pygame.Vector2(pos[0],pos[1]),pygame.Vector2(last_wind[0],last_wind[1])) > 180:
                    win_pos = DATA.moveTo(pos[0],pos[1],last_wind[0],last_wind[1],DATA.BOSSSPEED)
                    i.position = (win_pos[0],win_pos[1])
                pygame.draw.rect(i.get_surface(),"orange",pygame.Rect(50,50,80,80))     
            else:
                win_pos = DATA.moveTo(pos[0],pos[1],self.end_pos[0],self.end_pos[1],DATA.BOSSSPEED)
                i.position = (win_pos[0],win_pos[1])
                if pygame.Vector2.distance_to(pygame.Vector2(win_pos[0],win_pos[1]),pygame.Vector2(self.end_pos[0],self.end_pos[1])) < 10:
                    self.current_pos+=1
                    if self.current_pos == len(self.poses):
                        self.current_pos = 0
                    self.end_pos = self.poses[self.current_pos]
                pygame.draw.rect(i.get_surface(),"red",pygame.Rect(50,50,80,80))        
            last_wind = pos
            i.flip()
            
class App:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.boss = Boss(0,0)
    def update(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            self.boss.update()
_app = App()
_app.update()