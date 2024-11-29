import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar os dados limpos do backend
@st.cache_data
def load_data():
    data = pd.read_csv("accidents_cleaned.csv")
    return data

# Configuração da página Streamlit
st.set_page_config(page_title="Análise de Acidentes de Trânsito", layout="wide")

# Título da Aplicação
st.title("Análise Interativa de Acidentes de Trânsito no Brasil")

# Carregar dados
try:
    all_data = load_data()
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado. Execute o backend para gerar 'accidents_cleaned.csv'.")
    st.stop()

# Explicação da Aplicação
st.markdown("""
Esta aplicação fornece uma análise interativa dos acidentes de trânsito no Brasil. Utilize os filtros na barra lateral para selecionar os anos de interesse e explore as visualizações que mostram as causas mais comuns dos acidentes, a distribuição geográfica e outros detalhes relevantes.
""")

# Filtros
anos_disponiveis = sorted(all_data['ano'].dropna().unique())
anos_selecionados = st.sidebar.multiselect("Selecione o(s) ano(s):", options=anos_disponiveis, default=anos_disponiveis)

# Filtrar os dados pelo ano selecionado
dados_filtrados = all_data[all_data['ano'].isin(anos_selecionados)]

# Mostrar conjunto de dados filtrado
st.subheader("Conjunto de Dados Filtrado")
st.dataframe(dados_filtrados.rename(columns={
    'data_inversa': 'Data do Acidente',
    'dia_semana': 'Dia da Semana',
    'causa_acidente': 'Causa do Acidente',
    'feridos': 'Número de Feridos',
    'ano': 'Ano'
}))

# Explicação dos Dados Filtrados
st.markdown("""
O conjunto de dados filtrado mostra informações detalhadas sobre os acidentes de trânsito, incluindo a data do acidente, dia da semana, causa do acidente, número de feridos e o ano. Use esta tabela para explorar detalhes específicos dos acidentes ocorridos nos anos selecionados.
""")

# Estatísticas descritivas dos dados filtrados
st.subheader("Estatísticas Descritivas dos Dados Filtrados")
st.write(dados_filtrados.describe().rename(index={
    'count': 'Contagem',
    'mean': 'Média',
    'std': 'Desvio Padrão',
    'min': 'Valor Mínimo',
    '25%': '1º Quartil',
    '50%': 'Mediana',
    '75%': '3º Quartil',
    'max': 'Valor Máximo'
}))

# Explicação das Estatísticas Descritivas
st.markdown("""
As estatísticas descritivas fornecem um resumo dos dados, incluindo a contagem de registros, média, desvio padrão, valores mínimos e máximos, além dos quartis. Isso ajuda a entender melhor a distribuição e a variabilidade dos acidentes.
""")

# Distribuição de acidentes por dia da semana
if 'dia_semana' in dados_filtrados.columns:
    contagem_dia_semana = dados_filtrados['dia_semana'].value_counts().reset_index()
    contagem_dia_semana.columns = ['Dia da Semana', 'Número de Acidentes']
    fig = px.bar(contagem_dia_semana, x='Dia da Semana', y='Número de Acidentes',
                 title="Distribuição de Acidentes por Dia da Semana",
                 labels={'Dia da Semana': 'Dia da Semana', 'Número de Acidentes': 'Número de Acidentes'})
    st.plotly_chart(fig)
    
    # Explicação do Gráfico de Distribuição por Dia da Semana
    st.markdown("""
    Este gráfico mostra a distribuição dos acidentes de trânsito ao longo dos dias da semana. Ele ajuda a identificar quais dias são mais propensos a acidentes, permitindo uma análise mais aprofundada sobre possíveis causas.
    """)

# Gráfico de barras: Top 5 causas mais comuns dos acidentes
if 'causa_acidente' in dados_filtrados.columns:
    top5_causas = dados_filtrados['causa_acidente'].value_counts().nlargest(5).reset_index()
    top5_causas.columns = ['Causa', 'Quantidade']
    fig_causas = px.bar(top5_causas, x='Causa', y='Quantidade',
                        title="Top 5 Causas Mais Comuns dos Acidentes",
                        labels={'Causa': 'Causa do Acidente', 'Quantidade': 'Número de Ocorrências'})
    st.plotly_chart(fig_causas)
    
    # Explicação do Gráfico das Top 5 Causas
    st.markdown("""
    Este gráfico apresenta as cinco principais causas de acidentes de trânsito. Compreender essas causas pode ajudar a desenvolver estratégias para reduzir a ocorrência de acidentes.
    """)