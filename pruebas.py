import traceback
import collections
import random

import imagen

def ejercicio_1():
    # verificamos la creación
    img = imagen.Imagen(16, 20, 84)

    assert img.get_valor_max() == 16
    assert img.get_ancho() == 20
    assert img.get_alto() == 84

    # verificamos que todos los pixels tienen color negro
    for x in range(30):
        for y in range(60):
            assert img.get(x, y) == (0, 0, 0)

    img = imagen.Imagen(255, 30, 60)

    assert img.get_valor_max() == 255
    assert img.get_ancho() == 30
    assert img.get_alto() == 60

    # pintamos la imagen con un patrón arbitrario
    for x in range(30):
        for y in range(60):
            color = (x, y, x + y) # (r, g, b)
            img.set(x, y, color)

    # verificamos que cada uno de los pixels tiene el valor asignado
    for x in range(30):
        for y in range(60):
            color = (x, y, x + y)
            assert img.get(x, y) == color

    # asignar un pixel en una coordenada fuera de rango no debería dar error
    img.set(-1, -1, (255, 255, 255))
    img.set(30, 60, (255, 255, 255))

    # obtener un pixel en una coordenada fuera de rango debería dar siempre negro (0, 0, 0)
    img.get(-1, -1) == (0, 0, 0)
    img.get(30, 60) == (0, 0, 0)

    color = (255, 255, 255)

    # pintamos la imagen con un color uniforme
    img.pintar(color)

    # verificamos que cada uno de los pixels tiene el valor asignado
    for x in range(30):
        for y in range(60):
            assert img.get(x, y) == color

    # verificamos que set() aplica restricción de rango
    img.set(10, 10, (256, -1, -3))
    assert img.get(10, 10) == (255, 0, 0)


def ejercicio_2():
    # función auxiliar
    def _verificar_ppm(ruta, esperado):
        esperado = _quitar_sangria(esperado)
        with open(ruta) as f:
            obtenido = f.read()
        lesp = [l.strip() for l in esperado.split('\n') if l.strip()]
        lobt = [l.strip() for l in obtenido.split('\n') if l.strip()]
        assert len(lesp) == len(lobt), \
            f"El archivo PPM no es correcto (diferencia en la cantidad de líneas)\n" + \
            f"esperado:\n{esperado}\n" + \
            f"obtenido:\n{obtenido}"
        for i, (l1, l2) in enumerate(zip(lesp, lobt)):
            assert l1.split() == l2.split(), \
                f"El archivo PPM no es correcto (diferencia en la línea {i + 1}):\n" + \
                f"esperado:\n{esperado}\n" + \
                f"obtenido:\n{obtenido}"

    img = imagen.Imagen(255, 4, 5)

    # pintamos la imagen con un patrón arbitrario
    for x in range(4):
        for y in range(5):
            color = (x, y, x * x * y * y) # (r, g, b)
            img.set(x, y, color)

    # escribimos la imagen en formato PPM
    img.escribir_ppm("imagen.ppm")

    # verificamos el contenido del archivo
    _verificar_ppm("imagen.ppm", """
        P3
        4 5
        255
        0 0 0   1 0  0   2 0  0   3 0   0
        0 1 0   1 1  1   2 1  4   3 1   9
        0 2 0   1 2  4   2 2 16   3 2  36
        0 3 0   1 3  9   2 3 36   3 3  81
        0 4 0   1 4 16   2 4 64   3 4 144
    """)

def ejercicio_3():
    with open("imagen.ppm", "w") as f:
        f.write(_quitar_sangria("""
            P3
            4 5
            255
            0  0  0    0  0  0    0  0  0   15  0 15
            0  0  0    0 15  7    0  0  0    0  0  0
            0  0  0    0  0  0    0 15  7    0  0  0
            15 0 15    0  0  0    0  0  0    0  0  0
            15 0 15    0  0  0    0  0  0    0 15  0
        """))

    # leemos el archivo PPM
    img = imagen.leer_ppm("imagen.ppm")

    assert img.get_valor_max() == 255
    assert img.get_ancho() == 4
    assert img.get_alto() == 5
    assert img.get(0, 0) == (0, 0, 0)
    assert img.get(1, 1) == (0, 15, 7)
    assert img.get(0, 4) == (15, 0, 15)
    assert img.get(3, 4) == (0, 15, 0)

def ejercicio_4():
    negro = (0, 0, 0)
    blanco = (255, 255, 255)
    rojo = (255, 0, 0)
    verde = (0, 255, 0)

    histograma_esperado = {
        negro: 100,
        rojo: 250,
        verde: (100*100 - 100 - 200 - 250),
        blanco: 200,
    }

    colores = sum([[color] * cantidad for color, cantidad in histograma_esperado.items()], [])
    random.shuffle(colores)

    # creamos una imagen de 100 x 100 con un histograma arbitrario
    img = imagen.Imagen(255, 100, 100)
    for x in range(100):
        for y in range(100):
            color = (255 - x, y, x + y) # (r, g, b)
            img.set(x, y, colores.pop())
    assert len(colores) == 0

    h = img.histograma()

    assert h == histograma_esperado, f"\nhistograma         ={h}\nhistograma esperado={histograma_esperado}"

    c = img.colores_mas_frecuentes()

    c_esperado = [
        (verde, 100*100 - 100 - 200 - 250),
        (rojo, 250),
        (blanco, 200),
        (negro, 100),
    ]

    assert c == c_esperado, f"\colores         ={h}\colores esperado={histograma_esperado}"

    assert img.promedio() == (11, 246, 5)

def ejercicio_5():
    # función auxiliar
    def _pintar_patron(img, patron):
        for y, linea in enumerate(_quitar_sangria(patron).split('\n')):
            for x, c in enumerate(linea):
                color = (0, 0, 0) if c == '.' else (255, 255, 255)
                img.set(x, y, color)

    # función auxiliar
    def _verificar_patron(img, patron):
        for y, linea in enumerate(_quitar_sangria(patron).split('\n')):
            for x, c in enumerate(linea):
                color_esperado = (0, 0, 0) if c == '.' else (255, 255, 255)
                color = img.get(x, y)
                assert color == color_esperado, f"el pixel ({x}, {y}) debería ser color {color_esperado}, pero es {color}"

    img = imagen.Imagen(255, 10, 10)
    # pintamos una región "hueca". Los caracteres "." representan un pixel color negro,
    # y "#" un pixel color blanco.
    _pintar_patron(img, """
        ........#.
        ...######.
        ...#......
        ####..####
        ......#...
        ##...#....
        .#...#....
        .#..#.....
        .##.#.....
        ..#.#.....
    """)

    # rellenamos de color blanco a partir del pixel (4, 5).
    img.balde_de_pintura(4, 5, (255, 255, 255))

    _verificar_patron(img, """
        ........##
        ...#######
        ...#######
        ##########
        #######...
        ######....
        .#####....
        .####.....
        .####.....
        ..###.....
    """)


def _quitar_sangria(s):
    "Función auxiliar. Quita la sangría del texto."
    return ''.join([l.strip() + '\n' for l in s.split('\n') if l.strip()])

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
