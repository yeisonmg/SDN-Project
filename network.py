from random import randint


class Controller():
    def __init__(self,idController,deployedIn,priceController,state):
        self.idController=idController
        self.deployedIn=deployedIn
        self.controlledSW= [] # lista switches que controla, lista
        self.priceController=priceController
        self.state=state
        self.receivedRequest=0 ###Crear una funcion que agregue switches a "controlledSW", e integrar funcion para que sume las peticiones
        self.totalProcessingDelay=0
        
    def __str__(self):
        return """\
idController:\t\t{}
deployedId:\t\t{}
controlledSW:\t\t{}
priceController:\t{}
state:\t\t\t{}
receivedReques:\t\t{}
processingDelay:\t{}
""".format(self.idController,self.deployedIn,self.controlledSW,self.priceController,self.state,self.receivedRequest,self.totalProcessingDelay)
        

    def getPriceController(self):
        return self.priceController
    
    def addControlledSW(self, switch):    
        self.controlledSW.append(switch)
    
    def setSWDeployed(self, switch): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        self.deployedIn=switch #Aqui van almacenadoslos awitches todos
        
    def setState(self, state): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        self.state=state

    def getReceivedRequest(self): #Cambia el lugar del controlador (de switche a controlador)   se=configura, parametriza
        temp = 0
        for switch in self.controlledSW:
            temp += switch.getFlowSetupRequest() #Sumatoria total de peticiones de todos los switches que tiene el controlador
        self.receivedRequest = temp
        return self.receivedRequest
        
    def getTotalProcessingDelay(self): #Get: Obtiene datos, devolver datos, procesa         
        self.totalProcessingDelay = (self.getReceivedRequest()/1.6)*self.deployedIn.getProcessingDelay()                
        return self.totalProcessingDelay
  
class Switch():
    def __init__(self,idSwitch,flowSetupRequest,processingDelay):
        self.idSwitch=idSwitch
        self.flowSetupRequest=flowSetupRequest
        self.processingDelay=processingDelay

    def getFlowSetupRequest(self):
        return self.flowSetupRequest        
        
    def getProcessingDelay(self):
        #Time to process 1.6 M of flow setup request in ms.
        return self.processingDelay    
    
class Network():
    def __init__(self):
        self.controllerCost = 0 #Costo de todos los controladores de la red
        self.controllerSWLinkCost = 0  #Costo total de los enlaces de controlador a Switch
        self.intercontrollerLinkCost = 0
        self.totalCost = 0
        self.switches= []    
        self.controllers= []    
        self.links = []
    
    def addLink(self, link):
        self.links.append(link)
    
    def calculateTotalCost(self):
        cost = 0
        for link in self.links:
            if(link.getState() == True):
                cost += link.getPrice()
        return cost
    
    def calculateControllerCost(self):
            controllerCost = 0
            return controllerCost
        
    def getlinks(self):  #Imprime los links que hay
        return self.links
    
    def addSwitch(self, switch):
        self.switches.append(switch)    
    
    def addController(self, controller):
        self.controllers.append(controller)
        
    def linkActivation(self):
        '''This function activates randomly one link 
        between each pair of switches.
        '''
        #1.Iterate over "links" list and set status to False
        for link in self.links:
            link.setState(False)
        #2.Activate link: Choose each three positions a Link and set status to True
        lim_inf = 0        
        while(lim_inf <= len(self.links)-3):
            lim_sup = lim_inf + 2               
            index = randint(lim_inf,lim_sup)
            self.links[index].setState(True)
            lim_inf += 3
        
class Link():
    def __init__(self, idLink, latency, price, carrierId, sourceId , destinationId):
        self.idLink = idLink
        self.latency = latency        
        self.price = price        
        self.carrierId = carrierId        
        self.sourceId = sourceId        
        self.destinationId = destinationId
        self.state = False

    def getPrice(self):
        return self.price

    def getidLink(self):
        return self.idLink

    def getState(self):
        return self.state

    def setState(self, state):
        self.state=state

##MyNet
mynet = Network()

LC03 = Link("LC03", 2.98, 100, "Claro", "S0", "S3")
mynet.addLink(LC03) 
LM03 = Link("LM03", 2.98*1.05, 80, "Movistar", "S0", "S3")    
mynet.addLink(LM03)
LT03 = Link("LT03", 2.98*1.1, 70, "Tigo", "S0", "S3")    
mynet.addLink(LT03)

LC014 = Link("LC014", 4.75, 100, "Claro", "S0", "S14")    
mynet.addLink(LC014)
LM014 = Link("LM014", 4.75*1.05, 80, "Movistar", "S0", "S14")    
mynet.addLink(LM014)
LT014 = Link("LT014", 4.75*1.1, 70, "Tigo", "S0", "S14")    
mynet.addLink(LT014)
 

S0 = Switch("S0", randint(10000,500000), randint(2,10))
mynet.addSwitch(S0)    
S3 = Switch("S3", randint(10000,500000), randint(2,10))
mynet.addSwitch(S3)
S14 = Switch("S14", randint(10000,500000), randint(2,10))
mynet.addSwitch(S14)

priceController = 200
C0 = Controller("C0", "S0", priceController, False)
mynet.addController(C0)
C1 = Controller("C1", "S1", priceController, False)
mynet.addController(C1)

print(str(mynet.calculateTotalCost()))
mynet.linkActivation()
print(str(mynet.calculateTotalCost()))

#print(str(mynet.getlinks()[1].getPrice()))
# -*- coding: utf-8 -*-

#fsr = randint(10000,500000) #aleatorio flow set up request
