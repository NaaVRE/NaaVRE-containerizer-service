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

expected_arg_names <- unique(c(expected_arg_names, "io1"))


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
arg_name <- "io1"
arg_value <- get_arg_value(arg_name, opt, raw_args_list)
arg_type <- "int"
io1 <- parse_value(arg_value, arg_name, arg_type)




arg_value <- get_arg_value("id", opt, raw_args_list)
id <- parse_value(arg_value, "id", "str")

read_acolite_files <- function(station, ...){
    extra_args <- list(...)
    print(station)
    print(extra_args)
}


read_acolite_files("cloud42", "cloud95", "cloud144")
print(io1)
