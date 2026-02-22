# 🚴‍♂️ Evolución del Tour de Francia (1903 - 2025)
**Proyecto Final del Módulo de Python - Máster en Data Science & AI**

Este proyecto es un Análisis Exploratorio de Datos (EDA) completo y reproducible sobre la historia del Tour de Francia. El objetivo es aplicar los conocimientos de Python, Pandas y visualización modular para demostrar el cambio de paradigma de la carrera: de la pura supervivencia a la optimización fisiológica moderna.

---

## 🎯 1. Objetivo y Dataset
Analizar la evolución del trazado, la fisiología de los ganadores y la geopolítica de los finalistas mediante datos históricos.
* **Dataset:** https://www.kaggle.com/datasets/jeetahirwar/tour-de-france-from-1903-2022historical-dataset
               En el DataSet sólo venían datos hasta 2022. Antes de comenzar l proyecto, rellené los datos hasta 2025.
* **Archivos origen:** 4 archivos CSV ubicados en `data/raw/` (Tours, Etapas, Ganadores y Finalistas).

## ❓ 2. Preguntas de Investigación
1. **Dureza:** ¿Compensa la reducción moderna de kilómetros totales con una mayor densidad de montaña?
2. **Supervivencia:** ¿Se retiran ahora más ciclistas debido a esta mayor intensidad?
3. **Fisiología (Edad):** ¿Estamos realmente en la era de los "niños prodigio"?
4. **Fisiología (Biotipo):** ¿Cómo ha evolucionado el Índice de Masa Corporal (BMI) para el perfil de escalador?
5. **Geopolítica:** ¿Se ha globalizado el pelotón respecto a las potencias europeas clásicas?

---

## 🛠 3. Pipeline y Transformaciones
Se ha diseñado una arquitectura modular (`src/`) y un orquestador (`main.py`) que aplican transformaciones complejas:
* **Limpieza (`src/cleaning.py`):** Estandarización de textos, manejo de nulos históricos y limpieza de strings.
* **Feature Engineering (`src/features.py`):** * Cálculo de Edad exacta mediante `datetime`.
  * Creación del Índice de Masa Corporal (BMI).
  * **Índice de Dureza Ponderada:** Algoritmo propio que evalúa el desgaste de cada etapa multiplicando su distancia por un coeficiente técnico.
* **Merging:** Cruce de los 4 datasets usando el año (`year`) como clave para crear el archivo maestro de análisis.

---

## ⚙️ 4. Instrucciones de Ejecución (Reproducibilidad)
Sigue estos pasos para ejecutar el proyecto desde cero:

1. **Clona o descomprime** el proyecto y abre la terminal en la carpeta raíz.
2. **Crea y activa el entorno virtual:**
   ```bash
   python -m venv .venv
   
   # En Windows (PowerShell):
   .venv\Scripts\activate
   # En macOS / Linux:
   source .venv/bin/activate
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
4. **Ejecuta el pipline de datos**:
   ```bash
   python main.py
5. **Explora el análisis**
   ```bash
   jupyter notebook notebooks/eda.ipynb

## 📈 5. Conclusiones y Hallazgos
1. El paradigma de la Dureza: La carrera ha pasado de maratones llanos (5.000 km) a explosividad (3.400 km), donde la montaña representa ya el 40% del esfuerzo total.
2. La paradoja de la supervivencia: A pesar de la mayor intensidad y desnivel, la tasa de abandonos está en mínimos históricos gracias a la profesionalización médica y tecnológica.
3. Adaptación extrema: El biotipo del ganador corpulento ha desaparecido, convergiendo hacia una delgadez límite (BMI < 21). Además, la edad de victoria se ha desplomado a los 21-22 años y el pelotón se ha globalizado superando el antiguo monopolio europeo.