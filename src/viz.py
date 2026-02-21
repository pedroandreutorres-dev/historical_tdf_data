import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (14, 7)

def plot_hardness_composition(df_stages_feat):
    setup_style()
    df = df_stages_feat.copy()
    df['decade'] = (df['year'] // 10) * 10
    workload_pivot = df.groupby(['decade', 'type'])['stage_workload'].sum().reset_index().pivot(index='decade', columns='type', values='stage_workload').fillna(0)
    
    workload_perc = workload_pivot.div(workload_pivot.sum(axis=1), axis=0) * 100
    orden_columnas = ['Flat', 'Cobblestones', 'Team time-trial', 'Individual time-trial', 'Hilly', 'Mountain']
    
    colores = {'Flat': '#A8DADC', 'Cobblestones': '#8D99AE', 'Team time-trial': '#457B9D', 
               'Individual time-trial': '#1D3557', 'Hilly': '#F4A261', 'Mountain': '#E63946'}
               
    cols_exist = [c for c in orden_columnas if c in workload_perc.columns]
    
    ax = workload_perc[cols_exist].plot(kind='bar', stacked=True, color=[colores[c] for c in cols_exist], edgecolor='white', width=0.85)
    plt.title('Evolución del Trazado', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Década', fontsize=12, fontweight='bold')
    plt.ylabel('Porcentaje de la Dureza Total (%)', fontsize=12, fontweight='bold')
    plt.legend(title='Tipo de Etapa', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_paradigm_shift(df_analysis):
    setup_style()
    plt.figure()
    scatter = plt.scatter(x=df_analysis['distance_in_km'], y=df_analysis['mountain_percentage'], 
                          c=df_analysis['year'], cmap='plasma', s=100, alpha=0.8, edgecolors='white', linewidth=1)
    plt.colorbar(scatter, label='Año de Edición')
    
    z = np.polyfit(df_analysis['distance_in_km'], df_analysis['mountain_percentage'], 1)
    p = np.poly1d(z)
    plt.plot(df_analysis['distance_in_km'], p(df_analysis['distance_in_km']), "k--", alpha=0.7, linewidth=2)
    
    plt.title('El Cambio de Paradigma', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Distancia Total del Tour (Km)', fontsize=12, fontweight='bold')
    plt.ylabel('Proporción de Etapas de Montaña (%)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_survival_gap(df_analysis):
    setup_style()
    plt.figure()
    plt.fill_between(df_analysis['year'], df_analysis['starters'], color='#e0e0e0', label='Abandonos')
    plt.fill_between(df_analysis['year'], df_analysis['finishers'], color='#2A9D8F', alpha=0.8, label='Finalistas')
    plt.plot(df_analysis['year'], df_analysis['starters'], color='black', linewidth=1.5, label='Total Inscritos')
    
    plt.title('La Brecha de Supervivencia', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Año de Edición', fontsize=12, fontweight='bold')
    plt.ylabel('Número de Ciclistas', fontsize=12, fontweight='bold')
    plt.legend(loc='upper left', frameon=True, shadow=True)
    plt.xlim(df_analysis['year'].min(), df_analysis['year'].max())
    plt.tight_layout()
    plt.show()

def plot_age_evolution(df_winners_feat):
    setup_style()
    df_age = df_winners_feat.dropna(subset=['age']).sort_values('year').copy()
    plt.figure()
    
    scatter = plt.scatter(df_age['year'], df_age['age'], c=df_age['age'], cmap='coolwarm_r', 
                          s=80, alpha=0.8, edgecolors='white', linewidth=1.5, zorder=3)
    
    df_age['age_smooth'] = df_age['age'].rolling(window=5, center=True, min_periods=3).mean()
    plt.plot(df_age['year'], df_age['age_smooth'], color='black', linewidth=3, label='Tendencia (Media Móvil 5 ed.)', zorder=2)
    
    plt.axhspan(26, 29, color='gray', alpha=0.15, label='Pico Biológico Teórico (26-29 años)', zorder=1)
    
    plt.title('Evolución de la Edad del Campeón del Tour', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Año de Edición', fontsize=12, fontweight='bold')
    plt.ylabel('Edad Exacta al Ganar (Años)', fontsize=12, fontweight='bold')
    plt.legend(loc='lower left', frameon=True, shadow=True)
    plt.tight_layout()
    plt.show()

def plot_bmi_evolution(df_winners_feat):
    setup_style()
    df_bmi = df_winners_feat[df_winners_feat['year'] >= 1950].dropna(subset=['bmi']).sort_values('year').copy()
    plt.figure()
    
    scatter = plt.scatter(df_bmi['year'], df_bmi['bmi'], c=df_bmi['bmi'], cmap='YlOrRd', 
                          s=90, alpha=0.9, edgecolors='black', linewidth=1, zorder=3)
    cbar = plt.colorbar(scatter)
    cbar.set_label('Índice de Masa Corporal (BMI)', rotation=270, labelpad=20, fontweight='bold')
    
    z = np.polyfit(df_bmi['year'], df_bmi['bmi'], 2)
    p = np.poly1d(z)
    plt.plot(df_bmi['year'], p(df_bmi['year']), "k--", alpha=0.7, linewidth=3, label='Tendencia Histórica', zorder=2)
    
    plt.axhspan(18.5, 20.5, color='green', alpha=0.1, label='Biotipo Escalador (18.5 - 20.5)', zorder=1)
    
    plt.title('La Evolución del Biotipo (1950-Actualidad)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Año de Edición', fontsize=12, fontweight='bold')
    plt.ylabel('Índice de Masa Corporal (BMI)', fontsize=12, fontweight='bold')
    plt.legend(loc='lower left', frameon=True, shadow=True)
    plt.tight_layout()
    plt.show()
