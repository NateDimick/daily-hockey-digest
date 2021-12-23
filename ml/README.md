# Machine Learning

I think this application has a lot of promise as my first ML application.

The goal is to use stats as inputs and to get betting recommendation (BTTS, Under 9.5, either, or no bet) as an output.

then my stupid brain isn't making the picks, a computer is.

already played games will be classified as such:

* if the total score is under 10 and either team scores 0 or 1 goals, then the recommendation should be U 9.5.
* if both teams score at least 2 goals each and the total is between 5 and 7 inclusive, then the recommendation should be either bet.
* if both teams score at least 2 goals each and the total number of goals is greater than 7, then BTTS is the recommendation
* if the total is greater than 9 and one team score 0 or 1 goals, the bet best should be no bet.
