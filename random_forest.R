source("single_tree.R")
sourceCpp("bestsplit.cpp")
library(Rcpp)
library(plugdensity)

make_error <- function(error_list){
    errors <- list()#rep(0, length = length(error_list))
    for(x in 1:length(error_list))
        errors[[x]] <- rep(x, as.numeric(error_list[[x]]))
    return(as.numeric(unlist(errors)))
}

select_variables <- function(var_num, m=floor(var_num/3)){
    return(sample(1:(var_num-1),m, replace=FALSE))
}
data_bootstrap <- function(dataset){
    indices <- sample(1:dim(dataset)[1], dim(dataset)[1], replace = TRUE)
    dataset_new <- dataset[indices,]
    return(dataset_new)
}

predict_value_forest <- function(forest, X){
    predictions <- list()
    for(i in 1:length(forest)) predictions[[i]] <- predict_value(forest[[i]], X)
    return(mean(unlist(predictions)))
}

predict_forest <- function(forest, dataset){
    predictions <- list()
    for(i in 1:dim(dataset)[1]){
        predictions[[i]] <- predict_value_forest(forest, dataset[i,])
    }
    return(unlist(predictions))
}

seed_forest <- function(dataset, tree_num, m){
    forest <- list()
    errors <- list()
    corr <- dataset$y
    new_indi <- 0
    E <- rep(0, dim(dataset)[1])
    indexes <- list()
    for(i in 1:tree_num){
        if(!length(indexes)){
            tree_data <- data_bootstrap(dataset)
        }
        else
            tree_data <- dataset[indexes,]
        if(missing(m))
            var_indices <- select_variables(var_num=length(dataset))
        else{
            var_indices <- select_variables(var_num=length(dataset), m=m)
        }
        
        forest[[i]] <- build_tree(dataset=tree_data, indices=var_indices) 
        errors <- abs(corr - predict_forest(forest[1:i], dataset=dataset))
        indexes <- which(errors >=mean(errors))
        E[indexes] <- E[indexes] + 1
        errors <- make_error(E)
        fs <- plugin.density(errors)
        if(anyNA(fs$y)) fs$bw <- 0
        means <- sample(errors, dim(dataset)[1], replace = TRUE)
        new_indi <- floor(rnorm(dim(dataset)[1], mean=means, sd=fs$bw))
        new_indi[new_indi <= 0] <- 1
        new_indi[new_indi > length(new_indi)] <- length(new_indi)
        indexes <- new_indi
    }
    return(forest)
}













    
    
