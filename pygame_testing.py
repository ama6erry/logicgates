import pygame
from pygame import gfxdraw

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

square = pygame.Rect(150, 150, 150, 150)

def WorldToScreenCoords(x, y):
    return x + 640, y + 360

def ScreenToWorldCoords(x, y):
    return x - 640, y - 360

CamX = 0
CamY = 0

#loading images
notIMG = pygame.image.load('./assets/notGate.png')
andIMG = pygame.image.load('./assets/andGate.png')
nandIMG = pygame.image.load('./assets/nandGate.png')
orIMG = pygame.image.load('./assets/orGate.png')
norIMG = pygame.image.load('./assets/norGate.png')
xorIMG = pygame.image.load('./assets/xorGate.png')
xnorIMG = pygame.image.load('./assets/xnorGate.png')
inputIMG = pygame.image.load('./assets/inputGate.png')
outputIMG = pygame.image.load('./assets/outputGate.png')


class Connection: #Data type for storing connections
    def __init__(self, ConnectionNumber, GateID):
        self.ConnectionNumber = ConnectionNumber #Connection Number 2 is the output connection
        self.GateID = GateID #ID of the gate the connection resides in
        self.active = False #Determines whether 
        self.value = False #Value of signal (On / Off)
        self.LinkedWith = None #If the connection is not 2, stores the ID of the gate it recieves inputs from

class OutputSignal:
    def __init__(self, ConnectionNumber, idNum):
        self.ConnectionNumber = ConnectionNumber
        self.id = idNum

class GateConnections: #Stores all the connections and their values
    def __init__(self, gateType, GateID):
        self.gateType = gateType #Single input gate / Double input gate
        self.GateID = GateID
        if gateType == 'S':
            self.activeConnections = [Connection(0, GateID), -1, Connection(2, GateID)] #Stores the connections of the gate
        elif gateType == 'D':
            self.activeConnections = [Connection(0, GateID), Connection(1, GateID), Connection(2, GateID)]
        elif gateType == 'I':
            self.activeConnections = [-1, -1, Connection(2, GateID)]
        elif gateType == 'O':
            self.activeConnections = [Connection(0, GateID), -1, -1]
        self.ConnectedTo = [] #Array of OutputSignal's that store the ID of the gate and its connection number
    def ConnectTo(self, idNum, ConNum):
        self.ConnectedTo.append(OutputSignal(ConNum, idNum))
        print(self.GateID)
        gates[idNum].GateConnections.activeConnections[ConNum].LinkedWith = self.GateID
    def GetActiveConnection(self, ConNum):
        return self.activeConnections[ConNum]
    def SetConnection(self, ConNum, Value):
        if self.activeConnections[ConNum] != -1:
            self.activeConnections[ConNum].value = Value
    def OutputConnections(self):
        val = self.activeConnections[2].value
        for j in self.ConnectedTo:
            gates[j.id].GateConnections.SetConnection(j.ConnectionNumber, val)
    def Disconnect(self, idNum, ConNum):
        for i in self.ConnectedTo:
            if i.id == idNum and i.ConnectionNumber == ConNum:
                index = self.ConnectedTo.index(i)
        del self.ConnectedTo[index]
        gates[idNum].GateConnections.activeConnections[ConNum].LinkedWith = None
    def ToggleConnection(self, Active, ConNum):
        self.activeConnections[ConNum].active == Active

class LogicGate:
    def __init__(self, idNum, x, y, gateType, Image):
        self.id = idNum
        self.gateType = gateType
        self.Image = Image
        self.gateRect = Image.get_rect()
        self.gateRect.x = x
        self.gateRect.y = y
        self.GateConnections = GateConnections(gateType, idNum)
    def draw(self):      
        screen.blit(self.Image, self.gateRect)
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 29, 50, 50), 0) #Connection 0 
        gfxdraw.aacircle(screen, self.gateRect.x - 25, self.gateRect.y + 54, 25, (0, 0, 0))
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 111, 50, 50), 0)
        gfxdraw.aacircle(screen, self.gateRect.x - 25, self.gateRect.y + 136, 25, (0, 0 ,0))
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50), 0)
        gfxdraw.aacircle(screen, self.gateRect.x + 291, self.gateRect.y + 96, 25, (0, 0 ,0))

        ConnectedTo = self.GateConnections.ConnectedTo
        
        position1 = (self.gateRect.x + 266, self.gateRect.y + 71)

        for i in ConnectedTo:
            gate = gates[i.id]
            type = gate.gateType
            if type == 'D':
                if i.ConnectionNumber == 0:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 29)
                elif i.ConnectionNumber == 1:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 111)
            else:
                position2 = (gate.gateRect.x - 50, gate.gateRect.y + 71)
            pygame.draw.line(screen, (0, 0, 0), position1, position2, 15)

    def Connections(self):
        return [pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 29, 50, 50), pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 111, 50, 50), pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50)]

class inputGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
        self.value = self.GateConnections.activeConnections[2].value
        if self.value:
            self.Output = 1
        else:
            self.Output = 0
    def UpdateIO(self):
        self.value = self.GateConnections.activeConnections[2].value
        if self.value:
            self.Output = 1
        else:
            self.Output = 0
        self.GateConnections.OutputConnections()
    def draw(self):      
        screen.blit(self.Image, self.gateRect)
        DrawText(str(self.Output), 150, (0, 0, 0), self.gateRect.x + 162, self.gateRect.y + 103)
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50))
        gfxdraw.aacircle(screen, self.gateRect.x + 291, self.gateRect.y + 96, 25, (0, 0, 0))

        ConnectedTo = self.GateConnections.ConnectedTo

        position1 = (self.gateRect.x + 266, self.gateRect.y + 71)

        for i in ConnectedTo:
            gate = gates[i.id]
            type = gate.gateType
            if type == 'D':
                if i.ConnectionNumber == 0:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 29)
                elif i.ConnectionNumber == 1:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 111)
            else:
                position2 = (gate.gateRect.x - 50, gate.gateRect.y + 71)
            pygame.draw.line(screen, (0, 0, 0), position1, position2, 15)

    def Connections(self):
        return [-1, -1, pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50)]

class outputGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
        self.value = self.GateConnections.activeConnections[0].value
        if self.value:
            self.Output = 1
        else:
            self.Output = 0
    def UpdateIO(self):
        self.value = self.GateConnections.activeConnections[0].value
        if self.value:
            self.Output = 1
        else:
            self.Output = 0
    def draw(self):      
        screen.blit(self.Image, self.gateRect)
        DrawText(str(self.Output), 150, (0, 0, 0), self.gateRect.x + 102, self.gateRect.y + 103)
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 71, 50, 50))
        gfxdraw.aacircle(screen, self.gateRect.x - 25, self.gateRect.y + 96, 25, (0, 0, 0))
    def Connections(self):
        return [pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 71, 50, 50), -1, -1]

class notGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on = self.GateConnections.activeConnections[0].value
        self.GateConnections.activeConnections[2].value = not on
        self.GateConnections.OutputConnections()
    def draw(self):      
        screen.blit(self.Image, self.gateRect)
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 71, 50, 50))
        gfxdraw.aacircle(screen, self.gateRect.x - 25, self.gateRect.y + 96, 25, (0, 0, 0))
        pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50))
        gfxdraw.aacircle(screen, self.gateRect.x + 291, self.gateRect.y + 96, 25, (0, 0, 0))

        ConnectedTo = self.GateConnections.ConnectedTo

        position1 = (self.gateRect.x + 266, self.gateRect.y + 71)

        for i in ConnectedTo:
            gate = gates[i.id]
            type = gate.gateType
            if type == 'D':
                if i.ConnectionNumber == 0:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 29)
                elif i.ConnectionNumber == 1:
                    position2 = (gate.gateRect.x - 50, gate.gateRect.y + 111)
            else:
                position2 = (gate.gateRect.x - 50, gate.gateRect.y + 71)
            pygame.draw.line(screen, (0, 0, 0), position1, position2, 15)

    def Connections(self):
        return [pygame.Rect(self.gateRect.x - 50, self.gateRect.y + 71, 50, 50), -1, pygame.Rect(self.gateRect.x + 266, self.gateRect.y + 71, 50, 50)]

class andGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value = on1 and on2
        self.GateConnections.OutputConnections()

class nandGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value = not (on1 and on2)
        self.GateConnections.OutputConnections()

class orGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value = on1 or on2
        self.GateConnections.OutputConnections()
    
class norGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value =  not (on1 or on2)
        self.GateConnections.OutputConnections()

class xorGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value =  on1 ^ on2
        self.GateConnections.OutputConnections()
    
class xnorGate(LogicGate):
    def __init__(self, idNum, x, y, gateType, Image):
        super().__init__(idNum, x, y, gateType, Image)
    def UpdateIO(self):
        on1 = self.GateConnections.activeConnections[0].value
        on2 = self.GateConnections.activeConnections[1].value
        self.GateConnections.activeConnections[2].value =  not (on1 ^ on2)
        self.GateConnections.OutputConnections()

gates = []
activeGate = None
gateMoving = False
connectionMoving = False
InitialActiveConnection = None
activeConnection = [-1, -1] # Connection Rect / Gate ID

def createGate(gate):
    id = len(gates)
    value = None
    match gate:
        case 'NOT':
            value = notGate(id, *WorldToScreenCoords(0, 0), 'S', notIMG)
        case 'AND':
            value = andGate(id, *WorldToScreenCoords(0, 0), 'D', andIMG)
        case 'NAND':
            value = nandGate(id, *WorldToScreenCoords(0, 0), 'D', nandIMG)
        case 'OR':
            value = orGate(id, *WorldToScreenCoords(0, 0), 'D', orIMG)
        case 'NOR':
            value = norGate(id, *WorldToScreenCoords(0, 0), 'D', norIMG)
        case 'XOR':
            value = xorGate(id, *WorldToScreenCoords(0, 0), 'D', xorIMG)
        case 'XNOR':
            value = xnorGate(id, *WorldToScreenCoords(0, 0), 'D', xnorIMG)
        case 'INP':
            value = inputGate(id, *WorldToScreenCoords(0, 0), 'I', inputIMG)
        case 'OTP':
            value = outputGate(id, *WorldToScreenCoords(0, 0), 'O', outputIMG)

    gates.append(value)

def GetActiveGate(pos):
    global activeGate
    for num, gate in enumerate(gates):
        if gate.gateRect.collidepoint(pos):
            activeGate = num

def GetActiveConnection(pos):
    global activeConnection
    global connections
    global InitialActiveConnection
    for num, gate in enumerate(gates):
        connections = gate.Connections()
        if connections[0] != -1 and connections[0].collidepoint(pos):
            activeConnection[0] = connections[0]
            InitialActiveConnection = 0
            activeConnection[1] = num 
        elif connections[1] != -1 and connections[1].collidepoint(pos):
            activeConnection[0] = connections[1]
            InitialActiveConnection = 1
            activeConnection[1] = num    
        elif connections[2] != -1 and connections[2].collidepoint(pos):           
            activeConnection[0] = connections[2]
            InitialActiveConnection = 2
            activeConnection[1] = num

