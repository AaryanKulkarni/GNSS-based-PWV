import os
import pandas as pd


# Function to calculate hourly average of Temperature in folder T
def process_temperature_in_T(folder_path):
    print("\nProcessing Temperature data in folder 'T'...")
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            file_path = os.path.join(folder_path, file)
            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Group by 'H' (Hour) and calculate average temperature
                hourly_avg = df.groupby("H")["T"].mean()

                # Ensure 24 hours exist by filling missing hours with NaN
                hourly_avg = hourly_avg.reindex(range(24), fill_value=None)

                # Save the hourly average as a new Excel file
                new_file_path = os.path.join(folder_path, f"HourlyAvg_{file}")
                hourly_avg.to_excel(new_file_path, index=True, header=["Hourly_Temp"])

                print(f"Processed '{file}' -> '{new_file_path}'")

            except Exception as e:
                print(f"Failed to process '{file}': {e}")


# Function to calculate hourly average of HZTrop(m) and WZTrop(m) in folder Z
def process_trop_data_in_Z(folder_path):
    print("\nProcessing Trop data in folder 'Z'...")
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            file_path = os.path.join(folder_path, file)
            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Rename GPS_Time column if necessary
                gps_time_column = "GPS_Time(yyyy:mm:dd:hh:mm:ss.ssss)"
                if gps_time_column in df.columns:
                    df.rename(columns={gps_time_column: "GPS_Time"}, inplace=True)

                # Convert GPS_Time to datetime and extract hour
                df["GPS_Time"] = pd.to_datetime(df["GPS_Time"], format="%Y:%m:%d:%H:%M:%S.%f", errors="coerce")
                df["Hour"] = df["GPS_Time"].dt.hour

                # Convert HZTrop(m) and WZTrop(m) to millimeters
                df["HZTrop_mm"] = df["HZTrop(m)"] * 1000
                df["WZTrop_mm"] = df["WZTrop(m)"] * 1000

                # Group by hour and calculate averages
                hourly_avg = df.groupby("Hour")[["HZTrop_mm", "WZTrop_mm"]].mean()

                # Ensure 24 hours exist by filling missing hours with NaN
                hourly_avg = hourly_avg.reindex(range(24), fill_value=None)

                # Save the hourly average as a new Excel file
                new_file_path = os.path.join(folder_path, f"HourlyAvg_{file}")
                hourly_avg.to_excel(new_file_path, index=True)

                print(f"Processed '{file}' -> '{new_file_path}'")

            except Exception as e:
                print(f"Failed to process '{file}': {e}")


# Function to delete mismatched files based on dates
def delete_mismatched_files(folder_t, folder_z):
    print("\nDeleting mismatched files based on dates...")
    files_t = set(os.path.splitext(f)[0] for f in os.listdir(folder_t) if f.endswith(".xlsx"))
    files_z = set(os.path.splitext(f)[0] for f in os.listdir(folder_z) if f.endswith(".xlsx"))

    # Find common and mismatched files
    common_files = files_t & files_z
    files_to_delete_t = files_t - common_files
    files_to_delete_z = files_z - common_files

    # Delete files in T
    for file in files_to_delete_t:
        file_path = os.path.join(folder_t, f"{file}.xlsx")
        os.remove(file_path)
        print(f"Deleted '{file}.xlsx' from folder 'T'")

    # Delete files in Z
    for file in files_to_delete_z:
        file_path = os.path.join(folder_z, f"{file}.xlsx")
        os.remove(file_path)
        print(f"Deleted '{file}.xlsx' from folder 'Z'")


# Main function to process both folders
def main():
    main_folder_path = input("Enter the main folder path: ")

    # Define folder paths
    folder_t = os.path.join(main_folder_path, "T")
    folder_z = os.path.join(main_folder_path, "Z")

    # Check if folders exist
    if not os.path.exists(folder_t) or not os.path.exists(folder_z):
        print("Either folder 'T' or 'Z' does not exist. Exiting...")
        return

    # Delete files with missing dates
    delete_mismatched_files(folder_t, folder_z)

    # Process data in both folders
    process_temperature_in_T(folder_t)
    process_trop_data_in_Z(folder_z)


if __name__ == "__main__":
    main()
