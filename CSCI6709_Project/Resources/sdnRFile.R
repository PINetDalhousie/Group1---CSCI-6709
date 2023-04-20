#
#@author: Nathanael Timothy Bowley
#@Banner ID: B00742839
#@Course: Software Defined Networking 
#@Version: 1
#@Date: 4/18/2023 (MM/DD/YYYY)
#@Description: This code uses the sdnData.txt from our trails to generate two figures
# the first of which shows the overall trends in the f1_scores for Traffic variables by rounds and epochs.
# the second removes round 5 data and udp to show a better comparison between data.
#
library(tidyverse)

dataFrame <- read.table("sdnData.txt", header=TRUE, sep="\t", stringsAsFactors = TRUE)
dataFrame

glimpse(dataFrame)
summary(dataFrame)

dataFrameTest <- pivot_longer(dataFrame, cols= c(benign, ack, scan, syn, udp),
                              names_to = "Traffic",
                              values_to = "f1_score")


#citation: for renaming the Round labels I referenced here: https://stackoverflow.com/questions/50718397/labeller-not-applying-labels-with-facet-wrap-and-returns-na
labels <- c("5" = "Round 5", "10" = "Round 10", "15" = "Round 15")

ggplot(dataFrameTest, aes(x=Epochs, y=f1_score, color=Traffic, shape=Traffic)) + 
  geom_point() +
  geom_line() +
  facet_wrap(~Rounds, labeller = labeller(Rounds = labels)) +
  theme_bw() +
  scale_shape_manual(values=c(0,1,2,5,4))

#end citation for labeller code.

dataFrameTest2 <- dataFrame


#removal of round 5 and udp for better comparison.
dataFrameTest2$udp <- NULL
dataFrameTest2 <- dataFrameTest2[-1,]
dataFrameTest2 <- dataFrameTest2[-1,]
dataFrameTest2 <- dataFrameTest2[-1,]


dataFrameRemovedData <- pivot_longer(dataFrameTest2, cols= c(benign, ack, scan, syn),
                              names_to = "Traffic",
                              values_to = "f1_score")


ggplot(dataFrameRemovedData, aes(x=Epochs, y=f1_score, color=Traffic, shape=Traffic)) + 
  geom_point() +
  geom_line() +
  facet_wrap(~Rounds, labeller = labeller(Rounds = labels)) +
  theme_bw() +
  scale_shape_manual(values=c(0,1,2,5,4))