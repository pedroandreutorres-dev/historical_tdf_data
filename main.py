from src.io import load_data, save_data
from src.cleaning import clean_finishers, clean_stages, clean_tours, clean_winners
from src.features import calculate_stage_workload, create_hardness_analysis, calculate_physiology
from src.viz import plot_hardness_composition, plot_paradigm_shift, plot_survival_gap, plot_age_evolution, plot_bmi_evolution, plot_globalization



def main ():

    #cargamos datasets
    df_finishers = load_data('data/raw/tdf_finishers_master.csv')
    df_stages = load_data('data/raw/tdf_stages_master.csv')
    df_tours = load_data('data/raw/tdf_tours_master.csv')
    df_winners = load_data('data/raw/tdf_winners_master.csv')

    #limpiamos datasets
    df_finishers = clean_finishers(df_finishers)
    df_stages = clean_stages(df_stages)
    df_tours = clean_tours(df_tours)
    df_winners = clean_winners(df_winners)

    # Features
    df_stages_feat = calculate_stage_workload(df_stages)
    df_analysis = create_hardness_analysis(df_stages_feat, df_tours, df_winners)
    df_winners_feat = calculate_physiology(df_winners)

    # #guardamos todos los dataframes
    save_data(df_finishers, 'data/processed/tdf_finishers_clean.csv')
    save_data(df_stages_feat, 'data/processed/tdf_stages_feat.csv')
    save_data(df_analysis, 'data/processed/tdf_analysis.csv')
    save_data(df_winners_feat, 'data/processed/tdf_winners_feat.csv')

    # Generamos las visualizaciones
    plot_hardness_composition(df_stages_feat)
    plot_paradigm_shift(df_analysis)
    plot_survival_gap(df_analysis)
    plot_age_evolution(df_winners_feat)
    plot_bmi_evolution(df_winners_feat)
    plot_globalization(df_finishers)




if __name__ == "__main__":
    main()
