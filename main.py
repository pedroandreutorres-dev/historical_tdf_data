from src.io import load_data, save_data
from src.cleaning import clean_finishers, clean_stages, clean_tours, clean_winners
from src.features import feature_analisys, feature_workload, feature_speed, feature_age


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

    # Construimos dataset para analisis de dureza histórica
    df_analisys = feature_analisys(df_stages, df_tours, df_winners)
    # Construimos dataset para analisis de etapas
    df_workload = feature_workload(df_stages)
    # Construimos dataset para analisis de velocidad media
    df_speed = feature_speed(df_winners)
    # Construimos dataset para analisis de edad
    df_age = feature_age(df_winners)

    # Guardamos datasets




    print (df_age)

    # Guardamos datasets






if __name__ == "__main__":
    main()
