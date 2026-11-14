# Proyecto Integrador (Bitácora 2) — Equipo 1: Línea de Ordenamiento
## Priorización de Eventos Críticos del Centro de Cómputo de SIDOR con Heap y Quicksort 3 Vías

**Maestría en Tecnologías de la Información — UNEG**  
**Asignatura:** Análisis y Diseño de Algoritmos (Cohorte X · 2026-III)  
**Docente:** Profa. MSc. Ana Isabel Sosa London  

---

### Definición del Problema (SIDOR)

El centro de cómputo de la siderúrgica monitorea miles de señales por segundo: temperatura de altos hornos, presión de laminadores, estado de sistemas (ERP, mainframe) y disponibilidad de enlaces de planta. El objetivo es priorizar por criticidad los eventos que recibe cada minuto el centro de cómputo para la toma oportuna de decisiones operativas.

- **Entradas:** Un lote de `n` eventos de una ventana de 60 s, cada uno modelado como `(id, timestamp, origen, c)`, y un entero `k ≥ 0` (por ejemplo, `k = 10`).
- **Orígenes:** `alto horno`, `laminador`, `ERP`, `mainframe` o `enlace de planta`.
- **Criticidad:** Entero `c = 100·severidad + 80·impacto + 20·desviación`, acotado en `[0, 1000]`.
- **Clave de ordenamiento:** `(c, -timestamp, -id)`. A igual criticidad va primero el más antiguo, garantizando un orden total determinista.
- **Salidas:**
  - **S₁ (Tablero Gerencial):** Extracción de los `k` eventos más críticos en tiempo `Θ(n + k log n)` mediante Max-Heap (`top_k`), cumpliendo la restricción de respuesta sub-segundo (< 1 s).
  - **S₂ (Reporte de Turno):** Ordenamiento completo descendente de los `n` eventos mediante Heapsort (garantía `Θ(n log n)` y memoria `O(1)`) y Quicksort aleatorizado con partición de 3 vías (`particionar_3v`, optimizado a `Θ(n)` frente a inundaciones de claves repetidas y pila `O(log n)`).

---

## Estructura del Repositorio

```text
bitacora 2/
├── README.md                     # Comandos de reproducción y especificación del sistema
├── requirements.txt              # Dependencias del proyecto (hypothesis, matplotlib)
├── Equipo1_Bitacora2.docx        # Documento del informe consolidado del equipo
├── src/
│   ├── __init__.py
│   ├── eventos.py                # Modelo EventoSidor, cálculo de criticidad y generador sintético (semilla 2026)
│   └── ordenamiento.py           # Algoritmos: Max-Heap, Heapsort, Quicksort 3-vías y Quicksort Lomuto
├── tests/
│   └── test_ordenamiento.py      # 9 pruebas automatizadas (unitarias, límites, Hypothesis y diferencial)
└── experiments/
    ├── medicion_piloto.py        # Script reproducible de medición experimental (semilla 2026)
    ├── captura_consola_piloto.jpg# Evidencia de ejecución en consola
    └── grafica_piloto.png        # Gráfica comparativa generada para el informe
```

---

## Comandos para Reproducir Todo

### 1. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 2. Ejecutar la batería de pruebas (Unitarias, Hypothesis y Diferencial)

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

**Pruebas incluidas en `tests/test_ordenamiento.py`:**
- `test_01_limites_vacio_y_unitario`: Casos límite con lista vacía y lista de 1 elemento.
- `test_02_inundacion_claves_iguales`: Inundación de 2.000 alarmas con criticidad idéntica.
- `test_03_entradas_ordenadas_e_invertidas`: Comportamiento frente a entradas preordenadas e invertidas.
- `test_04_bordes_parametro_top_k`: Casos de borde para el parámetro `k` (`k=0`, `k > n`, `k=n`).
- `test_05_invariantes_heap_y_particion_3v`: Verificación estructural de invariantes de Max-Heap y partición ternaria.
- `test_06_caso_uso_sidor_alto_horno_y_laminador`: Caso de uso industrial con fallas en alto horno y caída de enlace.
- `test_07_propiedad_orden_y_multiconjunto`: Test con Hypothesis de invariante de permutación y orden estricto.
- `test_08_propiedad_top_k_contra_sorted`: Test con Hypothesis de equivalencia de `top_k`.
- `test_09_diferencial_eventos_sidor`: Prueba diferencial contra `sorted()` de Python y `heapq.nlargest`.

### 3. Ejecutar la medición experimental

```powershell
python experiments/medicion_piloto.py
```
