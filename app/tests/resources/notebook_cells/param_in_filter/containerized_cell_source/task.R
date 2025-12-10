setwd('/app')
library(optparse)
library(jsonlite)

if (!requireNamespace("SecretsProvider", quietly = TRUE)) {
	install.packages("SecretsProvider", repos="http://cran.us.r-project.org")
}
library(SecretsProvider)
if (!requireNamespace("dplyr", quietly = TRUE)) {
	install.packages("dplyr", repos="http://cran.us.r-project.org")
}
library(dplyr)
if (!requireNamespace("tidyr", quietly = TRUE)) {
	install.packages("tidyr", repos="http://cran.us.r-project.org")
}
library(tidyr)



print('option_list')
option_list = list(

make_option(c("--data_as_csv_filename"), action="store", default=NA, type="character", help="my description"),
make_option(c("--metadata_as_csv_filename"), action="store", default=NA, type="character", help="my description"),
make_option(c("--number_of_validation_errors"), action="store", default=NA, type="character", help="my description"),
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

print("Retrieving data_as_csv_filename")
var = opt$data_as_csv_filename
print(var)
var_len = length(var)
print(paste("Variable data_as_csv_filename has length", var_len))

data_as_csv_filename <- gsub("\"", "", opt$data_as_csv_filename)
print("Retrieving metadata_as_csv_filename")
var = opt$metadata_as_csv_filename
print(var)
var_len = length(var)
print(paste("Variable metadata_as_csv_filename has length", var_len))

metadata_as_csv_filename <- gsub("\"", "", opt$metadata_as_csv_filename)
print("Retrieving number_of_validation_errors")
var = opt$number_of_validation_errors
print(var)
var_len = length(var)
print(paste("Variable number_of_validation_errors has length", var_len))

number_of_validation_errors <- gsub("\"", "", opt$number_of_validation_errors)
id <- gsub('"', '', opt$id)

conf_temporary_data_directory<-"/tmp/data"

print("Running the cell")
library(dplyr)
library(tidyr)

print(paste(deparse(substitute(number_of_validation_errors)), number_of_validation_errors, sep=" = "))

validate_dataframe_has_data <- function(dataframe, dataframe_name) {
    if (nrow(dataframe) == 0) {
    stop(paste0(dataframe_name, " has no rows (0 rows). Halting execution."))
  } else {
    sprintf("%s has %i rows.", dataframe_name, nrow(dataframe))
    }
}


datecollected = ""
siteid = ""
decimallatitude = ""
decimallongitude = ""

md <- read.csv(paste(conf_temporary_data_directory, metadata_as_csv_filename, sep="/"), sep=",")
data <- read.csv(paste(conf_temporary_data_directory, data_as_csv_filename, sep="/"), sep=",")
validate_dataframe_has_data(data, "data read from csv")
validate_dataframe_has_data(md, "metadata read from csv")

sites <- data %>%
  group_by(siteid) %>%
  summarise(nyear = n_distinct(substr(datecollected, 1, 4))) %>%
  filter(nyear > param_years)

md <- merge(md,sites, by = "siteid")
validate_dataframe_has_data(md, "metadata merged by siteid")
validate_dataframe_has_data(data, "data after first years filter")

metadata_coordinates <- md %>% select(siteid, decimallatitude, decimallongitude)
print(metadata_coordinates)

md <- dplyr::filter(md, decimallatitude >= param_latitude_south, decimallatitude <= param_latitude_north,
                 decimallongitude >= param_longitude_west, decimallongitude <= param_longitude_east)
print(paste0("Number of sites found within the specified geolocation: ", nrow(md)))

data <- data %>% # Keep data from these sites
  filter(siteid %in% md$siteid)
validate_dataframe_has_data(data, "data filtered by coordinates")

data <- data %>% filter((maximumdepthinmeters >= param_upper_limit_max_depth & maximumdepthinmeters <= param_lower_limit_max_depth) %>% tidyr::replace_na(TRUE))
data <- data %>% filter((minimumdepthinmeters >= param_upper_limit_min_depth & minimumdepthinmeters <= param_lower_limit_min_depth) %>% tidyr::replace_na(TRUE))
validate_dataframe_has_data(data, "data filtered by depth")

data$month <- as.numeric(format(as.Date(data$datecollected), "%m")) # Create a column with the sampling month

season <- c(param_first_month:param_last_month)
data <- data %>%
  filter(month %in% season) #Remove those samples in non-consistent seasons (in this case keeps the months 1, 2 and 3, this is January, February and March)
validate_dataframe_has_data(data, "data filtered by season")


sites <- data %>%
  group_by(siteid) %>%
  summarise(nyear = n_distinct(substr(datecollected, 1, 4))) %>%
  filter(nyear > param_years)

data <- data %>% # Keep data from these sites
  filter(siteid %in% md$siteid)
md <- md %>% # Keep metadata from these sites
  filter(siteid %in% md$siteid)
validate_dataframe_has_data(data, "data filtered by years")

md_final <- md[,c(1:8)]
data_final <- data[,c(1:15)]

cleaned_metadata_filename <- "metadata_Example.csv"
cleaned_data_filename <- "data_Example.csv"
cleaned_metadata_path <- paste(conf_temporary_data_directory, cleaned_metadata_filename, sep="/")
cleaned_data_path <- paste(conf_temporary_data_directory, cleaned_data_filename, sep="/")
print(sprintf("Storing metadata in: %s, and data in %s", cleaned_metadata_path, cleaned_data_path))
write.csv(md_final, file = cleaned_metadata_path)
write.csv(data_final, file =  cleaned_data_path)