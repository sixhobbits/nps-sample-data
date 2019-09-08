# Sample Net Promoter Score data

This is some basic Python code to generate random Net Promoter Score (NPS) survey data. 
NPS is a metric used in many industries to track customer satisfaction. It is tracked by asking customers 
"How likely would you be to recommend <product> to a friend or family member" and customers leave a rating 
on a scale of 0 - 10.

Customers who rate your product in the range 0-6 are labeled 'detractors'. They are telling others not to use your product 
and are unlikely to be repeat customers

Customers who rate your product 7 or 8 are 'passives'. They are not promoting your product to their networks, but nor are 
they advising people to stay away

Customers who give you a 9 or a 10 'promoters' - they are actively promoting your product and are likely to become return customers. 

NPS is calculated as promoters/customers - detractors/customers -- so the percentge of promoters minus the percentage of detractors. 

Passives are not directly used in the calculation but they do affect the percentages -- having more passives is better than 
having more detractors as they do not count against your promoters. 

## Using the data

The two csv files `customer.csv` and `scores.csv` can be used as-is. They are simple CSV files with the following fields

```
customer.csv
------------
- id  (a primary key)
- created_at (the date the customer signed up)
- is_premier (whether or not the customer is on a 'premier' plan - these customers leave slightly higher scores
- is_spam (whether or not the customer has been identified as a spam account. Spam accounts always leave ratings of 0)


score.csv
----------
- id (a primary key)
- customer_id - the relevant id from customer.csv to show which customer left this score
- created_at - the date the score was left
- score - the value between 0 (very unlikely) and 10 (very likely) of how likely the customer is to recommend your product
```

## Using the code
The code is work in progress, but at the moment is structured as follows:

The `person.py` file is a class representing a customer. A customer joins at a specific date and has a given probabilty of
responding to the survey each day. Customers can be active, normal, or super active, which affects how often they respond 
to the survey. We tell the person the current product stability when getting an NPS score from them, and this also affects
the score they leave, along with whether or not they are a spam account and whether or not they have signed up for a premier plan.

The `nps_utils.py` file contains a bunch of functions for generating random NPS scores, calculating NPS, and other probability 
related functions for helping with the modelling.

The `generate_nps.py` file uses the Person class and the nps_utils functions to model a specific product. This product starts 
off in January 2018 doing pretty badly and being unstable. With very few customers, NPS in the first month is bad (0-10). The product grows 
in features and stability, getting higher and higher NPS (and new customers) each day. In September, things go badly and NPS drops 
sharply as a result, before recovering to new highs (70+) before the end of the year

Note that there are currently a lot of hard coded values that need to be moved into a structure that is easier to configure, 
including the growth rate and base weightings for generating NPS scores.

## License 

MIT

