import pygame, time, math, random, numpy

width = 1000
height = 1000
pygame.init()
screen = pygame.display.set_mode((width, height))
done = False
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
grey = (134, 136, 138)
gold = (249, 166, 2)
keys = pygame.key.get_pressed()
turtleSkin = pygame.image.load("arrow.png")
turtleSkin = pygame.transform.scale(turtleSkin, (10, 10))
turtleRect = turtleSkin.get_rect()
hawkSkin = pygame.image.load("hawk.png")
hawkSkin = pygame.transform.scale(hawkSkin, (15, 15))
hawkRect = hawkSkin.get_rect()
clock = pygame.time.Clock()
STAT_FONT = pygame.font.SysFont("comicsans", 50)
crunch = pygame.mixer.Sound("crunch.wav")
noFood = False

class Hawk:
    def __init__(self, maxVel, sight):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.xV = random.randint(-10, 10) / 10
        self.yV = random.randint(-10, 10) / 10
        while self.xV == 0 or self.yV == 0:
            self.xV = random.randint(-10, 10) / 10
            self.yV = random.randint(-10, 10) / 10
        self.width = 15
        self.height = 15
        self.angle = 0
        self.slope = self.xV / self.yV
        self.score = 0
        self.maxVel = maxVel
        self.sight = sight

    def move(self):
        if abs(self.xV) > self.maxVel or abs(self.yV) > self.maxVel:
            scaleFactor = self.maxVel / max(abs(self.xV), abs(self.yV))
            self.xV *= scaleFactor
            self.yV *= scaleFactor

        if self.xV != 0 and self.yV != 0:
            self.slope = self.xV / self.yV
        self.angle = math.degrees(math.atan(self.slope))
        if self.yV >= 0:
            self.angle += 180

        if self.x > width:
            self.xV *= -2
        if self.x < 0:
            self.xV *= -2
        if self.y > height:
            self.yV *= -2
        if self.y < 0:
            self.yV *= -2

        self.x += self.xV
        self.y += self.yV
        #pygame.draw.rect(screen, red, (self.x, self.y, self.width, self.height))
        rotatedHawkImage = pygame.transform.rotate(hawkSkin, self.angle)
        myRect = pygame.Rect(hawkRect)
        myRect.x = self.x
        myRect.y = self.y
        screen.blit(rotatedHawkImage, myRect)

    def hunt(self):
        hunting = False
        if len(turtles) > 0 and self.score < hawkFoodReproduce:
            minD = 10000
            for target in turtles:
                if self.distance(target) < self.sight:
                    currentMin = self.distance(target)
                    if currentMin < minD:
                        hunting = True
                        minD = currentMin
                        minTurtle = target
            if hunting:
                if minTurtle.x < self.x:
                    self.xV -= 1
                if minTurtle.x > self.x:
                    self.xV += 1
                if minTurtle.y < self.y:
                    self.yV -= 1
                if minTurtle.y > self.y:
                    self.yV += 1
                #pygame.draw.line(screen, red, (self.x, self.y), (minTurtle.x, minTurtle.y))

    def distance(self, turtle):
        distX = self.x - turtle.x
        distY = self.y - turtle.y
        return math.sqrt((distX ** 2) + (distY ** 2))

    def moveAway(self):
        minDistance = 40
        xDistance = 0
        yDistance = 0
        numClose = 0

        for hawk in hawks:
            distance = self.distance(hawk)
            if distance < minDistance:
                numClose += 1
                xdiff = (self.x - hawk.x)
                ydiff = (self.y - hawk.y)

                xDistance += xdiff
                yDistance += ydiff

        if numClose == 0:
            return

        self.xV += xDistance / 40
        self.yV += yDistance / 40

