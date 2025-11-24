@echo off
call conda activate corpus
set PYTHONPATH=D:\skills\SelfCraftedTools\vocabulary_system
streamlit run app/streamlit_app.py
pause