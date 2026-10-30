### Proyecto de código abierto bajo estándar y licencia GNU GPL 3.0
### Gestión de Datos - Liga de Espada Larga Praelium Australis 2026
### GDLPA

### Open source project under standarized rules and GNU GPL 3.0 license
### Data Management - Praelium Australis Longsword League 2026 -> Name should be use strictly in spanish, as intended originally
### GDLPA

### Code development is explained in spanish, you can translate it. Is that too much? i don´t think so, look for a serious problem
### If you have questions or advices, you can contact me to the email alexis.guerrero@ug.uchile.cl or in github (username: mapacheag, linked to the same email)
### I can communicate fluently in spanish, english and italian

##################################################################################################################################

### versión prototipo 0.1.0
### Estándar de SemVer; Ver X.Y.Z = Mayor.Menor.Parche

##################################################################################################################################

### Estructura de archivos

### Main folder  -> aquí reside y se de inicio al repositorio de github

### --> src     (aquí se encuentra el código principal)
###     --> DTPA.py (código de referencia de otro diseñador de torneos usado en el torneo de novatos [lo borraré cuando lo deje de usar])
###     --> GDLPA.py [CÓDIGO PRINCIPAL]
### --> assets  (aquí se encuentra el material visual e iconográfico (png, jpg, ico, svg y demás))
###     --> icons (todo archivo en formato .ico)
###         --> [Ejemplo] logo_pa.ico
###     --> images (el resto de formatos visuales)
###         --> [Ejemplo] imagen.png
### --> config  (aquí se encuentran los documentos de configuración del código, tanto de entrada como de salida)
###     --> [Ejemplo] lista_de_inscritos.csv [IN]
###     --> [Ejemplo] configuracion_final_2026.dtpa [OUT]
### --> resources  (aquí se encuentran los materiales adicionales que permiten definir el sistema, formato y detalles del código; ej: el reglamento del torneo)
###     --> reglamento_2024.pdf  (referencia anterior)
###     --> reglamento_2026.pdf  (reglamento actualizado)
### --> README.md   (aquí se encuentra un resumen general de todos los detalles importantes a considerar previamente (una copia de esto aproximadamente))
### --> .vscode  [NO INCLUIDO EN GITHUB] (aquí se encuentran los documentos de configuración local que adopta vscode en cada dispositivo) -> se debe agregar al .gitignore si no lo está ya
### --> index.html  (aquí se encuentra el diseño de la página web que adoptará github pages y que se actualizará tras cada cambio)

###################################################################################################################################################################################################


### Paquetes necesarios     (uso específico descrito en el README) [cuando lo actualice]

import pandas as pd
import random as rd
import datetime

#####################################


### Definición de clases y funciones principales

### Clase Esgrimista, envuelve todas su instancias particulares, como el nombre, sus puntajes, sanciones y demás

class Esgrimista:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.puntaje = []
        ## Los puntajes ingresados tendrán la forma P_i = [x,y,z,t]
        ## Donde P_i es el puntaje del iésimo duelo del esgrimista
        ## x es el puntaje final asignado
        ## y son los intercambios/puntos favorables
        ## z son los intercambios/puntos en contra
        ## t son los dobles ocurridos en el duelo
        self.sanciones = []
        ## Las sacniones ingresadas serán de la forma S_i = [x',y']
        ## Donde S_i es el registro de sanciones del iésimo duelo del esgrimista
        ## x' corresponde a las sanciones leves que hayan sido registradas
        ## y' corresponde a las sanciones graves que hayan sido registradas

    @property
    def puntaje_total(self) -> int:
        return sum(duelo[0] for duelo in self.puntaje)

    @property
    def dobles_total(self) -> int:
        return sum(duelo[3] for duelo in self.puntaje)

    @property
    def intercambios_favorables(self) -> int:
        return sum(duelo[1] for duelo in self.puntaje)

    @property
    def intercambios_desfavorables(self) -> int:
        return sum(duelo[2] for duelo in self.puntaje)

    @property
    def intercambios_diferencia(self) -> int:
        return self.intercambios_favorables - self.intercambios_desfavorables

    @property
    def descalificacion_graves(self) -> bool:
        return sum(sancion[1] for sancion in self.sanciones) >= 2

    @property
    def descalificacion_leves(self) -> bool:
        derrotas_por_leves = sum(1 for sancion in self.sanciones if sancion[0] == 2)
        return derrotas_por_leves >=2

    @property
    def descalificacion(self) -> bool:
        return self.descalificacion_graves or self.descalificacion_leves

    def __repr__(self):
        return f"{self.nombre}"


