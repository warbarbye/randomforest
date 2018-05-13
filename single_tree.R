library(ggplot2)
library(tibble)

split_test2 <- function(split_point, num, dataset){
    less_side <- list()
    grater_side <- list()
    less_pos <- which(dataset[[num]] <= split_point)
    less_side <- dataset[less_pos,]
    grater_side <- dataset[-less_pos,]
    return(list(less = less_side, grater = grater_side))
}

split_test3 <- function(split_point, num, dataset){
    less_pos <- which(dataset[[num]] <= split_point)
    return(list(less = dataset[less_pos,], grater = dataset[-less_pos,]))
} 
cost_func2 <- function(splits){
    beta_less <- mean(splits$less$y)#sum(splits$less$y)/length(splits$less$y)
    beta_grater <- mean(splits$grater$y)#sum(splits$grater$y)/length(splits$grater$y)
    cost <- sum((splits$less$y - beta_less)^2) + sum((splits$grater$y - beta_grater)^2)
    return(cost)
}

cost_func3 <- function(splits){
    return(sum((splits$less$y - mean(splits$less$y))^2) + sum((splits$grater$y - mean(splits$grater$y))^2))
}
best_split <- function(dataset){
    #TODO IMPROVE IT
    sse_min <- Inf
    index_min <- NULL
    split_var <- NULL
    splits_min <- list()
    for(i in 1:(length(dataset)-1)){
        for(l in 1:dim(dataset)[[1]]){
            splits <- split_test3(dataset[[i]][l], i, dataset)
            sse <- cost_func3(splits)
            if(sse < sse_min){
                sse_min <- sse
                index_min <- i
                split_var <- dataset[[i]][l]
                splits_min <- splits
                 }
        }
        
    }
    
    return(list(sse = sse_min, index = index_min, split_val = split_var, splits = splits_min, left = NULL, right = NULL))
}


best_split2 <- function(dataset){
    sse2 <- matrix(nrow=dim(dataset)[1], ncol=length((dataset))-1)
    for(i in 1:(length(dataset)-1)){
        for(l in 1:dim(dataset)[[1]]){
            splits <- split_test3(dataset[[i]][l], i, dataset)
            sse2[l,][i] <- as.numeric(cost_func3(splits))
        }
    }
    sse_min2 <- min(sse2)
    mins <- which(sse2 == sse_min2, arr.ind = TRUE)[1,]
    index1 <- unname(mins[2])
    index2 <- unname(mins[1])
    split_val2 <- dataset[[index1]][index2]
    splits2 <- split_test3(split_val2, index1, dataset)
    return(list(sse = sse_min2, index = index2, split_val = split_val2, splits = splits2, left = NULL, right = NULL))
}

best_split3 <- function(dataset){
    sse2 <- matrix(nrow=dim(dataset)[1], ncol=length((dataset))-1)
    for(i in 1:(length(dataset)-1)){
        for(l in 1:dim(dataset)[[1]]){
            splits <- split_test3(dataset[[i]][l], i, dataset)
            sse2[l,][i] <- as.numeric(cost_func3(splits))
        }
    }
    sse_min2 <- min(sse2)
    mins <- which(sse2 == sse_min2, arr.ind = TRUE)[1,]
    index1 <- unname(mins[2])
    index2 <- unname(mins[1])
    split_val2 <- dataset[[index1]][index2]
    splits2 <- split_test3(split_val2, index1, dataset)
    return(list(sse = sse_min2, index = index2, split_val = split_val2, splits = splits2, left = NULL, right = NULL))
}



    
terminal_node <- function(node_side){
    output <- sum(node_side$y)/length(node_side$y)
    return(output)
}
node_split <- function(node, max_depth, min_size, depth){
    left_node <- node$splits$less
    right_node <- node$splits$grater
    if(nrow(left_node) == 0){
        node$left <- terminal_node(right_node)
        node$right <- terminal_node(right_node)
        return(node)
    }
    else if(nrow(right_node) == 0){
        node$right <- terminal_node(left_node)
        node$left  <- terminal_node(left_node)
        return(node)
    }
   
     if(depth >= max_depth){
        node$left <- terminal_node(left_node)
        node$right <- terminal_node(right_node)
        
        return(node)
     }
    if(dim(left_node)[1] <= min_size){
        node$left <- terminal_node(left_node)
    }
    else{
        node$left <- best_split(left_node)
        node$left <-node_split(node$left, max_depth, min_size, depth+1)
    }
    if(dim(right_node)[1] <= min_size){
        node$right <- terminal_node(right_node)
        return(node)
    }
    else{
        node$right <- best_split(right_node)
        node$right <-node_split(node$right, max_depth, min_size, depth+1)
    }
    
    return(node)
    
        
}
predict_value <- function(node, X){
      if(X[node$index] < node$split_val){
          if(!is.numeric(node$left))
             predict_value(node$left, X)
          else
              return(node$left)
        }
     else{
          if(!is.numeric(node$right)){
              predict_value(node$right, X)
          }
            else{
                return(node$right)
          }
     }
    
}

predict <- function(tree, dataset){
    predicted <- list()
    for(i in 1:dim(dataset)[1]){
        predicted[[i]] <- predict_value(tree, dataset[i,])
    }
    return(predicted)
}
    
        
build_tree <- function(dataset, max_depth=20, min_size=1, indices){ 
    if(!missing(indices))
        dataset <- dataset[,c(indices, length(dataset))]
    root <- best_split(dataset)
    tree <- node_split(root, max_depth, min_size, 1)
     return(tree)
} 



print_tree <- function(node, depth=0, side="root"){
    if(!is.numeric(node)){
        cat(paste(rep(" ",depth), collapse = ""),"Variable = ", names(node$splits$grater)[node$index], "| split value = ", node$split_val,"|", side, "| depth =",depth, "\n")
        print_tree(node$left, depth+1, side="left_subtree")
        print_tree(node$right, depth+1, side="right_subtree")
    }
    else
        cat(paste(rep(" ",depth), collapse =""),"R = ",node, "|",side, "|depth =", depth, "\n")
    
}
