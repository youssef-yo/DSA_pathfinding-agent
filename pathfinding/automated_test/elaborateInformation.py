import pandas as pd
import os
import pathlib
import matplotlib.pyplot as plt
import seaborn as sns

class ElaborateInformation:

    def __init__(self, data):
        self.df = pd.DataFrame(data)


    def elaborateData(self):
        self.df.drop('seed', axis=1, inplace=True)

        print("Informazioni generali sul dataset:")
        print(self.df.info())
        print("\n")

        self.analyze_by_type(self.df)
        # self.analyze_by_type_and_parameters(self.df)
        self.compare_instances_across_types(self.df)

    def analyze_by_type(self, df):
        types = df['type'].unique()
        for t in types:
            type_df = df[df['type'] == t]

            # Numero di istanze risolte
            instances_solved = type_df[(type_df['initNewAgent'].notnull()) & (type_df['goalNewAgent'].notnull())]
            num_instances_solved = len(instances_solved)

            # Tempo medio, massimo e minimo
            avg_execution_time = type_df['executionTime'].mean()
            max_execution_time = type_df['executionTime'].max()
            min_execution_time = type_df['executionTime'].min()

            # Spazio medio, massimo e minimo
            avg_peak_memory = type_df['peakMemory'].mean()
            max_peak_memory = type_df['peakMemory'].max()
            min_peak_memory = type_df['peakMemory'].min()

            # Stampa dei risultati per il tipo corrente
            print(f"Tipo: {t}")
            print(f"Numero di istanze risolte: {num_instances_solved}")
            print(f"Tempo medio di esecuzione: {avg_execution_time:.2f} sec (max: {max_execution_time:.2f} sec, min: {min_execution_time:.2f} sec)")
            print(f"Spazio medio di memoria: {avg_peak_memory:.2f} KB (max: {max_peak_memory:.2f} KB, min: {min_peak_memory:.2f} KB)")
            print("\n")
    
    def analyze_by_type_and_parameters(self, df):
        # Creiamo un dizionario per contenere i nomi dei parametri e le loro colonne corrispondenti nel DataFrame
        parameter_columns = {
            'Dimensione della griglia': ['row', 'col'],
            'Percentuale di celle attraversabili': ['freeCellRatio'],
            'Numero di agenti preesistenti': ['nAgents'],
            'Lunghezza dei percorsi degli agenti preesistenti': ['pathLength'],
            'Valore dell’orizzonte temporale max': ['maxLengthNewAgent']
        }

        # Filtriamo il DataFrame per ciascun tipo
        types = df['type'].unique()
        for t in types:
            type_df = df[df['type'] == t]
            print(f"Tipo: {t}")

            # Analizziamo i parametri per questo tipo
            for parameter, columns in parameter_columns.items():
                print(f"\nAnalisi per il parametro: {parameter}")

                # Plot del tempo medio di esecuzione per ciascuna colonna associata al parametro
                plt.figure(figsize=(12, 5))
                for col in columns:
                    mean_execution_time = type_df.groupby(col)['executionTime'].mean()
                    plt.plot(mean_execution_time, marker='o', label=col)
                plt.title(f"{parameter} vs Tempo di esecuzione medio")
                plt.xlabel(parameter)
                plt.ylabel("Tempo di esecuzione medio")
                plt.legend()
                plt.show()

                # Plot del picco di memoria per ciascuna colonna associata al parametro
                plt.figure(figsize=(12, 5))
                for col in columns:
                    mean_peak_memory = type_df.groupby(col)['peakMemory'].mean()
                    plt.plot(mean_peak_memory, marker='o', label=col)
                plt.title(f"{parameter} vs Picco di memoria medio")
                plt.xlabel(parameter)
                plt.ylabel("Picco di memoria medio")
                plt.legend()
                plt.show()

    def compare_instances_across_types(self, df):
        # Troviamo le istanze con valori comuni
        common_instances = df.groupby(['row', 'col', 'nAgents', 'agglomerationFactor', 'freeCellRatio', 'maxLengthNewAgent']).groups.values()

        # Per ogni istanza comune, confrontiamo i quattro tipi
        for instance_indices in common_instances:
            print("---------------------------------------------------------------------")
            print("Istanza con valori comuni:")

            # Creiamo un DataFrame contenente solo le istanze corrispondenti agli indici specificati
            common_instance_df = df.loc[instance_indices]

            # Troviamo il tipo che richiede più e meno memoria
            max_memory_type = common_instance_df.loc[common_instance_df['peakMemory'].idxmax()]['type']
            min_memory_type = common_instance_df.loc[common_instance_df['peakMemory'].idxmin()]['type']

            # Troviamo il tipo che richiede più e meno tempo di esecuzione
            max_time_type = common_instance_df.loc[common_instance_df['executionTime'].idxmax()]['type']
            min_time_type = common_instance_df.loc[common_instance_df['executionTime'].idxmin()]['type']

            # Stampiamo i risultati per l'istanza corrente
            print(f"Tipo che richiede più memoria: {max_memory_type}")
            print(f"Tipo che richiede meno memoria: {min_memory_type}")
            print(f"Tipo che richiede più tempo di esecuzione: {max_time_type}")
            print(f"Tipo che richiede meno tempo di esecuzione: {min_time_type}")
            print("\n")



    

    def printData(self):
        print(self.df)

    def saveDataToFile(self):
        filePath = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output", "data.csv")
        self.df.to_csv(filePath, index=False)
    
    def loadDataFromFile(self):
        filePath = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output", "data.csv")
        self.df = pd.read_csv(filePath)
