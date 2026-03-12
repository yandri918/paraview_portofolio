import streamlit as st
import pyvista as pv
import numpy as np
import tempfile
import streamlit.components.v1 as components
import os

# Sangat Penting untuk Streamlit Cloud (Linux Headless): 
# Ini akan mengaktifkan virtual display OS secara otomatis 
pv.start_xvfb()

st.set_page_config(page_title="PyVista Demo", page_icon="🌪️", layout="wide")

st.title("🌪️ Rendering 3D Interaktif dengan PyVista")
st.markdown(
    """
    Di halaman ini, kita mereplikasi fungsionalitas rendering ilmiah (seperti ParaView) 
    langsung di dalam browser menggunakan **PyVista** dan **VTK.js**.
    """
)

# Sidebar controls
st.sidebar.header("3D Rendering Controls")
color_map = st.sidebar.selectbox("Pilih Colormap (Skema Warna)", ["jet", "viridis", "plasma", "magma", "inferno"])
show_edges = st.sidebar.checkbox("Tampilkan Edges (Jaring Mesh)", value=False)
resolution = st.sidebar.slider("Resolusi Mesh (Grid)", min_value=10, max_value=100, value=50, step=10)

st.write(f"Men-generate data gelombang 3D dengan resolusi **{resolution}x{resolution}**...")

# Generate a 3D dataset (Parametric surface representing a wave)
@st.cache_data
def generate_3d_wave(res):
    x = np.linspace(-10, 10, res)
    y = np.linspace(-10, 10, res)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x**2 + y**2)
    z = np.sin(r)
    
    # Create the PyVista StructuredGrid
    grid = pv.StructuredGrid(x, y, z)
    # Calculate some scalar data (e.g., height or "pressure") to color by
    grid.point_data["Elevation"] = z.flatten(order="F")
    return grid

# Ambil data
mesh = generate_3d_wave(resolution)

# --- 1. SETUP PLOTTER (RENDERER) ---
# Menggunakan off_screen=True karena kita berjalan di Cloud Server (tanpa monitor)
plotter = pv.Plotter(window_size=[800, 600], off_screen=True)
plotter.background_color = "white"

# Tambahkan mesh ke plotter
plotter.add_mesh(
    mesh,
    scalars="Elevation",       # Data yang akan diwarnai
    cmap=color_map,            # Pilihan warna dari sidebar
    show_edges=show_edges,     # Tampilkan garis antar elemen grid
    lighting=True,
    interpolate_before_map=True
)

# Tampilkan widget sumbu koordinat
plotter.add_axes()

# --- 2. RENDER KE STREAMLIT MENGGUNAKAN NATIVE HTML EXPORT ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Interactive View")
    st.info("💡 **Coba interaksi berikut:** Klik kiri (tahan & geser) untuk memutar. Scroll untuk zoom. Klik tengah (tahan) atau Shift+Klik Kiri untuk menggeser *(pan)* model.")
    
    # Bypassing stpyvista multiprocessing bug: 
    # Mengekspor scene PyVista ke format VTK.js HTML secara native, lalu di-embed ke Streamlit.
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = f.name
        
    plotter.export_html(html_path)
    
    with open(html_path, 'r') as f:
        html_data = f.read()
        
    # Tampilkan di browser pengguna
    components.html(html_data, height=600, scrolling=False)

with col2:
    st.markdown("### Object Info")
    st.write(f"**Tipe Data:** `StructuredGrid`")
    st.write(f"**Jumlah Titik:** `{mesh.n_points}`")
    st.write(f"**Jumlah Sel (Elemen):** `{mesh.n_cells}`")
    st.write(f"**Bounds (X, Y, Z):**")
    st.write([round(b, 2) for b in mesh.bounds])

st.markdown("---")
st.markdown("*Aplikasi dikembangkan sebagai demonstrasi portfolio visualisasi web menggunakan VTK.js dan PyVista Streamlit.*")
