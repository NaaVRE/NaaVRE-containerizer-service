setwd('/app')
library(optparse)
library(jsonlite)




print('option_list')
option_list = list(

make_option(c("--io1"), action="store", default=NA, type="integer", help="my description"),
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

print("Retrieving io1")
var = opt$io1
print(var)
var_len = length(var)
print(paste("Variable io1 has length", var_len))

io1 = opt$io1
id <- gsub('"', '', opt$id)


print("Running the cell")
read_acolite_files <- function(station, ...){
    extra_args <- list(...)
    print(station)
    print(extra_args)
}


read_acolite_files("cloud42", "cloud95", "cloud144")
print(io1)
