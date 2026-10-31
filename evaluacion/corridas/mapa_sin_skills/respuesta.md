Hice el mapa de pobreza monetaria 2024 por departamento. La tasa nacional que sale es 27,6 %, igual a la cifra oficial.

**Archivos**
- Mapa: `C:\Users\huarh\AppData\Local\Temp\enaho_eval_juemjfqc\salida\mapa_pobreza.png`
- Tabla con las tasas: `C:\Users\huarh\AppData\Local\Temp\enaho_eval_juemjfqc\salida\mapa_pobreza.csv`
- Script para reproducirlo: `C:\Users\huarh\AppData\Local\Temp\enaho_eval_juemjfqc\salida\mapa_pobreza.py`

**Cómo lo calculé**
- Usé el archivo Sumaria de `966-Modulo34.zip` (33 691 hogares), que ya trae la variable oficial `pobreza`. El zip del Módulo 02 no hizo falta.
- Conté como pobre a quien tiene `pobreza` 1 o 2 (pobre extremo o no extremo).
- Ponderé por `factor07 × mieperho`, para que la tasa sea sobre personas y no sobre hogares.
- Agrupé por los dos primeros dígitos del `ubigeo` y los uní al GeoJSON por `FIRST_IDDP`. Los 25 departamentos hicieron match.

**Resultados**
- **Más pobres:** Cajamarca 45 %, Loreto 43 %, Puno 40 %, Huánuco y Pasco 39 %.
- **Menos pobres:** Ica 6 %, Moquegua 11 %, Madre de Dios 11 %, Lambayeque 14 %, Arequipa 16 %.

**Limitaciones**
- Son estimaciones de encuesta. En departamentos con poca muestra, como Tacna, Moquegua o Madre de Dios, el margen de error es amplio. Las diferencias de pocos puntos entre departamentos no son significativas.
- Lima incluye Lima Metropolitana y las provincias, y Callao va aparte.