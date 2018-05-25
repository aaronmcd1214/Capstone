# Predicting Player Performance
This project is an attempt to use multiple predictive models to predict a baseball player's performance, specifically batting 
average.

## The Problem
I approached this problem from the point of view of a General Manager. In Major League Baseball, baseball players are 
typically eligible for free agency after reaching 6 years of Major League service so as a GM, I would need to be able to 
project player performance of free agents to determine whether or not I'm interested in signing them and for how much money
I'm interested in signing them for. To get this projection, at least for the next year after free agency, I collected all
the players that had at least 7 years of history; the first 6 to train the models and make a prediction, the 7th to be
able to compare my predictions too but a trained model could certainly predict on a player with only 6 years of history.

## Data
Data was obtained from www.seanlahman.com* in the form of .csv files.  More specifically, I used the Batting and Fielding files.
I used the Fielding file to map each player's most common position to their statistics in the Batting file. To work with 
the data, I imported the .csv files into Python Pandas Dataframes.

## Models
For my prediction models I chose to use the Decision Tree and Random Forest models from Sci-Kit Learn's library as well 
as a Long Short Term Memory model using Keras with a Tensor Flow backend.

## Results
Overall, it appears that the Random Forest model worked the best as you can see from the metrics below. For the Decision 
Tree and Random Forest models I was able to do some basic feature omittance by training on all features and then removing 
the features with an importance level less than or equal to 0. It is certainly possible that the LSTM model could perform 
much better had I done something similar to this with it, something I plan to implement in the future. For now, though, 
here are the metrics that I've gotten from each of the models:

Decision Tree:<br />
MSE:  0.0009244<br />
RMSE: 0.0304032<br />
R2:   0.399<br />

Random Forest:<br />
MSE:  0.0007535<br />
RMSE: 0.0274505<br />
R2:   0.496<br />

LSTM:
MSE:  0.0010391<br />
RMSE: 0.0322347<br />
R2:   0.304<br />

_\*This database is copyright 1996-2018 by Sean Lahman.
This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. 
For details see: http://creativecommons.org/licenses/by-sa/3.0/_
