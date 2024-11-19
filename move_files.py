import os
import shutil

source_files = ['DC,WB.jpg', 'E-Pets.jpeg', 'E-Pets2.jpeg']
destination_folder = 'static/images'

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

for file in source_files:
    source_path = file
    destination_path = os.path.join(destination_folder, file)
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        print(f"Moved {file} to {destination_folder}")
    else:
        print(f"File {file} not found")

print("File moving operation completed.")
