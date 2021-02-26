import traceback
import random
import aerodb

def ejercicio_1():
    a = aerodb.AeroDB()
    assert a.cantidad_aeropuertos() == 0

    a.aeropuerto_agregar("EZE", "Ministro Pistarini International Airport", "Buenos Aires", "Argentina", -34.8222, -58.5358)
    assert a.cantidad_aeropuertos() == 1
    assert a.aeropuerto_get_nombre("EZE") == "Ministro Pistarini International Airport"
    assert a.aeropuerto_get_ciudad("EZE") == "Buenos Aires"
    assert a.aeropuerto_get_pais("EZE") == "Argentina"
    assert a.aeropuerto_get_coords("EZE") == (-34.8222, -58.5358)

    a.aeropuerto_agregar("BRC", "San Carlos De Bariloche Airport", "San Carlos De Bariloche", "Argentina", -41.151199, -71.157501)
    assert a.cantidad_aeropuertos() == 2
    assert a.aeropuerto_get_nombre("BRC") == "San Carlos De Bariloche Airport"
    assert a.aeropuerto_get_ciudad("BRC") == "San Carlos De Bariloche"
    assert a.aeropuerto_get_pais("BRC") == "Argentina"
    assert a.aeropuerto_get_coords("BRC") == (-41.151199, -71.157501)

    a.aeropuerto_agregar("FRA", "Frankfurt am Main Airport", "Frankfurt", "Germany", 50.033333, 8.570556)
    assert a.cantidad_aeropuertos() == 3

    assert a.cantidad_rutas() == 0

    a.ruta_agregar("AR412", "EZE", "BRC")
    assert a.cantidad_rutas() == 1

    a.ruta_agregar("AR412", "BRC", "EZE")
    assert a.cantidad_rutas() == 2

    a.ruta_agregar("LH3320", "EZE", "FRA")
    assert a.cantidad_rutas() == 3

def ejercicio_2():
    a = aerodb.AeroDB()

    a.aeropuerto_agregar("EZE", "Ministro Pistarini International Airport", "Buenos Aires", "Argentina", -34.8222, -58.5358)
    a.aeropuerto_agregar("AEP", "Jorge Newbery Airpark", "Buenos Aires", "Argentina", -34.5592, -58.4156)
    a.aeropuerto_agregar("BRC", "San Carlos De Bariloche Airport", "San Carlos De Bariloche", "Argentina", -41.151199, -71.157501)
    a.aeropuerto_agregar("FRA", "Frankfurt am Main Airport", "Frankfurt", "Germany", 50.033333, 8.570556)
    a.aeropuerto_agregar("DUB", "Dublin Airport", "Dublin", "Ireland", 53.421299, -6.27007)
    a.ruta_agregar("AR412", "EZE", "BRC")
    a.ruta_agregar("AR412", "BRC", "EZE")
    a.ruta_agregar("AR412", "AEP", "BRC")
    a.ruta_agregar("AR412", "BRC", "AEP")
    a.ruta_agregar("LH3320", "EZE", "FRA")
    a.ruta_agregar("EI837", "DUB", "FRA")
    a.ruta_agregar("EI837", "FRA", "DUB")
    a.ruta_agregar("LH3320", "DUB", "FRA")
    a.ruta_agregar("LH3320", "FRA", "DUB")

    rutas = a.rutas_desde_ciudad("Buenos Aires")
    assert_iguales(
            'a.rutas_desde_ciudad("Buenos Aires")',
            sorted(rutas),
            [('AR412', 'AEP', 'BRC'), ('AR412', 'EZE', 'BRC'), ('LH3320', 'EZE', 'FRA')]
    )

    rutas = a.rutas_hacia_ciudad("Frankfurt")
    assert_iguales(
            'a.rutas_hacia_ciudad("Frankfurt")',
            sorted(rutas),
            [('EI837', 'DUB', 'FRA'), ('LH3320', 'DUB', 'FRA'), ('LH3320', 'EZE', 'FRA')]
    )

