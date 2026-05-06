setwd('/app')
library(optparse)
library(jsonlite)


load_json_args <- function(file_path) {
  data <- jsonlite::fromJSON(file_path)
  return(data)
}
parse_value <- function(value, field_name, target_type, elem_type = NULL) {
  # helper to mimic arg_parser.error
  arg_error <- function(msg) {
    stop(msg, call. = FALSE)
  }

  # list handling
  if (identical(target_type, "list")) {
    if (is.list(value)) {
      return(value)
    } else if (is.character(value)) {
      # try parsing as JSON
      parsed <- tryCatch(jsonlite::fromJSON(value), error = function(e) NULL)

      if (!is.null(parsed)) {
        return(parsed)
      } else {
        # fallback: handle "['a', 'b', 'c']"
        if (startsWith(value, "[") && endsWith(value, "]")) {
          inner <- trimws(substr(value, 2, nchar(value) - 1))

          if (nchar(inner) > 0) {
            elems <- strsplit(inner, ",")[[1]]
            elems <- trimws(elems)
            elems <- gsub("^['\"]|['\"]$", "", elems)  # strip quotes
            return(as.list(elems))
          } else {
            return(list())
          }
        } else {
          arg_error(paste(field_name, "is not a valid list"))
        }
      }
    }
  }

  # string
  if (identical(target_type, "str")) {
    return(as.character(value))
  }

  # integer
  if (identical(target_type, "int")) {
    return(as.integer(value))
  }

  # float (numeric in R)
  if (identical(target_type, "float")) {
    if (is.numeric(value)) {
      return(as.numeric(value))
    }
    if (is.character(value)) {
      return(as.numeric(value))
    }
  }

  arg_error(paste(field_name, "has unsupported target type"))
}

get_arg_value <- function(name, args, raw_args) {
  # helper to mimic arg_parser.error
  arg_error <- function(msg) {
    stop(msg, call. = FALSE)
  }

  for (arg in raw_args) {
    if (!is.null(arg$name) && arg$name == name) {
      return(arg$value)
    }
  }

  arg_error(paste0("Argument '", name, "' not found in JSON args"))
}

# normalize raw_args to a list of argument-like lists so we can safely iterate
normalize_raw_args <- function(raw_args) {
  if (is.data.frame(raw_args)) {
    # each row becomes a list
    return(lapply(seq_len(nrow(raw_args)), function(i) as.list(raw_args[i, , drop = FALSE])))
  } else if (is.list(raw_args)) {
    return(raw_args)
  } else if (is.atomic(raw_args) && !is.null(names(raw_args))) {
    # named atomic vector -> convert to list of {name, value}
    return(lapply(names(raw_args), function(n) list(name = n, value = raw_args[[n]])))
  } else if (is.character(raw_args)) {
    # JSON may provide a simple array of argument strings like ["--id=0"]
    # Parse entries like "--name=value" into list(name=name, value=value).
    return(lapply(raw_args, function(s) {
      if (is.na(s) || nchar(s) == 0) {
        return(list(name = NULL, value = NULL))
      }
      # strip leading dashes
      stripped <- sub('^--?', '', s)
      if (grepl('=', stripped)) {
        parts <- strsplit(stripped, '=', fixed = TRUE)[[1]]
        name <- parts[1]
        value <- paste(parts[-1], collapse = '=')
        return(list(name = name, value = value))
      } else {
        # a flag without value
        return(list(name = stripped, value = NULL))
      }
    }))
  } else {
    stop("Unsupported raw_args structure")
  }
}

# helper to mimic arg_parser.error
arg_error <- function(msg) {
  stop(msg, call. = FALSE)
}

option_list = list(
make_option(c("--args_json"), action="store", default=NA, type="character", help="args json path")
)

opt = parse_args(OptionParser(option_list=option_list))
raw_args = load_json_args(opt$args_json)
raw_args_list <- normalize_raw_args(raw_args)

# build expected arg names set and validate provided args
expected_arg_names <- character(0)

expected_arg_names <- unique(c(expected_arg_names, "var_float"))
expected_arg_names <- unique(c(expected_arg_names, "var_int"))
expected_arg_names <- unique(c(expected_arg_names, "var_list_int"))
expected_arg_names <- unique(c(expected_arg_names, "var_list_str"))
expected_arg_names <- unique(c(expected_arg_names, "var_string"))
expected_arg_names <- unique(c(expected_arg_names, "var_string_with_comment"))

expected_arg_names <- unique(c(expected_arg_names, "param_float"))
expected_arg_names <- unique(c(expected_arg_names, "param_int"))
expected_arg_names <- unique(c(expected_arg_names, "param_list_int"))
expected_arg_names <- unique(c(expected_arg_names, "param_list_str"))
expected_arg_names <- unique(c(expected_arg_names, "param_string"))
expected_arg_names <- unique(c(expected_arg_names, "param_string_with_comment"))

expected_arg_names <- unique(c(expected_arg_names, "conf_float"))
expected_arg_names <- unique(c(expected_arg_names, "conf_int"))
expected_arg_names <- unique(c(expected_arg_names, "conf_list_int"))
expected_arg_names <- unique(c(expected_arg_names, "conf_list_str"))
expected_arg_names <- unique(c(expected_arg_names, "conf_string"))
expected_arg_names <- unique(c(expected_arg_names, "conf_string_with_comment"))
expected_arg_names <- unique(c(expected_arg_names, "id"))



