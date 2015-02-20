#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt

class bicycle(StateSpace):
    def __init__(self, action, gval, curr_jobs, curr_location, curr_time, money_earned, unstarted_jobs, map, parent):
#IMPLEMENT
        '''Initialize a bicycle search state object.'''
        if action == 'START':   #NOTE action = 'START' is treated as starting the search space
            StateSpace.n = 0
        StateSpace.__init__(self, action, gval, parent)
        #implement the rest of this function.
        self.curr_jobs = curr_jobs
        self.curr_location = curr_location
        self.curr_time = curr_time
        self.money_earned = money_earned
        self.unstarted_jobs = unstarted_jobs
        self.map = map
        
    def successors(self): 
#IMPLEMENT
        '''Return list of bicycle objects that are the successors of the current object'''
        '''time weight '''
        states = list()
        if self.curr_location == "home":
            for i in range(len(self.unstarted_jobs)):
                curr_jobs = self.curr_jobs[:]
                curr_jobs.append(self.unstarted_jobs[i])
                unstarted_jobs = self.unstarted_jobs[:]
                unstarted_jobs.remove(self.unstarted_jobs[i])
                states.append(bicycle
                              ("first_pickup", self.gval,
                               curr_jobs, self.unstarted_jobs[i][1],
                               self.unstarted_jobs[i][2], self.money_earned, unstarted_jobs, self.map, self
                               )
                              )
        else:
            for i in range(len(self.unstarted_jobs)):
                if (not self.unstarted_jobs[i][1] in self.checker()):
                    if((self.get_load() + self.unstarted_jobs[i][4] <= 10000) and
                       (max((self.unstarted_jobs[i][2] + dist(self.unstarted_jobs[i][1],self.unstarted_jobs[i][3], self.map)),
                            (self.curr_time + dist(self.curr_location,self.unstarted_jobs[i][1], self.map) + dist(self.unstarted_jobs[i][1],self.unstarted_jobs[i][3], self.map)))
                        ) <= 1140):
                        curr_time = self.curr_time + dist(self.curr_location,self.unstarted_jobs[i][1], self.map)
                        if(curr_time < self.unstarted_jobs[i][2]):
                            curr_time = self.unstarted_jobs[i][2]
                        curr_jobs = self.curr_jobs[:]
                        curr_jobs.append(self.unstarted_jobs[i])
                        unstarted_jobs = self.unstarted_jobs[:]
                        unstarted_jobs.remove(self.unstarted_jobs[i])
                        states.append(bicycle
                                      ("pickup", self.gval,
                                       curr_jobs, self.unstarted_jobs[i][1],
                                       curr_time, self.money_earned, unstarted_jobs, self.map, self
                                       )
                                      )
            for i in range(len(self.curr_jobs)):
                real_payoff = 0
                curr_time = self.curr_time + dist(self.curr_location,self.curr_jobs[i][3], self.map)
                if((self.get_load() <= 10000) and curr_time <= 1140):
                    money_earned = self.money_earned
                    for j in range(len(self.curr_jobs[i][5])):
                        if (curr_time <= self.curr_jobs[i][5][j][0]):
                            money_earned = money_earned + self.curr_jobs[i][5][j][1]
                            real_payoff = self.curr_jobs[i][5][j][1]
                            break
                    curr_jobs = self.curr_jobs[:]
                    unstarted_jobs = self.unstarted_jobs[:]
                    curr_jobs.remove(curr_jobs[i])
                    states.append(bicycle("deliver", self.gval + (self.curr_jobs[i][5][0][1] - real_payoff),
                                             curr_jobs, self.curr_jobs[i][3],
                                             curr_time, money_earned, unstarted_jobs, self.map, self
                                             )
                                      )
                    
        return states

    def checker(self):
        names = []
        for i in range(len(self.curr_jobs)):
            names.append(self.curr_jobs[i][3])
        return names
    
    def money_earn(self, jobs, time):
        for i in jobs[5]:
             if i[0] >= time:
                return i[1]
        return 0
    
    def hashable_state(self) :
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        return (str(self.curr_jobs), self.curr_location, self.curr_time, self.money_earned, str(self.unstarted_jobs))
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("    Carrying: {} (load {} grams)".format(
                      self.get_carrying(), self.get_load()))
        print("    State time = {} loc = {} earned so far = {}".format(
                      self.get_time(), self.get_loc(), self.get_earned()))
        print("    Unstarted Jobs.{}".format(self.get_unstarted()))

    def get_loc(self):
