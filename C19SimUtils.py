import random

class Utils():
  '''
  A set of helper methods
  '''
  def __init__(self):
    '''
    get density function for age
    '''
    age_table = {'Age_85': 815,
                'Age_80_84': 1026,
                'Age_75_79': 1498,
                'Age_70_74': 2440,
                'Age_65_69': 2271,
                'Age_Less15': 10842,
                'Age_15_24': 7192,
                'Age_25_34': 7064,
                'Age_35_64': 22052,
                'Age_65_74': 4711}
    age_table['Age_85_100'] = age_table['Age_85']
    age_table['Age_0_15'] = age_table['Age_Less15']
    #
    age_table.pop('Age_85')
    age_table.pop('Age_Less15')
    #

    sum_age = sum(age_table.values())
    self. dens_age = {self.parse_age(k):v/sum_age for k,v in age_table.items() }
    #
    '''
    get denstiy function for death from COVID( covid.cdc.gov/covid-data-tracker/#demographics)
    '''
    self.dens_death = {
      (0,4):0,
      (5,17):0.001,
      (18,29):0.005,
      (30,39):0.12,
      (40,49):0.028,
      (50,64):0.143,
      (65,74):0.209,
      (75,84):0.275,
      (85,100):0.327
    }



  def parse_age(self, string):
    '''
    A method to parse the age range from the string
    '''
    return (int(string.split('_')[1]),int(string.split('_')[2]))


  def get_age(self):
    '''
    A method to return  a density of ages
    '''
    age_list = list(self.dens_age.keys())
    dist = list(self.dens_age.values())
    #
    l,u  = random.choices(age_list,dist)[0]
    return random.randint(l,u)

  def get_death_prob(self,age):
    '''
    return the age range and prob of death given an age
    '''
    for k  in self.dens_death.keys():      
      if age >= k[0] and age <= k[1] :        
        return self.dens_death[k]
  


          
