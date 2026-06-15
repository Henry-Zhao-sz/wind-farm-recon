"""
clean_and_extract.py

Parses the raw TSV files, normalizes coordinates, extracts
the primary velocity components (ux, uy, uz), and saves them as CSV files.
"""

import os
import pandas as pd

# --- Configuration ---
# Update this path if processing a different segment or looping through all
TARGET_PATH = './giverny_output_diurnal_3pm/time_1_30'

def main():
    # Loop through each expected Z-height file
    for z_points in range(10, 171, 20):
        input_filename = f'turbulence-interpolation_z{z_points}.tsv'
        output_filename = f'turbulence-interpolation_z{z_points}.csv'

        input_filepath = os.path.join(TARGET_PATH, input_filename)
        output_filepath = os.path.join(TARGET_PATH, output_filename)

        if not os.path.exists(input_filepath):
            print(f"[Skip] File not found: {input_filename}")
            continue

        try:
            # Read TSV, skipping the first two metadata rows
            df = pd.read_csv(input_filepath, sep='\t', skiprows=2, header=None)
            n_cols = len(df.columns)

            # Expected headers: coordinates + velocity components
            headers = ['time', 'x_point', 'y_point', 'z_point', 'ux', 'uy', 'uz']

            # Fallback header assignment if column counts mismatch
            if n_cols != len(headers):
                print(f"[Warn] {input_filename} has {n_cols} columns (expected {len(headers)}). Using generic headers.")
                headers = [f'col_{i + 1}' for i in range(n_cols - 3)] + ['ux', 'uy', 'uz']

            df.columns = headers

            # Normalize X coordinates (shift origin)
            df['x_point'] = pd.to_numeric(df['x_point'], errors='coerce') - 6500

            # Format velocity components
            for col in ['ux', 'uy', 'uz']:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

            # Extract only the velocity columns and save
            extracted_df = df[['ux', 'uy', 'uz']]
            extracted_df.to_csv(output_filepath, index=False)

            print(f"[Success] Processed: {input_filename} -> Shape: {extracted_df.shape}")

        except Exception as e:
            print(f"[Error] Failed processing {input_filename}: {e}")

    print("\n[Success] Data extraction completed.")

if __name__ == "__main__":
    main()