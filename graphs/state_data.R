library(googleVis)
library(ggplot2)
#require(datasets)
states <- read.csv("../metrics/state_distribution.csv")
GeoStates <- gvisGeoChart(states, "X", "state",
                          options=list(region="US", 
                                       displayMode="regions", 
                                       resolution="provinces",
                                       width=600, height=400))
plot(GeoStates)

titles <- read.csv("../metrics/title_distribution.csv")
titles <- titles[-8,]
colnames(titles) = c("title", "count")

p<-ggplot(titles, aes(x=title, y=count, fill=title)) +
  geom_bar(stat="identity")+theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())

p
