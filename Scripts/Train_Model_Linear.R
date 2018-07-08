# Regression Modeling
k <- 10
n <- nrow(train_with_win_lead)
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
    x0 <- train_with_win_lead[ii != j, ]
    
    first_model <- lm(VIEWERS ~ . , data=x0)
    second_model <- lm(VIEWERS ~ I(AWAY_TEAM %in% c("CLE", "GSW")) + I(HOME_TEAM %in% 
                                                                         c("CLE", "GSW")) + BROADCAST + OVERTIME + TIME + ATTENDANCE + 
                         AWAY_TREND + DAY + GAME_DATE + SEASON + HOME_TREND + DAY:SEASON + 
                         DAY:GAME_DATE + I(AWAY_TEAM %in% c("CLE", "GSW")):I(HOME_TEAM %in% 
                                                                               c("CLE", "GSW")) + TIME:GAME_DATE, data=x0)
    full_model <- lm(VIEWERS ~ . - GAME_ID, data=x0)
    
    
    
    pr.tr.one[ ii == j ] <- predict(first_model, newdata=train_with_win_lead[ii==j,])
    pr.tr.two[ ii == j ] <- predict(second_model, newdata=train_with_win_lead[ii==j,])
    pr.tr.full[ ii == j ] <- predict(full_model, newdata=train_with_win_lead[ii==j,])
    
  }
  
  mape.tr.one[i] <- mean( abs((train_with_win_lead$VIEWERS - pr.tr.one)/train_with_win_lead$VIEWERS) )
  mape.tr.two[i] <- mean( abs((train_with_win_lead$VIEWERS - pr.tr.two)/train_with_win_lead$VIEWERS) )
  mape.tr.full[i] <- mean( abs((train_with_win_lead$VIEWERS - pr.tr.full)/train_with_win_lead$VIEWERS) )
}

boxplot(mape.tr.one, mape.tr.two, mape.tr.full, names=c('Preliminary Model', 'Secondary Model', 'Full Model'), col=c('gray60', 'pink'), ylab='MAPE')