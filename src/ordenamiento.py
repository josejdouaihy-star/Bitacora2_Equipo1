import random


def obtener_valor_clave(elemento, funcion_clave):
    if funcion_clave is None:
        return elemento
    return funcion_clave(elemento)


def max_heapify(arreglo_datos, indice_raiz, tamano_heap, clave=None):
    indice_actual = indice_raiz
    while True:
        indice_hijo_izquierdo = 2 * indice_actual + 1
        indice_hijo_derecho = 2 * indice_actual + 2
        indice_mayor = indice_actual

        if indice_hijo_izquierdo < tamano_heap and obtener_valor_clave(arreglo_datos[indice_hijo_izquierdo], clave) > obtener_valor_clave(arreglo_datos[indice_mayor], clave):
            indice_mayor = indice_hijo_izquierdo

        if indice_hijo_derecho < tamano_heap and obtener_valor_clave(arreglo_datos[indice_hijo_derecho], clave) > obtener_valor_clave(arreglo_datos[indice_mayor], clave):
            indice_mayor = indice_hijo_derecho

        if indice_mayor == indice_actual:
            return

        arreglo_datos[indice_actual], arreglo_datos[indice_mayor] = arreglo_datos[indice_mayor], arreglo_datos[indice_actual]
        indice_actual = indice_mayor


def build_max_heap(arreglo_datos, clave=None):
    tamano_arreglo = len(arreglo_datos)
    for indice_nodo in range((tamano_arreglo // 2) - 1, -1, -1):
        max_heapify(arreglo_datos, indice_nodo, tamano_arreglo, clave=clave)


def heapsort(arreglo_datos, clave=None, descendente=False):
    build_max_heap(arreglo_datos, clave=clave)
    tamano_arreglo = len(arreglo_datos)

    for indice_fin in range(tamano_arreglo - 1, 0, -1):
        arreglo_datos[0], arreglo_datos[indice_fin] = arreglo_datos[indice_fin], arreglo_datos[0]
        max_heapify(arreglo_datos, 0, indice_fin, clave=clave)

    if descendente:
        arreglo_datos.reverse()

    return arreglo_datos


def top_k(arreglo_datos, cantidad_top, clave=None):
    if cantidad_top < 0:
        raise ValueError("El parametro cantidad_top debe ser mayor o igual a cero")
    if cantidad_top == 0 or len(arreglo_datos) == 0:
        return []

    copia_heap = list(arreglo_datos)
    build_max_heap(copia_heap, clave=clave)
    tamano_arreglo = len(copia_heap)
    limite_extraccion = min(cantidad_top, tamano_arreglo)
    eventos_criticos = []

    for paso_extraccion in range(limite_extraccion):
        eventos_criticos.append(copia_heap[0])
        indice_fin = tamano_arreglo - 1 - paso_extraccion
        copia_heap[0], copia_heap[indice_fin] = copia_heap[indice_fin], copia_heap[0]
        max_heapify(copia_heap, 0, indice_fin, clave=clave)

    return eventos_criticos


def clasificar_elemento_3v(arreglo_datos, indice_exploracion, frontera_menor, frontera_mayor, clave_pivote, clave, descendente):
    clave_actual = obtener_valor_clave(arreglo_datos[indice_exploracion], clave)
    debe_ir_izquierda = clave_actual > clave_pivote if descendente else clave_actual < clave_pivote
    debe_ir_derecha = clave_actual < clave_pivote if descendente else clave_actual > clave_pivote

    if debe_ir_izquierda:
        arreglo_datos[frontera_menor], arreglo_datos[indice_exploracion] = arreglo_datos[indice_exploracion], arreglo_datos[frontera_menor]
        return frontera_menor + 1, indice_exploracion + 1, frontera_mayor

    if debe_ir_derecha:
        arreglo_datos[indice_exploracion], arreglo_datos[frontera_mayor] = arreglo_datos[frontera_mayor], arreglo_datos[indice_exploracion]
        return frontera_menor, indice_exploracion, frontera_mayor - 1

    return frontera_menor, indice_exploracion + 1, frontera_mayor


def particionar_3v(arreglo_datos, indice_bajo, indice_alto, clave=None, descendente=False):
    clave_pivote = obtener_valor_clave(arreglo_datos[indice_bajo], clave)
    frontera_menor = indice_bajo
    indice_exploracion = indice_bajo + 1
    frontera_mayor = indice_alto

    while indice_exploracion <= frontera_mayor:
        frontera_menor, indice_exploracion, frontera_mayor = clasificar_elemento_3v(
            arreglo_datos,
            indice_exploracion,
            frontera_menor,
            frontera_mayor,
            clave_pivote,
            clave,
            descendente,
        )

    return frontera_menor, frontera_mayor


def quicksort(arreglo_datos, indice_bajo=0, indice_alto=None, clave=None, descendente=False, generador_azar=None):
    if len(arreglo_datos) <= 1:
        return arreglo_datos
    if indice_alto is None:
        indice_alto = len(arreglo_datos) - 1
    if generador_azar is None:
        generador_azar = random.Random(2026)

    while indice_bajo < indice_alto:
        indice_aleatorio = generador_azar.randint(indice_bajo, indice_alto)
        arreglo_datos[indice_bajo], arreglo_datos[indice_aleatorio] = arreglo_datos[indice_aleatorio], arreglo_datos[indice_bajo]
        frontera_menor, frontera_mayor = particionar_3v(arreglo_datos, indice_bajo, indice_alto, clave=clave, descendente=descendente)

        tamano_izquierdo = frontera_menor - indice_bajo
        tamano_derecho = indice_alto - frontera_mayor

        if tamano_izquierdo < tamano_derecho:
            quicksort(arreglo_datos, indice_bajo, frontera_menor - 1, clave=clave, descendente=descendente, generador_azar=generador_azar)
            indice_bajo = frontera_mayor + 1
        if tamano_izquierdo >= tamano_derecho:
            quicksort(arreglo_datos, frontera_mayor + 1, indice_alto, clave=clave, descendente=descendente, generador_azar=generador_azar)
            indice_alto = frontera_menor - 1

    return arreglo_datos


def particionar_lomuto(arreglo_datos, indice_izquierdo, indice_derecho, clave=None):
    valor_pivote = obtener_valor_clave(arreglo_datos[indice_derecho], clave)
    indice_frontera = indice_izquierdo - 1

    for indice_exploracion in range(indice_izquierdo, indice_derecho):
        if obtener_valor_clave(arreglo_datos[indice_exploracion], clave) <= valor_pivote:
            indice_frontera = indice_frontera + 1
            arreglo_datos[indice_frontera], arreglo_datos[indice_exploracion] = arreglo_datos[indice_exploracion], arreglo_datos[indice_frontera]

    arreglo_datos[indice_frontera + 1], arreglo_datos[indice_derecho] = arreglo_datos[indice_derecho], arreglo_datos[indice_frontera + 1]
    return indice_frontera + 1


def quicksort_lomuto(arreglo_datos, indice_izquierdo=0, indice_derecho=None, clave=None):
    if indice_derecho is None:
        indice_derecho = len(arreglo_datos) - 1

    if indice_izquierdo < indice_derecho:
        indice_pivote = particionar_lomuto(arreglo_datos, indice_izquierdo, indice_derecho, clave=clave)
        quicksort_lomuto(arreglo_datos, indice_izquierdo, indice_pivote - 1, clave=clave)
        quicksort_lomuto(arreglo_datos, indice_pivote + 1, indice_derecho, clave=clave)

    return arreglo_datos
