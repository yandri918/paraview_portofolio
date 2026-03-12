import streamlit as st

st.set_page_config(page_title="ParaView 3D Portfolio", page_icon="🧬", layout="wide")

st.title("🧬 Scientific 3D Web Visualization")
st.markdown("### Portofolio Integrasi ParaView & Streamlit")

st.write(
    """
    Selamat datang di proyek portofolio yang mendemonstrasikan kemampuan **Server-side 3D Rendering** 
    menggunakan ekosistem **VTK** dan **PyVista** (`stpyvista`).
    
    Aplikasi ini meniru kemampuan rendering dari *ParaView* langsung di dalam peramban web Anda tanpa bantuan plugin eksternal.
    
    ### Fitur Utama:
    - 🧊 **Interaktivitas 3D Penuh**: Putar, Zoom, dan Geser *(Pan)* model objek 3D secara *real-time*.
    - 🚀 **Server Rendering**: Mengolah dataset berat atau *mesh* ilmiah di server.
    - 🎨 **Kustomisasi Filter**: Menerapkan colormap dan pemetaan skalar ke objek tiga dimensi.
    
    ---
    👉 **Silakan buka menu 1_PyVista_Demo di sidebar untuk melihat rendering 3D interaktif!**
    """
)

st.info("💡 **Tips:** Untuk proyek profesional, server dengan memori yang cukup disarankan karena rendering ini menggunakan *backend* komputasi (VTK).")
