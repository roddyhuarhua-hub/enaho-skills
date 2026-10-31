# Evaluación: los tres pedidos con y sin skills

Corrí los tres pedidos de la clase con `claude -p` en la laptop (Windows, Claude Code) el 31 de octubre de 2026, con
[`evaluacion/evaluar.py`](evaluacion/evaluar.py). Cada corrida empieza en una **copia limpia** del proyecto que solo
tiene `datos/` con los dos zip del INEI:

- **Con skills:** la copia trae `.claude/skills/`, pero **no** `salidas/`. Así se ve si Claude encadena
  `limpiando-enaho` antes de graficar o mapear.
- **Sin skills:** la copia no trae `.claude/` y se corre con `--disallowedTools Skill`, como pide la clase. Claude
  tiene que resolver todo por su cuenta.

Las respuestas completas y las figuras de cada corrida están en [`evaluacion/corridas/`](evaluacion/corridas/) y el
resumen en [`evaluacion/resultados.csv`](evaluacion/resultados.csv).

## Resumen

| Pedido | Modo | Skills que se activaron | Cifra | ¿Ponderó? | Figura | Tiempo · costo |
|---|---|---|---|---|---|---|
| ¿Cuál fue la pobreza en Cusco en 2024? | con skills | `limpiando-enaho` | **18.5 %** (esperado 18.5) | Sí, `facpob07`, 3,777 personas | — | 48 s · US$0.10 |
| | sin skills | ninguna | **18,5 %** | Sí, `factor07 × mieperho`, 1,230 hogares | — | 37 s · US$0.18 |
| Grafica la pobreza urbana y rural | con skills | `graficando-enaho` → `limpiando-enaho` | **24.7 % / 39.4 %** (esperado 24.8 / 39.3) | Sí, `facpob07` | [barras](evaluacion/corridas/urbano_rural_con_skills/pobre_por_area_2024.png) con las reglas | 49 s · US$0.11 |
| | sin skills | ninguna | **24.8 % / 39.3 %** | Sí, `factor07 × mieperho` | [panel con barras y 2 mapas](evaluacion/corridas/urbano_rural_sin_skills/pobreza_urbano_rural_2024.png) | 53 s · US$0.12 |
| Haz un mapa de la pobreza por departamento | con skills | `mapeando-enaho` → `limpiando-enaho` | **Cajamarca 45.0 %, Ica 5.9 %** (esperado 45.0 / 6.0) | Sí, `facpob07` | [mapa](evaluacion/corridas/mapa_con_skills/pobreza_departamento.png) con las reglas | 41 s · US$0.11 |
| | sin skills | ninguna | **Cajamarca 45 %, Ica 6 %** | Sí, `factor07 × mieperho` | [mapa](evaluacion/corridas/mapa_sin_skills/mapa_pobreza.png) | 68 s · US$0.12 |

**Dos skills seguidas:** «Grafica la pobreza urbana y rural» activó `graficando-enaho` y esta llamó a
`limpiando-enaho` porque no existía `salidas/personas_2024.parquet`. Lo mismo pasó con el mapa:
`mapeando-enaho` → `limpiando-enaho`. Las tres descriptions se activaron solas en el primer intento, así que no hubo
que corregirlas.

## Qué cambió con las skills

**Las cifras, poco.** Sin skills, Claude también llegó a 18.5 %, 24.8/39.3 % y Cajamarca 45 %. Lo hizo por un atajo:
usó solo la sumaria, que ya trae la variable `pobreza` del INEI, y ponderó por hogar. Es un camino válido para la
pobreza total, pero no arma la base de personas, no filtra residentes habituales y no puede responder por sexo o edad.
Con las skills, todas las cifras salen de la misma base validada (108,664 residentes, 13 chequeos en `validacion.txt`).
Las diferencias de 0.1 puntos con la referencia vienen de ponderar personas con `facpob07` en vez de hogares con
`factor07 × mieperho`.

**La forma, mucho.** Esto es lo que una skill fija y un pedido suelto no:

| | Con skills | Sin skills |
|---|---|---|
| Validación contra el INEI | Siempre; si falla, se detiene | Ninguna en Cusco; en el mapa solo comparó el total nacional |
| Dónde deja los archivos | `figuras/` y `mapas/` del proyecto | En una carpeta temporal de Windows (`AppData\Local\Temp`), fuera del repo |
| Qué entrega | Lo pedido | En urbano/rural agregó dos mapas que nadie pidió |
| Gráfico | Barras desde 0, un color, valor en cada barra, fuente al pie, 200 dpi | Barras superpuestas (total y extrema) junto a dos mapas con otra paleta; ninguna regla fija |
| Mapa: escala | Un color (rojos) desde **0** hasta 50, leyenda «% de personas» | Escala de varios colores (amarillo a rojo) que empieza en **6** y termina en 45, lo que exagera las diferencias |
| Mapa: etiquetas | Un decimal; Callao con su etiqueta afuera | Enteros; la etiqueta de Callao (34) se monta sobre Lima (27) |
| Unión del mapa | Por código, con `assert` de 25 departamentos | Por código también (esta vez acertó), sin control |
| Reproducible | El mismo script cada vez | Un script nuevo distinto en cada corrida |

**Tiempo y costo, parecidos.** Entre 40 y 70 segundos y entre US$0.10 y 0.18 por pedido en los dos modos. Con
skills hubo más turnos (7 a 9) porque primero limpia y valida, pero no costó más: el pedido de Cusco sin skills fue el
más caro.

## Conclusión

Las tres skills se activaron solas y se encadenaron como pide la clase. Sin ellas, Claude acierta las cifras
nacionales pero cada vez decide distinto dónde guardar, qué graficar y cómo pintar el mapa, y no valida. Con ellas, el
resultado es el mismo para cualquiera que clone el repositorio.
