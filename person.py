import random

class Person:

    def __init__(self, id_, nps, created_at, activity_chance=1, product_stability_at_previous_rating=0, is_premier=False, is_spam=False):
        self.id = id_
        self.nps = nps
        self.activity_chance = activity_chance
        self.product_stability_at_previous_rating = product_stability_at_previous_rating
        self.is_premier = is_premier
        self.is_spam = is_spam
        self.created_at = created_at
        
    def set_activity_chance(self):
        # people are either inactive, normal, or superactive
        # if they are inactive, there is a 1% chance they will submit
        # if they are normal, there is 10% chance, if the are super active, there is 50%
        # there is a 10% chance that someone will become inactive, 80% that they will become normal
        # and 10% that they will become super active
        population = [0.01, 0.05, 0.2]
        activity_weights = [0.3, 0.6, 0.1]
        self.activity_chance = random.choices(
            population=population,
            weights=activity_weights
        )[0]        
        
    def get_nps(self, product_stability):
        experienced_difference = (product_stability - self.product_stability_at_previous_rating)
        self.product_stability_at_previous_rating = product_stability
        nps = self.nps # default to giving the same raiting as before
        
        if self.is_spam:  # robot signups always rate us badly
            return 0
        
        # same, better, worse, flip up, flip down
        case_weights =  [0.93, 0.025, 0.025, 0.01, 0.01]
        if experienced_difference == 1:
            case_weights = [0.60, 0.33, 0.01, 0.05, 0.01]
        elif experienced_difference == -1:
            case_weights = [0.60, 0.01, 0.33, 0.01, 0.05]
        elif experienced_difference >= 2:
            case_weights = [0.50, 0.40, 0.01, 0.8, 0.01]
        elif experienced_difference <= -2:
            case_weights = [0.1, 0.0, 0.0, 0.0, 0.9]
        case_weights =  [0.93, 0.025, 0.025, 0.01, 0.01]


        case = random.choices(
            population=[0,1,2,3,4],
            weights=case_weights
        )[0]
        
        if case == 0:
            nps = nps
        elif case == 1:
            nps = min(nps+1, 10)
        elif case == 2:
            nps =  max(nps-1, 0)
        elif case == 3:
            nps = 10
        elif case == 4:
            nps = 0
        else:
            raise Exception("Not accounted for")
        if self.is_premier:
            nps = min(nps+1, 10)
        self.nps = nps
        if nps > 10 or nps < 0:
            raise Exception("Invalid NPS")
        return nps 
