#NBA Hackathon Business Analytics

setwd("C:/Users/my_ma/Documents/NBA-Hackathon/Business Analytics/Business Analytics")
data.tr <- read.csv('training_set.csv')
data.te <- read.csv('test_set.csv')
player <- read.csv('player_data')
game <- read.csv('game_data.csv')

#Collapse data.tr on Rounded Viewers and remove Country -> train.clean

#Focus on Match-Ups