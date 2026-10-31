La pobreza monetaria en Cusco en 2024 fue de **18,5 %** de la población. Es la proporción de personas que viven en hogares con gasto per cápita por debajo de la línea de pobreza.

- **Pobreza extrema:** 2,1 %.
- **Pobreza no extrema:** 16,4 %.
- **No pobres:** 81,5 %.

**Cómo lo calculé:**
- Usé `sumaria-2024.dta` del Módulo 34 y filtré el departamento de Cusco con el código de ubigeo `08`, lo que dejó 1 230 hogares en la muestra.
- Usé la variable oficial `pobreza` (1 = extrema, 2 = no extrema, 3 = no pobre). Ponderé por `factor07 × mieperho`, es decir, el factor de expansión del hogar por el número de miembros.

No calculé intervalos de confianza. Con 1 230 hogares en la muestra, el margen de error es de varios puntos porcentuales. Puedo calcularlo con el diseño muestral (`conglome`, `estrato`) si lo necesitas.