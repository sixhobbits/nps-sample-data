"""
Generates fake NPS data in two tables - `customer` and `score`

Assume a product that has launched recently and has some ups and downs, which affect NPS.

NPS is primarily driven by ratings of new customers, but once a customer exists, they have a chance to leave a rating every day.

Hard coded 'stability' and growth rates

Generates NPS data for 365 days

Writes the result to csv files
"""

from datetime import datetime
from datetime import timedelta

from person import Person
from nps_utils import *

DATE_START = datetime(2018,1,1)
DATE_END = datetime(2018,12,31)

GLOBAL_CUSTOMER_ID = 0  # to fake database IDs / primary keys

# average new customers joining per day, jan-dec
num_new_customers = [10, 50, 100, 150, 200, 300, 400, 600, 650, 700, 1000, 2000]

# in bad months, customers are more likely to leave lower scores
# in good months, customers are more likely to leave higher scores
very_bad = [+0.15, +0.08, +0.04, +0.003, +0.003, +0.003, +0.001,    -0.02,    -0.01,   -0.1, -0.15] 
bad = [+0.1, +0.01, +0.03, +0.003, +0.003, +0.003, +0.001,    0,    0,   -0.05, -0.1] 
normal = [0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0]
good = [-0.02, -0.035, -0.0005, -0.0005, +0.01, +0.003, +0.001,    -0.008,    -0.01,   +0.01, +0.05] 
very_good = [-0.03, -0.04, -0.0005, -0.0005, +0.0, +0.003, -0.01,    -0.029,    -0.03,   +0.057, +0.08] 

# product stability weights in any given month jan-dec -- starts out bad, gets better, dip in September then recovery
stability_weights = [very_bad, bad, normal, normal, normal, very_good, good, very_good, very_bad, good, very_good, very_good]

# matches the above but raw product stability = -2 = very bad, 2 = very good
stabilities = [-2, -1, 0, 0, 0, 2, 1, 2, -2, 1, 2, 2]

def get_n_with_jitter(n, jitter_percent=0.2):
    jitter = n * jitter_percent
    return random.randrange(n-jitter, n+jitter)

def get_new_customers(date, n=1000, weight_adjustment=normal, product_stability=0):
    global GLOBAL_CUSTOMER_ID
    initial_nps = generate_random_nps(get_adjusted_weights(BASE_WEIGHTS, weight_adjustment), num_samples=n)
    customers = []
    for j in range(n):
        is_premier = flip_coin(0.1)
        is_spam = flip_coin(0.01)
        person = Person(GLOBAL_CUSTOMER_ID, 
                initial_nps[j],
                created_at=date,
                product_stability_at_previous_rating=product_stability,
                is_premier=is_premier,
                is_spam=is_spam 
        )
        customers.append(person)
        GLOBAL_CUSTOMER_ID += 1
    return customers


def main():
    date = DATE_START
    customers = []
    scores = []

    while date < DATE_END:
        
        # get scores from existing customers
        stability = stabilities[date.month-1]
        reset_customer_activity = date.weekday() == 0  # reset customers on monday

        # add new customers
        stability_weight = stability_weights[date.month-1]
        n = get_n_with_jitter(num_new_customers[date.month-1])
        created_at = get_random_date(date, date+timedelta(days=1))
        customers += get_new_customers(created_at, n, stability_weight, stability)

        # get scores from existing customers
        for customer in customers:
            active = flip_coin(customer.activity_chance)
            if active:
                nps = customer.get_nps(stability)
                survey_date = get_random_date(date, date + timedelta(days=1))
                scores.append([customer.id, survey_date, nps])
                
            if reset_customer_activity:
                customer.set_activity_chance()       
                
        # if tomorrow is first day of month, then today is last day of month 
        # print out some stats for the previous month
        if (date + timedelta(days=1)).day == 1:  
            print("Date: {}".format(date))

            # scores for all surveys left this month
            month_scores = [score[2] for score in scores if score[1].month == date.month]

            # scores for all surveys left this month from customers who joined this month
            customer_month_scores = [score[2] for score in scores if score[1].month == date.month and 
                customers[score[0]].created_at.month == date.month
            ]

            print("nps based on scores this month (num responses)")
            print(calculate_nps(month_scores), "({})".format(len(month_scores)))
            print("nps based on scores this month from customers who joined this month (num respones)")
            print(calculate_nps(customer_month_scores), "({})".format(len(customer_month_scores)))
            print("------")

        date += timedelta(days=1)
         

    # write out to file
    with open("customer.csv", "w") as f:
        f.write("id,created_at,is_premier,is_spam\n")
        for customer in customers:
            f.write("{},{},{},{}\n".format(customer.id+1, customer.created_at, customer.is_premier, customer.is_spam))

            
    with open("score.csv", "w") as f:
        f.write("id,customer_id,created_at,score\n")
        for i, score in enumerate(scores):
            f.write("{},{},{},{}\n".format(i+1, score[0]+1, score[1], score[2]))

if __name__ == "__main__":
    main()
