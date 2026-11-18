import random
import math
class Agent:
    #agent class created inorder to initialise each world's agent object
    def __init__(self):
        self.agent="A"
        self.icon=""
        self.pos = ()
    
    def returnPos(self):
        return self.pos


##TASK 1 :
class World():
    #classWorld instantiates the grid,situates the agent,food objects and Goal
    #it also holds the other helper methods such as set_AgentPos and movement functions
    
    def locate_items(self):
        #function responsible for situating food objects randomly , same for goal 
        for piece in self.food_pieces:
            index1,index2= (random.randint(0,3),random.randint(0,5))
            while (self.grid[index1][index2] in self.food_pieces ) or  (self.grid[index1][index2] == self.agent.agent) :
                index1,index2= (random.randint(0,3),random.randint(0,5))
            self.grid[index1][index2]=piece
                
        goal_ind1,goal_ind2=(random.randint(0,3),random.randint(0,5))
        while (self.grid[goal_ind1][goal_ind2] != ".") or  (self.grid[goal_ind1][goal_ind2] == self.agent.agent):
            goal_ind1,goal_ind2=(random.randint(0,3),random.randint(0,5))
        self.grid[goal_ind1][goal_ind2]="G"
            
    def __init__(self):
        #6x4 grid marking GOAL created 
        self.grid=[[".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", "."],
                   [".", ".", ".", ".", ".", "."]]
        #agent created and situated randomly 
        self.agent=Agent()
        ind1,ind2= (random.randint(0,3),random.randint(0,5))
        self.agent.icon = "."  #icon at agent's current field
        self.grid[ind1][ind2]=self.agent.agent
        self.agent.pos=(ind1,ind2)
        self.food_pieces = ["🍎","🍉","🍓","🍪","🥐","🍕","🍔","🍟","🧁","🍩"]
        self.food_consumed=0    #TASK 2 : agent should keep track of food consumed
        self.locate_items()     #food and goal objects situated
            
    
    def print(self):
        #print method
        print("+"+"---+" * 6)
        for row in self.grid:
            print("| " + " | ".join(row))
            print("+"+"---+" * 6)
            
    def consume_food(self):
        #TASK 2 : food consumption method
        if ((self.agent.icon !="." )and (self.agent.icon != "G")):
            self.food_consumed += 1
            self.agent.icon="."
            
    def sense_goal(self):
        #TASK 2 : sense agent standing on goal
        if self.agent.icon=="G":
            return True
        return False
    
    
    def food_available(self):
        #method that returns a list of coordinates of the fields with food ojects in them
        #aka checks adjacent fields for food and returns result
        list_coords=[]
        ind1,ind2= self.agent.returnPos()
        if ((0<=ind1<=3) and (0<=ind2<=5)):
            west_pos= (ind1,ind2-1)
            east_pos= (ind1,ind2+1)
            north_pos= (ind1-1,ind2)
            south_pos= (ind1+1,ind2)
            directions = [west_pos,east_pos,north_pos,south_pos]
            for d in directions:
                pi_1,pi_2=d
                if (((0<=pi_1<=3) and (0<=pi_2<=5)) and (self.grid[pi_1][pi_2] not in [ ".","A","G"])):
                    list_coords.append(d)
        return list_coords
    
    
    def sense_food(self):
        #TASK 2 : sense food adjacent or below agent
        if self.food_available():
            return True
        return False
            
    def set_Pos(self,index1,index2):
        #helper method for movement functions - no food consumption version
        ind1,ind2=self.agent.pos
        self.grid[ind1][ind2]= self.agent.icon
        self.agent.icon=self.grid[index1][index2]
        self.grid[index1][index2]=self.agent.agent
        self.agent.pos=(index1,index2)
        
    ##TASK 2 Start - movement functions
    def moveAgentWestBouncy(self):
        #moves west - bouncy border
        pos1,pos2=self.agent.returnPos()
        if (pos2==0):
            pass
        else:
            index1,index2=pos1,pos2-1
            
            self.set_Pos(index1,index2)
        
            
    def moveAgentEastBouncy(self):
        #method to move agent east (right) and bounce back if at border
        
        pos1,pos2=self.agent.returnPos()
        if (pos2==5):
            pass
        else:
            index1,index2=pos1,pos2+1
            
            self.set_Pos(index1,index2)
            
    
    def moveNorthAroundTheWorld(self):
        #method to move agent north (up) and wrap around if at border
        
        pos1,pos2= self.agent.returnPos()
        if (pos1==0):
            pos1=3
            
            self.set_Pos(pos1,pos2)
        else:
            index1,index2=pos1-1,pos2
            
            self.set_Pos(index1,index2)
            
    def moveSouthAroundTheWorld(self):
        #method to move agent south (down) and wrap around if at border
        
        pos1,pos2 = self.agent.returnPos()
        if (pos1==3):
            pos1=0
            self.set_Pos(pos1,pos2)
        else:
            index1,index2=pos1+1,pos2
            
            self.set_Pos(index1,index2)
            
    ##TASK 2 End 
    
    ##TASK 3 Start - movement functions 
    def move_onestep(self,index1,index2):
        #helper for agentPlay where we move one step towards where food is - 50% chance of happening
        num=random.random()
        if num<0.5:
            i1,i2=self.agent.pos
            if index1<i1:
                self.moveNorthAroundTheWorld()
            elif index1>i1:
                self.moveSouthAroundTheWorld()
            elif index2<i2:
                self.moveAgentWestBouncy()
            elif index2>i2:
                self.moveAgentEastBouncy()
        else:
            pass
   
    def random_movement(self):
        #random movement function (one step) for agentPlay - 50% chance of happening
        num=random.random()
        if num<0.5:
            list_of_directions=["north","south","east","west"]
            direction=random.choice(list_of_directions)
            if direction=="north":
                self.moveNorthAroundTheWorld()
            elif direction=="south":
                self.moveSouthAroundTheWorld()
            elif direction=="east":
                self.moveAgentEastBouncy()
            elif direction=="west":
                self.moveAgentWestBouncy()
        else:
            pass
            
    ##TASK 3 End 
            
            
       
    def pick_min(self,list_c):
        list_dist=[]
        #pick the one which is at the least distance
        #and move towards that food object
        #helper method
        for i in range(len(list_c)):
            ind1,ind2=list_c[i]
            p1,p2=self.agent.pos
            dist = math.sqrt(((p1-ind1)**2) + ((p2-ind2)**2))
            list_dist.append((dist,i))
        min_d,indice = min(list_dist)
        result = list_c[indice]
        return result
    
            
    ##TASK 4 : agent follows order of priority therefore - does'nt make decisions but moves as per instructions
    ##         hence no user input decisions.
    def agent_Play(self):
        self.print()
        while not self.sense_goal() : #TASK 4 - if on the goal then stop episode
            #TASK 3 - if agent chooses consumption , it happens 100%
            #TASK 4 - if standing on food consume
            if self.agent.icon not in [".", "G"]:
                self.consume_food()

                
            
            elif self.sense_food() :
            #if adjacent to food fields move towards them one step at a time
            #TASK 4 - if food adjacent, move towards it
                avai = self.food_available()       
                index1,index2 = self.pick_min(avai)
                
                #TASK 3 - agent searches for adjacent food , chances of movement happening 50/50
                
                self.move_onestep(index1,index2)          
                
            else:
                #TASK 3 - agent moves randomly , chancs of movement happening 50/50
                #TASK 4 - otherwise move randomly
                
                self.random_movement() 
                
        #ending message shows food consumed        
        print("food consumed: ",self.food_consumed)
        self.print()
            
##reference tests##    
world=World()
world.agent_Play()

