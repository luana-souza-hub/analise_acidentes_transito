import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# Configuração da página Streamlit
st.set_page_config(page_title="Análise de Acidentes de Trânsito", layout="wide")

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
        st.warning(f"Erro ao carregar o arquivo {file_path}: {e}")
        return None

# Carregar e consolidar os dados
@st.cache_data
def load_data():
    dataframes = [load_and_clean_csv(file_paths[year]) for year in file_paths]
    dataframes = [df for df in dataframes if df is not None]
    if len(dataframes) == 0:
        st.error("Nenhum DataFrame foi carregado. Verifique os arquivos CSV.")
        return None
    all_data = pd.concat(dataframes, ignore_index=True)
    
    # Tratamento de valores ausentes
    categorical_columns = all_data.select_dtypes(include='object').columns
    for col in categorical_columns:
        all_data.loc[:, col] = all_data[col].fillna(all_data[col].mode()[0])
    
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

# Carregar dados
all_data = load_data()

if all_data is not None:
    # Aplicação Streamlit
    st.title("Análise de Acidentes de Trânsito")

    # Filtros Interativos
    st.sidebar.header("Filtros")
    anos_disponiveis = sorted(all_data['ano'].dropna().unique())
    anos_selecionados = st.sidebar.multiselect("Selecione o(s) ano(s):", options=anos_disponiveis, default=anos_disponiveis)

    # Aplicar filtro de ano
    dados_filtrados = all_data[all_data['ano'].isin(anos_selecionados)]

    # Renomear colunas para nomes mais amigáveis
    colunas_renomeadas = {
        'data_inversa': 'Data do Acidente',
        'dia_semana': 'Dia da Semana',
        'horario': 'Horário',
        'uf': 'Estado',
        'br': 'BR',
        'km': 'Quilômetro',
        'municipio': 'Município',
        'causa_acidente': 'Causa do Acidente',
        'tipo_acidente': 'Tipo de Acidente',
        'classificacao_acidente': 'Classificação do Acidente',
        'fase_dia': 'Fase do Dia',
        'sentido_via': 'Sentido da Via',
        'condicao_metereologica': 'Condição Meteorológica',
        'tipo_pista': 'Tipo de Pista',
        'tracado_via': 'Traçado da Via',
        'uso_solo': 'Uso do Solo',
        'pessoas': 'Número de Pessoas Envolvidas',
        'mortos': 'Número de Mortos',
        'feridos_leves': 'Número de Feridos Leves',
        'feridos_graves': 'Número de Feridos Graves',
        'ilesos': 'Número de Ilesos',
        'veiculos': 'Número de Veículos Envolvidos',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'ano': 'Ano'
    }

    # Aplicar o renomeamento ao conjunto de dados filtrado
    dados_filtrados_renomeados = dados_filtrados.rename(columns=colunas_renomeadas)

    # Formatar a coluna 'Data do Acidente' para melhor visualização
    if 'Data do Acidente' in dados_filtrados_renomeados.columns:
        dados_filtrados_renomeados['Data do Acidente'] = pd.to_datetime(dados_filtrados_renomeados['Data do Acidente'], errors='coerce').dt.strftime('%d/%m/%Y')

    # Exibir dados básicos
    st.subheader("Conjunto de Dados Filtrado")
    st.write(dados_filtrados_renomeados.head())

    # Estatísticas descritivas
    st.subheader("Estatísticas Descritivas dos Dados Filtrados")
    
    # Função para calcular estatísticas da data
    def calculate_date_stats(df):
        if 'Data do Acidente' not in df.columns:
            return pd.DataFrame()
        
        dates = pd.to_datetime(df['Data do Acidente'], errors='coerce')
        date_stats = pd.DataFrame({
            'Contagem': [dates.count()],
            'Primeira Data': [dates.min().strftime('%d/%m/%Y') if not pd.isnull(dates.min()) else 'N/A'],
            'Última Data': [dates.max().strftime('%d/%m/%Y') if not pd.isnull(dates.max()) else 'N/A'],
            'Período (dias)': [(dates.max() - dates.min()).days if not pd.isnull(dates.min()) and not pd.isnull(dates.max()) else 'N/A']
        })
        return date_stats

    # Calcular estatísticas numéricas
    numeric_stats = dados_filtrados_renomeados.describe()
    
    # Calcular estatísticas da data
    date_stats = calculate_date_stats(dados_filtrados_renomeados)

    # Exibir estatísticas numéricas
    st.write("Estatísticas Numéricas:")
    st.write(numeric_stats)

    # Exibir estatísticas da data
    st.write("Estatísticas da Data do Acidente:")
    st.write(date_stats)

    # 1. Tendência de Acidentes ao Longo do Tempo
    st.subheader("Tendência de Acidentes ao Longo do Tempo")

    if 'Data do Acidente' in dados_filtrados_renomeados.columns:
        acidentes_por_dia = dados_filtrados_renomeados.groupby('Data do Acidente').size().reset_index(name='count')
        fig = px.line(acidentes_por_dia, x='Data do Acidente', y='count',
                      title="Número de Acidentes por Dia",
                      labels={'Data do Acidente': 'Data', 'count': 'Número de Acidentes'})
        st.plotly_chart(fig)
    else:
        st.warning("Dados de data não disponíveis para análise de tendência.")

    # 2. Distribuição de acidentes por dia da semana
    st.subheader("Distribuição de Acidentes por Dia da Semana")
    st.markdown("Este gráfico mostra a distribuição dos acidentes ao longo dos dias da semana. É possível identificar padrões como um aumento no número de acidentes em certos dias, que podem estar relacionados a comportamentos típicos, como maior tráfego ou eventos sociais.")
    if 'Dia da Semana' in dados_filtrados_renomeados.columns:
        contagem_dia_semana = dados_filtrados_renomeados['Dia da Semana'].value_counts().reset_index()
        contagem_dia_semana.columns = ['Dia da Semana', 'count']
        fig = px.bar(contagem_dia_semana, x='Dia da Semana', y='count',
                     title="Distribuição de Acidentes por Dia da Semana")
        st.plotly_chart(fig)
    else:
        st.warning("Dados de dia da semana não disponíveis.")

    # 3. Top 5 causas de acidentes
    st.subheader("Top 5 Causas de Acidentes")
    st.markdown("Este gráfico apresenta as cinco principais causas de acidentes. Esta análise é fundamental para priorizar campanhas de conscientização e políticas públicas visando reduzir as causas mais comuns de acidentes.")
    if 'Causa do Acidente' in dados_filtrados_renomeados.columns:
        top_5_causas = dados_filtrados_renomeados['Causa do Acidente'].value_counts().head(5).reset_index()
        top_5_causas.columns = ['Causa do Acidente', 'count']
        fig = px.bar(top_5_causas, x='Causa do Acidente', y='count',
                     title="Top 5 Causas de Acidentes")
        st.plotly_chart(fig)
    else:
        st.warning("Dados de causa de acidente não disponíveis.")

    # 4. Top 5 tipos mais comuns de acidentes
    st.subheader("Top 5 Tipos Mais Comuns de Acidentes")
    st.markdown("Este gráfico mostra os tipos de acidentes que mais ocorrem. Compreender os tipos mais comuns pode ajudar na formulação de estratégias de segurança viária e infraestrutura para mitigar esses acidentes.")
    if 'Tipo de Acidente' in dados_filtrados_renomeados.columns:
        top_5_tipos = dados_filtrados_renomeados['Tipo de Acidente'].value_counts().head(5).reset_index()
        top_5_tipos.columns = ['Tipo de Acidente', 'count']
        fig = px.bar(top_5_tipos, x='Tipo de Acidente', y='count',
                     title="Top 5 Tipos de Acidentes")
        st.plotly_chart(fig)
    else:
        st.warning("Dados de tipo de acidente não disponíveis.")

    # 5. Mapa interativo: Distribuição geográfica dos acidentes
    st.subheader("Distribuição Geográfica dos Acidentes")
    st.markdown("Este mapa mostra a distribuição geográfica dos acidentes registrados. Cada ponto representa a localização de um acidente, permitindo identificar áreas críticas que demandam maior atenção.")
    if 'Latitude' in dados_filtrados_renomeados.columns and 'Longitude' in dados_filtrados_renomeados.columns:
        # Converter latitude e longitude para valores numéricos
        dados_filtrados_renomeados['Latitude'] = pd.to_numeric(dados_filtrados_renomeados['Latitude'], errors='coerce')
        dados_filtrados_renomeados['Longitude'] = pd.to_numeric(dados_filtrados_renomeados['Longitude'], errors='coerce')

        # Remover linhas com valores NaN em latitude ou longitude
        geo_data = dados_filtrados_renomeados.dropna(subset=['Latitude', 'Longitude'])

        # Renomear as colunas para o formato que o Streamlit espera
        geo_data = geo_data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

        # Criar o mapa interativo se houver dados suficientes
        if not geo_data.empty:
            st.map(geo_data)
        else:
            st.warning("Não há dados geográficos válidos para criar o mapa.")
    else:
        st.warning("Os dados de latitude e longitude não estão disponíveis para criar um mapa interativo.")

    # 6. Gráfico de dispersão interativo: Relação entre número de vítimas e condições do tempo
    st.subheader("Relação entre Número de Vítimas e Condições do Tempo")
    st.markdown("Este gráfico de dispersão mostra como as condições meteorológicas influenciam o número de vítimas fatais nos acidentes. A análise pode revelar se certas condições climáticas, como chuva ou neblina, aumentam o risco de mortes em acidentes.")
    if 'Condição Meteorológica' in dados_filtrados_renomeados.columns and 'Número de Mortos' in dados_filtrados_renomeados.columns:
        fig = px.scatter(dados_filtrados_renomeados, x='Condição Meteorológica', y='Número de Mortos',
                         title="Relação entre Condições do Tempo e Número de Mortes")
        st.plotly_chart(fig)
    else:
        st.warning("Os dados de condições meteorológicas e/ou número de mortes não estão disponíveis para criar o gráfico de dispersão.")

    # 7. Distribuição de acidentes por ano
    st.subheader("Distribuição de Acidentes por Ano")
    st.markdown("Este gráfico mostra a quantidade de acidentes que ocorreram em cada ano, permitindo visualizar possíveis tendências de aumento ou diminuição ao longo dos anos.")
    if 'Ano' in dados_filtrados_renomeados.columns:
        contagem_ano = dados_filtrados_renomeados['Ano'].value_counts().sort_index().reset_index()
        contagem_ano.columns = ['Ano', 'count']
        fig = px.bar(contagem_ano, x='Ano', y='count',
                     title="Distribuição de Acidentes por Ano",
                     labels={'Ano': 'Ano', 'count': 'Número de Acidentes'})
        st.plotly_chart(fig)
    else:
        st.warning("Os dados de ano não estão disponíveis para criar o gráfico de distribuição por ano.")