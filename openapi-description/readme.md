
# Introducción

Se cambia el JSON original por esta carpeta donde se referencian otros especificadores de APIs.  

- `user-products-offer` es el JSON central para la API de este repo.  
- `loan-offer.json` es el correspondiente a la API del motor de decisión de préstamos. Lo copiamos del repo correspondiente.  La ubicación original es:  `data-loan-decision-engine-api/personal-loan-risk-analysiis.json`  
- `debit-account` es un especificador temporal, que incluimos sólo por consistencia con la entrada correspondiente.  El contenido es nulo.  

Como no se pudo usar el `one-of` para distinguir entre `loan-offer` y `debit-account`,
hacemos _copy-paste_ de las propiedades correspondientes.  
  