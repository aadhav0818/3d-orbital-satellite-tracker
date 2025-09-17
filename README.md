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


## Development Notes

- **Current propagation**: via [`cysgp4`](https://pypi.org/project/cysgp4/). (Cython)
- **Planned**: Switchable backend to Dan Warner's `sgp4_lib_cpp/` engine for more performance and flexibility.  


---

## Future Work

- Time controls (fast-forward, rewind, pause).  
- Ground track visualization on Earth’s surface.  
- User interface for satellite selection and data display.  

---

