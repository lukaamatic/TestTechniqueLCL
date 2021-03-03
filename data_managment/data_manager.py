import pandas as pd
import os
from io import StringIO
import shutil
import zipfile
from sqlalchemy.engine import create_engine


# Les fonctions suivantes sont utilisées pour divers traitements de données

# Création de la class DataManager
class DataManager:
    def __init__(self, files_location, destination_folder):
        self.files_location = files_location
        self.destination_folder = destination_folder

    def extract_from_file(self, files_list, first_id):
        # fonction that will extract the data from the csv files and insert it into a pandas dataframe
        # fonction qui extrait la data des fichiers csv et les insert dans un dataframe pandas

        first_file = True

        # iteration a travers les fichiers pour les ajouter au dataframe
        for filename in files_list:
            if filename.endswith(".csv"):
                print("Reading csv : " + filename)
                # Si il y a un probleme avec le traitement du fichier, on leve l'erreur et on passe au suivant
                try:
                    self.clean_files(self.destination_folder + "/" + filename)
                    if first_file:
                        df_deces = pd.read_csv(self.destination_folder + "/" + filename, sep=";", error_bad_lines=False)
                    else:
                        df_deces = df_deces.append(pd.read_csv(self.destination_folder + "/" + filename, sep=";",
                                                   error_bad_lines=False))
                except ValueError as err:
                    print("There was a problem with the file  " + filename)
                first_file = False
                print("df en est a " + str(df_deces.shape[0]))

        # Creation d'une clé unique pour chaque décès
        df_deces = df_deces.reset_index(drop=True)
        df_deces["id"] = df_deces.index + 1 + first_id
        last_id = df_deces["id"].iloc[[-1]]

        return df_deces, last_id

    def clean_dataset(self, df):
        # supprime les doublons, vérifie les lignes vides, formatte les colonne

        df.drop_duplicates(inplace=True)  # doublons
        df.dropna(how="all", inplace=True)  # valeurs vides
        df['datedeces'] = pd.to_datetime(df['datedeces'], format='%Y%m%d', errors='coerce')  # formate les colonnes de date
        df['datenaiss'] = pd.to_datetime(df['datenaiss'], format='%Y%m%d', errors='coerce')
        df.rename(columns={" prenom": "prenom"}, inplace=True)
        df.to_csv(self.destination_folder + "/concatenated_data.csv", index=False)

        return df

    def move_files(self):
        files = os.listdir(self.files_location)

        for f in files:
            if f.endswith(".zip"):
                shutil.move(self.files_location + "/" + f, self.destination_folder)

    def unzip(self, zip_file_name):
        # fonction qui dézippe les fichiers téléchargés
        # vérifie si le fichier existe, sinon renvoie une erreur

        file = self.destination_folder + "/" + zip_file_name

        if os.path.isfile(file):
            print("Extraction du fichier " + zip_file_name)
            myZip = zipfile.ZipFile(file)
            myZip.extractall(self.destination_folder)
        else:
            print("The zipped file you want to extract doesn't exist there")

    def clean_files(self, file_name):

        # Nettoie les fichiers csv pour qu'ils soient lisibles par la suite

        with open(file_name, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('*', ';').replace("/", "").replace("nomprenom", "nom; prenom").replace("\"", "").replace(";;", ";\"\";")

        # Write the file out again
        with open(file_name, 'w') as file:
            file.write(filedata)

    def inject_to_database(self, df):

        # Réalise la connexion avec la base de donnée
        db_connection_url = 'postgresql://postgres:admin@localhost/decesFrance'
        engine = create_engine(db_connection_url)

        # Injecte les données
        df.to_sql("data", engine, if_exists='append', index=False)
