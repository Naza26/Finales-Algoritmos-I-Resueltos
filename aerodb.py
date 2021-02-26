import csv
import math

def distancia_coordenadas(x1, y1, x2, y2):
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

class AeroDB:
    "AeroDB es una base de datos de aeropuertos y rutas"
    def __init__(self):
        self.aeropuertos = {}
        self.rutas = []

    def aeropuerto_agregar(self, designacion, nombre, ciudad, pais, latitud, longitud):
        self.aeropuertos[designacion] = {'nombre': nombre, 'ciudad': ciudad, 'pais': pais, 'latitud': latitud, 'longitud': longitud}

    def cantidad_aeropuertos(self):
        return len(self.aeropuertos)

    def aeropuerto_get_nombre(self, designacion):
        return self.aeropuertos[designacion]['nombre']
    
    def aeropuerto_get_ciudad(self, designacion):
        return self.aeropuertos[designacion]['ciudad']

    def aeropuerto_get_pais(self, designacion):
        return self.aeropuertos[designacion]['pais'] 
    
    def aeropuerto_get_coords(self, designacion):
        return self.aeropuertos[designacion]['latitud'], self.aeropuertos[designacion]['longitud']

    def ruta_agregar(self, codigo_vuelo, d_origen, d_destino):
        self.rutas.append((codigo_vuelo, d_origen, d_destino))
    
    def cantidad_rutas(self):
        return len(self.rutas)
        
    def rutas_desde_ciudad(self, ciudad):
        lista_rutas = []
        codigos = []
        for designacion in self.aeropuertos:
            if self.aeropuertos[designacion]['ciudad'] == ciudad:
                codigos.append(designacion)
        for codigo in codigos:
            for cod_vuelo, ciudad1, ciudad2 in self.rutas:
                if codigo.lower() == ciudad1.lower():
                    lista_rutas.append((cod_vuelo, ciudad1, ciudad2))
        return lista_rutas

    def rutas_hacia_ciudad(self, ciudad):
        lista_rutas = []
        codigos = []
        for designacion in self.aeropuertos:
            if self.aeropuertos[designacion]['ciudad'] == ciudad:
                codigos.append(designacion)
        for codigo in codigos:
            for cod_vuelo, ciudad1, ciudad2 in self.rutas:
                if codigo.lower() == ciudad2.lower():
                    lista_rutas.append((cod_vuelo, ciudad1, ciudad2))
        return lista_rutas

    def aeropuerto_con_mas_rutas(self):
        cantidad_r = {}
        for designacion in self.aeropuertos:
            for _ , ciudad1, ciudad2 in self.rutas:
                if designacion.lower() == ciudad1.lower() or designacion.lower() == ciudad2.lower():
                    cantidad_r[designacion] = cantidad_r.get(designacion, 0) + 1
            
        mas_rutas_d = max(cantidad_r, key=cantidad_r.get)

        return mas_rutas_d, cantidad_r[mas_rutas_d]

    def aeropuertos_ordenados_por_distancia(self, latitud, longitud):
        dic_aux = {}
        for designacion in self.aeropuertos:
            dic_aux[designacion] = dic_aux.get(designacion, distancia_coordenadas(latitud, longitud, self.aeropuertos[designacion]['latitud'], self.aeropuertos[designacion]['longitud']))
        distancias_ordenadas = sorted(dic_aux, key=dic_aux.get)
        return distancias_ordenadas

    def armar_itinerario(self, ciudad_origen, ciudad_destino):
        return self._armar_itinerario(ciudad_origen, ciudad_destino, R = [], V = {})

    def _armar_itinerario(self, ciudad_origen, ciudad_destino, R, V):

        for codigo, origen, destino in self.rutas:
            if ciudad_origen == origen and ciudad_destino == destino:
                return [(codigo, origen, destino)]
            if len(R) >= 1:
                if ciudad_origen == R[0][0][1] and R[-1][-1][-1] == ciudad_destino:
                    R.pop(0)
                    return R[0] + R[1]
            if ciudad_origen == origen and origen == destino:
                R.append((codigo, origen, destino))
                V[destino] = V.get(destino, True)
            if destino not in V:
                V[destino] = V.get(destino, True)
                r = self._armar_itinerario(origen, destino, R, V)
                R = R + [r]
        return None

def cargar(archivo_aerop, archivo_rutas):
    with open(archivo_aerop) as a_aeropuerto:
        with open(archivo_rutas) as a_rutas:
            lector_aerop = csv.reader(a_aeropuerto, delimiter='|')
            lector_rutas = csv.reader(a_rutas, delimiter='|')
            a = AeroDB()
            for fila in lector_aerop:
                a.aeropuerto_agregar(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
            for fila in lector_rutas:
                a.ruta_agregar(fila[0], fila[1], fila[2])
            return a