### Clase Duelo (todas las instancias que se relacionen o sean dependientes de los duelos)

class Duelo:
    def __init__(self, esgrimista_a: Esgrimista, esgrimista_b: Esgrimista):
        self.esgrimista_a = esgrimista_a
        self.esgrimista_b = esgrimista_b
        self.resultado = []
        ## El resultado ingresado será de la forma R_i = [\alpha,\beta,\gamma]
        ## Donde R_i es el resultado del iésimo duelo del registro
        ## \alpha es el puntaje de duelo del esgrimista_a
        ## \beta es el puntaje de duelo del esgrimista_b
        ## \gamma es la cantidad de dobles registrados en el duelo

    ## Función para asignar puntajes de un duelo finalizado
    def asignar_puntaje(self, intercambios_a : int, intercambios_b: int, dobles: int) -> None:
        puntaje_ingresado = [intercambios_a, intercambios_b, dobles]
        self.resultado.append(puntaje_ingresado)
        ## Victoria A
        if intercambios_a > intercambios_b:
            puntos_a = 3
            puntos_b = 0
        ## Victoria B
        elif intercambios_b > intercambios_a:
            puntos_a = 0
            puntos_b = 3
        ## Empate
        else:
            puntos_a = 1
            puntos_b = 1
        ## Asignación del puntaje en A y B
        puntaje_out_a = [
            puntos_a - dobles // 3,
            intercambios_a,
            intercambios_b,
            dobles
        ]
        puntaje_out_b = [
            puntos_b - dobles // 3,
            intercambios_b,
            intercambios_a,
            dobles
        ]
        self.esgrimista_a.puntaje.append(puntaje_out_a)
        self.esgrimista_b.puntaje.append(puntaje_out_b)

    ## Función para asignar sanciones de un duelo finalizado
    def asignar_sanciones(self, sancion_leve_a: int = 0, sancion_grave_a: int = 0, sancion_leve_b: int = 0, sancion_grave_b: int = 0):
        sanciones_ingresadas_a = [sancion_leve_a, sancion_grave_a]
        sanciones_ingresadas_b = [sancion_leve_b, sancion_grave_b]
        self.esgrimista_a.sanciones.append(sanciones_ingresadas_a)
        self.esgrimista_b.sanciones.append(sanciones_ingresadas_b)

    ## Función compuesta de ingreso de datos de un duelo (esta es la que se utilzará en el día a día)
    def asignar_resultado(self, input_asignar_puntaje: list, input_asignar_sanciones: list = None):
        if input_asignar_sanciones is None:
            input_asignar_sanciones = []
        self.asignar_puntaje(*input_asignar_puntaje)
        self.asignar_sanciones(*input_asignar_sanciones)

    def __repr__(self):
        return f"{self.esgrimista_a.nombre} vs {self.esgrimista_b.nombre}"


### Clase Configuración de Liga [ConfiguracionLiga] (contiene todos los elementos que realizan la gestión del torneo, utilizando elementos de Esgrimista y Duelo)

