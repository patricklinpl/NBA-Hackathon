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
n <- nrow(train_with_wins_entering)
ii <- (1:n) %% k + 1
set.seed(123)
N <- 100

mape.tr.one <- rep(0, N)
mape.tr.two <- rep(0, N)
mape.tr.full <- rep(0, N)

for(i in 1:N) {
  ii <- sample(ii)
  pr.tr.one <- rep(0, n)
  pr.tr.two <- rep(0, n)
  pr.tr.full <- rep(0, n)
  
  print(i)
  for(j in 1:k) {
    x0 <- train_with_wins_entering[ii != j, ]
    
    first_model <- lm(VIEWERS ~ . , data=x0)
    second_model <- lm(VIEWERS ~ I(AWAY_TEAM %in% c("CLE", "GSW")) + I(HOME_TEAM %in% 
                                                                         c("CLE", "GSW")) + BROADCAST + OVERTIME + TIME + ATTENDANCE + 
                         AWAY_TREND + DAY + GAME_DATE + SEASON + HOME_TREND + DAY:SEASON + 
                         DAY:GAME_DATE + I(AWAY_TEAM %in% c("CLE", "GSW")):I(HOME_TEAM %in% 
                                                                               c("CLE", "GSW")) + TIME:GAME_DATE, data=x0)
    full_model <- lm(VIEWERS ~ . - GAME_ID, data=x0)
    
    
    
    pr.tr.one[ ii == j ] <- predict(first_model, newdata=train_with_wins_entering[ii==j,])
    pr.tr.two[ ii == j ] <- predict(second_model, newdata=train_with_wins_entering[ii==j,])
    pr.tr.full[ ii == j ] <- predict(full_model, newdata=train_with_wins_entering[ii==j,])
    
  }
  
  mape.tr.one[i] <- mean( abs((train_with_wins_entering$VIEWERS - pr.tr.one)/train_with_wins_entering$VIEWERS) )
  mape.tr.two[i] <- mean( abs((train_with_wins_entering$VIEWERS - pr.tr.two)/train_with_wins_entering$VIEWERS) )
  mape.tr.full[i] <- mean( abs((train_with_wins_entering$VIEWERS - pr.tr.full)/train_with_wins_entering$VIEWERS) )
}

boxplot(mape.tr.one, mape.tr.two, mape.tr.full, names=c('Preliminary Model', 'Secondary Model', 'Full Model'), col=c('gray60', 'pink'), ylab='MAPE')