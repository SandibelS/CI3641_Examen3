import math

class Descripcion():

    def __init__(self, tipo : str, tam : int, alineacion : int, cant_bytes_desperdiciados):
        self.tipo = tipo
        self.tam = tam
        self.alineacion = alineacion
        self.cant_bytes_desperdiciados = cant_bytes_desperdiciados


class Atomico():

    def __init__(self, nombre : str, representacion : int, alineacion : int):
        self.nombre = nombre
        self.representacion = representacion
        self.alineacion = alineacion
    
    def describir_sin_empaquetacion(self):

        desperdicio = 4 - self.representacion % 4
        if desperdicio == 4:
            desperdicio = 0

        return Descripcion("sin_empaquetacion", self.representacion, self.alineacion, desperdicio)

    def describir_con_empaquetacion(self):

        desperdicio = 4 - self.representacion % 4
        if desperdicio == 4:
            desperdicio = 0

        return Descripcion("con_empaquetacion", self.representacion, self.alineacion, desperdicio)
    
    def describir_con_reorganizacion(self):
        
        desperdicio = 4 - self.representacion % 4
        if desperdicio == 4:
            desperdicio = 0

        return Descripcion("con_reorganizacion", self.representacion, self.alineacion, desperdicio)


class Struct():

    def __init__(self, nombre : str, tipos_campos : list[any]):
        self.nombre = nombre
        self.tipos_campos = tipos_campos
    
    def describir_sin_empaquetacion(self):

        representacion = 0
        desperdicio = 0
        alineacion = self.tipos_campos[0].alineacion
        dir_act = 0

        for tipo in self.tipos_campos:

            descripcion = tipo.describir_sin_empaquetacion()

            c = dir_act % tipo.alineacion
            while c != 0:
                dir_act += c
                desperdicio += c

                c = dir_act % tipo.alineacion
                
            dir_act += descripcion.tam
            
            if isinstance(tipo, Atomico) == False:
                desperdicio += descripcion.cant_bytes_desperdiciados

            representacion += descripcion.tam + desperdicio

        return Descripcion("sin_empaquetacion", representacion, alineacion, desperdicio)

    def describir_con_empaquetacion(self):

        representacion = 0
        alineacion = self.tipos_campos[0].alineacion

        for tipo in self.tipos_campos:

            descripcion = tipo.describir_con_empaquetacion()
            representacion += descripcion.tam
        
        return Descripcion("con_empaquetacion", representacion, alineacion, 0)
    
    def describir_con_reorganizacion(self):
        #
        #
        #
        representacion = 0
        alineacion = 0
        desperdicio = 0

        return Descripcion("con_reorganizacion", representacion, alineacion, desperdicio)

class Union():

    def __init__(self, nombre : str, tipos_campos : list[any]):
        self.nombre = nombre
        self.tipos_campos = tipos_campos

    def describir_sin_empaquetacion(self):

        representacion = 0 # LA MAXIMA REPRESENTACION

        desperdicio = 0 # DE LA MAX REPRESENTACION

        alineacion = 1 # MINIMO COMUN MULTIPLO DE TODAS LAS ALINEACIONES


        for tipo in self.tipos_campos:

            descripcion = tipo.describir_sin_empaquetacion()

            # Queremos como representacion, la del tipo que tenga el 
            # tam maximo     
            # Desperdicion del maximo
            if descripcion.tam > representacion:
                representacion = descripcion.tam
                desperdicio = descripcion.cant_bytes_desperdiciados

            # Queremos el mcm de todas las alineaciones
            alineacion = math.lcm(alineacion, tipo.alineacion)

        return Descripcion("sin_empaquetacion", representacion + desperdicio, alineacion, desperdicio)

    def describir_con_empaquetacion(self):

        representacion = 0 # LA MAXIMA REPRESENTACION

        desperdicio = 0 # DE LA MAX REPRESENTACION

        alineacion = 1 # MINIMO COMUN MULTIPLO DE TODAS LAS ALINEACIONES


        for tipo in self.tipos_campos:

            descripcion = tipo.describir_sin_empaquetacion()

            # Queremos como representacion, la del tipo que tenga el 
            # tam maximo     
            # Desperdicion del maximo
            if descripcion.tam > representacion:
                representacion = descripcion.tam
                desperdicio = descripcion.cant_bytes_desperdiciados

            # Queremos el mcm de todas las alineaciones
            alineacion = math.lcm(alineacion, tipo.alineacion)

        return Descripcion("con_empaquetacion", representacion + desperdicio, alineacion, desperdicio)
    
    def describir_con_reorganizacion(self):

        representacion = 0 # LA MAXIMA REPRESENTACION

        desperdicio = 0 # DE LA MAX REPRESENTACION

        alineacion = 1 # MINIMO COMUN MULTIPLO DE TODAS LAS ALINEACIONES


        for tipo in self.tipos_campos:

            descripcion = tipo.describir_sin_empaquetacion()

            # Queremos como representacion, la del tipo que tenga el 
            # tam maximo     
            # Desperdicion del maximo
            if descripcion.tam > representacion:
                representacion = descripcion.tam
                desperdicio = descripcion.cant_bytes_desperdiciados

            # Queremos el mcm de todas las alineaciones
            alineacion = math.lcm(alineacion, tipo.alineacion)

        return Descripcion("con_reorganizacion", representacion + desperdicio, alineacion, desperdicio)

class Simulador():

    def __init__(self):
        self.tipos_definidos = {}
    
    def definir_atomico(self, nombre, representacion, alineacion):

        if nombre in self.tipos_definidos:
            raise ValueError("Ya existe un tipo con ese nombre") 
        
        nuevo_atomico = Atomico(nombre, representacion, alineacion)
        self.tipos_definidos[nombre] = nuevo_atomico
    
    def definir_struct(self, nombre, lista_nombres_tipo):

        if nombre in self.tipos_definidos:
            raise ValueError("Ya existe un tipo con ese nombre") 
        
        lista_tipos = []

        for nombre_tipo in lista_nombres_tipo:
            if (nombre_tipo in self.tipos_definidos) == False:
                raise ValueError("No existe un tipo con ese nombre")
            lista_tipos += [self.tipos_definidos[nombre_tipo]]
        
        nuevo_struct = Struct(nombre, lista_tipos)
        self.tipos_definidos[nombre] = nuevo_struct
    
    def definir_union(self, nombre, lista_nombres_tipo):

        if nombre in self.tipos_definidos:
            raise ValueError("Ya existe un tipo con ese nombre")
        
        lista_tipos = []

        for nombre_tipo in lista_nombres_tipo:
            if (nombre_tipo in self.tipos_definidos) == False:
                raise ValueError("No existe un tipo con ese nombre")
            lista_tipos += [self.tipos_definidos[nombre_tipo]]
        
        nueva_union = Union(nombre, lista_tipos)
        self.tipos_definidos[nombre] = nueva_union

    def describir_sin_empaquetacion(self, nombre):

        if (nombre in self.tipos_definidos) == False:
            raise ValueError("No existe un tipo con ese nombre")
        
        return self.tipos_definidos[nombre].describir_sin_empaquetacion()
    
    def describir_con_empaquetacion(self, nombre):

        if (nombre in self.tipos_definidos) == False:
            raise ValueError("No existe un tipo con ese nombre")
        
        return self.tipos_definidos[nombre].describir_con_empaquetacion()

    def describir_con_reorganizacion(self, nombre):

        if (nombre in self.tipos_definidos) == False:
            raise ValueError("No existe un tipo con ese nombre")
        
        return self.tipos_definidos[nombre].describir_con_reorganizacion()