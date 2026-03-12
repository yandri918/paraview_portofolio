import streamlit as st
import pyvista as pv
import numpy as np
import os
from stpyvista import stpyvista

# Initialize pyvista backend
os.environ["PYVISTA_JUPYTER_BACKEND"] = "panel"
pv.global_theme.jupyter_backend = 'panel'

st.set_page_config(page_title="PyVista Demo", page_icon="🌪️", layout="wide")

st.title("🌪️ Rendering 3D Interaktif dengan PyVista")
st.markdown(
    """
    Di halaman ini, kita mereplikasi fungsionalitas rendering ilmiah (seperti ParaView) 
    langsung di dalam browser menggunakan **PyVista** dan **VTK**.
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
# Di sinilah "magic" VTK/ParaView terjadi
plotter = pv.Plotter(window_size=[800, 600])
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

# --- 2. RENDER KE STREAMLIT ---
# Render komponen stpyvista di dalam container st.columns untuk layout yang rapi
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Interactive View")
    st.info("💡 **Coba interaksi berikut:** Klik kiri (tahan & geser) untuk memutar. Scroll untuk zoom. Klik tengah (tahan) atau Shift+Klik Kiri untuk menggeser *(pan)* model.")
    # Hasil render stpyvista
    stpyvista(plotter)

with col2:
    st.markdown("### Object Info")
    st.write(f"**Tipe Data:** `StructuredGrid`")
    st.write(f"**Jumlah Titik:** `{mesh.n_points}`")
    st.write(f"**Jumlah Sel (Elemen):** `{mesh.n_cells}`")
    st.write(f"**Bounds (X, Y, Z):**")
    st.write([round(b, 2) for b in mesh.bounds])

st.markdown("---")
st.markdown("*Aplikasi dikembangkan sebagai demonstrasi portfolio integrasi engine vtk/pyvista ke web Streamlit.*")
