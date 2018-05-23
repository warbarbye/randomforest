source("randfor.R")
M <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
B <- c(5, seq(10, 500, by=10))
max_depth <- c(3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30)

true_val <- redwine_df$y[1:1000]

error_val <- list()
path_name_forest <- "~/Desktop/UM/sim/"
k <- 1
# for(depth in max_depth){
#     tree <- build_tree(redwine_df[1:1000,], max_depth = depth)
#     tree_predict <- unlist(predict(tree, redwine_df[1:1000,]))
#     error_val[[k]] <- true_val - tree_predict
#     k <- k + 1
#     print(depth)
#     print(k)
# }


for(b in B){
    forest <- seed_forest(redwine_df[1:1000,], b)
    forest_predict <- predict_forest(forest, redwine_df[1:1000,])
    error_val <- true_val - forest_predict
    write.csv(error_val, sep=";", file = paste0(path_name_forest, "mod_forest_error_tree_",b))
}
for(tn in c(5, 250, 500)){
    for(m in M){
      forest <- seed_forest(redwine_df[1:1000,],tree_num = tn,m=m)
        forest_predict <- predict_forest(forest, redwine_df[1:1000,])
        error_val <- true_val - forest_predict
        write.csv(error_val, sep=";", file = paste0(path_name_forest, "mod_forest_error_m",m,"_tree_",tn))
    }
}
