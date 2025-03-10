# Proyek Analisis Data : sparkle:
## Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir latihan_analisis_data
cd latihan_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Run streamlit app
streamlit run dashboard.py
