import os
import subprocess
import shutil

# Define the directory containing the files
input_directory = "assets/"
output_directory = "zero/"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Define the common part of the command
base_command = ["python", "predict.py", "--c", "configs/DTU3D-depth.json"]

# Loop through each file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".ply"):  # Process only .ply files
        file_path = os.path.join(input_directory, filename)
        
        # Run the command
        command = base_command + ["--n", file_path]
        subprocess.run(command)
        
        # Extract base filename without extension
        base_filename = os.path.splitext(filename)[0]
        
        # Check current directory for generated .txt and .vtk files
        txt_file = f"{base_filename}.txt"
        vtk_file = f"{base_filename}.vtk"
        
        # Print the paths to see where the script is looking
        print(f"Looking for {txt_file} and {vtk_file} in current directory")

        # Check if files exist and move them
        if os.path.exists(txt_file):
            print(f"Moving {txt_file} to {output_directory}")
            shutil.move(txt_file, os.path.join(output_directory, txt_file))
        else:
            print(f"{txt_file} not found")

        if os.path.exists(vtk_file):
            print(f"Moving {vtk_file} to {output_directory}")
            shutil.move(vtk_file, os.path.join(output_directory, vtk_file))
        else:
            print(f"{vtk_file} not found")