library(igraph)

setwd("/Users/jadezhang/Documents/2016-2017_data_science/insight_program/project/insight_project/previous_work/graphs")

link_mat <- read.csv("../metrics/confusion_matrix_all.csv")

link_mat <- link_mat[,2:dim(link_mat)[2]]

#filter out the very weak links
link_mat[link_mat<0.05] <- 0

supports <- diag(as.matrix(link_mat))


plot_foodweb(link_mat,supports)




plot_foodweb <- function(link_mat,sizes){
	index <- 1:dim(link_mat)[1]
	colors = rainbow(length(sizes))
	node_size <- sizes
	AJ = as.matrix(link_mat)
	net=graph.adjacency(AJ,mode="undirected",weighted="width",diag=F)

	V(net)$color = colors
	V(net)$size = 20*node_size
	V(net)$label.cex = rep(5, length(sizes))
	set.seed(8)

	par(bg="white",mar=rep(0,4))

	plot.igraph(net,vertex.label.cex=1.5,vertex.label=colnames(link_mat),edge.arrow.size = E(net)$width,vertex.frame.color=0,vertex.color=colors,edge.color="orange",edge.width=E(net)$width*10)

}
