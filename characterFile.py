import random
class Character:

    def __init__(self, name, startHealth, startAtk, startDef):
        self.name = name
        self.health = startHealth
        self.maxHealth = startHealth
        self.attack = startAtk
        self.defense = startDef

    def calculateDamage(self, incomingAttack):
        damage = (incomingAttack + random.randrange(-2, 2)) - self.defense
        if damage < 0:
            damage = 0
        return damage
    
    def getName(self):
        return self.name
    
    def getAttack(self):
        return self.attack

    def getAttackMessage(self):
        return str(self.name) + " attacked!"

    def getHealth(self):
        return self.health

    def getMaxHealth(self):
        return self.maxHealth
    
    def heal(self, amount):
        self.health += amount
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        return self.name + "healed " + str(amount) + " damage."

    def printStats(self):
        return (self.name) + "\n\tHealth: " + str(self.health) + "/" + str(self.maxHealth) + "\n\tAttack:" +  str(self.attack) + "\n\tDefense: " + str(self.defense)
    
    def takeDamage(self, incomingAttack):
        damage = self.calculateDamage(incomingAttack)
        self.setHealth(self.health - damage)
        return f"{self.name} took {damage} damage!"

    def setHealth(self, amount):
        self.health = amount
        if self.health < 0:
            self.health = 0

    def setName(self, name):
        self.name = name

class Player(Character):
    def __init__(self):
        super().__init__(self, 200, 40, 30)
        self.exp = 0
        self.level = 1
        self.expThreshold = 80
        self.money = 0

    def levelUp(self):
        if self.exp > self.expThreshold:
            self.exp = 0
            self.level += 1
        return self.printStats()
    
    def getMoney(self):
        return self.money
    
    def addMoney(self, amount):
        self.money += amount
        return f'''You gained {amount} of gold!'''
    
    def addExp(self, amount):
        self.exp += amount
        self.levelUp()
        return f'''You gained {amount} XP!'''
    
    def printStats(self):
        return f'''{super().printStats()}
        Level (80XP): {self.level} 
        Money: {self.money}
        XP: {self.exp} \n'''
    
    def spendMoney(self, amount):
        self.money -= amount

class Monster(Character):
    def __init__(self, name, health, attack, defense):
        name = name
        health = health + random.randrange(-5,20)
        attack = attack + random.randrange(-5,20)
        defense = defense + random.randrange(-5,30)
        super().__init__(name, health, attack, defense)

    def getAwardMoney(self):
        return (super().maxHealth + self.attack + self.defense) * .1 + random.randrange(0,5)
    
    def getAwardXP(self):
        return (super().maxHealth + self.attack + self.defense) * .5 + random.randrange(0,5)

class finalBoss(Character):
    def __init__(self, name, health, attack, defense):
        name = name
        health = health + random.randrange(-5, 50)
        attack = attack + random.randrange(-5,30)
        defense = defense + random.randrange(-5,40)
        super().__init__(name, health, attack, defense)
    
    def getAwardMoney(self):
        return (super().maxHealth + self.attack + self.defense) * .5 + random.randrange(2,7)
    
    def getAwardXP(self):
        return (super().maxHealth + self.attack + self.defense) * .8 + random.randrange(2,7)
