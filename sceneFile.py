import random
from characterFile import Monster
from characterFile import finalBoss
class Scene:
    def __init__(self, game):
        self.game = game

    def getRenderBuffer(self):
        return str(self.getSceneText()) + str(self.getMenu())
    
    def getMenu(self):
        return "Menu:" + "\n" + "1 - Journey onwards" + "\n" + "2 - Enter town" + "\n" + "3 - Quit"
    
    def getSceneText(self):
        return "You find yourself at a crossroads. Where do you want to go? \n"

    def handleInput(self,theInput):
        self.playerInput = theInput
    
    def update(self):
        if self.playerInput == "1":
            self.firstCommand()
        elif self.playerInput == "2" :
            self.secondCommand()
        elif self.playerInput == "3":
            self.thirdCommand()
        elif self.playerInput == "42069":
            self.game.player.addMoney(10000)
        else:
            pass
    
    def firstCommand(self):
        self.game.setScene(TravelScene(self.game))

    def secondCommand(self):
        pass

    def thirdCommand(self):
        self.quit()

    def quit(self):
        self.game.stop()

class IntroScene(Scene):
    
    def __init__(self,game):
        super().__init__(game)

    def getMenu(self):
        return "Enter player name: "
    
    def getSceneText(self):
        return "You are a wandering Jedi. Your goal is to defeat the Sith and save the galaxy! \n"
    
    def update(self):
        self.game.player.setName(self.playerInput)
        self.game.currentScene = TravelScene(self.game)

class TravelScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def getMenu(self):
        return f'''
        Menu:
        \t 1 - Journey Onward
        \t 2 - Land on planet
        \t 3 - Quit'''

    def getSceneText(self):
        return ("You have come across a town on the planet. \n")
    
    def firstCommand(self):
        self.game.currentScene = battleScene(self.game)
    
    def secondCommand(self):
        self.game.currentScene = TownScene(self.game)

class TownScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def getMenu(self):
        return f'''
        Menu:
       \t 1 - Leave town
       \t 2 - Enter Store
       \t 3 - Quit'''
    
    def getSceneText(self):
        return f'''You have entered into a town! \n '''
    
    def firstCommand(self):
        self.game.currentScene = TravelScene(self.game)

    def secondCommand(self):
        self.game.currentScene = storeScene(self.game)

class gameOverScene(Scene):
    def __init__(self, game):
        super().__init__(game)
    
    def getMenu(self):
        return "\n Please hit enter to quit"
    
    def getSceneText(self):
        return "You fought with honor. \n" + self.game.player.printStats()
    
    def update(self):
        self.game.stop()

class battleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.monster = Monster("Storm Trooper", 20, 25, 5)
        

    def getMenu(self):
        return f'''
        Menu:
       \t 1 - Attack!
       \t 2 - Run!
       \t 3 - Quit!'''

    def getSceneText(self):
        return f'''A {self.monster.getName()} appeared! What are you gonna do?!
        {self.monster.printStats()}
        

        {self.game.player.printStats()}'''
        

    def firstCommand(self):
        self.game.sendMessage(self.game.player.getAttackMessage())
        self.game.sendMessage(self.monster.takeDamage(self.game.player.getAttack()))
        if self.monster.getHealth() > 0:
            self.game.sendMessage(self.monster.getAttackMessage())
            self.game.sendMessage(self.game.player.takeDamage(self.monster.getAttack()))    
            if self.game.player.getHealth() <= 0:
                self.game.setScene(battleEndScene(self.game, self.monster))
        else:
            self.game.setScene(battleEndScene(self.game, self.monster))


    def secondCommand(self):
        self.game.setScene(TravelScene(self.game))
        self.game.sendMessage("You ran away!")

