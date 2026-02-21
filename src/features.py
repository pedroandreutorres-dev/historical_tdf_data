import pandas as pd

def calculate_stage_workload(df_stages):
    """Añade los pesos a las etapas y calcula la carga de trabajo."""
    df_feat = df_stages.copy()
    
    # Unificación de categorías
    type_mapping = {
        'Individual time-travel': 'Individual time-trial',
        'Mountain time-trial': 'Mountain',
        'Double sector': 'Flat'
    }
    df_feat['type'] = df_feat['type'].replace(type_mapping)
    
    # Pesos de Dureza
    weights = {
        'Mountain': 1.0, 'Hilly': 0.7, 'Individual time-trial': 0.6,
        'Team time-trial': 0.4, 'Cobblestones': 0.4, 'Flat': 0.2
    }
    
    df_feat['stage_workload'] = df_feat.apply(
        lambda x: x['distance_in_km'] * weights.get(x['type'], 0.2), axis=1
    )
    return df_feat

def create_hardness_analysis(df_stages_feat, df_tours_clean, df_winners_clean):
    """Cruza stages y tours para crear el dataframe de análisis de Dureza."""
    # Agregación anual
    df_annual = df_stages_feat.groupby('year').agg(
        total_workload=('stage_workload', 'sum'),
        actual_stages_count=('stage', 'count')
    ).reset_index()
    
    # Porcentaje de montaña
    mountain_stages = df_stages_feat[df_stages_feat['type'].isin(['Mountain', 'Hilly'])].groupby('year').size().reset_index(name='mountain_count')
    df_annual = pd.merge(df_annual, mountain_stages, on='year', how='left').fillna(0)
    df_annual['mountain_percentage'] = (df_annual['mountain_count'] / df_annual['actual_stages_count']) * 100
    
    # Merge Final
    df_analysis = pd.merge(df_tours_clean, df_annual, on='year', how='inner')
    df_analysis = pd.merge(df_analysis, df_winners_clean[['year', 'avg speed']], on='year', how='left')
    df_analysis['daily_intensity'] = df_analysis['total_workload'] / df_analysis['actual_stages_count']
    
    return df_analysis

def calculate_physiology(df_winners):
    """Calcula el BMI y la Edad exacta al ganar."""
    df_physio = df_winners.copy()
    
    # 1. Calcular BMI
    if 'weight' in df_physio.columns and 'height' in df_physio.columns:
        df_physio['bmi'] = df_physio['weight'] / (df_physio['height'] ** 2)
        
    # 2. Calcular Edad Exacta
    if 'born' in df_physio.columns:
        df_physio['tour_date'] = pd.to_datetime(df_physio['year'].astype(str) + '-07-15')
        df_physio['born'] = pd.to_datetime(df_physio['born'], errors='coerce')
        df_physio['age'] = (df_physio['tour_date'] - df_physio['born']).dt.days / 365.25
        
    return df_physio