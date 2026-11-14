import heapq
import os
import random
import sys
import unittest
from hypothesis import given, seed, settings
from hypothesis import strategies as estrategias_hypothesis

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.eventos import EventoSidor, clave_prioridad_evento, generar_lote_eventos_sidor
from src.ordenamiento import build_max_heap, heapsort, max_heapify, particionar_3v, quicksort, top_k

random.seed(2026)


class TestAlgoritmosOrdenamientoSidor(unittest.TestCase):

    def test_01_limites_vacio_y_unitario(self):
        self.assertEqual(heapsort([]), [])
        self.assertEqual(quicksort([]), [])
        self.assertEqual(top_k([], 5), [])
        self.assertEqual(heapsort([42]), [42])
        self.assertEqual(quicksort([42]), [42])
        self.assertEqual(top_k([42], 5), [42])

    def test_02_inundacion_claves_iguales(self):
        lote_inundacion = [940] * 2000
        self.assertEqual(heapsort(lote_inundacion.copy()), lote_inundacion)
        self.assertEqual(quicksort(lote_inundacion.copy()), lote_inundacion)
        self.assertEqual(top_k(lote_inundacion, 10), [940] * 10)

    def test_03_entradas_ordenadas_e_invertidas(self):
        datos_ordenados = list(range(500))
        datos_invertidos = list(range(499, -1, -1))
        self.assertEqual(heapsort(datos_ordenados.copy()), datos_ordenados)
        self.assertEqual(quicksort(datos_ordenados.copy()), datos_ordenados)
        self.assertEqual(heapsort(datos_invertidos.copy()), datos_ordenados)
        self.assertEqual(quicksort(datos_invertidos.copy()), datos_ordenados)

    def test_04_bordes_parametro_top_k(self):
        datos_base = [10, 50, 30, 90, 20]
        self.assertEqual(top_k(datos_base, 0), [])
        self.assertEqual(top_k(datos_base, 20), [90, 50, 30, 20, 10])
        with self.assertRaises(ValueError):
            top_k(datos_base, -1)

    def test_05_invariantes_heap_y_particion_3v(self):
        datos_heap = [14, 8, 25, 3, 19, 25, 7, 11, 2]
        build_max_heap(datos_heap)
        tamano_total = len(datos_heap)

        for indice_fin in range(tamano_total - 1, 0, -1):
            datos_heap[0], datos_heap[indice_fin] = datos_heap[indice_fin], datos_heap[0]
            max_heapify(datos_heap, 0, indice_fin)
            for indice_padre in range(indice_fin // 2):
                hijo_izq = 2 * indice_padre + 1
                hijo_der = 2 * indice_padre + 2
                if hijo_izq < indice_fin:
                    self.assertGreaterEqual(datos_heap[indice_padre], datos_heap[hijo_izq])
                if hijo_der < indice_fin:
                    self.assertGreaterEqual(datos_heap[indice_padre], datos_heap[hijo_der])
            sufijo_ordenado = datos_heap[indice_fin:]
            self.assertEqual(sufijo_ordenado, sorted(sufijo_ordenado))

        datos_particion = [50, 20, 50, 80, 10, 50, 90, 30]
        valor_pivote = datos_particion[0]
        frontera_menor, frontera_mayor = particionar_3v(datos_particion, 0, len(datos_particion) - 1)
        for elemento_izq in datos_particion[:frontera_menor]:
            self.assertLess(elemento_izq, valor_pivote)
        for elemento_medio in datos_particion[frontera_menor : frontera_mayor + 1]:
            self.assertEqual(elemento_medio, valor_pivote)
        for elemento_der in datos_particion[frontera_mayor + 1 :]:
            self.assertGreater(elemento_der, valor_pivote)

    def test_06_caso_uso_sidor_alto_horno_y_laminador(self):
        lote_sidor = generar_lote_eventos_sidor(500, semilla=2026)
        tablero_top_10 = top_k(lote_sidor, 10, clave=clave_prioridad_evento)
        self.assertEqual(len(tablero_top_10), 10)
        self.assertEqual(tablero_top_10[0].criticidad, 960)
        self.assertEqual(tablero_top_10[0].origen, "enlace_planta")
        self.assertEqual(tablero_top_10[1].criticidad, 940)
        self.assertEqual(tablero_top_10[1].origen, "alto_horno")
        for indice_pos in range(1, len(tablero_top_10) - 1):
            clave_actual = clave_prioridad_evento(tablero_top_10[indice_pos])
            clave_siguiente = clave_prioridad_evento(tablero_top_10[indice_pos + 1])
            self.assertGreaterEqual(clave_actual, clave_siguiente)

    @seed(2026)
    @settings(max_examples=100, derandomize=True)
    @given(estrategias_hypothesis.lists(estrategias_hypothesis.integers(min_value=-1000, max_value=1000)))
    def test_07_propiedad_orden_y_multiconjunto(self, lista_generada):
        referencia_ascendente = sorted(lista_generada)

        copia_heapsort = lista_generada.copy()
        heapsort(copia_heapsort)
        self.assertEqual(copia_heapsort, referencia_ascendente)

        copia_quicksort = lista_generada.copy()
        quicksort(copia_quicksort)
        self.assertEqual(copia_quicksort, referencia_ascendente)

    @seed(2026)
    @settings(max_examples=100, derandomize=True)
    @given(
        estrategias_hypothesis.lists(estrategias_hypothesis.integers(min_value=0, max_value=1000), max_size=200),
        estrategias_hypothesis.integers(min_value=0, max_value=50),
    )
    def test_08_propiedad_top_k_contra_sorted(self, lista_generada, cantidad_top):
        esperado_top = sorted(lista_generada, reverse=True)[:cantidad_top]
        obtenido_top = top_k(lista_generada, cantidad_top)
        self.assertEqual(obtenido_top, esperado_top)

    def test_09_diferencial_eventos_sidor(self):
        for tamano_lote in (1000, 20000):
            lote_eventos = generar_lote_eventos_sidor(tamano_lote, semilla=2026)
            referencia_s2 = sorted(lote_eventos, key=clave_prioridad_evento, reverse=True)
            referencia_s1 = heapq.nlargest(10, lote_eventos, key=clave_prioridad_evento)

            resultado_heapsort = heapsort(lote_eventos.copy(), clave=clave_prioridad_evento, descendente=True)
            resultado_quicksort = quicksort(lote_eventos.copy(), clave=clave_prioridad_evento, descendente=True)
            resultado_top_k = top_k(lote_eventos, 10, clave=clave_prioridad_evento)

            self.assertEqual(resultado_heapsort, referencia_s2)
            self.assertEqual(resultado_quicksort, referencia_s2)
            self.assertEqual(resultado_top_k, referencia_s1)


if __name__ == "__main__":
    unittest.main()
