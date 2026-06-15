"""
download_wind_farm_data.py

Downloads 3D wind velocity data from the JHU turbulence database.
Includes a robust retry mechanism for handling network instability
during long-running, large-scale data retrieval tasks.
"""

import os
import time
import random
import traceback
import numpy as np
from givernylocal.turbulence_dataset import *
from givernylocal.turbulence_toolkit import *

# --- Configuration ---
AUTH_TOKEN = 'your_auth_token'
DATASET_TITLE = 'diurnal_windfarm'
BASE_OUTPUT_PATH = './giverny_output_diurnal_3pm'

# --- Dataset Parameters ---
VARIABLE = 'velocity'
TEMPORAL_METHOD = 'none'
SPATIAL_METHOD = 'm2q8'
SPATIAL_OPERATOR = 'field'

# Grid definition
NX = 250
NY = 64
X_POINTS = np.linspace(6500, 11480, NX, dtype=np.float64)
Y_POINTS = np.linspace(0, 1260, NY, dtype=np.float64)

# Time segmentation (in seconds)
START_TOTAL = 1
END_TOTAL = 3600
SEGMENT_DURATION = 30
NUM_SEGMENTS = (END_TOTAL - START_TOTAL + 1) // SEGMENT_DURATION

# Wait time for network/API retries (seconds)
RETRY_WAIT_TIME = 300


def main():
    for seg in range(NUM_SEGMENTS):
        time_start = START_TOTAL + seg * SEGMENT_DURATION
        time_end = time_start + SEGMENT_DURATION - 1

        segment_folder = f"time_{time_start}_{time_end}"
        output_path = os.path.join(BASE_OUTPUT_PATH, segment_folder)
        os.makedirs(output_path, exist_ok=True)

        # Initialize dataset with a robust retry mechanism
        dataset = None
        while True:
            try:
                dataset = turb_dataset(
                    dataset_title=DATASET_TITLE,
                    output_path=output_path,
                    auth_token=AUTH_TOKEN
                )
                break
            except Exception as e:
                print(f"\n[Error] Dataset initialization failed (Time {time_start}-{time_end}): {e}")
                print(f"Sleeping for {RETRY_WAIT_TIME}s before retrying...")
                time.sleep(RETRY_WAIT_TIME)

        # Configure data retrieval options
        delta_t = 1.0
        option = [time_end, delta_t]

        print(f"\n--- Downloading time segment: {time_start} ~ {time_end} s ---")

        # Iterate through Z-axis (height layers)
        for z_val in range(10, 171, 20):
            z_points = float(z_val)

            # Generate 3D grid points
            points = np.array([
                axis.ravel() for axis in np.meshgrid(X_POINTS, Y_POINTS, z_points, indexing='ij')
            ], dtype=np.float64).T

            output_filename = f'turbulence-interpolation_z{z_points:.0f}'

            # Download data with retry mechanism
            while True:
                try:
                    result, times = getData(
                        dataset, VARIABLE, time_start, TEMPORAL_METHOD,
                        SPATIAL_METHOD, SPATIAL_OPERATOR, points, option, return_times=True
                    )
                    write_interpolation_tsv_file(dataset, points, result, output_filename)
                    break
                except Exception as e:
                    print(f"\n[Error] Data download failed (z={z_points}): {e}")
                    print(f"Sleeping for {RETRY_WAIT_TIME}s before retrying...")
                    time.sleep(RETRY_WAIT_TIME)

            print(f"  Successfully downloaded data for z = {z_points}")

            # Brief pause to prevent rate limiting
            time.sleep(random.randint(15, 25))

        # Longer pause between large time segments
        time.sleep(random.randint(60, 120))

    print("\n[Success] All time segments downloaded.")


if __name__ == "__main__":
    main()