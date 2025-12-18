setwd('/app')
library(optparse)
library(jsonlite)




print('option_list')
option_list = list(

make_option(c("--param_data_filename"), action="store", default=NA, type="character", help="my description"),
make_option(c("--param_use_dummy_data"), action="store", default=NA, type="integer", help="my description"),
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

print("Retrieving param_data_filename")
var = opt$param_data_filename
print(var)
var_len = length(var)
print(paste("Variable param_data_filename has length", var_len))

param_data_filename <- gsub("\"", "", opt$param_data_filename)
print("Retrieving param_use_dummy_data")
var = opt$param_use_dummy_data
print(var)
var_len = length(var)
print(paste("Variable param_use_dummy_data has length", var_len))

param_use_dummy_data = opt$param_use_dummy_data
id <- gsub('"', '', opt$id)

conf_minio_public_bucket<-"naa-vre-public"
conf_virtual_lab_biotisan_euromarec<-"vl-biotisan-euromarec"

print("Running the cell")
if (param_use_dummy_data) {
        file_path <- paste(conf_virtual_lab_biotisan_euromarec, param_data_filename, sep="/")
        print(sprintf("Using dummy data for testing purposes. Set param_use_dummy_data to 0 to use your own data. Downloading data from %s / %s", conf_minio_public_bucket, file_path))
    }