def ejercicio_3():
    a = aerodb.cargar("aeropuertos.csv", "rutas.csv")

    assert a.cantidad_aeropuertos() == 6072
    assert a.cantidad_rutas() == 67184

    assert a.aeropuerto_get_nombre("EZE") == "Ministro Pistarini International Airport"
    assert a.aeropuerto_get_ciudad("EZE") == "Buenos Aires"
    assert a.aeropuerto_get_pais("EZE") == "Argentina"

    #assert a.aeropuerto_con_mas_rutas() == ("ATL", 1826)

def ejercicio_4():
    a = aerodb.AeroDB()

    a.aeropuerto_agregar("EZE", "Ministro Pistarini International Airport", "Buenos Aires", "Argentina", -34.8222, -58.5358)
    a.aeropuerto_agregar("BRC", "San Carlos De Bariloche Airport", "San Carlos De Bariloche", "Argentina", -41.151199, -71.157501)
    a.aeropuerto_agregar("FRA", "Frankfurt am Main Airport", "Frankfurt", "Germany", 50.033333, 8.570556)
    a.aeropuerto_agregar("DUB", "Dublin Airport", "Dublin", "Ireland", 53.421299, -6.27007)

    assert_iguales(
            "a.aeropuertos_ordenados_por_distancia(-34, -58)",
            a.aeropuertos_ordenados_por_distancia(-34, -58),
            ['EZE', 'BRC', 'DUB', 'FRA']
    )

def ejercicio_5():
    a = aerodb.AeroDB()

    a.aeropuerto_agregar("EZE", "Ministro Pistarini International Airport", "Buenos Aires", "Argentina", -34.8222, -58.5358)
    a.aeropuerto_agregar("BRC", "San Carlos De Bariloche Airport", "San Carlos De Bariloche", "Argentina", -41.151199, -71.157501)
    a.aeropuerto_agregar("FRA", "Frankfurt am Main Airport", "Frankfurt", "Germany", 50.033333, 8.570556)
    a.aeropuerto_agregar("DUB", "Dublin Airport", "Dublin", "Ireland", 53.421299, -6.27007)
    a.ruta_agregar("AR412", "EZE", "BRC")
    a.ruta_agregar("LH3320", "EZE", "FRA")
    a.ruta_agregar("EI837", "DUB", "FRA")
    a.ruta_agregar("EI837", "FRA", "DUB")
    a.ruta_agregar("LH3320", "DUB", "FRA")
    a.ruta_agregar("LH3320", "FRA", "DUB")

    itinerario = a.armar_itinerario("BRC", "DUB")
    assert itinerario is None

    itinerario = a.armar_itinerario("EZE", "BRC")
    assert itinerario == [("AR412", "EZE", "BRC")]

    itinerario = a.armar_itinerario("EZE", "DUB")
    assert itinerario == [("LH3320", "EZE", "FRA"), ("EI837", "FRA", "DUB")] \
           or itinerario == [("LH3320", "EZE", "FRA"), ("LH3320", "FRA", "DUB")]


def assert_iguales(k, v1, v2):
    k1 = f"Resultado de {k}"
    k2 = f"Resultado esperado"
    n = max(len(k1), len(k2))
    assert v1 == v2, f"\n  {k1:<{n}}: {v1}\n  {k2:<{n}}: {v2}"

def main():
    ejercicios = [
        ejercicio_1,
        ejercicio_2,
        ejercicio_3,
        ejercicio_4,
        ejercicio_5,
    ]

    ejercicios_ok = 0

    for i, ejercicio in enumerate(ejercicios):
        try:
            random.seed(0)
            ejercicio()
            resultado = 'OK'
            ejercicios_ok += 1
        except:
            print()
            traceback.print_exc()
            print()
            resultado = 'FAIL'
        print(f"{ejercicio.__name__}: {resultado}")

    print(f"Cantidad de ejercicios OK: {ejercicios_ok}")

main()