class ConfiguracionLiga:
    def __init__(self):
        self.participantes = []
        self.cantidad_maxima_duelos = None
        self.duelos = []
        self.fechas_liga = {}
        self.fixture_de_liga = {}
        self.duelos_calendarizados = 0

    ## Función para crear esgrimistas a partir de un dataframe o una lista
    def obtener_participantes(self, participantes_lista: list = None, participantes_df = None) -> None:
        if participantes_lista is None and participantes_df is None:
            raise ValueError(f"No hay Liga más fácil de organizar que aquella que no tiene participantes...\nPorque no los tiene... cierto?\nDebes ingresar los participantes mediante una lista o un DataFrame")
        if participantes_df is None:
            for esgrimista in participantes_lista:
                self.participantes.append(Esgrimista(esgrimista))
        else:
            for esgrimista in participantes_df['Nombres']:
                self.participantes.append(Esgrimista(esgrimista))

    @property
    def cantidad_total_participantes(self) -> int:
        return len(self.participantes)

    @property
    def cantidad_total_duelos(self) -> int:
        return (self.cantidad_total_participantes * self.cantidad_maxima_duelos) / 2

    ## Función para crear todos los duelos de la liga
    def generar_duelos(self, duelos_max: int) -> None:
        self.cantidad_maxima_duelos = duelos_max
        N_aux = self.cantidad_total_participantes
        alcance_de_nodo = duelos_max // 2
        rd.shuffle(self.participantes)

        for i in range(N_aux):
            esgrimista_central = self.participantes[i]
            for k in range(1, alcance_de_nodo + 1):
                index_oponente = (i + k) % N_aux
                oponente = self.participantes[index_oponente]
                duelo = Duelo(esgrimista_central, oponente)
                self.duelos.append(duelo)
        rd.shuffle(self.duelos)

    ## Función para crear y detallar el formato de las fechas de competición de la liga
    def crear_fechas(self, fechas_ingresadas: list = None) -> None:
        if fechas_ingresadas is None:
            raise ValueError(f"Estamos todos regidos por la causalidad. Cómo piensas llevar a cabo un duelo sin un intervalo temporal en el que pueda existir?")
        for f, fecha in enumerate(fechas_ingresadas, start=1):
            self.fechas_liga[f"Fecha {f}"] = fecha

    ## Fucnión para asignar un conjunto de duelos a una fecha de la liga
    def calendarizar_duelo(self, asignar_fecha: str, cantidad_de_duelos: int = None) -> None:
        if cantidad_de_duelos is None:
            raise ValueError(f"Cuántos duelos quieres asignar a esta fecha? 0? infinitos?")
        if asignar_fecha not in self.fechas_liga:
            raise ValueError(f"La Fecha ingresada no existe... todavía, quizás deberías revisar de nuevo")
        self.fixture_de_liga[asignar_fecha] = self.duelos[self.duelos_calendarizados : self.duelos_calendarizados + cantidad_de_duelos]
        self.duelos_calendarizados = cantidad_de_duelos + self.duelos_calendarizados

    @property
    def fixture_de_fechas(self) -> pd.DataFrame:
        df_fixture_fechas_input_data = []
        for fecha, lista_duelos in self.fixture_de_liga.items():
            for duelo in lista_duelos:
                df_fixture_fechas_input_data.append({
                    'Fecha' : fecha,
                    'Duelo' : duelo
                })
        return pd.DataFrame(df_fixture_fechas_input_data)

    ### Construcción de la tabla de posiciones (dinámica) [No, no es dinámica de excel, no sé qué son las tablas dinámicas de excel lamentablemente]

    ## El criterio de orden será:
    ## En primer lugar según el puntaje total acumulado por el esgrimista   
    ## En segundo lugar, por la diferencia de intercambios acumulada por el esgrimista
    ## En tercer lugar, por la cantidad de intercambios a favor acumulados por el esgrimista
    ## En cuarto lugar, por la cantidad menor de dobles acumulada por el esgrimista
    ## En quinto lugar, que dios nos salve

    ### Esquema de datos (guía personal para no perderme), porque la tabla no me sale

    ## Posición --- Nombre --- Puntaje --- Diferencia --- A favor --- En contra --- Dobles

    ## Las posiciones son nominales de cada fila, ya que la primera fila con las etiquetas de cada columna es 0, así que queda excelente
    ## Los nombres, ptjes, intercambios y dobles los puedo traer desde cada clase
    ## El lío es, el ordenamiento

    def tabla_de_posiciones(self) -> pd.DataFrame:
        input_data_tabla_de_mierda = {}

        for esgrimista in ConfiguracionLiga.participantes:
            


        tabla_de_mierda = pd.DataFrame(input_data_tabla_de_mierda)