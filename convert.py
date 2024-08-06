import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def extract_values_from_diagonal(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # Assuming that the color scale is linear and the colormap is on the right side of the image
    # Extract the colorbar to create a mapping from color to value
    colorbar = img_array[:, -30:-10]  # Adjust these indices based on where the colorbar actually is in your image
    # Compute average color values in the colorbar
    colorbar_mean = np.mean(colorbar, axis=1)
    
    # Convert RGB to grayscale assuming standard NTSC conversion formula (or similar)
    grayscale_values = np.dot(colorbar_mean[..., :3], [0.2989, 0.5870, 0.1140])
    # Map grayscale values from 0 to 1
    min_val, max_val = grayscale_values.min(), grayscale_values.max()
    normalized_values = (grayscale_values - min_val) / (max_val - min_val)

    # Assuming values in colorbar are linearly spaced
    value_range = np.linspace(0, 1, len(normalized_values))

    # Map grayscale values to the corresponding numerical values using interpolation
    value_mapping = dict(zip(grayscale_values, value_range))

    # Extract diagonal
    diag_indices = np.diag_indices_from(img_array[:-50, 50:-50]) # Adjust slicing to exclude colorbar and align correctly
    diag_colors = img_array[diag_indices]
    diag_grayscales = np.dot(diag_colors, [0.2989, 0.5870, 0.1140])

    # Map colors on the diagonal to values using the nearest grayscale match
    diag_values = [value_mapping.get(np.abs(grayscale - diag_grayscales).argmin()) for grayscale in diag_grayscales]

    return diag_values

# Example usage
image_path = r'C:\Users\Sumfl\Downloads\FinalTraining\train7\confusion_matrix_normalized.png'
diag_values = extract_values_from_diagonal(image_path)
print(diag_values)

# Optionally visualize the diagonal extraction to verify correctness
plt.figure()
plt.imshow(Image.open(image_path))
plt.plot(np.diag_indices_from(np.array(Image.open(image_path)[:-50, 50:-50])[0]), color='red')
plt.title("Diagonal on Confusion Matrix")
plt.show()


