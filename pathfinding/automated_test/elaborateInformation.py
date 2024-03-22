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

        self.df = self.df.dropna()
        self.df.drop(columns=['initNewAgent'], inplace=True)
        self.df.drop(columns=['goalNewAgent'], inplace=True)

        # # self.plot_grouped_graphs(self.df)
        self.plot_row_col(self.df)
        self.plot_agents(self.df)
        self.plot_max_length_new_agent(self.df)
        # self.plot_grouped_agents_graphs(self.df)
        # self.plot_grouped_limit_len_ex_graphs(self.df)

        # # self.analyze_by_type(self.df)
        # # self.analyze_by_type_and_parameters(self.df)
        # # self.compare_instances_across_types(self.df)

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

    
    def plot_row_col(self, df):
        # Raggruppamento dei dati per tipo, righe e colonne e calcolo della media
        grouped_df = df.groupby(['type', 'row', 'col']).mean().reset_index()

        # Creazione dei grafici
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Definisci una griglia di subplot con 1 riga e 2 colonne

        # Grafico per il tempo di esecuzione
        sns.lineplot(x='row', y='executionTime', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[0])
        axes[0].set_xlabel('Dimensioni della griglia (NROWS o NCOLS)')
        axes[0].set_ylabel('Tempo di esecuzione (secondi)')
        axes[0].set_title('Tempo di esecuzione rispetto alle dimensioni della griglia')
        axes[0].grid(True)

        # Grafico per il picco di memoria
        sns.lineplot(x='row', y='peakMemory', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[1])
        axes[1].set_xlabel('Dimensioni della griglia (NROWS o NCOLS)')
        axes[1].set_ylabel('Picco di memoria (KB)')
        axes[1].set_title('Picco di memoria rispetto alle dimensioni della griglia')
        axes[1].grid(True)

        plt.tight_layout()
        plt.show()

    def plot_agents(self, df):
        # Raggruppamento dei dati per tipo, righe e colonne e calcolo della media
        grouped_df = df.groupby(['type', 'nAgents']).mean().reset_index()

        # Creazione dei grafici
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Definisci una griglia di subplot con 1 riga e 2 colonne

        # Grafico per il tempo di esecuzione
        sns.lineplot(x='nAgents', y='executionTime', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[0])
        axes[0].set_xlabel('Numero di agenti')
        axes[0].set_ylabel('Tempo di esecuzione (secondi)')
        axes[0].set_title('Tempo di esecuzione rispetto al numero di agenti')
        axes[0].grid(True)

        # Grafico per il picco di memoria
        sns.lineplot(x='nAgents', y='peakMemory', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[1])
        axes[1].set_xlabel('Numero di agenti')
        axes[1].set_ylabel('Picco di memoria (KB)')
        axes[1].set_title('Picco di memoria rispetto al numero di agenti')
        axes[1].grid(True)

        plt.tight_layout()
        plt.show()
        
    def plot_max_length_new_agent(self, df):
        # Raggruppamento dei dati per tipo, righe e colonne e calcolo della media
        grouped_df = df.groupby(['type', 'maxLengthNewAgent']).mean().reset_index()

        # Creazione dei grafici
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Definisci una griglia di subplot con 1 riga e 2 colonne

        # Grafico per il tempo di esecuzione
        sns.lineplot(x='maxLengthNewAgent', y='executionTime', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[0])
        axes[0].set_xlabel('Massima lunghezza per il nuovo agente')
        axes[0].set_ylabel('Tempo di esecuzione (secondi)')
        axes[0].set_title('Tempo di esecuzione rispetto alla massima lunghezza per il nuovo agente')
        axes[0].grid(True)

        # Grafico per il picco di memoria
        sns.lineplot(x='maxLengthNewAgent', y='peakMemory', hue='type', data=grouped_df, palette='colorblind', legend='full', ax=axes[1])
        axes[1].set_xlabel('Massima lunghezza per il nuovo agente')
        axes[1].set_ylabel('Picco di memoria (KB)')
        axes[1].set_title('Picco di memoria rispetto alla massima lunghezza per il nuovo agente')
        axes[1].grid(True)

        plt.tight_layout()
        plt.show()

    def plot_grouped_agents_graphs(self, df):

        grouped_df = df.groupby(['type','row', 'col', 'freeCellRatio', 'agglomerationFactor', 'nAgents']).mean().reset_index()
        
        # Creazione dei grafici
        for name, group in grouped_df.groupby(['row', 'col', 'freeCellRatio', 'agglomerationFactor']):
            fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Definisci una griglia di subplot con 1 riga e 2 colonne

            # Grafico per il tempo di esecuzione
            sns.lineplot(x='nAgents', y='executionTime', hue='type', data=group, palette='colorblind', legend='full', ax=axes[0])
            axes[0].set_title(f'Tempo di esecuzione - row={name[0]}, col={name[1]}')
            axes[0].set_xlabel('Numero di agenti')
            axes[0].set_ylabel('Tempo di esecuzione [secondi]')
            axes[0].grid(True)

            # Grafico per il picco di memoria
            sns.lineplot(x='nAgents', y='peakMemory', hue='type', data=group, palette='colorblind', legend='full', ax=axes[1])
            axes[1].set_title(f'Picco di memoria - row={name[0]}, col={name[1]}')
            axes[1].set_xlabel('Numero di agenti')
            axes[1].set_ylabel('Picco di memoria [KB]')
            axes[1].grid(True)

            plt.tight_layout()
            plt.show()

    def plot_grouped_limit_len_ex_graphs(self, df):

        grouped_df = df.groupby(['type','row', 'col', 'freeCellRatio', 'agglomerationFactor', 'limitLengthExistingPaths']).mean().reset_index()
        
        # Creazione dei grafici
        for name, group in grouped_df.groupby(['row', 'col', 'freeCellRatio', 'agglomerationFactor']):
            fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # Definisci una griglia di subplot con 1 riga e 2 colonne

            # Grafico per il tempo di esecuzione
            sns.lineplot(x='limitLengthExistingPaths', y='executionTime', hue='type', data=group, palette='colorblind', legend='full', ax=axes[0])
            axes[0].set_title(f'Tempo di esecuzione - row={name[0]}, col={name[1]}')
            axes[0].set_xlabel('Lunghezza percorsi Preesistenti')
            axes[0].set_ylabel('Tempo di esecuzione [secondi]')
            axes[0].grid(True)

            # Grafico per il picco di memoria
            sns.lineplot(x='limitLengthExistingPaths', y='peakMemory', hue='type', data=group, palette='colorblind', legend='full', ax=axes[1])
            axes[1].set_title(f'Picco di memoria - row={name[0]}, col={name[1]}')
            axes[1].set_xlabel('Lunghezza percorsi Preesistenti')
            axes[1].set_ylabel('Picco di memoria [KB]')
            axes[1].grid(True)

            plt.tight_layout()
            plt.show()
            

    def plot_grouped_graphs(self, df):

        # Raggruppa il DataFrame per righe e colonne uguali
        grouped_df = df.groupby(['type','row', 'col', 'freeCellRatio', 'agglomerationFactor', 'nAgents', 'limitLengthExistingPaths', 'maxLengthNewAgent']).mean().reset_index()
        
        # Creazione dei grafici
        for name, group in grouped_df.groupby(['row', 'col', 'freeCellRatio', 'agglomerationFactor']):
            fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))

            # Grafico per il numero di agenti
            sns.lineplot(x='nAgents', y='executionTime', hue='type', data=group, ax=axes[0, 0])
            axes[0, 0].set_title('Numero di agenti - Tempo di esecuzione')
            axes[0, 0].set_xlabel('Numero di agenti')
            axes[0, 0].set_ylabel('Tempo di esecuzione')

            sns.lineplot(x='nAgents', y='peakMemory', hue='type', data=group, ax=axes[1, 0])
            axes[1, 0].set_title('Numero di agenti - Picco di memoria')
            axes[1, 0].set_xlabel('Numero di agenti')
            axes[1, 0].set_ylabel('Picco di memoria')

            # Grafico per limitLengthExistingPaths
            sns.lineplot(x='limitLengthExistingPaths', y='executionTime', hue='type', data=group, ax=axes[0, 2])
            axes[0, 2].set_title('LimitLengthExistingPaths - Tempo di esecuzione')
            axes[0, 2].set_xlabel('LimitLengthExistingPaths')
            axes[0, 2].set_ylabel('Tempo di esecuzione')

            sns.lineplot(x='limitLengthExistingPaths', y='peakMemory', hue='type', data=group, ax=axes[1, 2])
            axes[1, 2].set_title('LimitLengthExistingPaths - Picco di memoria')
            axes[1, 2].set_xlabel('LimitLengthExistingPaths')
            axes[1, 2].set_ylabel('Picco di memoria')

            plt.tight_layout()
            plt.title(f'Grafici per row={name[0]}, col={name[1]}')
            # plt.suptitle(f'Grafici per row={name[0]}, col={name[1]}', y=1.05)
            plt.show()
            

    def printData(self):
        print(self.df)

    def saveDataToFile(self):
        filePath = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output", "data.csv")
        self.df.to_csv(filePath, index=False)
    
    def loadDataFromFile(self):
        filePath = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output", "data.csv")
        self.df = pd.read_csv(filePath)
