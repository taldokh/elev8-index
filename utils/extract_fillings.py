import os
import zipfile
import shutil


# Function to extract the necessary files (coverpage.tsv, infotable.tsv)
def extract_files_from_zip(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all files to a temporary location
        zip_ref.extractall(dest_dir)

        # List the extracted files
        extracted_files = zip_ref.namelist()

        # Identify and move the required files (coverpage.tsv and infotable.tsv)
        for file in extracted_files:
            if 'COVERPAGE.tsv' == file:
                shutil.move(os.path.join(dest_dir, file), os.path.join(dest_dir, 'COVERPAGE.tsv'))
            elif 'INFOTABLE.tsv' == file:
                shutil.move(os.path.join(dest_dir, file), os.path.join(dest_dir, 'INFOTABLE.tsv'))

        # Clean up any extra files (delete others that are not needed)
        for file in extracted_files:
            if 'COVERPAGE.tsv' not in file and 'INFOTABLE.tsv' not in file:
                os.remove(os.path.join(dest_dir, file))


# Main function to process each ZIP file in the local directory
def process_zip_files(directory):
    # Loop through all the files in the given directory
    for zip_file in os.listdir(directory):
        # Check if it's a ZIP file
        if zip_file.endswith(".zip"):
            # Construct full path to the ZIP file
            zip_path = os.path.join(directory, zip_file)

            # Extract the year and quarter from the file name (e.g., 2013q2_form13f.zip)
            base_name = zip_file.replace('_form13f.zip', '')
            if len(base_name) == 6:  # Ensure the format is like 2013q2
                year_quarter = base_name
                folder_path = os.path.join(directory, year_quarter)
                os.makedirs(folder_path, exist_ok=True)

                # Extract the coverpage.tsv and infotable.tsv to the folder
                extract_files_from_zip(zip_path, folder_path)

                print(f"Processed {zip_file} into {folder_path}")


if __name__ == "__main__":
    # Set the directory where your ZIP files are located
    zip_files_directory = "./"  # Modify this path

    process_zip_files(zip_files_directory)
