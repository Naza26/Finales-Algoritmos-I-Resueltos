import csv
class Imagen:
    "Representa una imagen digital"

    def __init__(self, valor_max, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.valor_max = valor_max
        self.imagen = {}
        for x in range(self.alto):
            for y in range(self.ancho):
                self.imagen[(x,y)] = (0,0,0)

    def get_valor_max(self):
        return self.valor_max

    def get_ancho(self):
        return self.ancho

    def get_alto(self):
        return self.alto

    def get(self, x, y):
        self.imagen[(x,y)] = self.imagen.get((x,y), (0,0,0))
        return self.imagen[(x,y)]

    def set(self, x, y, color):
        r,g,b = color
        lista_aux = []
        restriccion_rango = False
        try:
            if r > self.valor_max:
                restriccion_rango = True
                lista_aux.insert(0, (self.valor_max,g,b))
            if r < 0:
                restriccion_rango = True
                lista_aux.insert(0, (lista_aux[0][1],lista_aux[0][2]))
            if g > self.valor_max:
                restriccion_rango = True
                lista_aux.insert(0, (lista_aux[0][0],self.valor_max,lista_aux[0][2]))
            if g < 0:
                restriccion_rango = True
                lista_aux.insert(0, (lista_aux[0][0],0,lista_aux[0][2]))
            if b > self.valor_max:
                restriccion_rango = True
                lista_aux.insert(0, (lista_aux[0][0],lista_aux[0][1],self.valor_max))
            if b < 0:
                restriccion_rango = True
                lista_aux.insert(0, (lista_aux[0][0],lista_aux[0][1],0))
            if restriccion_rango:
                self.imagen[(x,y)] = lista_aux[0]
            else:
                self.imagen[(x,y)] = color
        except IndexError:
            pass

    def pintar(self, color):
        for x,y in self.imagen:
            self.imagen[(x,y)] = color

    def escribir_ppm(self, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write("P3\n")
            archivo.write(f"{self.ancho} {self.alto}\n")
            archivo.write(f"{self.valor_max}\n")
            for x in range(self.alto):
                archivo.write("\n")
                for y in range(self.ancho):
                    self.imagen[(y,x)] += (" ",)
                    archivo.write("{}".format(" ".join([''.join(map(str, str(x))) for x in self.imagen[(y,x)]])))
                    archivo.write("\t")
    def histograma(self):
        dic_histograma = {}
        for x,y in self.imagen:
            dic_histograma[self.imagen[(x,y)]] = dic_histograma.get(self.imagen[(x,y)], 0) + 1
        return dic_histograma

    def colores_mas_frecuentes(self):
        lista_colores = self.histograma().items()
        return sorted(lista_colores, key=lambda tupla: tupla[1], reverse=True)

    def promedio(self):
        cantidad = len(self.imagen)
        total_color_r = 0
        total_color_g = 0
        total_color_b = 0
        for x,y in self.imagen:
            total_color_r += self.imagen[(x,y)][0]
            total_color_g += self.imagen[(x,y)][1]
            total_color_b += self.imagen[(x,y)][2]
        return int(total_color_r / cantidad), int(total_color_g / cantidad), int(total_color_b / cantidad)

    def balde_de_pintura(self, x_ini, y_ini, color):
        return self._balde_de_pintura(x_ini, y_ini, color)

    def _balde_de_pintura(self, x_inicial, y_inicial, color):
        if self.alto > y_inicial >= 0 and self.ancho > x_inicial >= 0:
            if self.get(x_inicial,y_inicial) != color:
                self.set(x_inicial,y_inicial,color)
                self._balde_de_pintura(x_inicial+1, y_inicial, color)
                self._balde_de_pintura(x_inicial-1, y_inicial, color)
                self._balde_de_pintura(x_inicial, y_inicial+1, color)
                self._balde_de_pintura(x_inicial, y_inicial-1, color)

def remove_spaces(string): 
    return string.replace(" ", "")

def leer_ppm(nombre_archivo):
    with open(nombre_archivo) as archivo:
        lector_csv = csv.reader(archivo, delimiter=',')
        matriz = []
        for linea in lector_csv:
            matriz.append("".join(linea).strip().split("   "))
        valor_max = matriz[2][0]
        ancho_alto = matriz[1]
        ancho = " ".join(ancho_alto).split(" ")[0]
        alto = " ".join(ancho_alto).split(" ")[1]
        nueva_matriz = matriz[3:]
        imag = Imagen(int(valor_max), int(ancho), int(alto))
        for x in range(int(ancho)):
            for y in range(int(alto)):
                r = (",".join(nueva_matriz[y][x].strip().split(",")))
                if r.count(" ") >= 4:
                    t = remove_spaces(nueva_matriz[y][x].strip())
                    colores1 = tuple(map(int, t))
                    imag.set(x, y, colores1)
                else:
                    colores2 = []
                    for elem in nueva_matriz[y][x].strip().split():
                        if elem != " ":
                            colores2.append(int(elem))
                    imag.set(x, y, (tuple(colores2)))
                    colores2 = []
        return imag