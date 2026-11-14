import random
from dataclasses import dataclass

ORIGENES_SIDOR = (
    "alto_horno",
    "laminador",
    "erp",
    "mainframe",
    "enlace_planta",
)


@dataclass(frozen=True)
class EventoSidor:
    identificador: int
    marca_tiempo: int
    origen: str
    criticidad: int


def calcular_criticidad(severidad, impacto, desviacion):
    valor_bruto = 100 * severidad + 80 * impacto + 20 * desviacion
    return max(0, min(1000, valor_bruto))


def clave_prioridad_evento(evento):
    return (evento.criticidad, -evento.marca_tiempo, -evento.identificador)


def construir_evento_individual(indice_evento, tiempo_base, generador):
    marca_tiempo = tiempo_base + (indice_evento // 5) + generador.randint(0, 3)
    probabilidad_tipo = generador.random()

    if probabilidad_tipo < 0.80:
        severidad = generador.randint(0, 2)
        impacto = generador.randint(0, 1)
        desviacion = generador.randint(0, 2)
        origen_evento = generador.choice(ORIGENES_SIDOR)
        criticidad_calculada = calcular_criticidad(severidad, impacto, desviacion)
        return EventoSidor(indice_evento, marca_tiempo, origen_evento, criticidad_calculada)

    if probabilidad_tipo < 0.95:
        severidad = generador.randint(3, 4)
        impacto = generador.randint(1, 2)
        desviacion = generador.randint(1, 3)
        origen_evento = generador.choice(ORIGENES_SIDOR)
        criticidad_calculada = calcular_criticidad(severidad, impacto, desviacion)
        return EventoSidor(indice_evento, marca_tiempo, origen_evento, criticidad_calculada)

    severidad = generador.randint(5, 6)
    impacto = generador.randint(2, 3)
    desviacion = generador.randint(1, 2)
    origen_evento = generador.choice(("alto_horno", "laminador", "enlace_planta"))
    criticidad_calculada = calcular_criticidad(severidad, impacto, desviacion)
    return EventoSidor(indice_evento, marca_tiempo, origen_evento, criticidad_calculada)


def generar_lote_eventos_sidor(cantidad_eventos, semilla=2026):
    generador = random.Random(semilla)
    tiempo_base = 1763000000
    lista_eventos = [
        construir_evento_individual(indice_evento, tiempo_base, generador)
        for indice_evento in range(1, cantidad_eventos + 1)
    ]

    if cantidad_eventos >= 20:
        cantidad_rafaga_horno = min(800, max(5, cantidad_eventos // 40))
        for desplazamiento in range(cantidad_rafaga_horno):
            indice_objetivo = (desplazamiento * 7) % cantidad_eventos
            evento_previo = lista_eventos[indice_objetivo]
            lista_eventos[indice_objetivo] = EventoSidor(
                identificador=evento_previo.identificador,
                marca_tiempo=tiempo_base + 140 + desplazamiento,
                origen="alto_horno",
                criticidad=940,
            )

        evento_enlace = lista_eventos[cantidad_eventos // 2]
        lista_eventos[cantidad_eventos // 2] = EventoSidor(
            identificador=evento_enlace.identificador,
            marca_tiempo=tiempo_base + 145,
            origen="enlace_planta",
            criticidad=960,
        )

    return lista_eventos