#IMPLEMENT
        '''Return location of courier in this state'''
        return self.curr_location
    
    def get_carrying(self):
#IMPLEMENT
        '''Return list of NAMES of jobs being carried in this state'''
        name_list = []
        for i in range(len(self.curr_jobs)):
            name_list.append(self.curr_jobs[i][0])
        return name_list
    
    def get_load(self):
#IMPLEMENT
        '''Return total weight being carried in this state'''
        curr_weight = 0
        for i in range(len(self.curr_jobs)):
            curr_weight += self.curr_jobs[i][4]
        return curr_weight
    
    def get_time(self):
#IMPLEMENT
        '''Return current time in this state'''
        return self.curr_time
    
    def get_earned(self):
#IMPLEMENT
        '''Return amount earned so far in this state'''
        return self.money_earned
    
    def get_unstarted(self):
#IMPLEMENT
        '''Return list of NAMES of jobs not yet stated in this state'''
        name_list = []
        for i in range(len(self.unstarted_jobs)):
            name_list.append(self.unstarted_jobs[i][0])
        return name_list
    
def heur_null(state):
    '''Null Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_sum_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #Sum over every job J being carried: Lost revenue if we
    #immediately travel to J's dropoff point and deliver J.
    #Plus 
    #Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    sum_of_carried = 0
    sum_of_unstarted = 0
    curr_time = state.curr_time
    for i in range(len(state.curr_jobs)):
        curr_time = curr_time + dist(state.curr_location, state.curr_jobs[i][3], state.map)
        sum_of_carried = sum_of_carried + (state.curr_jobs[i][5][0][1] - state.money_earn(state.curr_jobs[i],curr_time))
    for i in range(len(state.unstarted_jobs)):
        if(curr_time +  dist(state.curr_location, state.unstarted_jobs[i][1], state.map) <= state.unstarted_jobs[i][2]):
            curr_time = state.unstarted_jobs[i][2] + dist(state.unstarted_jobs[i][1], state.unstarted_jobs[i][3], state.map)
        else:
            curr_time = state.curr_time + dist(state.curr_location, state.unstarted_jobs[i][1], state.map) + dist(state.unstarted_jobs[i][1], state.unstarted_jobs[i][3], state.map)
        sum_of_unstarted = sum_of_unstarted + (state.unstarted_jobs[i][5][0][1] - state.money_earn(state.unstarted_jobs[i],curr_time))
    return (sum_of_carried + sum_of_unstarted)


def heur_max_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff
    #point and deliver J.
    #m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup 
    #point then to J's dropoff poing and then deliver J.
    #heur_max_delivery_costs(state) = max(m1, m2)
##    max_of_carried = 0
##    max_of_unstarted = 0
##    curr_time = state.curr_time
##    for i in range(len(state.curr_jobs)):
##        curr_time = curr_time + dist(state.curr_location, state.curr_jobs[i][3], state.map)
##        max_of_carried = max(max_of_carried ,(state.curr_jobs[i][5][0][1] - state.money_earn(state.curr_jobs[i],curr_time)))
##    for i in range(len(state.unstarted_jobs)):
##        if(curr_time +  dist(state.curr_location, state.unstarted_jobs[i][1], state.map) <= state.unstarted_jobs[i][2]):
##            curr_time = state.unstarted_jobs[i][2] + dist(state.unstarted_jobs[i][1], state.unstarted_jobs[i][3], state.map)
##        else:
##            curr_time = curr_time + dist(state.curr_location, state.unstarted_jobs[i][1], state.map) + dist(state.unstarted_jobs[i][1], state.unstarted_jobs[i][3], state.map)
##        max_of_unstarted  = max(max_of_unstarted,(state.unstarted_jobs[i][5][0][1] - state.money_earn(state.unstarted_jobs[i],curr_time)))
##    return max(max_of_carried,max_of_unstarted)
    
    max_of_carried = 0
    max_of_unstarted = 0
    time = 0
    for j in state.curr_jobs:
        max_of_carried = max(max_of_carried, j[5][0][1] - state.money_earn(j, state.curr_time + dist(state.curr_location, j[3], state.map)))
    for i in state.unstarted_jobs:
        if (state.curr_time + dist(state.curr_location, i[1], state.map)) < i[2]: 
            time = i[2]
        else:
            time = state.curr_time + dist(state.curr_location, i[1], state.map)
        time += dist(i[1], i[3], state.map)
        max_of_unstarted = max(max_of_unstarted,(i[5][0][1] - state.money_earn(i, time)))
    return max(max_of_carried, max_of_unstarted)

def bicycle_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal (where all jobs have been delivered)?'''
    return (not state.unstarted_jobs) and (not state.curr_jobs)

