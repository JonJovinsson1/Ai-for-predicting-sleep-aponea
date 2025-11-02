import torch
import numpy as np
import pyvista as pv
import sys
from model import SimpleClassifier

# Function to load and combine data from a .txt file and a .vtk file
def load_data(txt_file, vtk_file):
    txt_data = np.loadtxt(txt_file)
    vtk_data = pv.read(vtk_file)
    vtk_points = np.array(vtk_data.points)

    combined_data = np.hstack((txt_data.flatten(), vtk_points.flatten()))
    return combined_data

if __name__ == '__main__':
    # Check if the script receives the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python run_model.py <txt_file> <vtk_file>")
        sys.exit(1)

    # Get the .txt and .vtk file paths from the command-line arguments
    txt_file = sys.argv[1]
    vtk_file = sys.argv[2]

    # Load and combine the features from the .txt and .vtk files
    input_features = load_data(txt_file, vtk_file)

    # Get the input size from the combined data
    input_size = input_features.shape[0]

    # Load the model and set it to evaluation mode
    model = SimpleClassifier(input_size=input_size)
    model.load_state_dict(torch.load('simple_classifier.pth'))
    model.eval()

    # Prepare the input tensor
    input_tensor = torch.tensor(input_features, dtype=torch.float32).unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

        # Output the prediction result
        if predicted_class == 0:
            print("Not predicted to have OSA")
        else:
            print("Predicted to have OSA")
