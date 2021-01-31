from C19SimUtils import Utils
import agentpy as ap
import networkx as nx
import random
from scipy.stats import bernoulli

class Person(ap.Agent):
  '''
  A person class
  '''
  def setup(self):
    '''
    instantiate the agent
    '''
    u = Utils()
    self.condition = 0 # start of as healthy
    self.age = u.get_age()
    self.prob_death = u.get_death_prob(self.age)
    self.recovery_time = random.randint(14,21) # model the period a patient is infective
    self.infected_ts = 0

  def being_sick(self):
    """
    Being able to transfer disease to peers on a network
    """
    
    for n in self.neighbors():
      if self.condition != 3 and self.condition !=4 : # if not vaccinated or there is a chance of transmitting  c19
        if self.condition == 1:
          if n.condition!=3 and self.p.infection_chance > random.random():  #cannot get disease if vaccinated
            n.condition = 1           # thats where  the self infects a neighbor who is not vaccinated
            n.infected_ts = n.model.t
            

    #  determine death or recovery for the self:

    if (self.condition == 1 and self.model.t >= self.infected_ts + self.recovery_time):
          self.condition = 2
          #print('infected  at:{0} recovered at:{1}'.format(self.infected_ts,self.model.t))
    else: 
      if self.condition ==1 and self.prob_death > random.random():
        self.die()
      

      
  def get_vaccinated(self):
    '''
    A step to get vaccinated (state = 3)
    '''
    if self.condition == 0 and self.p.vax_chance > random.random(): # only vaccinate the health with no history of c19
      self.condition = 3
  
  def die(self):
    '''
    a note that dies given they are ill (condition = 4)
    '''
    self.condition = 4

  def hospitalized(self):
    '''
    Another state denoting  being hospitalized
    '''
    self.condition = 5




class VirusModel(ap.Model):

  def setup(self):
    """
    Initialize the agents and netowkrs of model
    """
    #self.p.population = p.population
    self.graph = nx.watts_strogatz_graph(self.p.population,
                                    self.p.number_of_neighbors,
                                    self.p.network_randomness
    )

    #create agents and Network
    
    self.add_agents(self.p.population,Person)
    self.add_network(graph = self.graph, agents = self.agents)
    
    #Infect a random share of the population
    I0 = int(self.p.initial_infections * self.p.population)
    self.agents.random(I0).condition = 1


  def update(self):
      """ Records variables after setup and each step. """
      # Record share of agents with each condition
      for i, c in enumerate(('S', 'I', 'R','V','D')):
          self[c] = (len(self.agents.select(self.agents.condition == i))
                      / self.p.population)
          self.record(c)

      # Stop simulation if disease is gone
      if self.I == 0 or self.t >self.p.steps:
          self.stop()

  def step(self):
        """ Defines the models' events per simulation step. """
        # Call 'being_sick' for infected agents
        self.agents(self.agents.condition==1).being_sick()
        # call 'get_vaccinated' only for healthy agents
        self.agents(self.agents.condition == 0).get_vaccinated()
        

  def end(self):
      """ Records evaluation measures at the end of the simulation. """
      # Record final evaluation measures
      self.measure('Total share infected', self.I + self.R)
      self.measure('Peak share infected', max(self.log['I']))
      self.measure('Share of vaccinated',self.V)
      self.measure('Mortality Rate', self.D)


##
parameters = {
    'population': 3000,
    'vax_chance':0.01,
    
    'infection_chance': 0.01,
    'recovery_chance': 0.05,
    'initial_infections': 0.2,
    'number_of_neighbors': 5,
    'network_randomness': 0.3,
    'steps':150
}

model = VirusModel(parameters)
results = model.run()
print(results.measures)