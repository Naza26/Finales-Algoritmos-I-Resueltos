class Editor:
    "Representa el estado de un editor de texto."

    def __init__(self, contenido_archivo):

        self.x = 1
        self.y = 1

        if contenido_archivo == '':
            contenido_archivo += '\n'
        if contenido_archivo[-1] != '\n':
            contenido_archivo += '\n'
            self.contenido_archivo = contenido_archivo
            return

        self.contenido_archivo = contenido_archivo


    def cantidad_lineas(self):
        return self.contenido_archivo.count('\n')
    
    def __str__(self):
        if self.contenido_archivo[-1] != '\n':
            lista_aux = self.contenido_archivo.split('\n')
            nueva_lista = []
            for linea in lista_aux:
                nueva_lista.append((linea + '\n'))
                aux = ''.join(nueva_lista)
            return aux

        return self.contenido_archivo

    def escribir_archivo(self, archivo_destino):
        with open(archivo_destino, 'w') as archivo:
            for linea in self.contenido_archivo.split('\n')[:-1]:
                archivo.write(linea + '\n')

    def cursor_pos(self):
        lista = self.contenido_archivo.split('\n')
        indice_barra_n = lista.index("")

        if self.cursor_caracter() == '\n' and self.x == len(lista) and self.y > len(lista[self.x-1]) + 1:
            return self.x, self.y-1

        elif self.x > len(lista) and self.y == len(lista[self.x]):
            return self.x-1, self.y

        elif indice_barra_n <= len(lista) and self.cursor_caracter() == "":
            self.x = indice_barra_n
            self.y = len(lista[self.x - 1])
            return self.x, self.y
    
        return self.x, self.y
    
    def cursor_caracter(self):
        lista = self.contenido_archivo.split('\n')
        try:
            if self.x == 0:
                return lista[self.x][self.y - 1]
            if self.x == len(lista) - 1 and self.y == len(lista[self.x]):
                return '\n'
            return lista[self.x - 1][self.y - 1]
        except IndexError:
            return '\n'

    def mover_derecha(self):
        lista = self.contenido_archivo.split('\n')

        if self.cursor_caracter() == '\n' and (self.x == len(lista[:-1]) - 1):
            self.x += 1
            self.y = 1
            return
        
        if self.cursor_caracter() == '\n' and (self.x == len(lista) - 1):
            return 

        if self.x == len(lista) - 1 and self.y == len(lista[self.x]):
            self.x += 1
            self.y = 1 
            return

        if self.x == len(lista[:-1]) and len(lista[:-1]) == 1:
            self.y = len(lista[self.x - 1]) + 1
            return self.x, self.y

        self.y += 1
        if self.y == len(self.contenido_archivo[self.x]): 
            self.y = 0
            self.x += 1


    def mover_izquierda(self):
        lista = self.contenido_archivo.split('\n')
        if self.x - 1 == 0 and self.y - 1 == 0:
            self.x = 1
            self.y = 1
            return
        if self.x == len(lista[:-1]) and self.y -1 == 0:
            self.x = self.x - 1
            self.y = len(lista[self.x])
            return self.x, self.y

        self.y -= 1
        if self.y == len(self.contenido_archivo[self.x]): 
            self.y = 0
            self.x += 1

    def mover_arriba(self):
        lista = self.contenido_archivo.split('\n')
        if self.x == len(lista[:-1]) and self.cursor_caracter() == '\n':
            self.x = self.x - 1
            self.y = len(lista[self.x - 1]) + 1
            return self.x, self.y
        if self.x - 1 <= 0:
            return 
        self.x -= 1

    def mover_abajo(self):
        if self.x >= len(self.contenido_archivo.split('\n')) - 1:
            return
        self.x += 1

    def mover_inicio_linea(self):
        x, y = self.cursor_pos()
        if x > 1 and y == 1:
            self.x = x
        else:
            self.y = 1

    def mover_fin_linea(self):
        lista = self.contenido_archivo.split('\n')
        self.y = len(lista[self.x - 1]) + 1
        return self.x, self.y

    def mover_a(self, x, y):
        lista = self.contenido_archivo.split('\n')
        if x == 0:
            self.x = x
            self.y = y
            return self.x, self.y
        if x <= len(lista) and y - 1 > len(lista[self.x]):
            self.x = x
            self.y = len(lista[self.x])
            return self.x, self.y
        if x > len(lista[y - 2]) and y <= len(lista):
            self.x = y
            self.y = y
            return self.x, self.y

        self.x = x
        self.y = y
        return self.x, self.y

    def insertar(self, texto):
        lista_aux = texto.split()
        lista_aux.append('\n')
        cadena_aux = "".join(lista_aux)
        lista = self.contenido_archivo.split('\n')
        if len(self.contenido_archivo) == 1 and self.contenido_archivo[0] == '\n' and len(texto) == 1:
            self.contenido_archivo += cadena_aux
            return
        if len(self.contenido_archivo) == 1 and self.contenido_archivo[0] == '\n':
            self.contenido_archivo = cadena_aux
            self.mover_derecha()
            return
        else:
            if len(lista_aux[:-1]) >= 2 and '\n' not in lista_aux[:-1]:
                indice_barra_n = texto.index('\n')
                primera_insercion = list(lista[self.x - 1])
                primera_insercion.insert(indice_barra_n, texto[:indice_barra_n])
                primera_insercion.insert(indice_barra_n + 1, '\n')
                primera_insercion.insert(len(primera_insercion) - 2, texto[indice_barra_n + 1:])
                total = lista[: indice_barra_n - 1] + ['\n']+ primera_insercion + ['\n'] + lista[indice_barra_n:] + ['\n']
                self.contenido_archivo = "".join(total)
                self.x = indice_barra_n + 1
            else:
                valores_separados = list(lista[self.x])
                if valores_separados == []:
                    cant = self.cantidad_lineas()
                    for _ in range(cant):
                        valores_separados.append('\n')
                    valores_separados.insert(self.y, texto)
                    total = valores_separados
                else:
                    valores_separados.insert(self.y - 1, texto)
                    total = valores_separados + [] + ['\n']
                cadena_final = "".join(total)
                self.contenido_archivo = cadena_final
                indice_texto = cadena_final.index(texto)
                if texto == " ":
                    self.x += 1
                    self.y = indice_texto + 2
                elif self.cursor_caracter() == '\n':
                    self.x = indice_texto + 2
                else:
                    self.mover_derecha()

    def palabras_mas_frecuentes(self):
        palabras = {}
        lista_aux = self.contenido_archivo.strip().split()
        p_mas_frecuentes = {}
        for palabra in lista_aux:
            palabras[palabra] = palabras.get(palabra, 0) + 1
        palabras_ordenadas = sorted(palabras, key=palabras.get)

        for palabra in palabras_ordenadas:
            p_mas_frecuentes[palabra] = palabras[palabra]

        nuevo_dic = {p: cantidad for p, cantidad in sorted(p_mas_frecuentes.items(), key=lambda x: x[1], reverse=True)}
        return list(nuevo_dic.items())

    def buscar(self, cadena):
        contador = 1
        lista_tuplas = []
        texto_total = self.contenido_archivo.split('\n')
        largo_total = len(texto_total)
        for linea_pos in range(len(texto_total)):
            if contador <= largo_total:
                if cadena in texto_total[linea_pos]:
                    a_cadena = "".join(texto_total[linea_pos])
                    lista_tuplas.append((contador, a_cadena.index(cadena) + 1))
                    nueva = a_cadena[:a_cadena.index(cadena)] + a_cadena[a_cadena.index(cadena) + 1:]
                    if cadena in nueva:
                        lista_tuplas.append((contador, nueva.index(cadena) + 2))
            contador += 1
        return lista_tuplas

def leer_archivo(ruta_archivo):
    with open(ruta_archivo) as archivo_entrada:
        data = archivo_entrada.readlines()
        lista_aux = []
        for linea in data:
            lista_aux.append(linea)
        return Editor(''.join(lista_aux))