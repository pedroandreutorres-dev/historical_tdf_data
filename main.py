from src.io import load_data, save_data
from src.cleaning import clean_finishers, clean_stages, clean_tours, clean_winners
from src.features import feature_analisys


def main ():

    #cargamos datasets
    print ('Cargamos datasets')
    df_finishers = load_data('data/raw/tdf_finishers_master.csv')
    df_stages = load_data('data/raw/tdf_stages_master.csv')
    df_tours = load_data('data/raw/tdf_tours_master.csv')
    df_winners = load_data('data/raw/tdf_winners_master.csv')
    print ('Hecho')

    #limpiamos datasets
    print ('Limpiamos datasets')
    df_finishers = clean_finishers(df_finishers)
    df_stages = clean_stages(df_stages)
    df_tours = clean_tours(df_tours)
    df_winners = clean_winners(df_winners)
    print ('Hecho')

    # Construimos dataset para analisis de dureza histórica
    print ('Construimos dataset para analisis de dureza hostórica')
    df_analisys = feature_analisys(df_stages, df_tours, df_winners)
    print ('Hecho')
    print (df_analisys.head())



if __name__ == "__main__":
    main()
