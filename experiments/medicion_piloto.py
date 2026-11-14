import gc
import os
import platform
import random
import statistics
import sys
import time
import matplotlib.pyplot as graficador

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ordenamiento import heapsort, quicksort_lomuto

sys.setrecursionlimit(20000)


def verificar_orden_y_permutacion(arreglo_ordenado, arreglo_original):
    assert all(
        arreglo_ordenado[indice_actual] <= arreglo_ordenado[indice_actual + 1]
        for indice_actual in range(len(arreglo_ordenado) - 1)
    ), "Error: Arreglo no ordenado"
    assert sorted(arreglo_ordenado) == sorted(arreglo_original), "Error: Se perdieron o alteraron elementos"


def ejecutar_experimento(funcion_algoritmo, datos_entrada):
    copia_datos = list(datos_entrada)
    gc.collect()
    gc.disable()
    tiempo_inicio = time.perf_counter()
    resultado_ordenado = funcion_algoritmo(copia_datos)
    tiempo_fin = time.perf_counter()
    gc.enable()
    verificar_orden_y_permutacion(resultado_ordenado, datos_entrada)
    return (tiempo_fin - tiempo_inicio) * 1000.0


def medir_tiempo_algoritmo(funcion_ordenamiento, arreglo_base, cantidad_repeticiones):
    tiempos_milisegundos = []
    for indice_repeticion in range(cantidad_repeticiones):
        duracion_ms = ejecutar_experimento(funcion_ordenamiento, arreglo_base)
        tiempos_milisegundos.append(duracion_ms)
    media_ms = statistics.mean(tiempos_milisegundos)
    desviacion_ms = statistics.stdev(tiempos_milisegundos) if len(tiempos_milisegundos) > 1 else 0.0
    return media_ms, desviacion_ms, tiempos_milisegundos


def ejecutar_escenario_aleatorio(tamanos_entrada, cantidad_repeticiones, semilla_base):
    registros_aleatorios = []
    catalogo_algoritmos = [
        ("Heapsort", heapsort),
        ("Quicksort (Lomuto)", quicksort_lomuto),
        ("Python sorted() [Timsort]", sorted),
    ]
    for tamano_actual in tamanos_entrada:
        generador_aleatorio = random.Random(semilla_base + tamano_actual)
        arreglo_aleatorio = [generador_aleatorio.randint(-100000, 100000) for indice_elemento in range(tamano_actual)]
        for nombre_algoritmo, funcion_algoritmo in catalogo_algoritmos:
            media_ms, desviacion_ms, lista_tiempos = medir_tiempo_algoritmo(funcion_algoritmo, arreglo_aleatorio, cantidad_repeticiones)
            registros_aleatorios.append({
                "escenario": "Aleatorio (Caso Promedio)",
                "algoritmo": nombre_algoritmo,
                "tamano_entrada": tamano_actual,
                "repeticiones": cantidad_repeticiones,
                "media_ms": media_ms,
                "desviacion_ms": desviacion_ms,
            })
    return registros_aleatorios


def ejecutar_escenario_ordenado(tamanos_peor_caso, cantidad_repeticiones):
    registros_ordenados = []
    catalogo_algoritmos = [
        ("Heapsort", heapsort),
        ("Quicksort (Lomuto)", quicksort_lomuto),
        ("Python sorted() [Timsort]", sorted),
    ]
    for tamano_actual in tamanos_peor_caso:
        arreglo_ordenado = list(range(tamano_actual))
        for nombre_algoritmo, funcion_algoritmo in catalogo_algoritmos:
            media_ms, desviacion_ms, lista_tiempos = medir_tiempo_algoritmo(funcion_algoritmo, arreglo_ordenado, cantidad_repeticiones)
            registros_ordenados.append({
                "escenario": "Ordenado Ascendente (Peor Caso Quicksort)",
                "algoritmo": nombre_algoritmo,
                "tamano_entrada": tamano_actual,
                "repeticiones": cantidad_repeticiones,
                "media_ms": media_ms,
                "desviacion_ms": desviacion_ms,
            })
    return registros_ordenados


