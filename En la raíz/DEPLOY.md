# 🚀 Guía de Despliegue — PsicoEduc Platform

## Qué es este repositorio

Base de conocimiento interactiva para psicología clínica, desarrollo humano y educación superior. Incluye:

- **9 autores clínicos** con fichas estructuradas
- **8 autores del desarrollo** (embrión a adultez emergente)
- **Herramienta DSM-5** interactiva con 15+ diagnósticos
- **Biblioteca de referencia** con 32+ textos comentados
- **Línea de tiempo del desarrollo** embrión → adultez
- **Marco SIAAE** (Zimmerman) con sustento teórico integrado
- **Automatización** con Claude API vía GitHub Actions

---

## Paso 1 — Crear cuenta GitHub

1. Ve a [github.com](https://github.com)
2. Toca **Sign up**
3. Ingresa email, contraseña y nombre de usuario
4. Verifica tu email

---

## Paso 2 — Crear el repositorio

1. Toca el ícono **+** arriba a la derecha
2. Toca **New repository**
3. Nombre: `clinical-psych-education`
4. Visibilidad: **Public**
5. **NO** marcar "Add a README" (ya tienes uno)
6. Toca **Create repository**

---

## Paso 3 — Subir archivos (desde PC — método recomendado)

```bash
# Opción A: Git desde terminal
git clone https://github.com/TU_USUARIO/clinical-psych-education.git
cp -r /ruta/a/este/repositorio/* clinical-psych-education/
cd clinical-psych-education
git add .
git commit -m "feat: initial platform setup"
git push origin main
```

**Opción B: Desde la interfaz web de GitHub**
1. En tu repositorio vacío, toca **uploading an existing file**
2. Arrastra todos los archivos y carpetas
3. Toca **Commit changes**

---

## Paso 4 — Activar GitHub Pages (la web)

1. En tu repositorio → **Settings**
2. En el menú lateral → **Pages**
3. En *Branch* selecciona **main** → carpeta **/ (root)**
4. Toca **Save**
5. En ~2 minutos tu web queda en:

```
https://TU_USUARIO.github.io/clinical-psych-education
```

---

## Paso 5 — Activar la automatización (opcional)

1. En tu repositorio → **Settings → Secrets and variables → Actions**
2. Toca **New repository secret**
3. Nombre: `ANTHROPIC_API_KEY`
4. Valor: tu API key de Anthropic (obténla en console.anthropic.com)
5. Toca **Add secret**

La automatización se activa cada lunes a las 9am UTC o cuando editas un archivo de autor.

---

## Cómo actualizar el contenido

### Agregar un autor
Crea un archivo `authors/nombre.md` siguiendo la estructura de `authors/beck.md`.

### Agregar un libro/artículo a la biblioteca
Edita `data/library.json` y agrega un objeto con esta estructura:
```json
{
  "id": "apellido-año",
  "type": "libro",
  "year": 2025,
  "authors": "Apellido, N.",
  "title": "Título",
  "publisher": "Editorial",
  "categories": ["clinica"],
  "annotation": "Por qué vale la pena leerlo.",
  "language": "en",
  "era": "2020-presente"
}
```

### Actualizar un diagnóstico DSM
Abre `index.html`, busca `id:"codigo_diagnostico"` en el array `dsmData`, edita los campos `criteria`, `specifiers` o `dsm_version`.

---

## Estructura del repositorio

```
clinical-psych-education/
├── index.html                    ← La web completa
├── README.md                     ← Este archivo
├── .gitignore
├── authors/                      ← 9 autores clínicos
│   ├── beck.md
│   ├── bandura.md
│   └── ... (9 archivos)
├── frameworks/                   ← 5 marcos teóricos
│   ├── cognitivo_conductual.md
│   ├── apego.md
│   └── ...
├── applications/                 ← Aplicaciones institucionales
│   ├── bienestar_estudiantil.md
│   ├── aprendizaje_autorregulado.md
│   ├── salud_mental_ES.md
│   └── intervencion_psicoed.md
├── data/
│   ├── authors_index.json        ← Metadatos de autores
│   ├── library.json              ← Biblioteca de textos
│   └── cross_reference.json     ← Generado automáticamente
├── scripts/
│   ├── generate_summary.py       ← Genera apps educacionales (Claude API)
│   └── cross_reference.py        ← Genera tabla de referencias cruzadas
└── .github/
    └── workflows/
        ├── auto_summary.yml      ← Ejecución automática lunes
        └── validate_links.yml   ← Validación semanal de links
```

---

## Próximas funcionalidades sugeridas

- [ ] Módulo de protocolos de intervención por escenario clínico
- [ ] Árbol de decisión diagnóstica interactivo
- [ ] Exportación de fichas a PDF
- [ ] Formulario de tamizaje integrado (Forms → SharePoint)
- [ ] Versión en inglés para publicaciones internacionales

---

## Soporte

**Autor**: Manuel Dinamarca  
**Institución**: Duoc UC — Coordinación de Bienestar Estudiantil  
**Repositorio**: github.com/TU_USUARIO/clinical-psych-education
