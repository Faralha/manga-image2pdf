from tkinter import Tk, filedialog
from PIL import Image
import os

def images_to_pdf(image_files, output_pdf_path):
    if image_files:
        # Open images and convert them to RGB
        images = [Image.open(img).convert('RGB') for img in image_files]
        
        # Save the images as a PDF
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF saved successfully at {output_pdf_path}")
    else:
        print(f"No images found to create PDF.")

def main():
    # Create a Tkinter root window and hide it
    root = Tk()
    root.withdraw()

    print("Select the folder containing the volume with chapters to convert to PDF.")
    print("The folder should only contain chapters, each in a separate folder.")
    print("The parent folder must be the Volume number.")
    
    # Open a file dialog to select a folder
    parent_folder = filedialog.askdirectory(title="Select Parent Folder Containing Volumes")
    
    # If no folder is selected, exit the program
    if not parent_folder:
        print("No folder selected. Exiting.")
        return

    # Iterate through each volume folder in the parent folder
    volume_folders = sorted(os.listdir(parent_folder))  # Sort the volume folders
    for volume_folder in volume_folders:
        volume_path = os.path.join(parent_folder, volume_folder)
        if os.path.isdir(volume_path):
            # Collect all image files from each chapter folder within the volume
            all_image_files = []
            chapter_folders = sorted(os.listdir(volume_path))  # Sort the chapter folders
            total_chapters = len(chapter_folders)
            
            for index, chapter_folder in enumerate(chapter_folders):
                chapter_path = os.path.join(volume_path, chapter_folder)
                if os.path.isdir(chapter_path):
                    image_files = [os.path.join(chapter_path, f) for f in os.listdir(chapter_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                    image_files.sort()  # Sort the images by name
                    all_image_files.extend(image_files)
                    
                    # Update progress
                    print(f"Volume: {volume_folder}, Progress: {index + 1}/{total_chapters} chapters processed")

            # Define the output PDF path with the volume name
            output_pdf_path = os.path.join(parent_folder, f"{volume_folder}.pdf")

            # Create a single PDF with all the images
            images_to_pdf(all_image_files, output_pdf_path)

if __name__ == "__main__":
    main()