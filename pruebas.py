import traceback
import collections
import random

import tuiter

def ejercicio_1():
    t = tuiter.Tuiter()

    # creamos 2 autores
    id_grace = t.crear_autor("Grace")
    id_barbara = t.crear_autor("Barbara")
    assert id_grace is not None
    assert id_barbara is not None
    assert id_grace != id_barbara

    # ambos tienen 0 mensajes en su muro
    assert t.muro_cantidad(id_grace) == 0
    assert t.muro_cantidad(id_barbara) == 0

    # Grace publica un tuit
    id_tuit_grace = t.publicar(id_grace, "Hola, soy Grace")
    assert id_tuit_grace is not None

    assert t.tuit_id_autor(id_tuit_grace) == id_grace
    assert t.tuit_mensaje(id_tuit_grace) == "Hola, soy Grace"

    # El tuit fue publicado en el muro de Grace
    assert t.muro_cantidad(id_grace) == 1
    assert t.muro_cantidad(id_barbara) == 0

    # Grace no puede compartir su propio tuit
    ok = t.compartir(id_tuit_grace, id_grace)
    assert not ok

    # Barbara comparte el tuit
    ok = t.compartir(id_tuit_grace, id_barbara)
    assert ok

    assert t.muro_cantidad(id_grace) == 1
    assert t.muro_cantidad(id_barbara) == 1

    # barbara publica 100 tuits
    for i in range(100):
        t.publicar(id_barbara, f"Este es mi tuit nro {i + 1}")

    assert t.muro_cantidad(id_grace) == 1
    assert t.muro_cantidad(id_barbara) == 101

    # obtenemos un tuit en el medio del muro de Barbara
    id_tuit_barbara = t.muro_id_tuit(id_barbara, 50)
    assert id_tuit_barbara is not None

    assert t.tuit_id_autor(id_tuit_barbara) == id_barbara
    assert t.tuit_mensaje(id_tuit_barbara) == "Este es mi tuit nro 50"

    # Grace comparte el tuit
    ok = t.compartir(id_tuit_barbara, id_grace)
    assert ok

    assert t.muro_cantidad(id_grace) == 2
    assert t.muro_cantidad(id_barbara) == 101

def ejercicio_2():

    # función auxiliar
    def _verificar_csv(ruta, contenido_esperado):
        # quitamos la sangría y líneas vacías
        contenido_esperado = ''.join([l.strip() + '\n' for l in contenido_esperado.split('\n') if l.strip()])

        with open(ruta) as f:
            contenido = f.read()
            assert contenido == contenido_esperado, f"\n         contenido={contenido}\ncontenido_esperado={contenido_esperado}"

    t = tuiter.Tuiter()

    # creamos 2 autores
    id_grace = t.crear_autor("Grace")
    id_barbara = t.crear_autor("Barbara")

    # escribimos el muro de barbara (vacío) en un CSV
    t.muro_escribir_csv(id_barbara, "muro_barbara.csv")

    # el CSV solo debería tener la cabecera
    _verificar_csv("muro_barbara.csv", """
        autor|mensaje
    """)

    id_tuit_grace = t.publicar(id_grace, "Hola, soy Grace")

    t.publicar(id_barbara, "Hola, soy Barbara")
    ok = t.compartir(id_tuit_grace, id_barbara)

    # escribimos el muro de barbara (que tiene 2 tuits) en un CSV
    t.muro_escribir_csv(id_barbara, "muro_barbara.csv")

    _verificar_csv("muro_barbara.csv", """
        autor|mensaje
        Barbara|Hola, soy Barbara
        Grace|Hola, soy Grace
    """)

