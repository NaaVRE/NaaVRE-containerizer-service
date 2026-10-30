setwd('/app')
library(optparse)
library(jsonlite)

if (!requireNamespace("purrr", quietly = TRUE)) {
	install.packages("purrr", repos="http://cran.us.r-project.org")
}
library(purrr)



print('option_list')
option_list = list(

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

id <- gsub('"', '', opt$id)


print("Running the cell")
dummy_n1 <- list()
dummy_n1 <- c("zxcv")
# capturing outputs
print('Serialization of dummy_n1')
file <- file(paste0('/tmp/dummy_n1_', id, '.json'))
type = 'list'
if (type == 'list'){
    writeLines(toJSON(dummy_n1, auto_unbox=FALSE), file)
} else {
    writeLines(toJSON(dummy_n1, auto_unbox=TRUE), file)
}
close(file)
