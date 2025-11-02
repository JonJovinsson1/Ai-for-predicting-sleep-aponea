import subprocess
import os
import shutil

# Paths for Deep-MVLM and prediction scripts
DEEP_MVLM_PATH = os.path.abspath(os.path.join(os.getcwd(), '../Deep-MVLM-master'))
PREDICT_SCRIPT = os.path.join(DEEP_MVLM_PATH, 'predict.py')
CONFIG_FILE = os.path.join(DEEP_MVLM_PATH, 'configs', 'DTU3D-depth.json')

# Paths for uploads and assets folders
UPLOADS_FOLDER = os.path.abspath(os.path.join(os.getcwd(), 'uploads'))
ASSETS_FOLDER = os.path.join(DEEP_MVLM_PATH, 'assets')

# Path to the custom classifier folder and run_model.py script
CUSTOM_CLASSIFIER_PATH = os.path.abspath(os.path.join(os.getcwd(), '../CustomClassifier'))  # Path to the folder where run_model.py is
RUN_MODEL_SCRIPT = os.path.join(CUSTOM_CLASSIFIER_PATH, 'run_model.py')  # Path to run_model.py script

def move_ply_to_assets():
    # Check for a .ply file in the uploads folder
    for file in os.listdir(UPLOADS_FOLDER):
        if file.endswith('.ply'):
            ply_file = os.path.join(UPLOADS_FOLDER, file)
            # Move the file to the assets folder
            shutil.move(ply_file, os.path.join(ASSETS_FOLDER, file))
            return os.path.join(ASSETS_FOLDER, file)  # Return new path
    return None  # No .ply file found

def delete_files(ply_file, vtk_file, txt_file):
    try:
        if os.path.exists(ply_file):
            os.remove(ply_file)
        if os.path.exists(vtk_file):
            os.remove(vtk_file)
        if os.path.exists(txt_file):
            os.remove(txt_file)
    except Exception as e:
        print(f"Error deleting files: {str(e)}")

def run_process(command, cwd):
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    for stdout_line in iter(process.stdout.readline, ''):
        yield stdout_line.strip()

    for stderr_line in iter(process.stderr.readline, ''):
        yield stderr_line.strip()

    process.stdout.close()
    process.stderr.close()
    process.wait()

def run_prediction_stream():
    try:
        # Get the mesh file path (either moved .ply or error if none found)
        mesh_file = move_ply_to_assets()

        if not mesh_file:
            print("Error: No .ply file found in uploads folder.")
            return  # Terminate the function if no file is found

        # Extract the base name from the uploaded .ply file
        base_name = os.path.splitext(os.path.basename(mesh_file))[0]

        # Dynamically create the output file names based on the uploaded file
        vtk_file = os.path.join(ASSETS_FOLDER, f'{base_name}_landmarks.vtk')  # Example vtk file
        txt_file = os.path.join(ASSETS_FOLDER, f'{base_name}_landmarks.txt')  # Example txt file

        # Run the prediction process
        prediction_process = subprocess.Popen(
            ['python', PREDICT_SCRIPT, '--c', CONFIG_FILE, '--n', mesh_file],
            cwd=DEEP_MVLM_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Stream the output of the prediction process
        for stdout_line in iter(prediction_process.stdout.readline, ''):
            yield stdout_line.strip()
        for stderr_line in iter(prediction_process.stderr.readline, ''):
            yield stderr_line.strip()

        prediction_process.stdout.close()
        prediction_process.stderr.close()
        prediction_process.wait()

        # Run the second process (run_model.py) after prediction is finished and stream its output
        model_process = subprocess.Popen(
            ['python', RUN_MODEL_SCRIPT, txt_file, vtk_file],  # Pass in the .txt and .vtk file paths dynamically
            cwd=CUSTOM_CLASSIFIER_PATH,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Stream the output of the run_model.py process
        for stdout_line in iter(model_process.stdout.readline, ''):
            yield stdout_line.strip()
        for stderr_line in iter(model_process.stderr.readline, ''):
            yield stderr_line.strip()

        model_process.stdout.close()
        model_process.stderr.close()
        model_process.wait()

        # Delete the ply, vtk, and txt files after processing is done
        delete_files(mesh_file, vtk_file, txt_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
