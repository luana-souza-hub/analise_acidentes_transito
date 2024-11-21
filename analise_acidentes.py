import pandas as pd

# Carregar os arquivos CSV
file_paths = {
    "2021": "2021.csv",
    "2022": "2022.csv",
    "2023": "2023.csv",
    "2024": "2024.csv"
}

# Função para detectar o delimitador mais provável
def detect_delimiter(file_path, encoding='latin1', num_lines=5):
    delimiters = [',', ';', '\t', '|']
    delimiter_count = {d: 0 for d in delimiters}
    with open(file_path, 'r', encoding=encoding) as file:
        sample = [next(file) for _ in range(num_lines)]
        for line in sample:
            for d in delimiters:
                delimiter_count[d] += line.count(d)
    return max(delimiter_count, key=delimiter_count.get)

# Função para carregar e tratar cada arquivo CSV
def load_and_clean_csv(file_path):
    detected_delimiter = detect_delimiter(file_path)
    try:
        df = pd.read_csv(file_path, encoding='latin1', sep=detected_delimiter, on_bad_lines='warn')
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo {file_path}: {e}")
        return None

# Carregar e consolidar os dados
def load_data():
    dataframes = [load_and_clean_csv(file_paths[year]) for year in file_paths]
    dataframes = [df for df in dataframes if df is not None]
    if len(dataframes) == 0:
        raise ValueError("Nenhum DataFrame foi carregado. Verifique os arquivos CSV.")
    all_data = pd.concat(dataframes, ignore_index=True)
    
    # Tratamento de valores ausentes
    categorical_columns = all_data.select_dtypes(include='object').columns
    for col in categorical_columns:
        all_data[col].fillna(all_data[col].mode()[0], inplace=True)
    
    # Remoção de duplicatas
    all_data.drop_duplicates(inplace=True)
    
    # Conversão de colunas importantes
    if 'data_inversa' in all_data.columns:
        all_data['data_inversa'] = pd.to_datetime(all_data['data_inversa'], errors='coerce')
    
    # Adicionar coluna de ano (caso ainda não exista)
    if 'ano' not in all_data.columns:
        if all_data['data_inversa'].dtype == 'datetime64[ns]':
            all_data['ano'] = all_data['data_inversa'].dt.year
    
    return all_data

if __name__ == "__main__":
    all_data = load_data()
    print("Dados carregados e tratados com sucesso.")