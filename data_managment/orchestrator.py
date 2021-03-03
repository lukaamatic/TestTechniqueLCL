# L'ochestrateur appelle tour à tour les fonctions nécessaires pour notre application
import os
from data_managment.data_manager import DataManager
import data_visualisation


def orchestrator(files_location, destination_folder, unzip=True):

    # Initialise l'objet DataManager qui nous permet de traiter les data brutes
    data_manager = DataManager(files_location, destination_folder)

    # Deplace les fichiers .zip de notre dossier de téléchargement à celui de notre projet
    data_manager.move_files()

    # Faire une liste des fichiers disponibles
    files = os.listdir(destination_folder)
    files_zip = [f for f in files if f.endswith('.zip')]
    files_csv = [f for f in files if f.endswith('.csv') and f.startswith("concatenated") is False]

    if unzip:
        # Extrait les fichiers .csv des zip
        for f in files_zip:
            data_manager.unzip(f)

    # On divise le traitement des fichiers par 10
    chunks = [files_csv[x:x + 10] for x in range(0, len(files_csv), 10)]

    first_id = 0  # permettra d'indexer le dataframe

    for chunk in chunks:
        # Extrait la data des fichiers csv pour l'intégrer à un dataframe csv
        df_deces, last_id = data_manager.extract_from_file(chunk, first_id)

        first_id = last_id  # retient l'id du dernier element

        print(last_id)

        # pré-traitement des données
        print("Cleaning current dataset")
        df_deces = data_manager.clean_dataset(df_deces)

        # fonction pour la data visualisation
        #data_visualisation.data_vis(df_deces)
        #data_visualisation.plot_and_save(df_deces)

        # injecter dans la base de données
        print("Injection dans la base de données")
        data_manager.inject_to_database(df_deces)

        del df_deces


if __name__ == '__main__':
    orchestrator("C:/Users/L/PycharmProjects/testTechniqueLCL/rpa",
                 "C:/Users/L/PycharmProjects/testTechniqueLCL/data_managment/data_folder",
                 unzip=False)
