# Product Options

En este repositorio, generamos las especificaciones de los pedidos relacionados a productos de usuarios.  
En particular, las opciones de productos vigentes son aquellas a las que tiene accesibilidad los usuarios o clientes. 

Por ejemplo, una vez que el usuario hubo descargado su _app_, ahí podrá ver la opción de abrir una cuenta de débito. 
O bien, si ya hizo su validación del proceso de préstamo y recibió una oferta -caracterizada por tasa, monto, periodo-, entonces esa oferta aparecerá como opción de producto disponible. 

El contenido del repositorio se basa en las Azure Functions, generadas por la extensión de VSCode. 

En el inicio contiene el archivo tipo JSON, que especifica el `request-response`.  
En lo que sigue se desarrollará la funcionalidad, que busca en el _data lake_ las opciones correspondientes.  


## Preparación

La extensión de Azure ejecuta los comandos necesarios para utilizar este paquete:  ambientes virtuales y demás.  

Las nuevas configuraciones se irán agregando en este apartado.  

Para utilización, el contacto es [Diego Villamil](mail-to: dvillamil+epic@gmail.com)

