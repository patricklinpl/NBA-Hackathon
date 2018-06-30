#NBA Hackathon Business Analytics
library(readr)

setwd("C:/Users/my_ma/Documents/NBA-Hackathon/Business Analytics/Business Analytics")
data.tr <- read.csv('training_set.csv')
data.te <- read.csv('test_set.csv')

train_clean <- read_csv("train.clean.csv", 
                        col_types = cols(Game_Date = col_date(format = "%m/%d/%Y"), 
                                         X1 = col_skip()))

# Change Team CSV here
trend_team <- read.table('GoogleTrendTest.txt.csv', header=TRUE, sep=',')
trend_team <- data.frame(as.Date(trend_team$Week, format="%Y-%m-%d"), trend_team$Atlanta.Hawks...United.States.)

# Get Train Edit
train_edit <- data.frame(train_clean$Game_ID, train_clean$Season, as.Date(train_clean$Game_Date, format="%Y-%m-%d"), train_clean$Away_Team, train_clean$Home_Team, -1, -1, train_clean$Rounded.Viewers)
names(train_edit) <- c('Game_ID', 'Season', 'Game Date', 'Away Team', 'Home Team', 'Trend Away', 'Trend Home', 'Rounded.Viewers')






# Team CSV Here
trend_team <- read_delim("C:/Users/my_ma/Documents/NBA-Hackathon/Business Analytics/Business Analytics/Google Trends/multiTimeline Washington Wizards.csv", 
                            ";", escape_double = FALSE, col_types = cols(Week = col_date(format = "%Y-%m-%d")), 
                            trim_ws = TRUE)

# Assigning Trend Function
isHome <- FALSE
if (isHome == FALSE) {
  home = 4
  homeTrend = 6
} else {
  home = 5
  homeTrend = 7
}

for (train in 1:nrow(train_edit)) {
  
  # 4 for Away, 5 for Home
  if (train_edit[train, home] == 'WAS') {
    
    # Check if train_edit is greater/equal to trend_test and less than the next trend_test
    for (trend in 1:nrow(trend_team)) {
      
      if (train_edit[train, 3] >= trend_team[trend, 1]) {
        
        if (!is.na(train_edit[train, 3] < trend_team[(trend+1), 1])) {
          
          # 6 for Away, 7 for Home
          value <- trend_team[trend,2]
          train_edit[train, homeTrend] <- value
          
        } else {
          
          # 6 for Away, 7 for Home
          value <- trend_team[trend,2]
          train_edit[train, homeTrend] <- value
          
        }
      }
    }
  }
}