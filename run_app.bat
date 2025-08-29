@echo off
call conda activate corpus
set PYTHONPATH=G:\corpus2
streamlit run app/streamlit_app.py
pause