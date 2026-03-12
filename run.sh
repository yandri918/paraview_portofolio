#!/bin/bash
# Skrip ini digunakan di Streamlit Cloud untuk menjalankan xvfb (Virtual Frame Buffer)
# karena PyVista/VTK memerlukan display server untuk melakukan rendering 3D.

# Jalankan shell script ini sebelum Streamlit dijalankan
xvfb-run -a streamlit run app.py
