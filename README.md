# 🛰️ 3D Orbital Satellite Tracker

A 3D orbital visualization tool for simulating and viewing satellite motion around Earth using **TLE data** and the **SGP4 model** (via [`cysgp4`](https://pypi.org/project/cysgp4/)).

This project renders satellites orbiting Earth in a 3D view, with support for fetching NORAD TLEs, propagating positions in real-time, and visualizing them against Earth and star textures.

---

## ✨ Features

- Load and parse **NORAD TLE data** (from CelesTrak or local cache).  
- Propagate satellite orbits using **cysgp4** (Python SGP4 wrapper).  
- 3D visualization of Earth, starfield, and satellite orbits.  
- Includes high-quality textures for Earth (day/night) and sky.  
- Modular structure: easy to extend with new satellites, views, or physics.

---

## 📂 Project Structure

```
.
├── earth_orbital_viewer.py     # Main visualization script
├── norad_satellite_data.py     # Handles TLE parsing and updates
├── satellite.py                # Satellite class (wrapping cysgp4 propagation)
├── tle_cache/active.txt        # Cached TLE data
├── assets/                     # Textures (Earth, sky backgrounds)
│   ├── 8k_earth_daymap.jpg
│   ├── earth_starmap_2d_projection.jpg
│   └── night-sky-star-background.png
├── sgp4_lib_cpp/               # Future C++ SGP4 engine (not used yet)
└── test.py                     # Test harness / quick checks
```

---

## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/aadhav0818/3d-orbital-satellite-tracker.git
   cd 3d-orbital-satellite-tracker
   ```

2. **Install dependencies**  
   Make sure you have Python 3.10+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   If you don’t have a `requirements.txt`, you’ll at least need:
   ```bash
   pip install numpy matplotlib cysgp4
   ```

---

## 🚀 Usage

Run the main visualization:

```bash
python earth_orbital_viewer.py
```

- By default, the program will load cached TLEs from `tle_cache/active.txt`.  
- To use fresh data, download new TLEs (e.g. from [CelesTrak](https://celestrak.org/NORAD/elements/)) and replace the file.  
- The satellites will propagate in real-time using `cysgp4` and display around a textured Earth.

---

## 🛠 Development Notes

- **Current propagation**: via [`cysgp4`](https://pypi.org/project/cysgp4/).  
- **Planned**: Switchable backend for the custom `sgp4_lib_cpp/` engine for more performance and flexibility.  
- Visualization uses Python (OpenGL/Matplotlib/other plotting backends depending on your setup).  

---

## 📌 Future Work

- Time controls (fast-forward, rewind, pause).  
- Ground track visualization on Earth’s surface.  
- Support for large constellations (Starlink, GPS, ISS).  
- User interface for satellite selection and data display.  

---

## 🤝 Contributing

Contributions are welcome!  
- Open issues for bugs/feature requests.  
- Submit PRs for improvements (visuals, performance, features).  

---

## 📜 License

This project is under the **MIT License**. See `LICENSE` for details.
