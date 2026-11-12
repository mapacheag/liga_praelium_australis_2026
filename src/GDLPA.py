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
import pickle

#####################################


### Definición de clases y funciones principales

### Clase Esgrimista, envuelve todas su instancias particulares, como el nombre, sus puntajes, sanciones y demás

class Esgrimista:
    def __init__(self, nombre: str, rango: str, asistencia: float):
        self.nombre = nombre
        self.rango = rango
        self.asistencia = asistencia
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
    def duelos_peleados(self) -> int:
        return len(self.puntaje)

    @property
    def puntaje_total(self) -> float:
        if self.duelos_peleados == 0:
            return 0.0
        return sum(duelo[0] for duelo in self.puntaje) / self.duelos_peleados

    @property
    def dobles_total(self) -> float:
        if self.duelos_peleados == 0:
            return 0.0
        return sum(duelo[3] for duelo in self.puntaje) / self.duelos_peleados

    @property
    def intercambios_favorables(self) -> float:
        if self.duelos_peleados == 0:
            return 0.0
        return sum(duelo[1] for duelo in self.puntaje) / self.duelos_peleados

    @property
    def intercambios_desfavorables(self) -> float:
        if self.duelos_peleados == 0:
            return 0.0
        return sum(duelo[2] for duelo in self.puntaje) / self.duelos_peleados

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

    ## Función para crear esgrimistas a partir de un dataframe o una lista (AHORA, es solamente mediante un DF)
    def obtener_participantes(self, participantes_df = None) -> None:
        if participantes_df is None:
            raise ValueError(f"No hay Liga más fácil de organizar que aquella que no tiene participantes...\nPorque no los tiene... cierto?\nDebes ingresar los participantes mediante un DataFrame")
        for _, fila in participantes_df.iterrows():
            nombre = fila['Nombres']
            rango = fila['Curso o Rango Marcial']
            asistencia = fila['Asistencia']
            self. participantes.append(Esgrimista(nombre, rango, asistencia))

    def actualizar_asistencia(self, participantes_df: pd.DataFrame = None) -> None:
        if participantes_df is None:
            raise ValueError(f"Se debe ingresar un DataFrame con los datos de asistencia actualizados")
        mapeo_asistencia = dict(zip(participantes_df['Nombres'], participantes_df['Asistencia']))
        for esgrimista in self.participantes:
            if esgrimista.nombre in mapeo_asistencia:
                esgrimista.asistencia = mapeo_asistencia[esgrimista.nombre]

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

    def calendarizar_con_cota(self, cupos_por_fecha: list[int], max_por_persona: int = 2) -> None:
        nombres_fechas = list(self.fechas_liga.keys())
        if len(cupos_por_fecha) != len(nombres_fechas):
            raise ValueError("La lista de cupos debe coincidir en largo con las fechas creadas.")
        if sum(cupos_por_fecha) != len(self.duelos):
            raise ValueError(f"La suma de cupos ({sum(cupos_por_fecha)}) no coincide con el total de duelos ({len(self.duelos)}).")
        cupos_dict = dict(zip(nombres_fechas, cupos_por_fecha))
        for _ in range(1000):
            duelos_barajados = self.duelos.copy()
            rd.shuffle(duelos_barajados)
            asignacion = {f: [] for f in nombres_fechas}
            conteo = {f: {e.nombre: 0 for e in self.participantes} for f in nombres_fechas}
            exito_global = True

            for duelo in duelos_barajados:
                a = duelo.esgrimista_a.nombre
                b = duelo.esgrimista_b.nombre

                fechas_validas = [
                    f for f in nombres_fechas
                    if len(asignacion[f]) < cupos_dict[f]
                    and conteo[f][a] < max_por_persona
                    and conteo[f][b] < max_por_persona
                ]
                if not fechas_validas:
                    exito_global = False
                    break
                fecha_elegida = rd.choice(fechas_validas)
                asignacion[fecha_elegida].append(duelo)
                conteo[fecha_elegida][a] += 1
                conteo[fecha_elegida][b] += 1

            if exito_global:
                self.fixture_de_liga = asignacion
                self.duelos_calendarizados = len(self.duelos)
                return
        raise RuntimeError("No se logró encontrar una distribución aleatoria que cumpla la cota tras 1000 intentos.")

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

    def reagendar_duelo(self, nombre_a: str, nombre_b: str, nueva_fecha: str) -> None:
        if nueva_fecha not in self.fechas_liga:
            raise ValueError(f"La fecha '{nueva_fecha}' no existe en el calendario.")
        duelo_encontrado = None
        fecha_original = None

        for fecha, lista_duelos in self.fixture_de_liga.items():
            for duelo in lista_duelos:
                nombres_duelo = (duelo.esgrimista_a.nombre, duelo.esgrimista_b.nombre)
                if nombre_a in nombres_duelo and nombre_b in nombres_duelo:
                    duelo_encontrado = duelo
                    fecha_original = fecha
                    break
            if duelo_encontrado:
                break
        if not duelo_encontrado:
            raise ValueError(f"No se encontró un duelo entre {nombre_a} y {nombre_b} en el fixture.")     
        if fecha_original == nueva_fecha:
            return
        
        self.fixture_de_liga[fecha_original].remove(duelo_encontrado)
        if nueva_fecha not in self.fixture_de_liga:
            self.fixture_de_liga[nueva_fecha] = []
        self.fixture_de_liga[nueva_fecha].append(duelo_encontrado)

    ######### Tabla de posiciones
    ## El criterio de orden será:
    ## En primer lugar según el puntaje total acumulado por el esgrimista   
    ## En segundo lugar, por la diferencia de intercambios acumulada por el esgrimista
    ## En tercer lugar, por la cantidad de intercambios a favor acumulados por el esgrimista
    ## En cuarto lugar, por la cantidad menor de dobles acumulada por el esgrimista
    ## En quinto lugar, que dios nos salve
    def constructor_de_tabla(self) -> pd.DataFrame:
        data_posiciones = []
        for esgrimista in self.participantes:
                    data_posiciones.append({
                        'Nombre' : esgrimista.nombre,
                        'Curso o Rango Marcial' : esgrimista.rango,
                        'Pts P' : esgrimista.puntaje_total,
                        'Dif P' : esgrimista.intercambios_diferencia,
                        'Asistencia' : esgrimista.asistencia,
                        'Dobles P' : esgrimista.dobles_total                
                    })
        df_posiciones = pd.DataFrame(data_posiciones)

        return df_posiciones

    def sort_en_tabla(self, df_posiciones: pd.DataFrame) -> pd.DataFrame:
        df_posiciones_ordenadas = df_posiciones.sort_values(
            by=['Pts P', 'Dif P', 'Asistencia', 'Dobles P'],
            ascending=[False, False, False, True]
        ).reset_index(drop=True)
        df_posiciones_ordenadas.index = df_posiciones_ordenadas.index + 1
        df_posiciones_ordenadas['Estado'] = ''
        candidatos_validos = df_posiciones_ordenadas[df_posiciones_ordenadas['Curso o Rango Marcial'] != 'Ausbilder']
        indices_clasificados = candidatos_validos.head(12).index
        df_posiciones_ordenadas.loc[indices_clasificados, 'Estado'] = 'Clasificado'
        return df_posiciones_ordenadas

    @property
    def TABLA_POSICIONES(self) -> pd.DataFrame:
        df_bruto = self.constructor_de_tabla()
        return self.sort_en_tabla(df_bruto)

    def guardar_progreso(self, ruta_archivo: str) -> None:
        with open(ruta_archivo, 'wb') as archivo:
            pickle.dump(self, archivo)

    @classmethod
    def cargar_progreso(cls, ruta_archivo: str):
        with open(ruta_archivo, 'rb') as archivo:
            return pickle.load(archivo)


    def exportar_fixture_html(self, ruta_salida: str = "fixture.html") -> None:
        """Genera el HTML del Fixture con tablas separadas por fecha y barra de búsqueda."""
        
        df_calendario = pd.DataFrame(
            list(self.fechas_liga.items()),
            columns=["Fecha", "Fecha de calendario"]
        )
        tabla_fechas_html = df_calendario.to_html(index=False, classes="tabla-liga tabla-fechas", border=0)

        html_tablas_duelos = ""
        for fecha, lista_duelos in self.fixture_de_liga.items():
            html_tablas_duelos += f'<div class="contenedor-fecha"><h3 class="titulo-fecha">{fecha}</h3>\n'
            html_tablas_duelos += '<div class="tabla-responsive"><table class="tabla-liga tabla-fixture">\n'
            html_tablas_duelos += '<thead><tr><th>Esgrimista 1</th><th class="col-corta">Pts</th><th class="col-corta">Dobles</th><th class="col-corta">Pts</th><th>Esgrimista 2</th></tr></thead>\n<tbody>\n'
            
            for duelo in lista_duelos:
                try:
                    if hasattr(duelo, 'puntos_a') and duelo.puntos_a is not None:
                        pa, dob, pb = duelo.puntos_a, duelo.dobles, duelo.puntos_b
                    else:
                        pa, dob, pb = "-", "-", "-"
                except Exception:
                    pa, dob, pb = "-", "-", "-"

                html_tablas_duelos += f'''
                <tr class="fila-duelo">
                    <td>{duelo.esgrimista_a.nombre}</td>
                    <td class="casilla-resultado">{pa}</td>
                    <td class="casilla-resultado">{dob}</td>
                    <td class="casilla-resultado">{pb}</td>
                    <td>{duelo.esgrimista_b.nombre}</td>
                </tr>'''
            
            html_tablas_duelos += '</tbody></table></div></div>\n'

        html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fixture - Liga Praelium Australis 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #262626;
            color: #ffffff;
            font-family: 'Cardo', serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            text-decoration: none;
            color: white;
        }}
        .logo-club {{ height: 90px; width: auto; }}
        .header-text h1 {{ margin: 0; font-size: 1.8rem; font-weight: 400; }}
        .header-text h2 {{ margin: 0; font-size: 1.4rem; font-weight: 400; color: #E86509; }}
        
        .boton-volver {{
            background-color: #E86509;
            color: #000;
            text-decoration: none;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 25px;
            transition: 0.2s;
        }}
        .boton-volver:hover {{ background-color: #ff7e23; }}

        .buscador-container {{
            width: 90%;
            max-width: 800px;
            margin-bottom: 30px;
            display: flex;
            justify-content: center;
        }}
        #buscador {{
            width: 100%;
            max-width: 400px;
            padding: 12px 20px;
            font-size: 1.1rem;
            border-radius: 8px;
            border: 1px solid #E86509;
            background-color: #1e1e1e;
            color: white;
            font-family: 'Cardo', serif;
        }}
        #buscador:focus {{ outline: none; box-shadow: 0 0 8px rgba(232, 101, 9, 0.7); }}

        .tabla-responsive {{
            width: 90vw;
            max-width: 800px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            border: 1px solid #444;
            margin-bottom: 40px;
        }}
        .tabla-fechas {{ margin-bottom: 20px; max-width: 500px; margin-left: auto; margin-right: auto; }}
        
        .contenedor-fecha {{ width: 100%; max-width: 800px; }}
        .titulo-fecha {{
            color: #ffffff;
            font-size: 1.5rem;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: left;
            border-bottom: 2px solid #E86509;
            padding-bottom: 5px;
        }}

        .tabla-liga {{ border-collapse: collapse; width: 100%; min-width: 600px; background-color: #1e1e1e; }}
        .tabla-liga th {{ background-color: #E86509; color: #000000; font-weight: 700; padding: 12px; text-align: center; font-size: 1.1rem; }}
        .tabla-liga td {{ padding: 10px; text-align: center; border-bottom: 1px solid #333; }}
        .tabla-liga tr:nth-child(even) {{ background-color: #262626; }}
        
        .col-corta {{ width: 60px; }}
        .casilla-resultado {{ font-weight: bold; color: #E86509; background-color: #151515; }}
    </style>
</head>
<body>
    <a href="index.html" class="header-container">
        <img src="assets/images/logo_PA.png" alt="Logo PA" class="logo-club">
        <div class="header-text">
            <h1>Fixture de Liga</h1>
            <h2>Espada Larga 2026</h2>
        </div>
    </a>
    <a href="index.html" class="boton-volver">← Volver al Inicio</a>

    {tabla_fechas_html}

    <div class="buscador-container">
        <input type="text" id="buscador" onkeyup="filtrarDuelos()" placeholder="🔎 Buscar esgrimista (ej. Alexis)...">
    </div>

    {html_tablas_duelos}

    <script>
        function filtrarDuelos() {{
            let input = document.getElementById('buscador');
            let filter = input.value.toLowerCase();
            let contenedores = document.getElementsByClassName('contenedor-fecha');

            for (let i = 0; i < contenedores.length; i++) {{
                let contenedor = contenedores[i];
                let filas = contenedor.getElementsByClassName('fila-duelo');
                let fechaVisible = false;

                for (let j = 0; j < filas.length; j++) {{
                    let fila = filas[j];
                    let textoFila = fila.textContent || fila.innerText;
                    
                    if (textoFila.toLowerCase().indexOf(filter) > -1) {{
                        fila.style.display = "";
                        fechaVisible = true;
                    }} else {{
                        fila.style.display = "none";
                    }}
                }}
                
                // Si ningún duelo coincide en esta fecha, ocultamos la fecha completa
                if (fechaVisible) {{
                    contenedor.style.display = "";
                }} else {{
                    contenedor.style.display = "none";
                }}
            }}
        }}
    </script>
</body>
</html>"""

        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(html_completo)
        print(f"¡Fixture HTML actualizado con búsqueda en '{ruta_salida}'!")


    def exportar_ranking_html(self, ruta_salida: str = "ranking.html") -> None:
        df_rank = self.TABLA_POSICIONES
        
        def resaltar_clasificados(row):
            if row['Estado'] == 'Clasificado':
                return ['background-color: #1e3a24; color: #73e68c; font-weight: bold;'] * len(row)
            return [''] * len(row)

        tabla_html = (
            df_rank.style
            .apply(resaltar_clasificados, axis=1)
            .format({
                "Pts P": "{:.2f}",
                "Dif P": "{:.2f}",
                "Asistencia": "{:.1f}",
                "Dobles P": "{:.2f}"
            })
            .set_table_attributes('class="tabla-liga" border="0"')
            .to_html(index=True)
        )

        html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ranking - Liga Praelium Australis 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cardo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #262626;
            color: #ffffff;
            font-family: 'Cardo', serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
            text-decoration: none;
            color: white;
        }}
        .logo-club {{ height: 90px; width: auto; }}
        .header-text h1 {{ margin: 0; font-size: 1.8rem; font-weight: 400; }}
        .header-text h2 {{ margin: 0; font-size: 1.4rem; font-weight: 400; color: #E86509; }}
        
        .boton-volver {{
            background-color: #E86509;
            color: #000;
            text-decoration: none;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 25px;
            transition: 0.2s;
        }}
        .boton-volver:hover {{ background-color: #ff7e23; }}
        .tabla-responsive {{
            width: 95%;
            max-width: 950px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            border: 1px solid #444;
        }}
        .tabla-liga {{
            border-collapse: collapse;
            width: 95%;
            max-width: 950px;
            background-color: #1e1e1e;
        }}
        .tabla-liga th {{
            background-color: #E86509;
            color: #000000;
            font-weight: 700;
            padding: 12px;
            text-align: center;
            font-size: 1rem;
        }}
        .tabla-liga td {{
            padding: 8px 12px;
            text-align: center;
            border-bottom: 1px solid #333;
        }}

        .glosario {{
            width: 95%;
            max-width: 950px;
            margin-top: 25px;
            margin-bottom: 40px;
            color: #ffffff;
            font-size: 0.9rem;
            line-height: 1.6;
            text-align: left;
        }}
        .glosario h3 {{
            margin: 0 0 8px 0;
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .glosario p {{
            margin: 4px 0;
        }}
        .destacado-naranjo {{
            color: #E86509;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <a href="index.html" class="header-container">
        <img src="assets/images/logo_PA.png" alt="Logo PA" class="logo-club">
        <div class="header-text">
            <h1>Ranking de Liga</h1>
            <h2>Espada Larga 2026</h2>
        </div>
    </a>
    <a href="index.html" class="boton-volver">← Volver al Inicio</a>
<div class="tabla-responsive">
    {tabla_html}
</div>

    <div class="glosario">
        <h3>Glosario</h3>
        <p><strong>Pts P:</strong> Puntaje total ponderado por la cantidad de duelos combatidos por el esgrimista <span class="destacado-naranjo">[más es mejor]</span></p>
        <p><strong>Dif P:</strong> Diferencia total de intercambios ponderada por la cantidad de duelos combatidos por el esgrimista (Para ello considere la diferencia entre los intercambios favorables ponderados y los intercambios desfavorables ponderados) <span class="destacado-naranjo">[más es mejor]</span></p>
        <p><strong>Asistencia:</strong> Cantidad de clases a las que asistió el esgrimista <span class="destacado-naranjo">[más es mejor]</span></p>
        <p><strong>Dobles P:</strong> Cantidad de dobles cometidos por el esgrimista ponderados por la cantidad de duelos combatidos <span class="destacado-naranjo">[menos es mejor]</span></p>
    </div>
</body>
</html>"""
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(html_completo)
        print(f"¡Ranking HTML generado con éxito en '{ruta_salida}'!")