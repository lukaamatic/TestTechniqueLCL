# Fichier contenant les fonctions permettant de la data visualisation

import matplotlib.pyplot as plt
import pandas


def data_vis(df):
    # opérations sur le dataframe pour réaliser des statistiques sur les données

    df["year_of_death"] = df["datedeces"].dt.year
    print(df.head())

    # calcul du nombre de décès par an
    df["death_per_year"] = df['datedeces'].groupby([df.year_of_death]).agg('count')

    # Calcul de l'esperance de vie moyenne chaque année
    df["age"] = df.year_of_death - df["datenaiss"].dt.year
    df.age_average = df['age'].groupby([df.datedeces.dt.year]).mean()

    print(df.head())

    return df


def plot_and_save(df):

    # créé le graphique concernant le nombre de décès par année
    df.plot(x='year_of_death', y='death_per_year', kind='scatter')
    plt.show()
    plt.savefig('../flask/static/death_per_year.png')  # sauvegarde le graphique dans un fichier

    # créé le graphique concernant l'age moyen des personnes décédées par année
    df.plot(x='year_of_death', y='age_average', kind='bar')
    plt.show()
    plt.savefig('../flask/static/age_average.png')  # sauvegarde le graphique dans un fichier


