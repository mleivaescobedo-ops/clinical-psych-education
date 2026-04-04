"""
generate_summary.py
-------------------
Genera aplicaciones educacionales automáticas para cada autor
usando la API de Claude. Solo procesa autores con educational_relevance = "alta".

Uso:
    ANTHROPIC_API_KEY=sk-... python scripts/generate_summary.py

Requiere:
    pip install anthropic python-frontmatter
"""

import anthropic
import frontmatter
import os
import json
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
MODEL = "claude-opus-4-5"
MAX_TOKENS = 1200
AUTHORS_PATH = Path("Authors")
OUTPUT_PATH = Path("applications/auto_generated")
INDEX_PATH = Path("data/authors_index.json")

SYSTEM_PROMPT = """Eres un experto en psicología educacional aplicada a educación superior chilena.
Dado el perfil de un autor de psicología clínica, genera una síntesis de aplicación concreta en:

1. **Bienestar estudiantil** — cómo sus conceptos se operacionalizan en un programa de acompañamiento
2. **Aprendizaje autorregulado** — conexión con el modelo de Zimmerman (previsión / ejecución / autorreflexión)
3. **Intervención psicoeducativa** — un taller o actividad concreta derivada de su marco

Formato: Markdown estructurado, sin introducción genérica, directamente aplicable.
Extensión: 400-500 palabras. Sin redundancias. Prioriza aplicabilidad sobre descripción teórica."""

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_index() -> list[dict]:
    """Carga el índice de autores desde JSON."""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_high_relevance_authors(index: list[dict]) -> list[str]:
    """Retorna IDs de autores con relevancia alta."""
    return [a["id"] for a in index if a.get("educational_relevance") == "alta"]

def generate_application(client: anthropic.Anthropic, author_name: str, content: str) -> str:
    """Llama a Claude API para generar aplicación educacional."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Autor: **{author_name}**\n\nContenido de referencia:\n{content[:3000]}"
        }]
    )
    return response.content[0].text

def write_output(author_id: str, author_name: str, content: str) -> Path:
    """Escribe el archivo generado en applications/auto_generated/."""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m")
    out_file = OUTPUT_PATH / f"{author_id}_edu_app.md"
    
    header = f"""---
generated: {timestamp}
author: {author_name}
source: auto-generated via Claude API
---

# Aplicación Educacional: {author_name}
> *Generado automáticamente — revisar antes de uso institucional*

"""
    out_file.write_text(header + content, encoding="utf-8")
    return out_file

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY no está definida en el entorno.")
    
    client = anthropic.Anthropic(api_key=api_key)
    index = load_index()
    high_relevance = get_high_relevance_authors(index)
    
    print(f"🔍 Procesando {len(high_relevance)} autores con relevancia alta...\n")
    
    results = {"generated": [], "skipped": [], "errors": []}
    
    for author_data in index:
        if author_data["id"] not in high_relevance:
            results["skipped"].append(author_data["id"])
            continue
        
        author_file = Path(author_data.get("file", f"authors/{author_data['id']}.md"))
        
        if not author_file.exists():
            print(f"  ⚠️  Archivo no encontrado: {author_file}")
            results["errors"].append(author_data["id"])
            continue
        
        try:
            post = frontmatter.load(author_file)
            author_name = post.get("author", author_data["name"])
            
            print(f"  ⚙️  Generando: {author_name}...")
            summary = generate_application(client, author_name, post.content)
            
            out_path = write_output(author_data["id"], author_name, summary)
            print(f"  ✅  Guardado en: {out_path}")
            results["generated"].append(author_data["id"])
            
        except Exception as e:
            print(f"  ❌  Error con {author_data['id']}: {e}")
            results["errors"].append(author_data["id"])
    
    print(f"\n{'─'*50}")
    print(f"✅ Generados: {len(results['generated'])}")
    print(f"⏭️  Omitidos:  {len(results['skipped'])}")
    print(f"❌ Errores:   {len(results['errors'])}")

if __name__ == "__main__":
    main()
