# 3D Orbital Satellite Tracker

A 3D orbital visualization tool for simulating and viewing satellite motion around Earth using **TLE data** and the **SGP4 model** (via [`cysgp4`](https://pypi.org/project/cysgp4/)).

This project renders satellites orbiting Earth in a 3D view, with support for fetching NORAD TLEs, propagating positions in real-time, and visualizing them against Earth and star textures.

---

## Features

- Load and parse **NORAD TLE data** (from CelesTrak or local cache).  
- Propagate satellite orbits using **cysgp4** (C++ SGP4 wrapper).  
- 3D visualization of Earth, starfield, and satellite orbits.  
- Includes high-quality textures for Earth (day/night) and sky.  
- Modular structure: easy to extend with new satellites, views, or physics.

---

<<<<<<< HEAD

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/aadhav0818/3d-orbital-satellite-tracker.git
   cd 3d-orbital-satellite-tracker
   ```

2. **Install dependencies**  
   Make sure you have Python 3.10+ installed, then run:
   
 
   ```bash
   pip install numpy matplotlib cysgp4
   ```

---

## Usage

Run the main visualization:

```bash
python earth_orbital_viewer.py
```

- By default, the program will load cached TLEs from `tle_cache/active.txt`.  
- To use fresh data, download new TLEs (e.g. from [CelesTrak](https://celestrak.org/NORAD/elements/)) and replace the file.  
- The satellites will propagate in real-time using `cysgp4` and display around a textured Earth.

---

## Development Notesg
=======
## Development Notes
>>>>>>> 1a251f3d441f08b0aae5b3b7fa7ba19953166ffb

- **Current propagation**: via [`cysgp4`](https://pypi.org/project/cysgp4/). (Cython)
- **Planned**: Switchable backend to Dan Warner's `sgp4_lib_cpp/` engine for more performance and flexibility.  


---

## Future Work

- Time controls (fast-forward, rewind, pause).  
- Ground track visualization on Earth’s surface.  
- User interface for satellite selection and data display.  

---

