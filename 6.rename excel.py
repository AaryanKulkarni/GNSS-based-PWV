import os
import pandas as pd


# Function to rename Excel files in folder T based on date columns
def rename_excels_based_on_date(folder_path):
    print(f"\nProcessing folder '{folder_path}' (Date-based renaming)...")
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx") or file.endswith(".xls"):  # Check for Excel files
            file_path = os.path.join(folder_path, file)

            try:
                # Read the Excel file
                df = pd.read_excel(file_path, header=None)  # No headers assumed

                # Extract date from the second row
                year = int(df.iloc[1, 0]) + 2000  # Assumes 'Y' column (2-digit year)
                month = int(df.iloc[1, 1])
                day = int(df.iloc[1, 2])

                # Create new file name in DD_MM_YYYY format
                new_file_name = f"{str(day).zfill(2)}_{str(month).zfill(2)}_{year}.xlsx"
                new_file_path = os.path.join(folder_path, new_file_name)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file}' to '{new_file_name}'")

            except Exception as e:
                print(f"Failed to process '{file}': {e}")


# Function to rename Excel files in folder Z based on GPS_Time
def rename_excels_based_on_gps_time(folder_path):
    print(f"\nProcessing folder '{folder_path}' (GPS_Time-based renaming)...")
    for file in os.listdir(folder_path):
        if file.startswith("~$"):  # Skip temporary Excel files
            continue

        if file.endswith(".xlsx") or file.endswith(".xls"):  # Check for Excel files
            file_path = os.path.join(folder_path, file)

            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Extract date from the second row 'GPS_Time' column
                gps_time = str(df.iloc[0, 1])  # 'GPS_Time' assumed to be column B (index 1)

                # Ensure GPS_Time is valid and has the expected format
                if ":" not in gps_time:
                    print(f"Invalid GPS_Time format in '{file}'. Skipping...")
                    continue

                # Extract date part (handles "yyyy:mm:dd" or longer formats)
                date_part = gps_time.split("T")[0] if "T" in gps_time else gps_time.split()[0]
                parts = date_part.split(":")
                if len(parts) >= 3:
                    year, month, day = parts[:3]
                else:
                    print(f"Unexpected GPS_Time format in '{file}'. Skipping...")
                    continue

                # Create new file name in DD_MM_YYYY format
                new_file_name = f"{day}_{month}_{year}.xlsx"
                new_file_path = os.path.join(folder_path, new_file_name)

                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file}' to '{new_file_name}'")

            except Exception as e:
                print(f"Failed to process '{file}': {e}")


# Main function to handle both folders (T and Z)
def main():
    main_folder_path = input("Enter the main folder path: ")

    # Define subfolders T and Z
    folder_t = os.path.join(main_folder_path, "T")
    folder_z = os.path.join(main_folder_path, "Z")

    # Check and process folder T
    if os.path.exists(folder_t):
        rename_excels_based_on_date(folder_t)
    else:
        print(f"Folder 'T' not found in '{main_folder_path}'.")

    # Check and process folder Z
    if os.path.exists(folder_z):
        rename_excels_based_on_gps_time(folder_z)
    else:
        print(f"Folder 'Z' not found in '{main_folder_path}'.")


if __name__ == "__main__":
    main()