for (arg in raw_args_list) {
  if (is.null(arg[["name"]])) {
    stop("Argument with no name found in JSON args")
  }
  name <- if (!is.null(arg[["name"]])) arg[["name"]] else NULL
  if (is.null(name) && is.atomic(arg) && !is.null(names(arg))) {
    # pick the first named element
    nm <- names(arg)[1]
    name <- arg[[nm]]
  }
  if (!(name %in% expected_arg_names)) {
    arg_error(paste0("Unexpected argument '", name, "' found in JSON args"))
  }

  if (!startsWith(name, "conf")) {
    if (is.null(arg$value)) {
      arg_error(paste0("Argument '", name, "' has no value in JSON args"))
    }
  }

  if (startsWith(name, "conf")) {
    if (is.null(arg$assignation)) {
      arg_error(paste0("Argument '", name, "' has no assignation in JSON args"))
    }
  }
}
arg_name <- "var_float"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "float"
var_float <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "var_int"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "int"
var_int <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "var_list_int"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "list"
var_list_int <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "var_list_str"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "list"
var_list_str <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "var_string"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "str"
var_string <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "var_string_with_comment"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "str"
var_string_with_comment <- parse_value(arg_value, arg_name, arg_type)

arg_name <- "param_float"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "float"
param_float <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "param_int"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "int"
param_int <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "param_list_int"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "list"
param_list_int <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "param_list_str"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "list"
param_list_str <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "param_string"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "str"
param_string <- parse_value(arg_value, arg_name, arg_type)
arg_name <- "param_string_with_comment"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "str"
param_string_with_comment <- parse_value(arg_value, arg_name, arg_type)

conf_float = 1.1
conf_int = 1
conf_list_int = list(1, 2, 3)
conf_list_str = list('list_str', 'space in elem', '3')
conf_string = 'param_string value'
conf_string_with_comment = 'param_string value'


arg_value <- get_arg_value("id", opt, raw_args_list)
id <- parse_value(arg_value, "id", "str")

print(paste('conf_string: ', conf_string, ' type: ', class(conf_string)))
print(paste('conf_string_with_comment: ', conf_string_with_comment, ' type: ', class(conf_string_with_comment)))
print(paste('conf_int: ', conf_int, ' type: ', class(conf_int)))
print(paste('conf_float: ', conf_float, ' type: ', class(conf_float)))
print(paste('conf_list_int: ', toString(conf_list_int), ' type: ', class(conf_list_int)))
print(paste('conf_list_str: ', toString(conf_list_str), ' type: ', class(conf_list_str)))

print(paste('param_string: ', param_string, ' type: ', class(param_string)))
print(paste('param_string_with_comment: ', param_string_with_comment, ' type: ', class(param_string_with_comment)))
print(paste('param_int: ', param_int, ' type: ', class(param_int)))
print(paste('param_float: ', param_float, ' type: ', class(param_float)))
print(paste('param_list_int: ', toString(param_list_int), ' type: ', class(param_list_int)))
print(paste('param_list_str: ', toString(param_list_str), ' type: ', class(param_list_str)))

print(paste('var_string: ', var_string, ' type: ', class(var_string)))
print(paste('var_string_with_comment: ', var_string_with_comment, ' type: ', class(var_string_with_comment)))
print(paste('var_int: ', var_int, ' type: ', class(var_int)))
print(paste('var_float: ', var_float, ' type: ', class(var_float)))
print(paste('var_list_int: ', toString(var_list_int), ' type: ', class(var_list_int)))
print(paste('var_list_str: ', toString(var_list_str), ' type: ', class(var_list_str)))

check_type <- function(var, expected_types) {
  
  if (!any(sapply(expected_types, function(x) inherits(var, x)))) {
    stop(paste('Variable is not of the expected types:', paste(expected_types, collapse = ', '),
               '. It is a', class(var)))
  }
  
  if ('list' %in% expected_types) {
    if (!is.list(var) && !is.vector(var)) {
      stop(paste('Variable', var, 'is not iterable.'))
    }
  }
}

check_type(conf_string, c(c("character")))
check_type(conf_string_with_comment, c("character"))
check_type(conf_int, "numeric")
check_type(conf_float, "numeric")
if (is.numeric(conf_list_int)) {
  conf_list_int <- list(conf_list_int)
}

check_type(conf_list_int, c("list"))
if (is.character(conf_list_str)) {
  conf_list_str <- list(conf_list_str)
}
check_type(conf_list_str, c("list"))

check_type(param_string, c("character"))
check_type(param_string_with_comment, c("character"))
check_type(param_int, c("numeric", "integer"))
check_type(param_float, c("numeric", "float"))
if (is.numeric(param_list_int)) {
  param_list_int <- list(param_list_int)
}
check_type(param_list_int, c("list"))
check_type(conf_list_int, c("list"))
if (is.character(param_list_str)) {
  param_list_str <- list(param_list_str)
}
check_type(param_list_str, c("list"))

check_type(var_string, c("character"))
check_type(var_string_with_comment, c("character"))
check_type(var_int, c("numeric", "integer"))
check_type(var_float, c("numeric", "float"))
if (is.numeric(var_list_int)) {
  var_list_int <- list(var_list_int)
}
check_type(var_list_int, c("list"))

if (is.character(var_list_str)) {
  var_list_str <- list(var_list_str)
}
check_type(var_list_str, c("list"))

print('All vars are of the correct type')

done <- TRUE