def DrawText(text, size, color, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

while running:
    screen.fill("grey")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, gate in enumerate(gates):
                    if gate.gateRect.collidepoint(event.pos):
                        activeGate = num
                    if activeGate == None:
                        connections = gate.Connections()
                        if connections[0] != -1 and connections[0].collidepoint(event.pos):
                            output = False
                            activeConnection[0] = connections[0]
                            InitialActiveConnection = 0
                            activeConnection[1] = num
                            connectionMoving = True
                        elif connections[1] != -1 and connections[1].collidepoint(event.pos):
                            output = False
                            activeConnection[0] = connections[1]
                            InitialActiveConnection = 1
                            activeConnection[1] = num
                            connectionMoving = True
                        elif connections[2] != -1 and connections[2].collidepoint(event.pos):
                            output = True
                            activeConnection[0] = connections[2]
                            activeConnection[1] = num
                            connectionMoving = True
            if event.button == 3:
                GetActiveConnection(pygame.mouse.get_pos())
                if InitialActiveConnection != 2:
                    gate1 = gates[activeConnection[1]]
                    SourceGateID = gate1.GateConnections.activeConnections[InitialActiveConnection].LinkedWith
                    print('source : ', str(SourceGateID))
                    print('IAC : ', str(InitialActiveConnection))
                    gate2 = gates[SourceGateID]
                    print(gate2.gateType)
                    gate2.GateConnections.Disconnect(gate1.id, InitialActiveConnection)
                    gate1.GateConnections.activeConnections[InitialActiveConnection].value = False
        if event.type == pygame.MOUSEMOTION:
            if activeGate != None:
                gateMoving = True
                gates[activeGate].gateRect.move_ip(event.rel)
            elif activeConnection[0] != -1:
                pass #Do nothing
            elif event.buttons == (1, 0, 0):
                for gate in gates:
                    gate.gateRect.move_ip(event.rel)
                dx, dy = event.rel
                CamX += dx
                CamY += dy
        if event.type == pygame.MOUSEBUTTONUP:
            if not gateMoving and not connectionMoving:
                if activeGate != None:
                    gate = gates[activeGate]
                    if gate.gateType == 'I':
                        gate.GateConnections.activeConnections[2].value = not gate.GateConnections.activeConnections[2].value

            gateMoving = False
            activeGate = None
            if activeConnection[0] != None:
                for num, gate in enumerate(gates):
                    gateID = activeConnection[1]
                    if num != gateID:
                        connections = gate.Connections()
                        if connections[0] != -1 and connections[0].collidepoint(event.pos) and output == True:
                            gates[gateID].GateConnections.ConnectTo(num, 0)
                            print('Gate ' + str(gateID) + 'connected to gate ' + str(num))
                        elif connections[1] != -1 and connections[1].collidepoint(event.pos) and output == True:
                            gates[gateID].GateConnections.ConnectTo(num, 1)
                            print('Gate ' + str(gateID) + 'connected to gate ' + str(num))
                        elif connections[2] != -1 and connections[2].collidepoint(event.pos) and output == False:
                            gates[num].GateConnections.ConnectTo(gateID, InitialActiveConnection)
                            print('Gate ' + str(num) + 'connected to gate ' + str(gateID))
                connectionMoving = False
                        
            activeConnection[0] = -1     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                createGate('NOT')
            if event.key == pygame.K_b:
                createGate('AND')
            if event.key == pygame.K_m:
                createGate('NAND')
            if event.key == pygame.K_o:
                createGate('OTP')
            if event.key == pygame.K_p:
                createGate('NOR')
            if event.key == pygame.K_v:
                createGate('OR')
            if event.key == pygame.K_x:
                createGate('XOR')
            if event.key == pygame.K_c:
                createGate('XNOR')
            if event.key == pygame.K_i:
                createGate('INP')
            if event.key == pygame.K_d:
                position = pygame.mouse.get_pos()
                GetActiveGate(position)
                gate = gates[activeGate]
                print('Current active connections for gate ', activeGate, ':')
                for i in gate.GateConnections.ConnectedTo:
                    print('Gate: ', i.id)
                    print('Connection Number: ', i.ConnectionNumber)
                    print('----------------------')
                if gate.gateType == 'O':
                    print('Connection 0: ', gate.GateConnections.activeConnections[0].value, f' (Connected to gate {gate.GateConnections.activeConnections[0].LinkedWith})')
                    print('Current output value = ', gate.Output)
                else:
                    print('Current output value = ', gate.GateConnections.activeConnections[2].value)           
                    if gate.gateType == 'S':
                        print('Connection 0: ', gate.GateConnections.activeConnections[0].value, f' (Connected to gate {gate.GateConnections.activeConnections[0].LinkedWith})')
                        print('Connection 2: ', gate.GateConnections.activeConnections[2].value)
                    elif gate.gateType == 'D':
                        print('Connection 0: ', gate.GateConnections.activeConnections[0].value, f' (Connected to gate {gate.GateConnections.activeConnections[0].LinkedWith})')
                        print('Connection 1: ', gate.GateConnections.activeConnections[1].value, f' (Connected to gate {gate.GateConnections.activeConnections[1].LinkedWith})')
                        print('Connection 2: ', gate.GateConnections.activeConnections[2].value)
                    elif gate.gateType == 'I':
                        print('Connection 2: ', gate.GateConnections.activeConnections[2].value)
                print('<--------------------------------------------->')
                
                activeGate = None



    x, y = WorldToScreenCoords(CamX, CamY)

    for i in gates:
        i.draw()
        i.UpdateIO()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()