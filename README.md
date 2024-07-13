# E-Commerce Dashboard 

## Setup Environment - Anaconda
```
conda create --name dashboard-ecommerce python=3.9
conda activate dashboard-ecommerce
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir dashboard-ecommerce
cd dashboard-ecommerce\dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```