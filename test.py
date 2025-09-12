from norad_satellite_data import TLEFetcher, SatelliteManager

fetcher = TLEFetcher()
manager = SatelliteManager(fetcher, "gps")
manager.load_tles()

