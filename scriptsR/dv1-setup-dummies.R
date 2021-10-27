# Diego Villamil, Epic Bank
# CDMX, 25 de octubre de 2021

library(reticulate)
library(readxl)
library(lubridate)

#%% Provienen de otro Repo: 

loans_dir <- ("../../cx-debt-collections")

attrs_file <- "refs/catalogs/sap_attributes.feather" %>% 
    file.path(loans_dir, .)
loan_cols <- arrow::read_feather(attrs_file)

loans_file <- "data/cache_tables/all_loans.feather" %>% 
    file.path(loans_dir, .)
all_loans <- arrow::read_feather(loans_file)


#%% Preparación de simulaciones. 

tools     <- source_python("../src/utilities/tools.py")
linked_xl <- shortcut_target("../refs/Sampling 360.xlsx.lnk")
ranges    <- list(
    "product_offers" = "Catalogs!B3:I7", 
    "etiquetas"      = "Catalogs!B10:B17", 
    "lifecycles"     = "Catalogs!D10:D15",
    "personas"       = "Catalogs!F10:F13")

users_0 <- all_loans %>% 
  select(id=BorrowerID, name=BorrowerName, city=BorrowerCity) %>% 
  unique()

product_offers_0 <- read_excel(linked_xl, range=ranges$product_offers)
names_offers    <- names(product_offers_0) %>% 
  set_names(., str_replace_all(., c("-"="_", "amount"="amnt")))
product_offers  <- product_offers_0 %>% 
  rename(names_offers) %>% select(-num_pymts)
    
etiquetas   <- read_excel(linked_xl, range=ranges$etiquetas) $`user-tags`
lifecycles  <- read_excel(linked_xl, range=ranges$lifecycles)$lifecycle
personas    <- read_excel(linked_xl, range=ranges$personas)  $persona

k_productos <- 3*nrow(users_0)
k_etiquetas <- 2*nrow(users_0)

#%% Las simulaciones
set.seed(42)
users <- users_0 %>% 
    mutate(persona = sample(personas, nrow(users_0), replace=TRUE), 
           context = sample(50:90,    nrow(users_0), replace=TRUE))

productos_0 <- data_frame(
    id        = sample(1e5:(1e6-1),          k_productos, FALSE),
    userId    = sample(users$id,             k_productos, TRUE ), 
    class     = sample(product_offers$product_class, k_productos, TRUE), 
    date      = today() - sample(365,        k_productos, TRUE ), 
    accepted  = sample(c(TRUE, FALSE),       k_productos, TRUE ),
    expiry    = if_else(!accepted, date + 30, NA %>% as.Date()), 
    lifecycle = if_else( accepted, sample(lifecycles, k_productos, TRUE),
                                   NA %>% as.character())) 

productos <- productos_0 %>% 
  left_join(product_offers, by=c("class" = "product_class")) %>% 
  mutate(
    rand_rate  = runif(k_productos),
    rand_amnt  = runif(k_productos),
    rand_tenor = runif(k_productos),
    rand_pymts = sample(2, k_productos, TRUE),
    
    annualRate = (min_rate  + rand_rate *(max_rate - min_rate )) %>% round( 2), 
    amount     = (min_amnt  + rand_amnt *(max_amnt - min_amnt )) %>% round(-3), 
    tenor      = (min_tenor + rand_tenor*(max_tenor- min_tenor)) %>% round(), 
    payments   = rand_pymts*tenor ) %>% 
  select(!matches("^(rand|min|max)"))


tags <- data_frame(
    userId     = sample(users$id,  k_etiquetas, TRUE), 
    contextTag = sample(etiquetas, k_etiquetas, TRUE)) %>% 
    unique()

write_feather(users,     "../data/sims/users_tidy.feather")
write_feather(tags,      "../data/sims/tags_tidy.feather")
write_feather(productos, "../data/sims/products_tidy.feather")
