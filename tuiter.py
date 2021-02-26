class Tuiter:
    "Modela el funcionamiento de una plataforma sospechosamente similar a Twitter"
    def __init__(self):
        self.autores = {}
        self.tuits = {}
        self.muro = {}
        self.cantidad_compartida_tuits = {}
        self.tuits_likeados = {}
        self.hilo = {}

    def crear_autor(self, nombre_autor):
        id_autor = len(self.autores) + 1
        if id_autor not in self.autores: 
            self.autores[id_autor] = {'nombre': nombre_autor, 'muro': {'propios': [], 'compartidos': [], 'totales': []}, 'likeados': {}}
        return id_autor

    def publicar(self, id_autor, mensaje):
        id_tuit = len(self.tuits) + 1
        self.tuits[id_tuit] = {'id_autor': id_autor, 'mensaje': mensaje}
        self.autores[id_autor]['muro']['propios'].append(mensaje)
        return id_tuit

    def compartir(self, id_tuit, id_autor):
        if self.tuits[id_tuit]['id_autor'] != id_autor:
            self.publicar(id_autor, self.tuits[id_tuit]['mensaje'])
            self.cantidad_compartida_tuits[id_tuit] = self.cantidad_compartida_tuits.get(id_tuit, 0) + 1
            return True
        return False

    def tuit_id_autor(self, id_tuit):
        return self.tuits[id_tuit]['id_autor']

    def tuit_mensaje(self, id_tuit):
        return self.tuits[id_tuit]['mensaje']

    def muro_cantidad(self, id_autor):
        contador = 0
        for id_tuit in self.tuits:
            if self.tuits[id_tuit]['id_autor'] == id_autor:
                contador += 1
        return contador 

    def muro_id_tuit(self, id_autor, p):
        indice = 0
        mensaje = ''
        for m in self.autores[id_autor]['muro']['propios']:
            if indice == p:
                mensaje += m
            indice += 1
        for id_tuit in self.tuits:
            if mensaje == self.tuits[id_tuit]['mensaje']:
                return id_tuit

    def muro_escribir_csv(self,id_autor, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write("autor|mensaje\n")
            for id_tuit in self.tuits:
                for mensaje in self.autores[id_autor]['muro']['propios']: 
                    if self.tuits[id_tuit]['mensaje'] == mensaje:
                        autor_original = self.tuit_id_autor(id_tuit)
                        archivo.write(f"{self.autores[autor_original]['nombre']}|{mensaje}\n")
                    else:
                        archivo.write(f"{self.autores[id_autor]['nombre']}|{mensaje}\n")
                break

    def tuits_mas_compartidos(self):
        nuevo_dic = {id_tuit: cantidad for id_tuit, cantidad in sorted(self.cantidad_compartida_tuits.items(), key=lambda item: item[1])}
        return nuevo_dic.items()

    def tuit_dar_like(self, id_tuit, id_autor):
        if self.tuits[id_tuit]['id_autor'] == id_autor:
            return False
        if id_tuit not in self.autores[id_autor]['likeados']:
            self.autores[id_autor]['likeados'][id_tuit] = 1
        else:
            self.autores[id_autor]['likeados'][id_tuit] += 1
        if self.autores[id_autor]['likeados'][id_tuit] >= 2:
            return False
        return True

    def tuit_fue_likeado_por(self, id_tuit, id_autor):
        if not id_tuit in self.autores[id_autor]['likeados']:
            return False
        if self.autores[id_autor]['likeados'][id_tuit] >= 1:
            return True
        return False

    def responder(self, id_tuit, id_autor, mensaje):
        self.hilo[id_tuit] = self.hilo.get(id_tuit, [])
        respuesta_id = self.publicar(id_autor, mensaje)
        self.hilo[id_tuit].append(respuesta_id)
        return respuesta_id

    def tuit_respuestas(self, id_tuit):
        if len(self.hilo) == 0:
            return []
        for k in self.hilo:
            return self.hilo[id_tuit]

    def tuit_en_respuesta_de(self, id_tuit):
        for k in self.hilo:
            if id_tuit in self.hilo[k]:
                return k
    
    def tuit_cantidad_hilo(self, id_tuit, acumulador = 1, indice = 0):
        if id_tuit not in self.hilo:
            self.hilo[id_tuit] = self.hilo.get(id_tuit, [])
        if len(self.hilo[id_tuit]) == 0 or indice >= len(self.hilo):
            return acumulador
        for k in self.hilo:
            indice += 1
            acumulador += len(self.hilo[k])
        return self.tuit_cantidad_hilo(id_tuit, acumulador, indice)