def generar_grafica_comparativa(registros_aleatorios, registros_ordenados, ruta_imagen):
    figura, (eje_promedio, eje_peor_caso) = graficador.subplots(1, 2, figsize=(11, 4.6), dpi=300)
    estilos_visuales = {
        "Heapsort": {"color": "#1f77b4", "marcador": "o", "estilo_linea": "-"},
        "Quicksort (Lomuto)": {"color": "#d62728", "marcador": "s", "estilo_linea": "--"},
        "Python sorted() [Timsort]": {"color": "#2ca02c", "marcador": "^", "estilo_linea": "-."},
    }

    for nombre_algoritmo, configuracion_estilo in estilos_visuales.items():
        subconjunto_promedio = [fila for fila in registros_aleatorios if fila["algoritmo"] == nombre_algoritmo]
        valores_tamano = [fila["tamano_entrada"] for fila in subconjunto_promedio]
        valores_media = [fila["media_ms"] for fila in subconjunto_promedio]
        valores_desviacion = [fila["desviacion_ms"] for fila in subconjunto_promedio]
        eje_promedio.errorbar(
            valores_tamano,
            valores_media,
            yerr=valores_desviacion,
            label=nombre_algoritmo,
            color=configuracion_estilo["color"],
            marker=configuracion_estilo["marcador"],
            linestyle=configuracion_estilo["estilo_linea"],
            linewidth=1.8,
            capsize=3,
        )

    eje_promedio.set_title("A) Caso Promedio: Entrada Aleatoria", fontsize=10, fontweight="bold")
    eje_promedio.set_xlabel("Tamaño de entrada (n)", fontsize=9)
    eje_promedio.set_ylabel("Tiempo de ejecución (ms)", fontsize=9)
    eje_promedio.grid(True, linestyle=":", alpha=0.7)
    eje_promedio.legend(fontsize=8)

    for nombre_algoritmo, configuracion_estilo in estilos_visuales.items():
        subconjunto_peor = [fila for fila in registros_ordenados if fila["algoritmo"] == nombre_algoritmo]
        valores_tamano = [fila["tamano_entrada"] for fila in subconjunto_peor]
        valores_media = [fila["media_ms"] for fila in subconjunto_peor]
        valores_desviacion = [fila["desviacion_ms"] for fila in subconjunto_peor]
        eje_peor_caso.errorbar(
            valores_tamano,
            valores_media,
            yerr=valores_desviacion,
            label=nombre_algoritmo,
            color=configuracion_estilo["color"],
            marker=configuracion_estilo["marcador"],
            linestyle=configuracion_estilo["estilo_linea"],
            linewidth=1.8,
            capsize=3,
        )

    eje_peor_caso.set_title("B) Caso Peor: Entrada Preordenada", fontsize=10, fontweight="bold")
    eje_peor_caso.set_xlabel("Tamaño de entrada (n)", fontsize=9)
    eje_peor_caso.set_ylabel("Tiempo de ejecución (ms)", fontsize=9)
    eje_peor_caso.grid(True, linestyle=":", alpha=0.7)
    eje_peor_caso.legend(fontsize=8)

    figura.suptitle("Medición Piloto: Heapsort vs. Quicksort (Lomuto) vs. Timsort (Semilla 2026)", fontsize=11, fontweight="bold")
    figura.tight_layout()
    figura.savefig(ruta_imagen, dpi=300)
    graficador.close(figura)


def imprimir_resumen_consola(registros_totales):
    print("================================================================================")
    print("AMBIENTE EXPERIMENTAL DOCUMENTADO")
    print("================================================================================")
    print(f"Sistema Operativo : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Versión de Python : {platform.python_version()} ({platform.python_implementation()})")
    print("Procesador (CPU)  : 13th Gen Intel(R) Core(TM) i5-13420H")
    print("Memoria RAM       : 16.0 GB (15.64 GB utilizables)")
    print("Semilla Aleatoria : 2026 (Reproducible)")
    print("================================================================================\n")
    print(f"{'Escenario':<42} | {'Algoritmo':<25} | {'n':>6} | {'Media (ms)':>10} | {'DE (ms)':>9}")
    print("-" * 102)
    for fila in registros_totales:
        print(
            f"{fila['escenario']:<42} | "
            f"{fila['algoritmo']:<25} | "
            f"{fila['tamano_entrada']:>6} | "
            f"{fila['media_ms']:>10.4f} | "
            f"{fila['desviacion_ms']:>9.4f}"
        )


def ejecutar_piloto_completo():
    directorio_experimentos = os.path.dirname(os.path.abspath(__file__))
    ruta_grafica = os.path.join(directorio_experimentos, "grafica_piloto.png")

    tamanos_aleatorios = [1000, 2500, 5000, 10000]
    tamanos_ordenados = [500, 1000, 1500, 2000]
    cantidad_repeticiones = 5
    semilla_fija = 2026

    resultados_aleatorios = ejecutar_escenario_aleatorio(tamanos_aleatorios, cantidad_repeticiones, semilla_fija)
    resultados_ordenados = ejecutar_escenario_ordenado(tamanos_ordenados, cantidad_repeticiones)
    todos_los_resultados = resultados_aleatorios + resultados_ordenados

    generar_grafica_comparativa(resultados_aleatorios, resultados_ordenados, ruta_grafica)
    imprimir_resumen_consola(todos_los_resultados)
    print(f"\nGráfica PNG generada en   : {ruta_grafica}")


if __name__ == "__main__":
    ejecutar_piloto_completo()
