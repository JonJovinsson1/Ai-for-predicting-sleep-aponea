import os
import torch
from torch.utils.data import Dataset
import numpy as np
import pyvista as pv

class CustomVTKDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.classes = ['zero', 'one']
        self.data = []

        # Load file pairs and labels
        for label, folder in enumerate(self.classes):
            folder_path = os.path.join(root_dir, folder)
            vtk_files = [f for f in os.listdir(folder_path) if f.endswith('.vtk')]
            for vtk_file in vtk_files:
                txt_file = vtk_file.replace('.vtk', '.txt')
                txt_path = os.path.join(folder_path, txt_file)
                vtk_path = os.path.join(folder_path, vtk_file)
                if os.path.exists(txt_path):
                    self.data.append((vtk_path, txt_path, label))
                else:
                    print(f'Warning: Corresponding txt file not found for {vtk_file}')
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        vtk_path, txt_path, label = self.data[idx]


        txt_data = np.loadtxt(txt_path)

        # Load and preprocess vtk file
        vtk_data = pv.read(vtk_path)
        vtk_points = np.array(vtk_data.points)  # Extracting the points from the VTK file

        # Combine features from both txt and vtk files
        combined_data = np.hstack((txt_data.flatten(), vtk_points.flatten()))

        # Convert to torch tensors
        combined_data = torch.tensor(combined_data, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.long)

        return combined_data, label