class Turtle:

    def __init__(self, maxVelEating, maxVelRunning, sight):

        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.xV = random.randint(-10, 10) / 10
        self.yV = random.randint(-10, 10) / 10
        while self.xV == 0 or self.yV == 0:
            self.xV = random.randint(-10, 10) / 10
            self.yV = random.randint(-10, 10) / 10

        self.width = turtleSkin.get_width()
        self.height = turtleSkin.get_height()
        self.closeTurtles = []
        self.angle = 0
        self.slope = 0
        self.alive = True
        self.nearWall = False
        self.focus = "food"
        self.score = 0
        self.maxVelEating = maxVelEating
        self.maxVelRunning = maxVelRunning
        self.maxVel = maxVelEating
        self.full = False
        self.sight = sight

    def move(self):
        if abs(self.xV) > self.maxVel or abs(self.yV) > self.maxVel:
            scaleFactor = self.maxVel / max(abs(self.xV), abs(self.yV))
            self.xV *= scaleFactor
            self.yV *= scaleFactor

        # if self.x > width:
        #     self.xV *= -2
        #     #self.yV += maxVel
        # if self.x < 0:
        #     self.xV *= -2
        #     #self.yV -= maxVel
        # if self.y > height:
        #     self.yV *= -2
        #     #self.xV += maxVel
        # if self.y < 0:
        #     self.yV *= -2
        #     #self.xV -= maxVel

        if self.x > width:
            self.x = 0

        if self.x < 0:
            self.x = width

        if self.y > height:
            self.y = 0

        if self.y < 0:
            self.y = height

        if self.xV != 0 and self.yV != 0:
            self.slope = self.xV / self.yV
        self.angle = math.degrees(math.atan(self.slope))
        if self.yV >= 0:
            self.angle += 180


        #print(self.angle)
        self.x += self.xV
        self.y += self.yV

        rotatedImage = pygame.transform.rotate(turtleSkin, self.angle)
        myRect = pygame.Rect(turtleRect)
        myRect.x = self.x
        myRect.y = self.y
        screen.blit(rotatedImage, myRect)
        #pygame.draw.rect(screen, red, (self.x, self.y,self.width, self.height))

    def moveClose(self):
        averageX = 0
        averageY = 0
        self.closeTurtles = [self]
        for turtle in turtles:
            if turtle == self:
                pass
            if self.distance(turtle) < self.sight: # 200
                #pygame.draw.line(screen, black, (self.x, self.y,),( turtle.x, turtle.y))
                self.closeTurtles.append(turtle)
                #counter += 1
                averageX += self.x - turtle.x
                averageY += self.y - turtle.y

        if len(self.closeTurtles) != 0:
            averageX /= len(self.closeTurtles)
            averageY /= len(self.closeTurtles)
            self.xV -= averageX / 100
            self.yV -= averageY / 100

    def moveWith(self):
        averageXVel = 0
        averageYVel = 0

        for turtle in self.closeTurtles:

            averageXVel += turtle.xV
            averageYVel += turtle.yV

        averageXVel /= len(self.closeTurtles)
        averageYVel /= len(self.closeTurtles)

        self.xV += averageXVel / 40
        self.yV += averageXVel / 40

    def moveAway(self):
        minDistance = 30
        xDistance = 0
        yDistance = 0
        numClose = 0

        for turtle in self.closeTurtles:
            distance = self.distance(turtle)
            if distance < minDistance:
                numClose += 1
                xdiff = (self.x - turtle.x)
                ydiff = (self.y - turtle.y)

                xDistance += xdiff
                yDistance += ydiff

        if numClose == 0:
            return

        self.xV += xDistance / 40
        self.yV += yDistance / 40

    def distance(self, other):
        distX = self.x - other.x
        distY = self.y - other.y
        return math.sqrt(distX * distX + distY * distY)

    def flee(self):
        foodTime = True
        for hawk in hawks:
            if self.distance(hawk) < self.sight: # 100
                foodTime = False
                self.focus = "dontDie"
                self.maxVel = self.maxVelRunning
                if hawk.x > self.x:
                    self.xV -= 3
                if hawk.x < self.x:
                    self.xV += 3
                if hawk.y > self.y:
                    self.yV += 3
                if hawk.y < self.y:
                    self.yV -= 3
        if foodTime:
            self.focus = "food"
            self.maxVel = self.maxVelEating

    # def wallRun(self):
    #     if self.nearWall == "bottom": # closest to right wall
    #         self.yV -= maxVel
    #         self.xV -= maxVel
    #
    #     elif self.nearWall == "top":
    #         self.yV += maxVel
    #         self.xV += maxVel
    #
    #     elif self.nearWall == "bottom": # closest to bottom
    #         self.xV += maxVel
    #         self.yV -= maxVel
    #
    #     elif self.nearWall == "top":
    #         self.xV -= maxVel
    #         self.yV += maxVel
    #
    # def wallScan(self):
    #     if width - self.x < 25: # closest to right wall
    #         self.nearWall = "right"
    #         return True
    #
    #     elif self.x < 25:
    #         self.nearWall = "left"
    #         return True
    #
    #     elif height - self.y < 25: # closest to bottom
    #         self.nearWall = "bottom"
    #         return True
    #
    #     elif self.y < 25:
    #         self.nearWall = "top"
    #         return True
    #
    #     else:
    #         return False

    def hunt(self):
        foodClose = False
        if self.focus == "food" and len(foods) > 0 and self.score < 2:
            minD = 10000
            for food in foods:
                if self.distance(food) < self.sight:
                    foodClose = True
                    currentMin = self.distance(food)
                    if currentMin < minD:

                        minD = currentMin
                        minFood = food

            if foodClose:
                #minFood.color = red
                if minFood.x < self.x:
                    self.xV -= 1
                if minFood.x > self.x:
                    self.xV += 1
                if minFood.y < self.y:
                    self.yV -= 1
                if minFood.y > self.y:
                    self.yV += 1
                #pygame.draw.line(screen, red, (self.x, self.y), (minFood.x, minFood.y))
                if abs(self.x - minFood.x) < minFood.radius * 2 and abs(self.y - minFood.y) < minFood.radius * 2:
                    food.eaten = True
                    foods.remove(minFood)
                    self.score += 1
                    global turtlePopulation
                    turtlePopulation.append(self)
                if self.score > 1 and not self.full:
                    self.full = True
                    turtlePopulation.append(self)
                    #turtlePopulation += 1


