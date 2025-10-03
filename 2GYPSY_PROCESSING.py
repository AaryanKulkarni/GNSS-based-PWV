from gdgps_apps.apps import APPS
from gdgps_apps import defines
import os
import time
import threading

# Set paths
#"portal": "https://pppx.gdgps.net/"
settings_file = r""  # Path to APPS settings file
data_folder = r""  # Path to orbital files

# Initialize APPS client with settings file
apps = APPS(settings_file=settings_file, log_level=None)

# Flag to indicate if the program is running
running = True

def process_file(file_name, file_id):
    """Handles processing and downloading of a file after upload."""
    while running:
        try:
            info = apps.detail(file_id)

            if info['state'] == defines.Data.AVAILABLE:
                path = apps.download_result(file_id)
                print(f'Retrieved results for {file_name}, downloaded to {path}.')

                # Delete unnecessary data
                apps.delete_data(file_id)
                return  # Exit thread

            elif info['state'] == defines.Data.ERROR:
                for flag in info['flags']:
                    if flag['level'] == defines.DataFlag.ERROR:
                        print(f'APPS encountered an error processing {file_name}: ({flag["header"]}) {flag["detail"]}')

                apps.delete_data(file_id)
                return  # Exit thread

            elif info['state'] == defines.Data.VERIFIED:
                apps.approve(file_id)  # Approve for processing

            time.sleep(10)  # Wait before checking status again

        except Exception as e:
            if not running:
                break  # Stop the thread when interrupted
            print(f"Error processing {file_name}: {e}")
            time.sleep(10)


if __name__ == '__main__':
    try:
        # Get all files in the specified folder
        files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]

        threads = []

        # Upload and process files in parallel
        for file_name in files:
            file_path = os.path.join(data_folder, file_name)
            print(f'Uploading {file_name}...')
            file_id = apps.upload_gipsyx(file_path)['id']

            # Start processing as soon as the file is uploaded
            t = threading.Thread(target=process_file, args=(file_name, file_id))
            t.start()
            threads.append(t)

        print("All files are being uploaded and processed in parallel.")

        # Keep the main thread running until all processing is done
        for t in threads:
            t.join()

    except KeyboardInterrupt:
        print("\nExecution interrupted by user. Stopping all processes...")

        running = False  # Stop all threads
