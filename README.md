# README

Extrae los precios de diferentes comercializadoras de energía de la página web de la [Comisión Nacional de los Mercados y Competencia](https://comparador.cnmc.gob.es).

Para ejecutar el código es necesario instalar la siguientes bibliotecas:

```
pip install sys
pip install time
pip install selenium
pip install pandas
pip install beautifulsoup4
```

Una vez en la página mencionada, se elige el tipo de contrato deseado:

* Electricidad
* Gas Natural
* Ofertas conjuntas

Para cada una de esas opciones, el programa entrará en una página donde se visualizan las diferentes opciones disponibles con la forma representada en la presente [página](https://comparador.cnmc.gob.es/comparador/formulario/5D5E29215FAD02BA82D6EC15EA57E6707507132D1CB33FB71622CA951C0B53FAD94DE0BF91E5A4328677C319ED295B785ED9E0C9485A38FE10BEA9A6C46B2F68182AE7C518763ABB39197536C32D8342DB19C3BFB40E50DB2D5142E1A0859A52FC807141D40689C2525E25DC93B8194541ECBCE4000000000000000000000000000000). Posteriormente, es necesario introducir un código postal y rellenar un formulario, el cual se mantiene por defecto.

Finalmente, se llega a una [página](https://comparador.cnmc.gob.es/comparador/listado/7738ED71561C92C55D917695806B21581EF735C14D13F91730C93B40265BC792175E0D978858D57ED82FB9333DE1AD39A8AC2D2B0A212DA90F27900570976B0A3AA7D73322504BD9716C9CFA3352DD4891857EB6B2617C63A4DAF21E8BE498458F2A144FC199F9DA9FF68DBC87A521AD119FFEA953377DDEA447A81857293567F76B8C) con todas las opciones disponibles.

Actualmente se extraen los siguientes atributos de la web:

* Comercializadora
* Oferta
* Importe primera factura
* Importe siguientes facturas
* Validez
* Servicios adicionales incluidos
* Penalización
* Verde