class Food:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.color = gold
        self.radius = 5
        self.eaten = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


turtles = []
hawks = []
foods = []
turtlePopulation = 100
hawkPopulation = 5
foodPopulation = 200
for i in range(turtlePopulation):
    turtles.append(Turtle(10, 20, 200))
for i in range(hawkPopulation):
    hawks.append(Hawk(9, 1000))
for i in range(foodPopulation):
    foods.append(Food())

hawkScore = 0
averageScore = 0
time = 10
timeLeft = 10
counter = 200
hawkFoodLive = 1
hawkFoodReproduce = 4
roundOver = False
generation = 1
print("---Generation " + str(generation) + '---')
print("Turtles: " + str(len(turtles)) + ", " + "Hawks: " + str(len(hawks)))
turtlePopulation = []
while not done:
    #clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(grey)
    for food in foods:
        food.draw()
    if len(turtles) > 0:
        for turtle in turtles:
            turtle.moveClose()
            turtle.moveWith()
            turtle.flee()
            turtle.moveAway()
            turtle.hunt()
            turtle.move()

            if len(hawks) > 0:
                for hawk in hawks:
                    if hawk.score < hawkFoodReproduce:
                        if turtle.distance(hawk) < 10 and turtle.alive:
                            crunch.play()
                            hawkScore += 1
                            hawk.score += 1
                            averageScore += turtle.score
                            turtles.remove(turtle)
                            turtle.alive = False
    if len(hawks) > 0:
        for hawk in hawks:
            hawk.hunt()
            hawk.moveAway()
            hawk.move()

    # if len(turtles) == 0:
    #     print("Average score was: " + str(averageScore / turtlePopulation))

    counter -= 1

    fps = clock.get_fps()
    if counter < 1:
        roundOver = True

    if roundOver:
        generation += 1
        print("---Generation " + str(generation) + '---')
        roundOver = False

        counter = 500


        hawkPopulation = 0
        # for turtle in turtles:
        #     if turtle.score == 1:
        #         turtlePopulation += 1
        #
        #     elif turtle.score > 1:
        #         turtlePopulation += 3
        #     else:
        #         pass
        for hawk in hawks:
            if hawk.score == hawkFoodLive:
                hawkPopulation += 1
            elif hawk.score >= hawkFoodReproduce:
                hawkPopulation += 2
            else:
                pass
        turtles = []
        hawks = []
        foods = []
        foodPopulation2 = foodPopulation
        hawkScore = 0
        turtleTraits = [turtle.maxVelEating, turtle.maxVelRunning, turtle.sight]
        for turtle in turtlePopulation:
            if turtle.score == 1:
                turtles.append(turtle)
            if turtle.score > 1:
                traits = []
                tuple(turtleTraits)
                for trait in turtleTraits:

                    randomNum = random.randint(1, 10)
                    if randomNum == 1:
                        trait *= .5
                    elif randomNum == 10:
                        trait *= 1.5
                    else:
                        trait *= 1
                    traits.append(trait)

                turtles.append(Turtle(traits[0], traits[1], traits[2]))
        # for i in range(len(turtleTraits)):
        #     avr = 0
        #     for turtle in turtles:
        #         avr += trait
        #     print(str(turtleTraits[i]) + " average: " + (str(avr / len(turtles))))

            # randomNum = random.randint(1, 4)
            # if randomNum == 1:
            #     turtleMaxVelEating = random.randint(6, 8)
            # elif randomNum == 2 or random == 3:
            #     turtleMaxVelEating = random.randint(9, 11)
            # else:
            #     turtleMaxVelEating = random.randint(11, 13)
            #
            # randomNum = random.randint(1, 4)
            # if randomNum == 1:
            #     turtleMaxVelRunning = random.randint(18, 20)
            # elif randomNum == 2 or random == 3:
            #     turtleMaxVelRunning = random.randint(21, 23)
            # else:
            #     turtleMaxVelRunning = random.randint(24, 26)
            # randomNum = random.randint(1, 4)
            # if randomNum == 1:
            #     turtleSight = random.randint(100, 200)
            # elif randomNum == 2 or random == 3:
            #     turtleSight = random.randint(200, 300)
            # else:
            #     turtleSight = random.randint(300, 400)
            #turtles.append(Turtle(turtleMaxVelEating, turtleMaxVelRunning, turtleSight))

        turtlePopulation = []

        for i in range(hawkPopulation):
            randomNum = random.randint(1, 4)
            if randomNum == 1:
                hawkMaxVel = random.randint(2, 4)
            elif randomNum == 2 or random == 3:
                hawkMaxVel = random.randint(5, 7)
            else:
                hawkMaxVel = random.randint(8, 10)

            randomNum = random.randint(1, 4)
            if randomNum == 1:
                hawkSight = random.randint(200, 400)
            elif randomNum == 2 or random == 3:
                hawkSight = random.randint(500, 700)
            else:
                hawkSight = random.randint(800, 1000)
            hawks.append(Hawk(hawkMaxVel, hawkSight))

            #print("Hawk " + str(i) + " stats: " + "Max Vel: " + str(hawkMaxVel) + ", " + "Sight: " + str(hawkSight))
        for i in range(foodPopulation2):
            foods.append(Food())
        print("Turtles: " + str(len(turtles)) + ", " + "Hawks: " + str(len(hawks)))

    score = STAT_FONT.render('Score: ' + str(hawkScore), 1, (255, 255, 255))
    time = STAT_FONT.render("Time: " + str(counter), 1, (255, 255, 255))
    screen.blit(score, (width - 10 - score.get_width(), 10))
    screen.blit(time, (10, 10))
    pygame.display.flip()
