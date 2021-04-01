setwd("~/DATS1M/Q2/SINF2275 - Data mining and decision making/GitHub/Projet-1-SINF2275")

library(ggplot2)
theme_set(theme_bw())

############################
# empirical vs theoretical #
############################

squares = c(1:14)

expTrue = c(14.07014607, 13.40348304, 11.4034907 , 12.47367008, 11.03069297,
         9.61841567,  8.        ,  6.        ,  4.        ,  2.        ,
         7.85964323,  5.85964498,  3.85964622,  2. )

expFalse = c(13.58640836, 12.91974496, 10.91975186, 11.85689378, 10.38481428,
             8.96422179,  7.33333333,  5.33333333,  3.33333333,  1.33333333,
             7.66583266,  5.66583469,  3.66583611,  2. )

empCostTrue = c(13.767288, 13.092932751599333, 11.10008, 11.92851202314229, 
                10.468895713156913, 9.489897657569331, 7.996686589315401, 
                6.003039499493676, 4.001069041252152, 2.0020760818725196, 
                7.978325971400763, 5.966017556637405, 3.96924742286187, 2.003546725162418)

empCostFalse = c(13.294082, 12.609393588972663, 10.625866, 11.329465408528488, 
                 9.83053340361497, 8.830713247182729, 7.3219214216298765, 
                 5.333029239943324, 3.333748309624548, 1.3340894866409825, 
                 7.748332809608603, 5.773064954220855, 3.789260558191624, 2.0078440614058715)

costTrue = c(expTrue, empCostTrue)
costFalse = c(expFalse, empCostFalse)
themp = c(rep("Theoretical", 14), rep("Empirical", 14), 
          rep("Theoretical", 14), rep("Empirical", 14))

df1 = as.data.frame(cbind(squares, costTrue, costFalse, themp))

df1$costTrue = as.numeric(costTrue)
df1$costFalse = as.numeric(costFalse)
df1$squares = as.numeric(squares)

df1$themp <- factor(df1$themp,
                       levels = c('Theoretical', 'Empirical'), 
                       ordered = TRUE)

png("~/DATS1M/Q2/SINF2275 - Data mining and decision making/GitHub/Projet-1-SINF2275/barplot False.png", 
    units="in", width=6, height=5, res=600)

ggplot(df1) + aes(x=squares, y=costFalse, fill = themp) +
  geom_bar(stat="identity", color = "black", 
           width = 0.5, position="dodge") +
  labs(title = "Theoretical cost vs. Empirical cost",
       subtitle = "circle = False") +
  xlab("Number of the square") +
  ylab("Average cost") +
  guides(fill=guide_legend("")) +
  theme(legend.position="bottom")

dev.off()


png("~/DATS1M/Q2/SINF2275 - Data mining and decision making/GitHub/Projet-1-SINF2275/barplot True.png", 
    units="in", width=6, height=5, res=600)

ggplot(df1) + aes(x=squares, y=costTrue, fill = themp) +
  geom_bar(stat="identity", color = "black", 
           width = 0.5, position="dodge") +
  labs(title = "Theoretical cost vs. Empirical cost",
       subtitle = "circle = True") +
  xlab("Number of the square") +
  ylab("Average cost") +
  guides(fill=guide_legend("")) +
  theme(legend.position="bottom")

dev.off()

############################
# Bxoplot diff strategies  #
############################

# --- Circle = True --- #

df3 = read.csv("distTrue.csv", sep = ",")
df3 = df3[,-1]

turnsTrue = c(df3$Optimal, df3$Security, df3$Normal,
              df3$Risky, df3$Random)

dfTrue = as.data.frame(cbind(strategy, turnsTrue))
dfTrue$turnsTrue = as.numeric(turnsTrue)
dfTrue$strategy <- factor(dfTrue$strategy,
                       levels = c('Optimal', 'Security','Normal', 'Risky', 'Random'), 
                       ordered = TRUE)

png("boxplot true.png", units="in", width=6, height=5, res=600)

ggplot(dfTrue) + aes(x = strategy, y = turnsTrue) +
  geom_boxplot(fill = "grey", outlier.shape = NA) +
  labs(title = "Distribution of simulated games using different strategies",
       subtitle = "circle = True") +
  stat_summary(fun = mean, geom = "point", show.legend = F,
               shape = 18, color = "red", size = 3) +
  xlab("Strategy") +
  ylab("Number of turns") +
  coord_cartesian(ylim = c(0, 200))

dev.off()

# --- Circle = False --- #

df4 = read.csv("distFalse.csv", sep = ",")
df4 = df4[,-1]

turnsFalse = c(df4$Optimal, df4$Security, df4$Normal,
              df4$Risky, df4$Random)

dfFalse = as.data.frame(cbind(strategy, turnsFalse))
dfFalse$turnsFalse = as.numeric(turnsFalse)
dfFalse$strategy <- factor(dfFalse$strategy,
                          levels = c('Optimal', 'Security','Normal', 'Risky', 'Random'), 
                          ordered = TRUE)

png("boxplot false.png", units="in", width=6, height=5, res=600)

ggplot(dfFalse) + aes(x = strategy, y = turnsFalse) +
  geom_boxplot(fill = "grey", outlier.shape = NA) +
  labs(title = "Distribution of simulated games using different strategies",
       subtitle = "circle = False") +
  stat_summary(fun = mean, geom = "point", show.legend = F,
               shape = 18, color = "red", size = 3) +
  xlab("Strategy") +
  ylab("Number of turns") +
  coord_cartesian(ylim = c(0, 100))

dev.off()

# --- Human Brain --- #

humanDist = read.csv("distHuman.csv", sep = ",")[,2]

costHuman = c(df4$Optimal, humanDist)
strat2 = c(rep("Optimal", 1000000), rep("Human", 1000000))

df5 = as.data.frame(cbind(strat2, costHuman))

df5$costHuman = as.numeric(costHuman)
df5$strat2 = factor(df5$strat2,
                    levels = c('Optimal', 'Human'), 
                    ordered = TRUE)

png("boxplot human.png", units="in", width=7, height=5, res=600)

ggplot(df5) + aes(x = strat2, y = costHuman) +
  geom_boxplot(fill = "grey", outlier.shape = NA) +
  labs(title = "Optimal policy vs. Human based policy",
       subtitle = "circle = False") +
  stat_summary(fun = mean, geom = "point", show.legend = F,
               shape = 18, color = "red", size = 3) +
  xlab("Strategy") +
  ylab("Number of turns") +
  coord_cartesian(ylim = c(0, 37.5))

dev.off()