def ejercicio_3():
    t = tuiter.Tuiter()

    # creamos 2 autores
    id_grace = t.crear_autor("Grace")
    id_barbara = t.crear_autor("Barbara")

    # grace publica 100 tuits
    ids_tuits = []
    for i in range(100):
        id_tuit = t.publicar(id_grace, f"Tuit nro {i + 1}")
        ids_tuits.append(id_tuit)

    # Barbara comparte muchos tuits, muchas veces
    compartidos = collections.Counter()
    for i in range(1000):
        id_tuit = random.choice(ids_tuits)
        ok = t.compartir(id_tuit, id_barbara)
        assert ok
        compartidos.update((id_tuit,))

    # obtenemos los IDs de los tuits ordenados por cantidad de veces que fueron compartidos
    tuits_mas_compartidos = t.tuits_mas_compartidos()

    resultado_esperado = compartidos.most_common()
    assert sorted(tuits_mas_compartidos) == sorted(resultado_esperado), f"\ntuits_mas_compartidos={tuits_mas_compartidos}\n   resultado_esperado={resultado_esperado}"

def ejercicio_4():
    t = tuiter.Tuiter()

    # creamos 2 autores
    id_grace = t.crear_autor("Grace")
    id_barbara = t.crear_autor("Barbara")

    # grace publica un tuit
    id_tuit = t.publicar(id_grace, "Hola")

    # grace no puede dar like a su propio tuit
    ok = t.tuit_dar_like(id_tuit, id_grace)
    assert not ok
    assert not t.tuit_fue_likeado_por(id_tuit, id_grace)

    # barbara le da like
    ok = t.tuit_dar_like(id_tuit, id_barbara)
    assert ok
    assert t.tuit_fue_likeado_por(id_tuit, id_barbara)

    # barbara no puede darle like dos veces
    ok = t.tuit_dar_like(id_tuit, id_barbara)
    assert not ok
    assert t.tuit_fue_likeado_por(id_tuit, id_barbara)

    # creamos 10000 autores, algunos le dan like al tuit
    ids_autores = []
    for i in range(10000):
        id_autor = t.crear_autor(f"Autor nro {i + 1}")
        ids_autores.append(id_autor)

        if random.randint(0, 1) == 1:
            ok = t.tuit_dar_like(id_tuit, id_autor)
            assert ok

    # verificamos que tuit_fue_likeado_por es eficiente:
    for i in range(100000):
        id_autor = random.choice(ids_autores)
        t.tuit_fue_likeado_por(id_tuit, id_autor)

def ejercicio_5():
    t = tuiter.Tuiter()

    # creamos 2 autores
    id_grace = t.crear_autor("Grace")
    id_barbara = t.crear_autor("Barbara")

    # grace publica un tuit
    id_tuit = t.publicar(id_grace, "Hola")

    # el tuit no tiene respuestas
    assert list(t.tuit_respuestas(id_tuit)) == []

    # el tuit no es en respuesta de otro tuit
    assert t.tuit_en_respuesta_de(id_tuit) is None

    # la cantidad del hilo es 1
    assert t.tuit_cantidad_hilo(id_tuit) == 1

    # barbara responde al tuit
    id_respuesta = t.responder(id_tuit, id_barbara, f"Respuesta")

    # el tuit se publica en el muro de barbara
    assert t.muro_cantidad(id_barbara) == 1

    # el tuit es en respuesta del tuit de grace
    assert t.tuit_en_respuesta_de(id_respuesta) == id_tuit

    # el tuit original tiene a id_respuesta entre sus respuestas
    assert list(t.tuit_respuestas(id_tuit)) == [id_respuesta]

    # la cantidad del hilo es 2
    assert t.tuit_cantidad_hilo(id_tuit) == 2

    # hay más respuestas
    id_respuesta_2 = t.responder(id_respuesta, id_grace, f"Respuesta 2")
    id_respuesta_3 = t.responder(id_respuesta_2, id_barbara, f"Respuesta 3")
    # ojo, esta respuesta es al tuit original
    id_respuesta_4 = t.responder(id_tuit, id_barbara, f"Otra Respuesta")

    # la "forma" del hilo es:
    # id_tuit
    # | id_respuesta
    # | | id_respuesta_2
    # | | | id_respuesta_3
    # | id_respuesta_4

    # el tuit original tiene 2 respuestas
    assert list(t.tuit_respuestas(id_tuit)) == [id_respuesta, id_respuesta_4]

    # la cantidad del hilo es 5
    assert t.tuit_cantidad_hilo(id_tuit) == 5

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