def make_start_state(map, job_list):
#IMPLEMENT
    '''Input a map list and a job_list. Return a bicycle StateSpace object
    with action "START", gval = 0, and initial location "home" that represents the 
    starting configuration for the scheduling problem specified'''
    return bicycle("START",0,[],"home",420,0,job_list,map,None)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_map(nlocs):
    '''Generate a random collection of locations and distances 
    in input format'''
    lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
    lpairs = list(set(lpairs))  #remove duplicates
    nlocs = len(lpairs)
    lnames = ["loc{}".format(i) for i in range(nlocs)]
    ldists = list()

    for i in range(nlocs):
        for j in range(i+1, nlocs):
            ldists.append([lnames[i], lnames[j],
                           int(round(euclideandist(lpairs[i], lpairs[j])))])
    return [lnames, ldists]

def dist(l1, l2, map):
    '''Return distance from l1 to l2 in map (as output by make_rand_map)'''
    ldist = map[1]
    if l1 == l2:
        return 0
    for [n1, n2, d] in ldist:
        if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
            return d
    return 0
    
def euclideandist(p1, p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
    '''input a map (as output by make_rand_map) object and output n jobs in input format'''
    jobs = list()
    for i in range(njobs):
        name = 'Job{}'.format(i)
        ploc = map[0][randint(0,len(map[0])-1)]
        ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
        dloci = randint(0, len(map[0])-1)
        if map[0][dloci] == ploc:
            dloci = (dloci + 1) % len(map[0])
        dloc = map[0][dloci]
        weight = randint(10, 5000)
        job = [name, ploc, ptime, dloc, weight]
        payoffs = list()
        amount = 50
        #earliest delivery time
        time = ptime + dist(ploc, dloc, map)
        for j in range(randint(1,5)): #max of 5 payoffs
            time = time + randint(5, 120) #max of 120mins between payoffs
            amount = amount - randint(5, 25)
            if amount <= 0 or time >= 19*60:
                break
            payoffs.append([time, amount])
        job.append(payoffs)
        jobs.append(job)
    return jobs

def test(nloc, njobs):
    map = make_rand_map(nloc)
    jobs = make_rand_jobs(map, njobs)
    print("Map = ", map)
    print("jobs = ", jobs)
    s0 = make_start_state(map, jobs)
    print("heur Sum = ", heur_sum_delivery_costs(s0))
    print("heur max = ", heur_max_delivery_costs(s0))
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)
    

