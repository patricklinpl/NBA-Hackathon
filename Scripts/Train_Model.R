library(readr)

setwd("~/NBA-Hackathon/Business Analytics/Business Analytics")

# Import training set
train_edit_df <- read_delim("~/NBA-Hackathon/Business Analytics/Business Analytics/train_edit.csv", 
                         ";", escape_double = FALSE, col_types = cols(`Game Date` = col_date(format = "%Y-%m-%d"), 
                                                                              X1 = col_skip()), trim_ws = TRUE)

names(train_edit_df) <- c('GAME_ID', 'SEASON', 'GAME_DATE', 'AWAY_TEAM', 'HOME_TEAM', 'AWAY_TREND', 'HOME_TREND', 'VIEWERS')
train_edit_df <- data.frame(train_edit_df$GAME_ID, as.factor(train_edit_df$SEASON), train_edit_df$GAME_DATE, as.factor(train_edit_df$AWAY_TEAM), as.factor(train_edit_df$HOME_TEAM), train_edit_df$AWAY_TREND, train_edit_df$HOME_TREND, train_edit_df$VIEWERS)
names(train_edit_df) <- c('GAME_ID', 'SEASON', 'GAME_DATE', 'AWAY_TEAM', 'HOME_TEAM', 'AWAY_TREND', 'HOME_TREND', 'VIEWERS')

                        
# Regression Modeling
k <- 10
n <- nrow(train_edit_df)
ii <- (1:n) %% k + 1
set.seed(123)
N <- 100

mape.tr.one <- rep(0, N)
mape.tr.two <- rep(0, N)

for(i in 1:N) {
  ii <- sample(ii)
  pr.tr.one <- rep(0, n)
  pr.tr.two <- rep(0, n)

  print(i)
  for(j in 1:k) {
    x0 <- train_edit_df[ii != j, ]
    
    first_model <- lm(VIEWERS ~ I(AWAY_TEAM %in% c('GSW', 'CLE', 'OKC', 'HOU', 'LAL', 'BOS', 'SAS', 'PHI')) * I(HOME_TEAM %in% c('GSW', 'CLE', 'OKC', 'HOU', 'LAL', 'BOS', 'SAS', 'PHI')) * AWAY_TREND * HOME_TREND * I(GAME_DATE == 2016-12-25) * I(GAME_DATE == 2017-12-25) + I(2016-10-25 > GAME_DATE & GAME_DATE > 2017-01-31) + I(2017-10-17 > GAME_DATE & GAME_DATE > 2018-01-31), data=x0)
    second_model <- lm(VIEWERS ~ I(AWAY_TEAM %in% c('GSW', 'CLE')) * I(HOME_TEAM %in% c('GSW', 'CLE')) * I(GAME_DATE == 2016-12-25) * I(GAME_DATE == 2017-12-25) + I(AWAY_TEAM %in% c('GSW', 'CLE', 'OKC', 'HOU', 'LAL', 'BOS', 'SAS', 'PHI')) * I(HOME_TEAM %in% c('GSW', 'CLE', 'OKC', 'HOU', 'LAL', 'BOS', 'SAS', 'PHI')) * AWAY_TREND * HOME_TREND * I(GAME_DATE == 2016-12-25) * I(GAME_DATE == 2017-12-25) + I(2016-10-25 > GAME_DATE & GAME_DATE > 2017-01-31) + I(2017-10-17 > GAME_DATE & GAME_DATE > 2018-01-31), data=x0)
    
    
    pr.tr.one[ ii == j ] <- predict(first_model, newdata=train_edit_df[ii==j,])
    pr.tr.two[ ii == j ] <- predict(second_model, newdata=train_edit_df[ii==j,])

  }
  
  mape.tr.one[i] <- mean( abs((train_edit_df$VIEWERS - pr.tr.one)/train_edit_df$VIEWERS) )
  mape.tr.two[i] <- mean( abs((train_edit_df$VIEWERS - pr.tr.two)/train_edit_df$VIEWERS) )
  
}

boxplot(mape.tr.one, mape.tr.two, names=c('Preliminary Model', 'Secondary Model'), col=c('gray60', 'pink'), ylab='MAPE')