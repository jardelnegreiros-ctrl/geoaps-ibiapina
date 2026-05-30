@echo off
cd /d C:\Projetos\geoaps_ibiapina
call .venv\Scripts\activate
python -m streamlit run C:\Projetos\geoaps_ibiapina\app.py --server.port 8503
pause