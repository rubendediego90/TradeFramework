from backtesting.lib import plot_heatmaps
import os
from datetime import datetime
import re
import shutil

class Optimizer:
    path = ""
    
    def __init__(self, bt,symbol_casted,name_strategy,plot_heatmap=True,text=""):
        self.bt = bt
        self.path = self.get_path()
        self.symbol_casted = symbol_casted
        self.name_strategy = name_strategy
        self.plot_heatmap = plot_heatmap
        self.text = text
        
    def optimizeFunc(self, series):
        if series['# Trades'] < 10:
            return -1 #
        '''

        if series['Win Rate [%]'] < 60:
            return -1 #
        '''
        return series["Profit Factor"]

    def run(self):
            '''
        stats_op = bt.optimize(
            sma_quick_data=range(1,299,1),
            sma_slow_data=range(2,300,1),
            stop_loss=[0.9, 0.93, 0.95],
            maximize=optimizeFunc
        )
        '''

            stats, heatmap = self.bt.optimize(
                #sma_quick_data=range(280,310,1),
                #sma_slow_data=range(120,150,1),
                sma_quick_data=range(1,299,1),
                sma_slow_data=range(2,300,1),
                stop_loss=[0.9, 0.93, 0.95],
                maximize=self.optimizeFunc,
                #maximize='Return [%]',
                return_heatmap=True
            )

            heatmap_reset = heatmap.reset_index()

            # Si alguna columna no tiene nombre, asignamos nombres manualmente
            heatmap_reset.columns = ['sma_quick_data', 'sma_slow_data', 'stop_loss', 'Profit Factor']
            heatmap_reset = heatmap_reset.sort_values(by='Profit Factor', ascending=False)

            # Guardar el DataFrame en un archivo CSV sin el índice original
            #heatmap_reset.to_csv('mi_data.csv', index=False)
            
            # print('Resultados de la optimización:', stats_op)
            
            #result = stats_op["_strategy"]
            # print('resultado optimizacion',result)
            #stats['_trades'] 
            #print('_trades',stats_op["_trades"])
            '''optimizar'''
            
            '''Crear la carperta'''
            folder_name = self.set_folder_name(self.path)
            self.create_folder(folder_name,self.path)
            
            '''Añadir text con las notas'''
            if(self.text):
                self.create_txt(f"{self.path}/{folder_name}/readme.txt",self.text)
            
            '''guardar el mapa de calor'''
            if(self.plot_heatmap):
                self.print_heatmap(heatmap,f"{self.path}/{folder_name}")
            
            '''csv con las n mas rentable'''
            
            '''cvs para cada una de las n mas rentables con sus operaciones'''
            
            '''-grafico de fecha en las x inicio y fin en una linea. Precio del activo en las y'''
            
    def get_folder_names(self,path):
    # Obtener una lista de directorios (carpetas) dentro de la ruta dada
        return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    
    def filter_by_base(self,input_list, base_string):
        # Filtramos las cadenas que empiezan con base_string y terminan con '_N' seguido de un número
        filtered = [s for s in input_list if s.startswith(base_string) and '_N' in s]
        
        return filtered

    def get_highest_number(self,filtered_list):
        # Extraemos el número después de 'N' y encontramos el más alto
        numbers = []
        for s in filtered_list:
            # Buscamos el número después de '_N'
            match = re.search(r'_N(\d+)', s)
            if match:
                numbers.append(int(match.group(1)))  # Añadimos el número encontrado
        
        return max(numbers) if numbers else 0  # Devolvemos el número máximo

    def set_folder_name(self,path):
        #ORO_2025_03_26_SMA_N1
        today = datetime.today()
        formatted_date = today.strftime('%Y_%m_%d')
        
        initial = f"{self.symbol_casted}_{formatted_date}_{self.name_strategy}"
        n_value = self.get_version_folder(initial,path)
        
        return f"{initial}_N{n_value+1}"
    
    def get_version_folder(self,base_string,path):
        folders_list = self.get_folder_names(path)
        filtered_list = self.filter_by_base(folders_list, base_string)

        # Obtener el número más alto de las cadenas filtradas
        return self.get_highest_number(filtered_list)
        
    def get_path(self):
        current_directory = os.getcwd()
        destination_folder_path = os.path.join(current_directory, 'testing', 'optimize')
        return destination_folder_path
        
    def export_csv(path,file_name,data):
        # Crear la ruta completa del archivo CSV
        full_path = f"{path}/{file_name}.csv"
        data.to_csv(full_path, index=False)
        
    def print_heatmap(self,heatmap,path):
        plot_heatmaps(heatmap)
        self.move_most_recent_html(path,"MapaCalor.html")
        
    def create_folder(self,folder_name,path):
        full_path = os.path.join(path, folder_name)

        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Folder '{folder_name}' created at {full_path}")
        else:
            print(f"The folder '{folder_name}' already exists at {full_path}")
    
    def create_txt(self,path,text):
        with open(path, "w") as file:
            file.write(text)
            
    def move_most_recent_html(self, target_dir, new_name):
        # Ruta del directorio temporal donde se guardan los archivos temporales
        temp_dir = r"C:\Users\Rubén de Diego\AppData\Local\Temp"
        
        # Buscar todos los archivos .html en la carpeta temporal
        html_files = [f for f in os.listdir(temp_dir) if f.endswith('.html')]
        
        if not html_files:
            print("No se encontraron archivos .html en la carpeta temporal.")
            return
        
        # Obtener la ruta completa de los archivos .html
        html_file_paths = [os.path.join(temp_dir, f) for f in html_files]
        
        # Obtener el archivo más reciente (basado en la fecha de modificación)
        most_recent_file = max(html_file_paths, key=os.path.getmtime)
        
        # Crear la nueva ruta de destino con el nuevo nombre
        new_file_path = os.path.join(target_dir, new_name)
        
        # Mover el archivo más reciente a la ruta de destino con el nuevo nombre
        shutil.copy(most_recent_file, new_file_path)
        
        print(f"El archivo {most_recent_file} ha sido copiado y renombrado a: {new_file_path}")



