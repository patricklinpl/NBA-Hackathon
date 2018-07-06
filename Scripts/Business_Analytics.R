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
train_edit_df <- data.frame(train_clean$Game_ID, train_clean$Season, as.Date(train_clean$Game_Date, format="%Y-%m-%d"), train_clean$Away_Team, train_clean$Home_Team, -1, -1, train_clean$Rounded.Viewers)
names(train_edit_df) <- c('Game_ID', 'Season', 'Game Date', 'Away Team', 'Home Team', 'Trend Away', 'Trend Home', 'Rounded.Viewers')




# Team List
team_list <- c('ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'WAS', 'UTA', 'TOR', 'SAS', 'SAC', 'POR', 'PHX')

# Assigning Trend Function (Modified for Daily Trends)
home <- 5
away <- 4
homeTrend <- 7
awayTrend <- 6

for (team in team_list) {
  print(team)
  
  # Team CSV Here
  trend_team <- read_delim(paste0("~/NBA-Hackathon/Business Analytics/Business Analytics/Google Trends Daily/multiTimeline ",team," (",2,").csv", sep =""), 
                           ",", escape_double = FALSE, col_types = cols(Day = col_date(format = "%Y-%m-%d")), 
                           trim_ws = TRUE)
  
  for (train in 1:nrow(train_edit_df)) {
    
    # 4 for Away, 5 for Home
    if (train_edit_df[train, home] == team) {
      
      # Trend CSV
      for (trend in 1:nrow(trend_team)) {
        
        if (train_edit_df[train, 3] == trend_team[trend, 1]) {
          
          # 6 for Away, 7 for Home
          value <- trend_team[trend,2]
          train_edit_df[train, homeTrend] <- value
          
        }
      }
    } else if (train_edit_df[train, away] == team) {
      
      # Trend CSV
      for (trend in 1:nrow(trend_team)) {
        
        if (train_edit_df[train, 3] == trend_team[trend, 1]) {
          
          # 6 for Away, 7 for Home
          value <- trend_team[trend,2]
          train_edit_df[train, awayTrend] <- value
          
        }
      }
    }
  }
}

# Weekday Addition
train_edit_df_day <- data.frame(train_edit_df$GAME_ID, as.character(train_edit_df$SEASON), train_edit_df$GAME_DATE, as.character(train_edit_df$AWAY_TEAM), as.character(train_edit_df$HOME_TEAM), train_edit_df$AWAY_TREND, train_edit_df$HOME_TREND, train_edit_df$VIEWERS, -1)
names(train_edit_df_day) <- c('GAME_ID', 'SEASON', 'GAME_DATE', 'AWAY_TEAM', 'HOME_TEAM', 'AWAY_TREND', 'HOME_TREND', 'VIEWERS', 'DAY')

for (train in 1:nrow(train_edit_df_day)) {
  if (train_edit_df_day[train, 3] == '2016-12-25' | train_edit_df_day[train, 3] == '2017-12-25') {
    train_edit_df_day[train, 9] <- 'Christmas Day'
  } else if (train_edit_df_day[train, 3] == '2016-01-01' | train_edit_df_day[train, 3] == '2017-01-01') {
    train_edit_df_day[train, 9] <- 'New Years Day'
  } else if (train_edit_df_day[train, 3] == '2016-11-23' | train_edit_df_day[train, 3] == '2017-11-22') {
    train_edit_df_day[train, 9] <- 'Day Before Thanksgiving'
  } else if (train_edit_df_day[train, 3] == '2016-11-25' | train_edit_df_day[train, 3] == '2017-11-24') {
    train_edit_df_day[train, 9] <- 'Black Friday'
  } else if (train_edit_df_day[train, 3] == '2017-01-16' | train_edit_df_day[train, 3] == '2018-01-15') {
    train_edit_df_day[train, 9] <- 'Martin Luther King Day'
  } else {
    day <- weekdays(train_edit_df_day[train, 3])
    train_edit_df_day[train, 9] <- day
  }
}

# Factorize
train_edit_df_day <- data.frame(train_edit_df$GAME_ID, as.character(train_edit_df$SEASON), train_edit_df$GAME_DATE, as.character(train_edit_df$AWAY_TEAM), as.character(train_edit_df$HOME_TEAM), train_edit_df$AWAY_TREND, train_edit_df$HOME_TREND, train_edit_df$VIEWERS, as.character(train_edit_df_day$DAY))
names(train_edit_df_day) <- c('GAME_ID', 'SEASON', 'GAME_DATE', 'AWAY_TEAM', 'HOME_TEAM', 'AWAY_TREND', 'HOME_TREND', 'VIEWERS', 'DAY')


# Broadcast Addition
train_edit_df_day_cast <- data.frame(train_edit_df$GAME_ID, as.character(train_edit_df$SEASON), train_edit_df$GAME_DATE, as.character(train_edit_df$AWAY_TEAM), as.character(train_edit_df$HOME_TEAM), train_edit_df$AWAY_TREND, train_edit_df$HOME_TREND, train_edit_df$VIEWERS, train_edit_df_day$DAY, -1, -1)
names(train_edit_df_day_cast) <- c('GAME_ID', 'SEASON', 'GAME_DATE', 'AWAY_TEAM', 'HOME_TEAM', 'AWAY_TREND', 'HOME_TREND', 'VIEWERS', 'DAY', 'TIME', 'BROADCAST')

library(hms)

for (train in 1:nrow(train_edit_df_day_cast)) {
  for (time in 1: nrow(X2017_2018_NBA_National)) {
    home_factor <- as.character(X2017_2018_NBA_National[time, 4]) 
    away_factor <- as.character(X2017_2018_NBA_National[time, 3])
    
    if (train_edit_df_day_cast[train,3] == X2017_2018_NBA_National[time, 1] & train_edit_df_day_cast[train,5] == home_factor & train_edit_df_day_cast[train,4] == away_factor) {
      train_edit_df_day_cast[train,10] <- X2017_2018_NBA_National[time, 2]
      train_edit_df_day_cast[train,11] <- X2017_2018_NBA_National[time, 5]
      break
    } 
  }
}


# Time and Broadcast Gap Addition

for (train in 1:nrow(temp)) {
  print(train)
  for (time in 1:nrow(temp_time)) {
    home_factor <- as.character(temp_time[time, 5]) 
    away_factor <- as.character(temp_time[time, 3])
    
    if (temp[train,3] == temp_time[time,1] & temp[train,5] == home_factor & temp[train,4] == away_factor) {
        temp[train,10] <- temp_time[time, 2]
        temp[train,12] <- temp_time[time, 9]
        if (temp_time[time, 8] == 'OT') {
          temp[train,13] <- temp_time[time, 8]
        }
        break
    }
  }
}

