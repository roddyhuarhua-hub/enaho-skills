# enaho-skills · Tres skills de Claude Code que limpian, grafican y mapean la ENAHO 2024

Tarea de la **sesión 16** del curso [Data-Science-Python](https://github.com/d2cml-ai/Data-Science-Python/tree/main/sessions/16-skills-enaho)
(issue [#200](https://github.com/d2cml-ai/Data-Science-Python/issues/200)). Autor: Roddy Huarhua.

Cualquiera que clone este repositorio y le pida a Claude Code «un mapa de la pobreza por departamento» obtiene la misma
base, los mismos gráficos y el mismo mapa, con la pobreza oficial del INEI replicada.

| Skill | Entra | Sale |
|---|---|---|
| [`limpiando-enaho`](.claude/skills/limpiando-enaho/SKILL.md) | `datos/966-Modulo34.zip` y `datos/966-Modulo02.zip` | `salidas/personas_2024.parquet` y [`salidas/validacion.txt`](salidas/validacion.txt) |
| [`graficando-enaho`](.claude/skills/graficando-enaho/SKILL.md) | la base limpia y un grupo: área, sexo, edad, departamento | `figuras/*.png` |
| [`mapeando-enaho`](.claude/skills/mapeando-enaho/SKILL.md) | la base limpia y los límites de los 25 departamentos | `mapas/pobreza_departamento.png` |

Las dos últimas dicen «si no existe `salidas/personas_2024.parquet`, usa primero la skill `limpiando-enaho`», así un
solo pedido activa dos skills seguidas.

## Resultados

<!-- RESULTADOS -->

## Cómo correrlo

### 1. Requisitos

- [uv](https://docs.astral.sh/uv/) (instala Python y las librerías solo).
- [Claude Code](https://code.claude.com) para usar las skills.

```bash
git clone https://github.com/roddyhuarhua-hub/enaho-skills.git
cd enaho-skills
uv sync
```

### 2. Bajar los datos del INEI

Desde el navegador (el portal del INEI a veces bloquea descargas automáticas), baja estos dos archivos y guárdalos
**sin descomprimir** en la carpeta `datos/` del repositorio:

| Archivo | Qué es | Enlace |
|---|---|---|
| `966-Modulo34.zip` | Sumaria, una fila por hogar (33,691) | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip |
| `966-Modulo02.zip` | Miembros del hogar, una fila por persona (117,721) | https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo02.zip |

`966` es el código de la ENAHO 2024 en el [portal de microdatos del INEI](https://proyectos.inei.gob.pe/microdatos/).
Los límites departamentales (`peru_departamental_simple.geojson`) los baja solo la skill de mapas. La carpeta `datos/`
está en `.gitignore`: los microdatos no se suben.

### 3. Usarlo con Claude Code

Abre una terminal en la carpeta del repositorio, escribe `claude` y pide, por ejemplo:

- `¿Cuál fue la pobreza en Cusco en 2024?`
- `Grafica la pobreza urbana y rural`
- `Haz un mapa de la pobreza por departamento`

Claude elige la skill por su `description`. También se pueden llamar a mano: `/limpiando-enaho 2024`,
`/graficando-enaho sexo`, `/mapeando-enaho`. Con `/skills` se ve la lista.

### 4. O sin Claude, directo con los scripts

```bash
uv run .claude/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
uv run .claude/skills/graficando-enaho/scripts/graficar.py --por area      # sexo, edad, departamento, lima
uv run .claude/skills/mapeando-enaho/scripts/mapear.py
```

### 5. Evaluar con y sin skills

```bash
uv run evaluacion/evaluar.py
```

Corre los tres pedidos de la clase con `claude -p`, cada uno en una copia limpia del proyecto: una con las skills y
otra sin `.claude/` y con `--disallowedTools Skill`. Deja las respuestas y figuras en `evaluacion/corridas/` y la
tabla en `evaluacion/resultados.csv`. El análisis está en [`evaluacion.md`](evaluacion.md).

## Decisiones que fija la limpieza

El script `limpiar.py` hace siempre lo mismo, en siete pasos:

1. **Leer** con `pd.read_stata(..., convert_categoricals=False)` directo desde el zip.
2. **Normalizar** columnas a minúscula sin tildes (`aÑo` pasa a `anio`) y llaves como **texto** con ceros
   (`conglome` 6 dígitos, `ubigeo` 6).
3. **Filtrar** residentes habituales: `(p204 == 1 & p205 == 2) | (p204 == 2 & p206 == 1)`.
4. **Unir** personas y hogares con `merge(..., validate="m:1")`.
5. **Construir** `departamento = ubigeo[:2]`, `urbano = estrato <= 5`, `pobre = pobreza <= 2`.
6. **Validar** llaves únicas, que la unión no pierda ni duplique filas, 108,664 residentes y la pobreza oficial
   (27.6 %, extrema 5.5 %, urbana 24.8 %, rural 39.3 %) con tolerancia de 0.1 puntos.
7. **Guardar** la base y `validacion.txt`. Si algún chequeo falla, no guarda la base.

## Estructura

```text
.claude/skills/
  limpiando-enaho/   SKILL.md, reference.md, scripts/limpiar.py
  graficando-enaho/  SKILL.md, scripts/graficar.py
  mapeando-enaho/    SKILL.md, scripts/mapear.py
referencias/         pobreza por departamento 2024 y mapa de referencia (del curso)
salidas/validacion.txt
figuras/  mapas/
evaluacion/evaluar.py  evaluacion/resultados.csv  evaluacion.md
README.md  pyproject.toml  uv.lock
```

## Fuente

INEI, Encuesta Nacional de Hogares (ENAHO) 2024, módulos 02 y 34. Límites departamentales del curso
(sesión 06). Las skills siguen el estándar [Agent Skills](https://code.claude.com/docs/en/skills).
