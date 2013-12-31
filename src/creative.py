 
import rg

# TODOs: Problem: Gegner mit <10 HP machen Suicide. Loesung? zB Wenn nur 1 Gegner und der hat < 10 HP und wir haben mehr HP als er: weg gehen (oder guard?)

# http://robotgame.net/robotsource/4465

#TODO: Describe enemiesAround Structure

class Robot:

    def act(self, game):

        # Scheint unsere Erfolgsaussichten zu reduzieren
        # Wenn im Spawn Bereich, dann ist das wichtigste dass man da mal raus kommt..
        #if 'spawn' in rg.loc_types(self.location):
        #    return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        #else:

        # Make game avaiable for whole class
        self.game = game

        #rg.roboDict = dict((loc,bot) for loc, bot in game.robots.iteritems())

        # Get enemies within wdist 1
        self.enemiesAround = self.getRobotsAround(self.location, 1)

        #print self.enemiesAround
        #print len(self.enemiesAround)

        #print '[%s]' % ', '.join(map(str, game.robots))
        #print game.robots
        #print '[%s]' % ', '.join(map(str, self.enemiesAround))


        # If enemies around: attack, flee or kill yourself..
        if(len(self.enemiesAround) > 0):
            if self.shouldFlee():
                return ['move', self.getFleeLocation()]
            elif self.isSuicidal():
                return ['suicide']
            else:
                return ['attack', self.getAttackTarget()]
        else:
            distToCenter = rg.dist(self.location, rg.CENTER_POINT)
            if(distToCenter > 3):
            	return['move',rg.toward(self.location, rg.CENTER_POINT)]

        return['guard']

    def shouldFlee(self):
        numberOfEnemies = len(self.enemiesAround)

        if(numberOfEnemies < 1):
            raise Exception("No enemies around to flee from!")
        elif(numberOfEnemies > 1):
            return False

        threat = self.enemiesAround[0]
        threat_hp = threat[1]

        # If they are likely to explode.. FLEE!
        if(threat_hp < 10):
            #print "Flee: feind HP" + str(threat_hp) + "eig HP: " + str(self.hp) + "eig LOC: " + str(self.location)
            return True

        return False

    def getFleeLocation(self):
        numberOfEnemies = len(self.enemiesAround)

        if(numberOfEnemies < 1):
            raise Exception("No enemies around to flee from!")
        elif(numberOfEnemies > 1):
            raise Exception("To many enemies to flee from!")

        threat_loc = self.enemiesAround[0][0]

        flee_locations = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))

        for flee_location in flee_locations:
            if(flee_location not in self.game.robots):
                return flee_location

        # If no flee_location is available, flee nowhere..
        return self.location
        #if(threat_loc in flee_locations[0]):
        #    flee_location = flee_locations[1]
        #else:
        #    flee_location = flee_locations[0]

        #return flee_location

    def getAttackTarget(self):
        if(len(self.enemiesAround) < 1):
            raise Exception("No enemies around to target!")

        target = self.enemiesAround[0]

        # Attack enemy with lowest hp
        for (loc),hp in self.enemiesAround:
            if(hp < target[1] and hp >= 10): # dont attack robots with hp < 10 since they will explode anyway
                target[0] = loc
                target[1] = hp

        return target[0]

    def isSuicidal(self):
        if(self.hp < len(self.enemiesAround) * 10):
            return True
        return False

    def getRobotsAround2(self, loc, dist, onlyEnemies=True):
        result = []

        for botLoc, bot in self.game.robots.iteritems():
            if (not(onlyEnemies) or bot.player_id != self.player_id):
                if rg.wdist(botLoc, loc) <= dist:
                    result.append([botLoc, bot.hp])

        return result


    #TODO: TEST WITH DIST > 1
    def getRobotsAround(self, loc, dist, onlyEnemies=True):
        searchDistance = 1
        result = []

        for xrelative in range(dist*(-1), dist+1):
            x=xrelative+loc[0]
            bottom=loc[1]+(searchDistance/2)

            for y in range(bottom-searchDistance+1, bottom+1):
                if ((x,y) in self.game.robots) and (not(onlyEnemies) or self.game.robots[(x,y)].player_id != self.player_id):
                #if ((x,y) in rg.roboDict) and ((x,y) != loc) and rg.roboDict[(x,y)].player_id != self.player_id:
                    result.append([(x,y), self.game.robots[(x,y)].hp])
                    #print "gegner gefunden" + "x,y: " + str(x) + "," + str(y)
                    #print result

            if(x < loc[0]):
                searchDistance+=2
            else:
                searchDistance-=2

        return result
