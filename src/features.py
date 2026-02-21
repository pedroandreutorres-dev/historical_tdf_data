import pandas as pd
import numpy as np

def feature_analisys (df_stages: pd.DataFrame, df_tours: pd.DataFrame, df_winners: pd.DataFrame) -> pd.DataFrame:
    
    # Estandarización de tipos de etapa (Corregir typos detectados)
    type_mapping = {
                'Mountain time-trial': 'Mountain', # La contamos como montaña pura por esfuerzo
                'Double sector': 'Flat' # Históricamente solían ser llanas
                }
    
    df_stages['type'] = df_stages['type'].replace(type_mapping)

    # Defnimos Pesos de Esfuerzo (Hardness Weights)
    weights = {
        'Mountain': 1.0,
        'Hilly': 0.7,
        'Individual time-trial': 0.6,
        'Team time-trial': 0.4,
        'Cobblestones': 0.4,
        'Flat': 0.2
    }

    # Creamos la columna de Carga de Trabajo (Workload) por etapa
    df_stages['stage_workload'] = df_stages.apply(
        lambda x: x['distance_in_km'] * weights.get(x['type'], 0.2), axis=1
    )

    # Calculamosla dureza anual
    # Sumamos la carga de trabajo y contamos las etapas reales
    df_hardness_annual = df_stages.groupby('year').agg(
        total_workload=('stage_workload', 'sum'),
        actual_stages_count=('stage', 'count')
    ).reset_index()

    df_analysis = pd.merge(df_tours, df_hardness_annual, on='year', how='inner')
    df_analysis = pd.merge(df_analysis, df_winners[['year', 'avg speed']], on='year', how='left')

    # Calculamos la Intensidad Diaria
    df_analysis['daily_intensity'] = df_analysis['total_workload'] / df_analysis['actual_stages_count']

    # Calculamos el porcentaje de etapas de Montaña/Media Montaña por año
    mountain_stages = df_stages[df_stages['type'].isin(['Mountain', 'Hilly'])].groupby('year').size().reset_index(name='mountain_count')
    df_analysis = pd.merge(df_analysis, mountain_stages, on='year', how='left').fillna(0)
    df_analysis['mountain_percentage'] = (df_analysis['mountain_count'] / df_analysis['actual_stages_count']) * 100

    return df_analysis

def feature_workload (df_stages: pd.DataFrame) -> pd.DataFrame:

    # Agrupamos por década
    df_stages['decade'] = (df_stages['year'] // 10) * 10
    workload_by_type = df_stages.groupby(['decade', 'type'])['stage_workload'].sum().reset_index()
    workload_pivot = workload_by_type.pivot(index='decade', columns='type', values='stage_workload').fillna(0)

    # Convertimos a porcentajes
    workload_perc = workload_pivot.div(workload_pivot.sum(axis=1), axis=0) * 100

    # Ordenamos columnas
    orden_columnas = ['Flat', 'Cobblestones', 'Team time-trial', 'Individual time-trial', 'Hilly', 'Mountain']
    workload_perc = workload_perc[orden_columnas]

    return workload_perc

def feature_speed (df_winners: pd.DataFrame) -> pd.DataFrame:
    # Preparamos los datos limpios de velocidad (eliminamos nulos de los primeros años)
    df_speed = df_winners.dropna(subset=['avg speed']).sort_values('year').copy()
    return df_speed

def feature_age (df_winners: pd.DataFrame) -> pd.DataFrame:
    # Calculamos la Edad Exacta al ganar
    # Convertimos el año del Tour en una fecha aproximada (el 15 de julio)
    df_winners['tour_date'] = pd.to_datetime(df_winners['year'].astype(str) + '-07-15')
    df_winners['born'] = pd.to_datetime(df_winners['born'], errors='coerce')

    # Calculamos la edad exacta en años
    df_winners['age'] = (df_winners['tour_date'] - df_winners['born']).dt.days / 365.25

    # Limpiamos valores nulos y preparamos para graficar
    df_age = df_winners.dropna(subset=['age']).copy()
    df_age.sort_values('year', inplace=True)

    return df_age