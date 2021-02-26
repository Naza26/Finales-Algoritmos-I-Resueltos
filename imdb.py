import csv
class IMDB:
    "IMDB es una base de datos de cine"
    def __init__(self):
        self.actores = {}
        self.films = {}

    def actor_agregar(self, nombre, año, mes, dia):
        id_actor = len(self.actores) + 1
        self.actores[id_actor] = {'nombre':nombre, 'fecha_nac':(año,mes,dia), 'films': {}}
        return id_actor

    def cantidad_actores(self):
        return len(self.actores)

    def actor_nombre(self, id_actor):
        return self.actores[id_actor]['nombre']

    def actor_nacimiento(self, id_actor):
        return self.actores[id_actor]['fecha_nac']

    def film_agregar(self, nombre, año, mes, dia, ids_actores):
        id_film = len(self.films)
        listado_act = set()
        for id_a in ids_actores:
            listado_act.add(id_a)
        self.films[id_film] = {'nombre_film':nombre, 'fecha_film': (año,mes,dia), 'listado_actores': listado_act, 'listado_califi':[]}
        for id_a in ids_actores:
            self.actores[id_a]['films'][id_film] = True
        return id_film

    def cantidad_films(self):
        return len(self.films)

    def film_nombre(self, id_film):
        return self.films[id_film]['nombre_film']

    def film_lanzamiento(self, id_film):
        return self.films[id_film]['fecha_film']

    def film_actores(self, id_film):
        return self.films[id_film]['listado_actores']
    def actor_films(self, id_actor):
        lista_ids = []
        for id_film in self.films:
            if id_actor in self.films[id_film]['listado_actores']:
                lista_ids.append(id_film)
        return lista_ids


    def escribir_csv(self):
        with open('actores.csv', 'w') as archivo_actores:
            escritor = csv.writer(archivo_actores)
            for id_actor in self.actores:
                año, mes, dia = self.actores[id_actor]['fecha_nac']
                escritor.writerows((f"{id_actor}, {self.actores[id_actor]['nombre']}, {año}, {mes}, {dia}"))

        with open('films.csv', 'w') as archivo_films:
            escritor = csv.writer(archivo_films)
            for id_film in self.films:
                año, mes, dia = self.films[id_film]['fecha_film']
                escritor.writerows(f"{self.films[id_film]['nombre_film']},{año},{mes},{dia}")

    def films_decadas(self):
        diccionario = {}
        for id_film in self.films:
            año, mes, dia = self.films[id_film]['fecha_film']
            resto = año % 10
            clave = (año - resto)
            if clave not in diccionario:
                diccionario[clave] = diccionario.get(clave, [])
                diccionario[clave].append(id_film)
            else:
                diccionario[clave].append(id_film)

        return diccionario

    
    def calificar(self, id_film, calificacion):
        self.films[id_film]['listado_califi'].append(calificacion)

    def film_promedio(self, id_film):
        if len(self.films[id_film]['listado_califi']) == 0:
            return 0
        else:
            return sum(self.films[id_film]['listado_califi']) / len(self.films[id_film]['listado_califi'])

    def films_top10(self):
        dic_aux = {}
        for id_film in self.films:
            dic_aux[id_film] = dic_aux.get(id_film, self.film_promedio(id_film))
        ordenado = sorted(dic_aux, key=dic_aux.get)
        mayor_a_menor = ordenado[::-1]
        return mayor_a_menor[:10]


    def distancia(self, A, B):
        actores_visitados = {}
        lista_de_tuplas = []

        actores_visitados[A] = True
        lista_de_tuplas.append((A,0))

        while len(lista_de_tuplas) > 0:
            (V,D) = lista_de_tuplas.pop(0)
            if V == B:
                return D
            for film in self.actores[V]['films']:
                for W in self.films[film]['listado_actores']:
                    if W not in actores_visitados:
                        actores_visitados[W] = True
                        lista_de_tuplas.append((W, D + 1))




