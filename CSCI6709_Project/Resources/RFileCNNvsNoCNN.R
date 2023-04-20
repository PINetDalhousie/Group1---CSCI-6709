
#
#@author: Nathanael Timothy Bowley
#@Banner ID: B00742839
#@Course: CSCI6709
#@Version: 1
#@Date: 4/20/2023 (MM/DD/YYYY)
#@Description: This code generates the CNN vs No CNN figure for the Traffic / Metric values from the 5epoch, 5round testing.
#

#citation for replicating c() https://www.tutorialspoint.com/how-to-create-a-vector-with-repeated-values-in-r
dataFrame <- data.frame(Type = rep(c("CNN", "No CNN"), each=15), Traffic = rep(c("Benign", "Ack", "Scan", "Syn", "Udp"), each=3), Metric = rep(c("Recall", "Precision", "f1_score"), times=10), Mean = c(0.998625, 0.999525, 0.99905, 0.77915, 0.98, 0.858675, 0.999525, 0.9994, 0.99945, 0.9084, 0.894, 0.9132, 0.98395, 0.896525, 0.927,  0.99376, 0.49878, 0.66418, 0.97238, 0.33084, 0.49364, 0,0,0, 0.0361, 0.2443, 0.0624, 0,0,0), Std = c(0.00275, 0.00095, 0.00132, 0.167653, 0.034023, 0.091134, 0.00095, 0.000898, 0.000911, 0.137603, 0.122417, 0.071078, 0.018628, 0.2033, 0.122569,  0.008587, 0.001418, 0.003103, 0.036303, 0.002818, 0.007578, 0, 0, 0, 0.049646, 0.302362, 0.085713, 0, 0, 0))

#end citation

#generating the figure to be used in the paper.
ggplot(dataFrame, aes(x = Metric, y = Mean, fill = Traffic)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(width = 0.2, outlier.shape = NA, position = position_dodge(0.9), aes(lower=Mean-Std,upper=Mean+Std,middle=Mean,ymin=Mean-Std,ymax=Mean+Std)) +
  labs(x = "Metric", y = "Mean Value") +
  theme_bw() +
  facet_grid(. ~Type)