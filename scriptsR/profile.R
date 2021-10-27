library(magrittr)
library(tidyverse)
library(readxl)
library(lubridate)

## Functions

all_equal <- function (x) all(x %in% x[1])

not_na <- function (x) not(is.na(x))

not_in <- function (x, y_set) not(x %in% y_set)

not_exists <- function (file) not(file.exists(file))

classes <- function (a_df) {
  its_classes_df <- tibble(
      name  = names(a_df), 
      class = map_chr(a_df, ~class(.x)[1])) 
  return (its_classes_df) }

quotemeta <- function (x) str_replace_all(x, "(\\W)", "\\\\\\1")

str_delatinize <- function (x) chartr("ÁÉÍÓÚÑáéíóúñ", "AEIOUÑaeiouñ", x)
  

 
# Funny stuff

if (interactive()) {
  fortunes::fortune()
} else {
  options(readr.num_columns=0)
}

