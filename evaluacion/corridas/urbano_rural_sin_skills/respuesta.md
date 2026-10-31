Hice el gráfico de pobreza urbana y rural con la ENAHO 2024. Tiene un panel de barras a nivel nacional y dos mapas departamentales, uno para el área urbana y otro para la rural.

En 2024 la pobreza total fue de 27.6 % a nivel nacional. En el área urbana fue de 24.8 % y en la rural de 39.3 %. La pobreza extrema fue de 3.1 % en el área urbana y de 15.5 % en la rural, es decir, unas cinco veces más.

Entre departamentos, la pobreza rural llega a más de 60 % en Loreto y es alta en Puno y en el norte andino. La urbana es más baja y homogénea.

**Cómo lo calculé**
- Usé el módulo Sumaria (`sumaria-2024.dta`), que ya trae la variable `pobreza` calculada por el INEI.
- Definí como urbano los estratos 1 a 5 y como rural los estratos 6 a 8.
- Ponderé por `factor07 × mieperho` para que la tasa sea de personas y no de hogares.

Las tasas rurales por departamento se basan en muestras pequeñas en algunos casos, así que tómalas como referenciales.

**Archivos** (en `C:\Users\huarh\AppData\Local\Temp\enaho_eval__gvcnlc7\`)
- `pobreza_urbano_rural_2024.png`
- `pobreza_area_departamento_2024.csv`
- `graficar_pobreza.py`