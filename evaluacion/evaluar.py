"""Corre los tres pedidos de la sesión 16 con y sin skills usando `claude -p`.

Uso (desde la raíz del repositorio, con los zip ya en datos/):
    uv run evaluacion/evaluar.py

Para que la comparación sea justa, cada corrida trabaja en una copia limpia del proyecto:
  - con skills:  copia con .claude/skills/ pero SIN salidas/, así se ve si encadena limpiando -> graficando/mapeando
  - sin skills:  copia SIN .claude/ ni salidas/ y con --disallowedTools Skill, como pide la clase
Guarda en evaluacion/corridas/ la respuesta, las skills que se activaron y las figuras de cada corrida,
y escribe evaluacion/resultados.csv. La tabla final de evaluacion.md se llena a partir de esos archivos.
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

RAIZ = Path.cwd()
SALIDA = RAIZ / "evaluacion" / "corridas"

PEDIDOS = {
    "cusco": "¿Cuál fue la pobreza en Cusco en 2024? Usa la ENAHO 2024 del INEI que está en datos/.",
    "urbano_rural": "Grafica la pobreza urbana y rural con la ENAHO 2024 del INEI que está en datos/.",
    "mapa": "Haz un mapa de la pobreza por departamento con la ENAHO 2024 del INEI que está en datos/.",
}
HERRAMIENTAS = "Bash Read Write Edit Glob Grep Skill"


def ruta_claude() -> str:
    """En Windows, npm instala claude.cmd, que subprocess no ejecuta sin shell: busca el claude.exe real."""
    ruta = shutil.which("claude")
    if ruta and ruta.lower().endswith(".cmd"):
        exe = Path(ruta).parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if exe.exists():
            return str(exe)
    return ruta or "claude"


def preparar_copia(con_skills: bool) -> Path:
    destino = Path(tempfile.mkdtemp(prefix="enaho_eval_"))
    shutil.copytree(RAIZ / "datos", destino / "datos")
    for f in ["pyproject.toml", "uv.lock", ".python-version"]:
        if (RAIZ / f).exists():
            shutil.copy(RAIZ / f, destino / f)
    if con_skills:
        shutil.copytree(RAIZ / ".claude" / "skills", destino / ".claude" / "skills")
        shutil.copytree(RAIZ / "referencias", destino / "referencias")
    return destino


def correr(nombre: str, pedido: str, con_skills: bool) -> dict:
    modo = "con_skills" if con_skills else "sin_skills"
    carpeta = preparar_copia(con_skills)
    cmd = [ruta_claude(), "-p", pedido, "--output-format", "stream-json", "--verbose",
           "--allowedTools", HERRAMIENTAS]
    if not con_skills:
        cmd += ["--disallowedTools", "Skill"]
    print(f"-> {nombre} · {modo} (en {carpeta})", flush=True)
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=carpeta, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=1800, shell=False)
    segundos = round(time.time() - t0)

    skills, respuesta, costo, turnos = [], "", None, None
    for linea in proc.stdout.splitlines():
        try:
            ev = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "assistant":
            for bloque in ev.get("message", {}).get("content", []):
                if bloque.get("type") == "tool_use" and bloque.get("name") == "Skill":
                    skills.append(bloque.get("input", {}).get("skill") or bloque.get("input", {}).get("command"))
        if ev.get("type") == "result":
            respuesta = ev.get("result", "")
            costo = ev.get("total_cost_usd")
            turnos = ev.get("num_turns")

    destino = SALIDA / f"{nombre}_{modo}"
    if destino.exists():
        shutil.rmtree(destino)
    destino.mkdir(parents=True)
    (destino / "respuesta.md").write_text(respuesta, encoding="utf-8")
    (destino / "transcripcion.jsonl").write_text(proc.stdout, encoding="utf-8")
    for png in carpeta.rglob("*.png"):
        if ".venv" not in png.parts:
            shutil.copy(png, destino / png.name)
    shutil.rmtree(carpeta, ignore_errors=True)

    return {"pedido": nombre, "modo": modo, "skills": " -> ".join(s for s in skills if s) or "ninguna",
            "segundos": segundos, "turnos": turnos, "costo_usd": costo,
            "figuras": ", ".join(p.name for p in destino.glob("*.png")) or "ninguna",
            "respuesta": respuesta.strip().replace("\n", " ")[:400]}


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    filas = []
    for nombre, pedido in PEDIDOS.items():
        for con_skills in (True, False):
            filas.append(correr(nombre, pedido, con_skills))
            print(f"   skills: {filas[-1]['skills']} · {filas[-1]['segundos']} s", flush=True)
    with open(RAIZ / "evaluacion" / "resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print("\nListo: evaluacion/resultados.csv y evaluacion/corridas/")


if __name__ == "__main__":
    main()
