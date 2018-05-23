#include <Rcpp.h>
// [[Rcpp::plugins(cpp11)]]
// [[Rcpp::export]]
Rcpp::List bestSplit(Rcpp::NumericMatrix dataset){
	double sse_min = std::numeric_limits<double>::infinity();
	int index_min = 0;
	double split_var = 0;
	double sse = 0;
	Rcpp::List splits_min;
	Rcpp::List splits;
	Rcpp::Environment G = Rcpp::Environment::global_env();
	Rcpp::Function split = G["split_test_matrix"];
	Rcpp::Function cost = G["cost_func_matrix"];
	
	int ncol = dataset.ncol()-1;
	int nrow = dataset.nrow();
	for(int i = 0; i < ncol; i++){
		for(int l = 0; l < nrow; l++){
			 splits = Rcpp::as<Rcpp::List>(split(dataset(l, i), (int)i+1, dataset));
             sse = Rcpp::as<double>(cost(splits));
			if(sse < sse_min){
				sse_min = sse;
				index_min = i;
				split_var = dataset(l, i);
				splits_min = splits;
			}
		}
}
	Rcpp::List return_list;
	return_list["sse"] = sse_min;
	return_list["index"] = index_min+1;
	return_list["split_val"] = split_var;
    return_list["splits"] = splits_min;
    
    return return_list;
}

