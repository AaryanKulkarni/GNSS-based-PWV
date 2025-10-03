import os
import tarfile
import shutil

# Get user input for folder path
folder_path = input("Enter the folder path containing .tar files: ").strip()

# Ensure the folder exists
if not os.path.exists(folder_path):
    print("Folder does not exist. Please check the path.")
    exit()

# Get all .tar files in the folder
tar_files = [f for f in os.listdir(folder_path) if f.endswith(".gz")]

# Ensure there are .tar files to process
if not tar_files:
    print("No .tar files found in the folder.")
    exit()

# Output folder for extracted files
output_folder = os.path.join(folder_path, "Extracted_Summaries")
os.makedirs(output_folder, exist_ok=True)

for tar_file in tar_files:
    tar_path = os.path.join(folder_path, tar_file)

    # Open the tar file
    with tarfile.open(tar_path, 'r') as tar:
        # Look for APPS_summary file inside 'run' folder
        summary_file = None
        for member in tar.getmembers():
            if "run/APPS_summary" in member.name:
                summary_file = member
                break

        if summary_file:
            # Extract APPS_summary to a temporary location
            tar.extract(summary_file, path=output_folder)
            extracted_path = os.path.join(output_folder, summary_file.name)

            # Rename and move the file
            new_name = f"APPS_summary_{tar_file.replace('.tar', '')}.txt"
            new_path = os.path.join(output_folder, new_name)
            shutil.move(extracted_path, new_path)

            print(f"Extracted and saved: {new_name}")
        else:
            print(f"No APPS_summary found in {tar_file}")

print("Extraction complete.")
