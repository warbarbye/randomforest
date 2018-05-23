split_test_matrix <- function(split_point, num, dataset){
    less_pos <- which(dataset[,num] <= split_point)
    return(list(less = matrix(dataset[less_pos,], ncol=dim(dataset)[[2]]), grater = matrix(dataset[-less_pos,], ncol=dim(dataset)[[2]])))
}

cost_func_matrix <- function(splits){
#   index <- dim(sp
   # beta_less <- mean(splits$less[,dim(splits$less)[[2]]])#sum(splits$less$y)/length(splits$less$y)
   # beta_grater <- mean(splits$grater[,dim(splits$grater)[[2]]])
   # cost <- sum((splits$less[,dim(splits$less)[[2]]] - mean(splits$less[,dim(splits$less)[[2]]]))^2) + sum((splits$grater[,dim(splits$grater)[[2]]] - mean(splits$grater[,dim(splits$grater)[[2]]]))^2)
    return(as.numeric(sum((splits$less[,dim(splits$less)[[2]]] - mean(splits$less[,dim(splits$less)[[2]]]))^2) + sum((splits$grater[,dim(splits$grater)[[2]]] - mean(splits$grater[,dim(splits$grater)[[2]]]))^2)))
}

terminal_node_matrix <- function(node_side){
    return(mean(node_side[,ncol(node_side)]))
}
node_split <- function(node, max_depth, min_size, depth){
    left_node <- node$splits$less
    right_node <- node$splits$grater
    if(!nrow(left_node)){
        node$left <- terminal_node_matrix(right_node)
        node$right <- terminal_node_matrix(right_node)
        return(node)
    }
    else if(!nrow(right_node)){
        node$right <- terminal_node_matrix(left_node)
        node$left  <- terminal_node_matrix(left_node)
        return(node)
    }
   
     if(depth >= max_depth){
        node$left <- terminal_node_matrix(left_node)
        node$right <- terminal_node_matrix(right_node)
        
        return(node)
     }
    if(nrow(left_node) <= min_size){
        node$left <- terminal_node_matrix(left_node)
    }
    else{
        node$left <- bestSplit(left_node)
        node$left <-node_split(node$left, max_depth, min_size, depth+1)
    }
    if(nrow(right_node) <= min_size){
        node$right <- terminal_node_matrix(right_node)
        return(node)
    }
    else{
        node$right <- bestSplit(right_node)
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
    
build_tree <- function(dataset, max_depth=3, min_size=50, indices){ 
    dataset <- data.matrix(dataset)
    if(is.matrix(dataset)) ncol_ <- dim(dataset)[2]
    if(!missing(indices)){
        dataset <- dataset[,c(indices, dim(dataset)[2])]
    }
    if(!is.matrix(dataset)) dataset <- matrix(dataset, ncol=length(dataset))
    root <- bestSplit(dataset)
    tree <- node_split(root, max_depth, min_size, 1)
     return(tree)
} 



print_tree <- function(node, depth=0, side="root", dataset){
    ds_names <- colnames(dataset)
    if(!is.numeric(node)){
        cat(paste(rep(" ",depth), collapse = ""),"Variable = ", ds_names[node$index], "| split value = ", node$split_val,"|", side, "| depth =",depth, "\n")
        print_tree(node$left, depth+1, side="left_subtree", dataset)
        print_tree(node$right, depth+1, side="right_subtree", dataset)
    }
    else
        cat(paste(rep(" ",depth), collapse =""),"R = ",node, "|",side, "|depth =", depth, "\n")
}
