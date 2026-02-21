import pandas as pd
import numpy as np
import re

def time_to_seconds(time_str):
    if pd.isnull(time_str):
        return np.nan
    clean_time = time_str.replace('"', ' ').replace('+', '').replace('h', '').replace("'", "").replace("′", "").replace("″", "").split()
    if len(clean_time) == 3:
        hours, minutes, seconds = clean_time
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    elif len(clean_time) == 2:
        minutes, seconds = clean_time
        return int(minutes) * 60 + int(seconds)
    elif len(clean_time) == 1:
        return int(clean_time[0])
    else:
        return np.nan
    
def extract_km (distance_str):
    km_index = distance_str.find ('km')
    km_value = distance_str[:km_index].strip()
    return float (km_value)

def extract_km (distance_str):
    km_index = distance_str.find ('km')
    km_value = distance_str[:km_index].strip()
    km_value = km_value.replace(',', '')

    return float (km_value)

def normalizar_fechas_final(fecha_texto):
    meses = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 
        'May': '05', 'June': '06', 'July': '07', 'August': '08', 
        'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }
    
    texto = str(fecha_texto)
    
    #Limpieza base
    texto = re.sub(r'\[.*?\]', '', texto)          
    texto = re.sub(r'\d{4}$', '', texto)           
    texto = texto.replace('\xa0', ' ')             
    
    # Reemplazamos CUALQUIER carácter que no sea alfanumérico (\w) o espacio (\s) por un '-'
    # Esto cazará automáticamente esos "–" o "—" invisibles y corruptos.
    texto = re.sub(r'[^\w\s]', '-', texto)
    
    # Limpiamos espacios alrededor del nuevo guion y colapsamos espacios dobles
    texto = re.sub(r'\s*-\s*', '-', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()     
    
    # Separación
    partes = texto.split('-')
    
    if len(partes) != 2:
        return fecha_texto 
        
    inicio_str = partes[0].strip()
    fin_str = partes[1].strip()
    
    inicio_partes = inicio_str.split()
    fin_partes = fin_str.split()
    
    try:
        # Lógica A: Mismo mes (ej. "1", "19 July")
        if len(inicio_partes) == 1:
            dia_inicio = inicio_partes[0].zfill(2)
            dia_fin = fin_partes[0].zfill(2)
            mes = meses.get(fin_partes[1], '00')
            return f"De {dia_inicio}/{mes} a {dia_fin}/{mes}"
            
        # Lógica B: Meses distintos (ej. "8 July", "4 August")
        else:
            dia_inicio = inicio_partes[0].zfill(2)
            mes_inicio = meses.get(inicio_partes[1], '00')
            dia_fin = fin_partes[0].zfill(2)
            mes_fin = meses.get(fin_partes[1], '00')
            return f"De {dia_inicio}/{mes_inicio} a {dia_fin}/{mes_fin}"
            
    except Exception as e:
        return fecha_texto

def clean_finishers(df_finishers: pd.DataFrame) -> pd.DataFrame:
    # Se detecta un error en el archivo csv que impide cargar bien dos filas del año 1979.
    # Localizamos la celda y arreglamos
    mask_corrupta = df_finishers['Time'].str.contains('\r\n', na=False)

    if mask_corrupta.any():
        idx = df_finishers[mask_corrupta].index[0]
        texto_sucio = df_finishers.at[idx, 'Time']
        equipo_desplazado = df_finishers.at[idx, 'Team']
        
        # Troceamos el texto para separar a Joop de Joaquim
        partes = texto_sucio.splitlines()
        
        # A. Arreglamos a Joop Zoetemelk (Fila actual)
        datos_joop = partes[0].split(',')
        df_finishers.at[idx, 'Time'] = datos_joop[0].replace('"', '')
        df_finishers.at[idx, 'Team'] = datos_joop[1]
        
        # B. Creamos a Joaquim Agostinho (Fila nueva)
        # No le ponemos Rank todavía, dejamos que el cumcount lo haga luego
        datos_joaquim = partes[1].split(',')
        fila_nueva = pd.DataFrame({
            'Year': [1979],
            'Rank': [3],
            'Rider': [datos_joaquim[2]],
            'Time': [datos_joaquim[3].replace('"', '').strip()],
            'Team': [equipo_desplazado]
        })
        
        # Insertamos la fila justo debajo de Joop para que el orden sea el de llegada
        df_finishers = pd.concat([df_finishers.iloc[:idx+1], fila_nueva, df_finishers.iloc[idx+1:]]).reset_index(drop=True)

    # Convertimos rank a int
    df_finishers['Rank'] = df_finishers.groupby('Year').cumcount() + 1
    df_finishers['Rank'] = df_finishers['Rank'].astype(int)

    #Limpieza de la columna Rider
    df_finishers['Rider'] = df_finishers['Rider'].str.replace(r'\[.*?\]', '', regex=True)
    df_finishers['Rider'] = df_finishers['Rider'].str.replace(r'\s+', ' ', regex=True).str.strip()
    df_finishers[['Rider_name', 'Country']] = df_finishers['Rider'].str.extract(r'^(.*)\s\((.*)\)$')
    df_finishers.loc[df_finishers['Rider_name'].isnull(), 'Rider_name'] = df_finishers['Rider']
    df_finishers.loc[df_finishers['Country'].isnull(), 'Country'] = 'RUS'    
    df_finishers['Rider_name'] = df_finishers['Rider_name'].str.strip()
    df_finishers['Country'] = df_finishers['Country'].str.strip()
    df_finishers.drop(columns=['Rider'], inplace = True)

    #limpiamos la columna 'Country'
    #Creo uin diccionario para unificar datos.
    unificated_country = {'FRA': 'Francia', 'ITA': 'Italia', 'BEL': 'Bélgica', 'GER': 'Alemania', 'LUX': 'Luxemburgo',
                    'SUI': 'Suiza', 'Italy': 'Italia', 'AUS': 'Australia', 'MON': 'Mónaco', 'ESP': 'España', 'NZL': 'Nueva Zelanda',
                    'AUT': 'Austria', 'NED': 'Países Bajos', 'ALG': 'Argelia', 'POL': 'Polonia', 'GBR': 'Reino Unido',
                    'FRG': 'Alemania', 'POR': 'Portugal', 'IRL': 'Irlanda', 'DEN': 'Dinamarca', 'SWE': 'Suecia',
                    'COL': 'Colombia', 'NOR': 'Noruega', 'IRE': 'Irlanda', 'USA': 'Estados Unidos', 'CAN': 'Canadá',
                    'YUG': 'Yugoslavia', 'MEX': 'México', 'TCH': 'Checoslovaquia', 'URS': 'URSS', 'DDR': 'Alemania',
                    'UZB': 'Uzbekistán', 'UKR': 'Ucrania', 'BRA': 'Brasil', 'LIT': 'Lituania', 'RUS': 'Rusia',
                    'VEN': 'Venezuela', 'LAT': 'Letonia', 'SVK': 'Eslovaquia', 'FIN': 'Finlandia', 'EST': 'Estonia',
                    'KAZ': 'Kazajistán', 'CZE': 'República Checa', 'SPA': 'España', 'LTU': 'Lituania', 'HUN': 'Hungría',
                    'SAF': 'Sudáfrica', 'SLO': 'Eslovenia', 'CRO': 'Croacia', 'BLR': 'Bielorrusia', 'RSA': 'Sudáfrica',
                    'JPN': 'Japón', 'MDA': 'Moldavia', 'SVN': 'Eslovenia', 'CRC': 'Costa Rica', 'ARG': 'Argentina',
                    'UK': 'Reino Unido', 'CHN': 'China', 'ERI': 'Eritrea', 'SWI': 'Suiza', 'ETH': 'Etiopía', 
                    'ECU': 'Ecuador', 'ISR': 'Israel', 'NLD': 'Países Bajos'}
    df_finishers['Country_normalized'] = df_finishers['Country'].map(unificated_country)
    df_finishers.drop(columns='Country', inplace=True)
    df_finishers.rename (columns = {'Country_normalized': 'country'}, inplace = True)

    #Limpieza de la columna Time
    # Aplico la función a la columna Time para crear una nueva columna Time_seconds
    df_finishers['Time_seconds'] = df_finishers['Time'].apply(time_to_seconds)
    # Ahora, año a año, sumo los segundos del primero a cada uno de los otros corredores para que salga el total de segundos 
    # que ha empleado cada corredor
    df_finishers['winner_time_base'] = df_finishers.groupby('Year')['Time_seconds'].transform('first')
    df_finishers['rider_total_time'] = np.where(
        df_finishers['Time_seconds'] == df_finishers['winner_time_base'],
        df_finishers['winner_time_base'],
        df_finishers['winner_time_base'] + df_finishers['Time_seconds']
    )
    df_finishers.drop(columns=['winner_time_base', 'Time_seconds', 'Time'], inplace=True)

    #Últimos cambios
    #Cambiamos de orden las columnas
    new_order = ['Year', 'Rank', 'Rider_name', 'country', 'Team', 'rider_total_time']
    df_clean_finishers = df_finishers[new_order]
    df_clean_finishers.columns = df_clean_finishers.columns.str.lower()


    return df_clean_finishers

def clean_stages(df_stages: pd.DataFrame) -> pd.DataFrame:
    
    #Titulos de columnas en minusculas
    df_stages.columns = df_stages.columns.str.lower()

    #Convertimos la columna date a tipo de fecha
    df_stages['date'] = pd.to_datetime(df_stages['date'])

    #Vemos que la columna 'distance' tiene el formato 160.4 km (99.7 mi)
    #Eliminamos las millas y los caracteres km y convertimos.
    df_stages['distance_in_km'] = df_stages['distance'].apply(extract_km)
    df_stages.drop(columns = 'distance', inplace = True)

    # Limpiamos columna winner y creamos columna país
    # Limpieza inicial (Corchetes y espacios)
    df_stages['winner'] = df_stages['winner'].str.replace(r'\[.*?\]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()

    # INTENTO A: País con paréntesis al FINAL -> "Nombre (ESP)"
    df_stages[['winner_name', 'country']] = df_stages['winner'].str.extract(r'^(.*)\s+\(([^()]+)\)$')

    # INTENTO B: País con paréntesis al PRINCIPIO -> "(ESP) Nombre"
    # Rellenamos solo donde 'country' sea nulo
    ext_inicio_par = df_stages['winner'].str.extract(r'^\(([^()]+)\)\s+(.*)$')
    df_stages['country'] = df_stages['country'].fillna(ext_inicio_par[0])
    df_stages['winner_name'] = df_stages['winner_name'].fillna(ext_inicio_par[1])

    # INTENTO C: País SIN paréntesis al FINAL -> "Nombre ESP"
    # Buscamos 3 letras mayúsculas exactas al final de la línea
    ext_fin_sin = df_stages['winner'].str.extract(r'^(.*?)\s+([A-Z]{3})$')
    df_stages['country'] = df_stages['country'].fillna(ext_fin_sin[1])
    df_stages['winner_name'] = df_stages['winner_name'].fillna(ext_fin_sin[0])

    # INTENTO D: País SIN paréntesis al PRINCIPIO -> "ESP Nombre"
    # Buscamos 3 letras mayúsculas exactas al principio de la línea
    ext_ini_sin = df_stages['winner'].str.extract(r'^([A-Z]{3})\s+(.*)$')
    df_stages['country'] = df_stages['country'].fillna(ext_ini_sin[0])
    df_stages['winner_name'] = df_stages['winner_name'].fillna(ext_ini_sin[1])

    # CASO FINAL: Si no hay país, el nombre es el original
    df_stages['winner_name'] = df_stages['winner_name'].fillna(df_stages['winner'])

    # Limpieza final de espacios
    df_stages['winner_name'] = df_stages['winner_name'].str.strip()
    df_stages['country'] = df_stages['country'].str.strip()

    # Quedan dos en los que winner '—'. Son etapas sin ganador, por lo que asignamos 'Unknown' a winner_name
    df_stages['winner_name'] = df_stages['winner_name'].replace('—', 'cancelled')

    # Limpiamos y arreglamos la columna 'country'
    #Primer paso, relleno lacolumna con el pais o equipo ganador.
    df_stages['country'] = df_stages.apply(lambda row: row['winner_name'] if pd.isnull(row['country']) else row['country'], axis=1)

    # A través de un diccionario, normalizamos el nombre del pais y eliminamos los campos en los que no es un pais dejandolos en nulo.
    country_normalized = {'FRA': 'Francia', 'SUI': 'Suiza', 'LUX': 'Luxemburgo', 'BEL': 'Bélgica', 'ITA': 'Italia', 'ESP': 'España', 'AUT': 'Austria',
                      'GER': 'Alemania', 'NED': 'Países Bajos', 'Switzerland': 'Suiza', 'Netherlands': 'Países Bajos', 'France': 'Francia',
                      'GBR': 'Reino Unido', 'FRG': 'Alemania', 'IRL': 'Irlanda', 'Belgium': 'Bélgica', 'Belgium A': 'Bélgica', 'POR': 'Portugal',
                      'DEN': 'Dinamarca', 'IRE': 'Irlanda', 'AUS': 'Australia', 'COL': 'Colombia', 'USA': 'Estados Unidos', 'NOR': 'Noruega',
                      'CAN': 'Canadá', 'MEX': 'México', 'GDR': 'Alemania', 'URS': 'URSS', 'BRA': 'Brasil', 'UZB': 'Uzbekistán', 'POL': 'Polonia',
                      'SVK': 'Eslovaquia', 'LAT': 'Letonia', 'UKR': 'Ucrania', 'RUS': 'Rusia', 'CZE': 'República Checa', 'SWE': 'Suecia', 'EST': 'Estonia',
                      'KAZ': 'Kazajistán', 'RSA': 'Sudáfrica', 'LTU': 'Lituania', 'SLO': 'Eslovenia', 'ERI': 'Eritrea', 'ECU': 'Ecuador'}
    
    df_stages['country'] = df_stages['country'].map(country_normalized)

    # Limpiamos y arreglamos columna 'type'
    # Normalizamos los valores mediante un diccionario
    type_normalzed = {'Plain stage': 'Flat', 'Stage with mountain(s)': 'Mountain', 'Stage with mountain': 'Mountain', 'Team time trial': 'Team time-trial',
                  'Individual time trial': 'Individual time-trial', 'Mountain time trial': 'Mountain time-trial', 'Stage with mountains': 'Mountain',
                  'Flat stage': 'Flat', 'Medium mountain stage': 'Hilly', 'High mountain stage': 'Mountain', 'Hilly stage': 'Hilly', 'Flat Stage': 'Flat',
                  'Half Stage': 'Double sector', 'Hilly Stage': 'Hilly', 'Mountain Stage': 'Mountain', 'Plain stage with cobblestones': 'Cobblestones',
                  'Mountain stage': 'Mountain', 'Mountain Stage (s)': 'Mountain', 'Intermediate stage': 'Flat', 'Transition stage': 'Hilly',
                  'Flat cobblestone stage': 'Cobblestones',  'Medium mountain stage[c]': 'Hilly', 'Flat': 'Flat', 'Medium-mountain stage': 'Hilly',
                  'Etapa escarpada': 'Hilly', 'Etapa llana': 'Flat', 'Etapa de montaña': 'Mountain', 'Contrarreloj individual': 'Individual time-trial',
                  'Etapa de media montaña': 'Hilly', 'Cronoescalada': 'Mountain time-trial'}

    df_stages['type'] = df_stages['type'].map(type_normalzed)

    #Elimino la columna winner
    df_stages.drop(columns = 'winner', inplace = True)

    return df_stages

def clean_tours(df_tours: pd.DataFrame) -> pd.DataFrame:
    
    #Vemos que la columna 'distance' tiene el formato 2,160.4 km (99.7 mi)
    #Eliminamos las millas y los caracteres km y convertimos.
    df_tours['distance_in_km'] = df_tours['Distance'].apply(extract_km)
    df_tours.drop(columns = 'Distance', inplace = True)

    # Separo en dos la columna Stages. 
    # Dejo dentro de la columna el número de etapas y en una nueva columna el texto     
    # Quitamos espacios invisibles (como \xa0) de toda la columna
    # Esto es vital para que el número al principio se detecte bien
    df_tours['Stages'] = df_tours['Stages'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    # Extracción con una Regex más flexible
    # ^(\d+) -> Captura el número inicial
    # \s* -> Salta cualquier espacio opcional que haya justo después del número
    # (.*)   -> Captura TODO lo que quede hasta el final
    df_tours[['Stages_clean', 'stages_observations']] = df_tours['Stages'].str.extract(r'^(\d+)\s*(.*)')

    # Mantenemos el número en la columna original y limpiamos la nueva
    df_tours['Stages'] = df_tours['Stages_clean']
    df_tours['stages_observations'] = df_tours['stages_observations'].str.strip()

    # Borramos la columna temporal
    df_tours.drop(columns=['Stages_clean'], inplace=True)

    # Convertimos a null las que no tiene texto en 'stages_observation'
    df_tours['stages_observations'] = df_tours['stages_observations'].replace('', np.nan)  

    #Ahora, según lo que contenga la taba 'stages_observations', se suma a 'Stages' para que de el número correcto de stages.
    add_stages = {np.nan: 0, ', including one split stage': 1, ', including six split stages': 6, ', including five split stages': 5, ', including eight split stages': 8,
                ', including one split stages': 1, ', including two split stages': 2, ', including three split stages': 3, '+ Prologue, including two split stages': 3,
                ', including four split stages': 4, '+ Prologue, including three split stages': 4, '+ Prologue, including five split stages': 6,
                '+ Prologue, including four split stages': 5, '+ Prologue, including six split stages': 7, '+ Prologue': 1, '+ Prologue, including one split stage': 2,
                '+ prologue': 1}

    extra_stages = df_tours['stages_observations'].map(add_stages).astype(int)
    df_tours['Stages'] = df_tours['Stages'].astype(int) + extra_stages  

    #Creo nueva columna con el % de abandonos
    df_tours['abandon_rate'] = (1 - (df_tours['Finishers'] / df_tours ['Starters'])).round(2)

    # Limipiamos columna Date
    df_tours['Dates'] = df_tours['Dates'].apply(normalizar_fechas_final)

    #Ponemos todos los tituls de columnas en minusculas
    df_tours.columns = df_tours.columns.str.lower()

    #Ordenamos columnas
    column_order = ['year', 'dates', 'stages', 'stages_observations', 'distance_in_km', 'starters', 'finishers', 'abandon_rate']
    df_clean_tours = df_tours[column_order]

    return df_clean_tours

def clean_winners(df_winners: pd.DataFrame) -> pd.DataFrame:
    
    # Hay cierta información que ya están disponibles en otros dataframes, por lo que eliminamos las columnas Country	Rider	Team	Time	Margin y Died
    df_winners.drop(columns = ['Country', 'Rider', 'Team', 'Time', 'Margin', 'Died'], inplace=True)

    # Covertimos Stages Led a int, manteniendo nulos, exceptpo tres nulos, los dejamos
    df_winners['Stages Led'] = df_winners['Stages Led'].astype('Int64')  

    #Limpiamos Avg Speed, Height y Weight
    # Quitamos los caracteres km/h y convertimos a float
    df_winners['Avg Speed'] = df_winners['Avg Speed'].str.replace('km/h', '', regex=False).str.strip()
    df_winners['Avg Speed'] = df_winners['Avg Speed'].astype(float)

    #Quitamos los caracteres m y convertimos a float
    df_winners['Height'] = df_winners['Height'].str.replace('m', '', regex=False).str.strip()
    df_winners['Height'] = df_winners['Height'].astype(float)

    # Lo mismo con Weight qutando kg
    df_winners['Weight'] = df_winners['Weight'].str.replace('kg', '', regex=False).str.strip()
    df_winners['Weight'] = df_winners['Weight'].astype(float)

    # Convertimos Born en formato fecha
    df_winners['Born'] = pd.to_datetime(df_winners['Born'])

    # Cambiamoslos títulos de las columnas a minúsculas
    df_winners.columns = df_winners.columns.str.lower()

    return df_winners