class battleEndScene(Scene):

    def __init__(self, game, monster):
        self.game = game
        self.monster = monster
    
    def getMenu(self):
        return "\n Hit enter"

    def getSceneText(self):
        if self.monster.getHealth() <= 0:
            self.game.player.addMoney(100)
            self.game.player.addExp(70 + random.randrange(0,10))
            return f'''{self.monster.getName()} was defeated by {self.game.player.getName()} !'''
        elif self.game.player.getHealth() <= 0:
                return f''' You were killed by the {self.monster.getName()}'''
        

    def handleInput(self, theInput):
        self.playerInput = theInput

    def update(self):
        super().update()
        if self.monster.getHealth() <= 0:
            self.game.player.addMoney(10)
            self.game.player.addExp(20)
            print("Player Won!!")
            if self.game.player.level < 15:
                self.game.setScene(TravelScene(self.game))
            else:
                self.game.setScene(finalBossScene(self.game))
        elif self.game.player.getHealth() <= 0:
            self.game.setScene(gameOverScene(self.game))
        

class storeScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def getMenu(self):
        return f'''
        Menu:
       \t 1 - Buy Items
       \t 2 - Leave Store
       \t 3 - Quit'''
    
    def getSceneText(self):
        return f'''You have entered the local store! \n '''
    
    def firstCommand(self):
        self.game.currentScene = ShopScene(self.game)

    def secondCommand(self):
        self.game.currentScene = TownScene(self.game)

class ShopScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
    def getMenu(self):
        return f'''
        Welcome to the shop inventory! What would you like to buy? \n
        Menu:
        \t 1 - Ancient Saber of the Jedi Knights
        \t 2 - Medical Droid
        \t 3 - Leave Shop Inventory'''

    def firstCommand(self):
        if self.game.player.getMoney() > 1000:
            self.game.player.attack = 10000
            self.game.player.spendMoney(1000)
            self.game.sendMessage("Congrats you have purchased the Ancient Saber of the Jedi Knights! Your attack has been raised drastically!")
        else:
            self.game.sendMessage("You dont have enough credits to purchase this item.")

    def secondCommand(self):
        if self.game.player.health < self.game.player.maxHealth:
            if self.game.player.getMoney() > 15:
                self.game.player.heal(25)
                self.game.player.spendMoney(15)
                self.game.sendMessage("You healed 25 HP! ")
            else:
                self.game.sendMessage("You do not have enough credits to heal. ")
        else:
            self.game.sendMessage("You are already at max health! ")

    def thirdCommand(self):
        self.game.currentScene = storeScene(self.game)

class victoryScene(Scene):
    def __init__(self, game, finalBoss):
        super().__init__(game)
        self.finalBoss = finalBoss

    def getMenu(self):
        return "\n Please hit enter to finish your journey"
    
    def getSceneText(self):
        return f'''Congrats you have defeated {self.finalBoss.getName()}. \n Now peace has been restored to the galaxy... for now.''' + self.game.player.printStats()
    
    def update(self):
        self.game.stop()

class finalBossScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.finalBoss = finalBoss("Darth Vader", 250, 45, 20)
    
    def getMenu(self):
        return f'''
        Menu:
       \t 1 - Attack!
       \t 2 - Run!
       \t 3 - Quit!'''

    def getSceneText(self):
        return f'''{self.finalBoss.getName()} has arrived! He must be defeated to win! So what are you going to do?!
        {self.finalBoss.printStats()}
        

        {self.game.player.printStats()}'''
        

    def firstCommand(self):
        self.game.sendMessage(self.game.player.getAttackMessage())
        self.game.sendMessage(self.finalBoss.takeDamage(self.game.player.getAttack()))
        if self.finalBoss.getHealth() > 0:
            self.game.sendMessage(self.finalBoss.getAttackMessage())
            self.game.sendMessage(self.game.player.takeDamage(self.finalBoss.getAttack()))    
            if self.game.player.getHealth() <= 0:
                self.game.setScene(battleEndScene(self.game, self.finalBoss))
        else:
            self.game.setScene(victoryScene(self.game, self.finalBoss))


    def secondCommand(self):
        self.game.setScene(TravelScene(self.game))
        self.game.sendMessage("You ran away!")