setwd('/app')
library(optparse)
library(jsonlite)




print('option_list')
option_list = list(

make_option(c("--io"), action="store", default=NA, type="integer", help="my description"),
make_option(c("--param_neg_decimal"), action="store", default=NA, type="numeric", help="my description"),
make_option(c("--param_neg_num"), action="store", default=NA, type="integer", help="my description"),
make_option(c("--param_neg_string"), action="store", default=NA, type="character", help="my description"),
make_option(c("--id"), action="store", default=NA, type="character", help="task id")
)


opt = parse_args(OptionParser(option_list=option_list))

var_serialization <- function(var){
    if (is.null(var)){
        print("Variable is null")
        exit(1)
    }
    tryCatch(
        {
            var <- fromJSON(var)
            print("Variable deserialized")
            return(var)
        },
        error=function(e) {
            print("Error while deserializing the variable")
            print(var)
            var <- gsub("'", '"', var)
            var <- fromJSON(var)
            print("Variable deserialized")
            return(var)
        },
        warning=function(w) {
            print("Warning while deserializing the variable")
            var <- gsub("'", '"', var)
            var <- fromJSON(var)
            print("Variable deserialized")
            return(var)
        }
    )
}

print("Retrieving io")
var = opt$io
print(var)
var_len = length(var)
print(paste("Variable io has length", var_len))

io = opt$io
print("Retrieving param_neg_decimal")
var = opt$param_neg_decimal
print(var)
var_len = length(var)
print(paste("Variable param_neg_decimal has length", var_len))

param_neg_decimal = opt$param_neg_decimal
print("Retrieving param_neg_num")
var = opt$param_neg_num
print(var)
var_len = length(var)
print(paste("Variable param_neg_num has length", var_len))

param_neg_num = opt$param_neg_num
print("Retrieving param_neg_string")
var = opt$param_neg_string
print(var)
var_len = length(var)
print(paste("Variable param_neg_string has length", var_len))

param_neg_string <- gsub("\"", "", opt$param_neg_string)
id <- gsub('"', '', opt$id)


print("Running the cell")
print(param_neg_string)
print(io)
print(param_neg_num)
print(param_neg_decimal)