import os
import time
import requests
import numpy as np
from cysgp4  import PyTle, PyDateTime, propagate_many
from datetime import datetime, timezone
from satellite import Satellite

class TLEFetcher:

    SAT_GROUPS = {
        "stations": "https://celestrak.org/NORAD/elements/gp.php?GROUP=STATIONS&FORMAT=TLE",
        "starlink": "https://celestrak.org/NORAD/elements/gp.php?GROUP=STARLINK&FORMAT=TLE",
        "gps": "https://celestrak.org/NORAD/elements/gp.php?GROUP=GPS-OPS&FORMAT=TLE",
        "active": "https://celestrak.org/NORAD/elements/gp.php?GROUP=ACTIVE&FORMAT=TLE",
    }



    def __init__(self, cache_dir="tle_cache", max_cache_age=12): # max_cache_age is in hours
        self.cache_dir = cache_dir
        self.max_cache_age = max_cache_age * 3600
    
    def fetch(self, sat_group="gps"):
        url = self.SAT_GROUPS.get(sat_group)
        if not url:
            raise ValueError(f"Unknown satellite group: {sat_group}")
        
        cache_filepath = os.path.join(self.cache_dir, f"{sat_group}.txt")

        if os.path.exists(cache_filepath):
            last_modified_time = os.path.getmtime(cache_filepath)
            file_age = time.time() - last_modified_time
            if file_age < self.max_cache_age:
                print(f"Existing cache found for GROUP: {sat_group}, VALID FOR: {self.format_time(self.max_cache_age - file_age)}")
                with open(cache_filepath, "r") as file:
                    return file.read()
        
        response = requests.get(url)
        response.raise_for_status()
        tle_data = response.text
        
        with open(cache_filepath, "w") as file:
            file.write(response.text)
        
        with open(cache_filepath, "r") as file:
            return file.read()
    
    def format_time(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{round(hours)}h:{round(minutes)}m:{round(secs)}s"
    
class SatelliteManager:

    EARTH_RADIUS_KM = 6371.0

    def __init__ (self, tle_fetcher: TLEFetcher, group = "gps", earth_units_radius = 1.5):
        self.tle_fetcher = tle_fetcher
        self.group = group
        self.earth_units_radius = earth_units_radius
        self.scale = earth_units_radius/self.EARTH_RADIUS_KM
        self.satellite_names = []
        self.satellites = []
        self.pos_km = np.zeros((0,3), dtype=float)
             

    def load_tles(self):
        raw = self.tle_fetcher.fetch(self.group).splitlines()
        lines = [line.strip() for line in raw if line.strip() != ""]

        sat_TLEs = []
        for i in range(0, len(lines), 3):
            name = lines[i]
            line1 = lines[i+1]
            line2 = lines[i+2]
            sat_TLEs.append((name, line1, line2))

        self.create_satellites(sat_TLEs)
        
        
    def create_satellites(self, sat_TLEs):
        cysgp4_satellites = [PyTle(name, line1, line2) for name, line1, line2 in sat_TLEs]
        
        now = datetime.now(timezone.utc)
        obs_time = PyDateTime(now)
        
        mjds = np.array([obs_time.mjd] * len(cysgp4_satellites))
        tles = np.array(cysgp4_satellites)
        
        result = propagate_many(mjds, tles, do_eci_pos=True, do_eci_vel=True,
                                do_geo=False, do_topo=False, observers=None)

        self.satellite_names =  [name for name, _, _ in sat_TLEs]
        positions = result['eci_pos']
        velocities = result['eci_vel']

        self.satellites = [Satellite(name, pos, vel, self.scale) for name, pos, vel in zip(self.satellite_names, positions, velocities)]

        # ** FOR TESTING **
        # for name, pos, vel in zip(self.satellite_names, positions, velocities):
        #     print(f"Satellite Name: {name}")
        #     print(f"Position (km): {pos}")
        #     print(f"Velocity (km/s): {vel}")
        #     print()
