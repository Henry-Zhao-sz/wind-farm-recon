"""
build_dataset.py

Aggregates individual CSV files into multi-dimensional NumPy arrays (.npy).
Reshapes the flat tables into a 5D spatio-temporal tensor suitable for
Deep Learning frameworks (e.g., PyTorch).
Final Tensor Shape: (Channels, Time, Z, Y, X)
"""

import os
import glob
import re
import numpy as np
import pandas as pd
from tqdm import tqdm

# --- Configuration ---
RAW_DATA_ROOT = "./giverny_output_diurnal_3pm"
PROCESSED_DATA_ROOT = "./processed_data"

# Tensor dimensions
NX = 250  # X points
NY = 64  # Y points
NZ = 9  # Z layers
T = 30  # Timesteps (seconds)
CHANNELS = 3  # Velocity components (u, v, w)


def extract_z_height(filename):
    """Extracts the Z-height integer from the filename for proper sorting."""
    match = re.search(r'(\d+)', os.path.basename(filename))
    return int(match.group(1)) if match else 0


def process_single_sample(sample_folder_path, save_path):
    """Reads 9 CSV layers from a sample folder and compiles them into a 5D tensor."""

    csv_files = glob.glob(os.path.join(sample_folder_path, "*.csv"))
    # Sort files to ensure layers are stacked sequentially from bottom to top
    csv_files.sort(key=extract_z_height)

    if len(csv_files) != NZ:
        print(f"\n[Warning] Skipping {sample_folder_path}: Found {len(csv_files)} files, expected {NZ}")
        return

    z_layers_data = []

    # Iterate through each Z-layer
    for fpath in csv_files:
        try:
            df = pd.read_csv(fpath, header=0)
            raw_vals = df.values.astype(np.float32)
        except Exception as e:
            print(f"\n[Error] Reading {fpath}: {e}")
            return

        # Reshape flat table to (Time, X, Y, Channels)
        # Assuming original memory layout iterates Y -> X -> Time
        try:
            reshaped_layer = raw_vals.reshape(T, NX, NY, CHANNELS)
        except ValueError:
            print(f"\n[Error] Shape mismatch in {fpath}. Expected {T * NX * NY * CHANNELS} elements.")
            return

        z_layers_data.append(reshaped_layer)

    # Stack along the Z-axis -> Shape: (Z, T, X, Y, Channels)
    full_data = np.stack(z_layers_data, axis=0)

    # Transpose to PyTorch standard format: [Channels, Time, Z, Y, X]
    # Original indices: 0:Z, 1:T, 2:X, 3:Y, 4:C
    # Target indices:   4:C, 1:T, 0:Z, 3:Y, 2:X
    final_data = np.transpose(full_data, (4, 1, 0, 3, 2))

    # Save to disk as a NumPy array
    np.save(save_path, final_data)


def main():
    os.makedirs(PROCESSED_DATA_ROOT, exist_ok=True)

    # Discover all sample sub-directories
    sample_folders = sorted([
        f for f in glob.glob(os.path.join(RAW_DATA_ROOT, "*"))
        if os.path.isdir(f)
    ])

    print(f"Found {len(sample_folders)} sample folders. Starting tensorization...")

    # Process each folder and display progress
    for folder in tqdm(sample_folders):
        folder_name = os.path.basename(folder)
        save_name = os.path.join(PROCESSED_DATA_ROOT, f"{folder_name}.npy")
        process_single_sample(folder, save_name)

    print(f"\n[Success] All data processed and saved to '{PROCESSED_DATA_ROOT}'")


if __name__ == "__main__":
    main()