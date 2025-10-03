import pandas as pd
import os

# Constants
k2_prime = 17  # K/mbar
k3_prime = 377600  # K^2/mbar
Rv = 461.5  # J/(kg*K)
rho = 1000  # kg/m^3


def calculate_Tm(Ts, is_daytime):
    """
    Calculate Tm based on surface temperature Ts and time of day.

    Parameters:
    Ts (float): Surface temperature (K)
    is_daytime (bool): True if daytime, False if nighttime

    Returns:
    float: Tm (K)
    """
    if is_daytime:
        return 0.6066 * Ts + 113.2914
    else:
        return 0.7938 * Ts + 57.4856


def calculate_K(Tm):
    """
    Calculate K.

    Parameters:
    Tm (float): weighted mean temperature (K)

    Returns:
    float: K
    """
    return 10 ** 6 / (rho * ((k3_prime / Tm) + k2_prime) * Rv)


def calculate_PWV(K, ZWD):
    """
    Calculate PWV.

    Parameters:
    K (float): conversion factor
    ZWD (float): Zenith Wet Delay (mm)

    Returns:
    float: PWV (mm)
    """
    return K * ZWD


def process_files(main_folder_path):
    z_folder = os.path.join(main_folder_path, "Z")
    t_folder = os.path.join(main_folder_path, "T")

    output_data = []

    for z_file in os.listdir(z_folder):
        # Process only files starting with 'HourlyAvg' and ending with '.xlsx'
        if z_file.startswith("HourlyAvg") and z_file.endswith(".xlsx"):
            date_part = z_file.split("_")[1:]  # Extract date components from filename
            date = "_".join(date_part).split(".")[0]  # Extract date string (DD_MM_YYYY)
            formatted_date = pd.to_datetime(date, format="%d_%m_%Y").strftime(
                "%d/%m/%Y"
            )  # Convert to DD/MM/YYYY format

            z_path = os.path.join(z_folder, z_file)
            t_path = os.path.join(t_folder, z_file)

            if not os.path.exists(t_path):
                print(f"Temperature file for {formatted_date} not found. Skipping.")
                continue

            # Read Z and T files
            z_data = pd.read_excel(z_path)
            t_data = pd.read_excel(t_path)

            # Convert temperature from Celsius to Kelvin
            t_data["Hourly_Temp"] = t_data["Hourly_Temp"] + 273.15

            # Merge data on Hour
            merged_data = pd.merge(z_data, t_data, left_on="Hour", right_on="H")
            merged_data["is_daytime"] = merged_data["Hour"].apply(
                lambda h: 6 <= h <= 18
            )
            merged_data["Tm"] = merged_data.apply(
                lambda row: calculate_Tm(row["Hourly_Temp"], row["is_daytime"]), axis=1
            )
            merged_data["K"] = merged_data["Tm"].apply(calculate_K)
            merged_data["PWV"] = merged_data.apply(
                lambda row: calculate_PWV(row["K"], row["WZTrop_mm"]), axis=1
            )

            # Multiply PWV values by 100 and include formatted date
            merged_data["PWV"] = merged_data["PWV"] * 100
            merged_data["Date"] = formatted_date

            output_data.append(merged_data[["Date", "Hour", "PWV"]])

    if output_data:
        result = pd.concat(output_data, ignore_index=True)
        result.to_excel(os.path.join(main_folder_path, "PWV_Results.xlsx"), index=False)
        print(f"PWV values saved to 'PWV_Results.xlsx'.")
    else:
        print("No data processed.")


if __name__ == "__main__":
    main_folder_path = input("Enter the path to the main folder: ").strip()
    process_files(main_folder_path)

