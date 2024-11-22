# Análise de Acidentes de Trânsito no Brasil
## Descrição do Projeto
Este projeto tem como objetivo realizar uma análise exploratória de dados de acidentes de trânsito no Brasil. A partir dos dados coletados de diferentes anos (2021 a 2024), a aplicação fornece visualizações interativas e insights sobre as principais causas dos acidentes, distribuição geográfica, e condições climáticas relacionadas aos acidentes.
O projeto é dividido em duas partes principais:
- Backend: Responsável por carregar, processar e tratar os dados, consolidando em um arquivo CSV que é utilizado no frontend.
- Frontend: Desenvolvido em Streamlit, o frontend apresenta visualizações interativas, incluindo gráficos de barras, mapas interativos e gráficos de dispersão para melhor compreensão dos dados

### Tecnologias Utilizadas
- **Backend**: Python, Pandas
- **Frontend**: Streamlit, Plotly
- **Análise de Dados**: NumPy, Scikit-learn

## Instruções de Instalação e Execução
1. Clonar o Repositório
Clone este repositório para a sua máquina local:
git clone https://github.com/luana-souza-hub/analise_acidentes_transito.git
2. Criar e Ativar o Ambiente Virtual
Crie um ambiente virtual e ative-o:
- No Windows
  - python -m venv venv
  - venv\Scripts\activate

- No Linux/Mac
  - python3 -m venv venv
  - source venv/bin/activate

3. Instalar as Dependências
Instale todas as dependências listadas no arquivo requirements.txt:
  - pip install -r requirements.txt
4. Executar o Backend
  - Execute o script do backend para gerar o arquivo de dados consolidado (accidents_cleaned.csv):
python backend_acidentes.py
5. Executar o Frontend
  - Depois de gerar o arquivo de dados, execute a aplicação Streamlit para visualizar os dados:
  - streamlit run interface_streamlit.py

## Principais Resultados e Insights Obtidos
- Top 5 Causas dos Acidentes: Os principais fatores contribuintes para os acidentes foram identificados, ajudando a direcionar políticas públicas e campanhas de conscientização.
- Distribuição Geográfica: A distribuição geográfica dos acidentes foi analisada através de mapas interativos, facilitando a identificação de áreas de risco elevado.
- Impacto das Condições Climáticas: O projeto também revelou a relação entre o número de vítimas e as condições climáticas, destacando como determinadas condições impactam na gravidade dos acidentes.

## Dependências
Certifique-se de que todas as dependências estejam listadas no arquivo requirements.txt. Caso precise gerá-las automaticamente, utilize o comando:
pip freeze > requirements.txt
As principais dependências incluem:
  - pandas
  - plotly
  - streamlit

## Preview
![tela 1](https://github.com/user-attachments/assets/7dc4609b-7ea9-4989-9519-29d2ce9f6fba)
![tela 2](https://github.com/user-attachments/assets/75bff058-6792-41d9-83e4-13712a970b56)
![tela 3](https://github.com/user-attachments/assets/a420860e-da41-4e48-afcc-9de52c62f88b)
![tela 4](https://github.com/user-attachments/assets/81c226cf-0fb9-4695-923f-596bb524fecf)



