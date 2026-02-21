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

    return df_analysis