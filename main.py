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

def process_volumes(parent_folder):
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

def process_unsorted(parent_folder, chapters_per_volume):
    # Collect all chapter folders directly under the parent folder
    chapter_folders = [os.path.join(parent_folder, chapter_folder) for chapter_folder in sorted(os.listdir(parent_folder)) if os.path.isdir(os.path.join(parent_folder, chapter_folder))]

    total_chapters = len(chapter_folders)
    if chapters_per_volume == 0:
        chapters_per_volume = total_chapters

    for i in range(0, total_chapters, chapters_per_volume):
        volume_image_files = []
        for chapter_folder in chapter_folders[i:i + chapters_per_volume]:
            image_files = [os.path.join(chapter_folder, f) for f in os.listdir(chapter_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_files.sort()  # Sort the images by name
            volume_image_files.extend(image_files)
        
        # Define the output PDF path with the volume name
        output_pdf_path = os.path.join(parent_folder, f"Volume_{i // chapters_per_volume + 1}.pdf")
        
        # Create a single PDF with all the images
        images_to_pdf(volume_image_files, output_pdf_path)

def main():
    # Create a Tkinter root window and hide it
    root = Tk()
    root.withdraw()

    # Ask the user for the processing option
    print("Choose an option:")
    print("1. Process each volume folder separately")
    print("2. Combine chapters into volumes (unsorted)")
    option = int(input("Enter 1 or 2: "))

    # Prompt for folder selection after the user chooses an option
    print("Select the parent folder containing the volumes.")
    print("Each volume should be in a separate folder within the parent folder.")

    # Open a file dialog to select a folder
    parent_folder = filedialog.askdirectory(title="Select Parent Folder Containing Volumes")

    # If no folder is selected, exit the program
    if not parent_folder:
        print("No folder selected. Exiting.")
        return

    if option == 1:
        process_volumes(parent_folder)
    elif option == 2:
        chapters_per_volume = int(input("Enter the number of chapters per volume (0 for all chapters in a single PDF): "))
        process_unsorted(parent_folder, chapters_per_volume)
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    main()