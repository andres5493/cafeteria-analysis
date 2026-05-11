# Origen — Análisis de Cafetería de Especialidad

> Análisis exploratorio de datos para identificar oportunidades de optimización del menú de una cafetería de especialidad en Montevideo, Uruguay.

![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 Contexto

Las cafeterías de especialidad operan con márgenes ajustados y catálogos que suelen crecer por intuición más que por evidencia. Este proyecto explora datos de ventas para responder preguntas concretas que cualquier dueño debería hacerse antes de cambiar su menú.

El análisis usa **datos sintéticos en UYU** modelados sobre el catálogo real de una cafetería en Montevideo. La generación sintética permite trabajar con un volumen y estructura realistas sin comprometer información comercial sensible.

---

## ❓ Preguntas de negocio

El análisis busca responder:

1. ¿Cuáles son los productos estrella en términos de **ingresos** y **margen**?
2. ¿Qué productos están **subutilizados** y deberían revisarse o eliminarse?
3. ¿Existen patrones de **estacionalidad** o horarios pico que sugieran cambios en el flujo de operación?
4. ¿Qué productos **premium** podrían escalarse?
5. ¿Hay combinaciones de productos frecuentes que justifiquen **combos** o cross-sell?

---

## 📊 Catálogo modelado

El dataset sintético replica un catálogo real:

| Producto | Categoría | Rol estratégico |
|---|---|---|
| Carrot Cake | Pastelería | ⭐ Producto estrella |
| White Chocolate Cookie | Pastelería | 💎 Premium |
| Pistachio Cookie | Pastelería | 💎 Premium |
| Muffin | Pastelería | ⚠️ Producto en declive |
| Bondiola | Salado | Producto regular |
| Focaccia Vegetariana | Salado | Producto regular |

---

## 🛠️ Stack técnico

- **Python 3.11** — análisis y procesamiento
- **Pandas** — manipulación de datos
- **SQL (SQLite)** — consultas sobre el dataset
- **Matplotlib / Plotly** — visualización
- **Jupyter Notebook** — exploración interactiva

---

## 📁 Estructura del repositorio

afeteria-analysis/
├── data/                  # Datasets (sintéticos y procesados)

├── notebooks/             # Jupyter notebooks de análisis

├── reports/figures/       # Visualizaciones exportadas

├── src/                   # Scripts Python reutilizables

├── requirements.txt       # Dependencias del proyecto

└── README.md

---

## 🚀 Cómo correrlo localmente

```bash
# 1. Clonar el repo
git clone https://github.com/andres5493/cafeteria-analysis.git
cd cafeteria-analysis

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Abrir los notebooks
jupyter notebook notebooks/
```

---

## 📈 Estado del proyecto

| Fase | Estado |
|---|---|
| Definición del catálogo | ✅ Completo |
| Generación de datos sintéticos | 🔄 En desarrollo |
| Análisis exploratorio (EDA) | ⏳ Pendiente |
| Modelado SQL de consultas | ⏳ Pendiente |
| Visualización de hallazgos | ⏳ Pendiente |
| Informe ejecutivo | ⏳ Pendiente |

---

## 🎯 Próximos pasos

- [ ] Generar dataset sintético de 12 meses de ventas
- [ ] Definir esquema SQL y cargar datos en SQLite
- [ ] Análisis de productos estrella vs productos en declive
- [ ] Análisis de estacionalidad y horarios pico
- [ ] Dashboard final con visualizaciones clave

---

## 👤 Autor

**Andres** — .

- 🌐 Portfolio: [github.com/andres5493/Web-Portafolio](https://github.com/andres5493/Web-Portafolio)
- 💼 LinkedIn: [ahttps://www.linkedin.com/in/andresdominguezroselli/](https://www.linkedin.com/in/andresdominguezroselli/)

---

