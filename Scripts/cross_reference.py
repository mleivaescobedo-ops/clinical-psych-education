"""
cross_reference.py
------------------
Genera una tabla de referencias cruzadas entre autores, frameworks y diagnósticos DSM-5.
Útil para visualizar el mapa conceptual del repositorio.

Uso:
    python scripts/cross_reference.py

Output:
    data/cross_reference.json
    data/cross_reference.md
"""

import json
import re
from pathlib import Path
from collections import defaultdict

AUTHORS_PATH = Path("authors")
DATA_PATH = Path("data")

def extract_frontmatter(file_path: Path) -> dict:
    """Extrae metadatos YAML del frontmatter de un archivo Markdown."""
    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm_text = content[3:end].strip()
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip('"\'') for v in val[1:-1].split(",")]
            result[key.strip()] = val
    return result

def build_cross_reference() -> dict:
    """Construye la tabla de referencias cruzadas."""
    matrix = defaultdict(dict)
    authors_summary = []

    for author_file in sorted(AUTHORS_PATH.glob("*.md")):
        fm = extract_frontmatter(author_file)
        author_name = fm.get("author", author_file.stem)
        framework = fm.get("framework", "Sin clasificar")
        relevance = fm.get("educational_relevance", "—")
        tags = fm.get("tags", [])
        siaae = fm.get("siaae_component", "—")
        instruments = fm.get("instruments", [])

        authors_summary.append({
            "id": author_file.stem,
            "name": author_name,
            "framework": framework,
            "educational_relevance": relevance,
            "siaae_component": siaae,
            "tags": tags if isinstance(tags, list) else [tags],
            "instruments": instruments if isinstance(instruments, list) else [instruments],
            "file": str(author_file)
        })

    return {
        "generated": "auto",
        "total_authors": len(authors_summary),
        "authors": authors_summary
    }

def export_markdown(data: dict) -> str:
    """Exporta la tabla en formato Markdown."""
    lines = [
        "# Tabla de Referencias Cruzadas\n",
        "| Autor | Framework | Relevancia ES | Componente SIAAE | Instrumentos |",
        "|---|---|---|---|---|"
    ]
    for a in data["authors"]:
        instruments = ", ".join(a["instruments"]) if a["instruments"] else "—"
        lines.append(f"| {a['name']} | {a['framework']} | {a['educational_relevance']} | {a['siaae_component']} | {instruments} |")
    return "\n".join(lines)

def main():
    DATA_PATH.mkdir(exist_ok=True)
    data = build_cross_reference()

    json_out = DATA_PATH / "cross_reference.json"
    json_out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ JSON: {json_out}")

    md_out = DATA_PATH / "cross_reference.md"
    md_out.write_text(export_markdown(data), encoding="utf-8")
    print(f"✅ Markdown: {md_out}")
    print(f"\n📊 Total autores procesados: {data['total_authors']}")

if __name__ == "__main__":
    main()
