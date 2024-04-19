import os
from characterFile import Character
from characterFile import Player
from sceneFile import Scene
# from sceneFile import battleEndScene
from sceneFile import IntroScene

class Game():

    def __init__(self):
        self.currentScene = IntroScene(self)
        self.player = Player()
        self.messages = []
        self.renderBuffer = ""
        self.done = False

    def start(self):
        self.render()
        self.gameLoop()

    def stop(self):
        self.done = True

    def gameLoop(self):
        while self.done == False:
            self.processInput()
            self.update()
            self.render()
        self.cls()

    def processInput(self):
        playerInput = input("Input: ")
        self.currentScene.handleInput(playerInput)

    def update(self):
        self.currentScene.update()

    def render(self):
        for msg in self.messages:
            self.renderBuffer = self.renderBuffer + msg + "\n"
        self.renderBuffer = self.renderBuffer + self.currentScene.getRenderBuffer()
        self.cls()
        print(self.renderBuffer)
        self.renderBuffer = ""
        self.messages.clear()


    def sendMessage(self, theMessage):
        self.messages.append(theMessage)


    def setScene(self, theScene):
        self.currentScene = theScene

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')