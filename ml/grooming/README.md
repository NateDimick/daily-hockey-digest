# Machine Learning - Data Grooming

The idea here is to use the data from the requests from the collection module to pluck out the relevant stats as well as calculate new stats. These stats may or may not be used as inputs to the learning model.

Stats provided include:

* number of goals scored
* number of shot attempts
* giveaways and takeaways
* hits
* power play opportunities/goals
* date
* faceoffs (if that is deemed relevant)

Stats that can be derived:

* goals per game
* goals per game allowed
* shots per game
* shots per game allowed
* shooting percent
* save percent
* shutout percent
* power play %
* goals/shots scored above opponent average
* goals/shots allowed above opponent scoring average
* days/hours since last game
* distance travelled since last game

Try to find a relationship between each of the above and determine which should go in the input tensor
