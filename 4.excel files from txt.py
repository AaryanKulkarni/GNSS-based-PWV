import os
import pandas as pd


def import_and_save_as_excel(folder_path):
    # Get all .txt files in the specified folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the specified folder.")
        return

    for txt_file in txt_files:
        text_file_path = os.path.join(folder_path, txt_file)

        try:
            # Read the text file starting from the header line containing 'Secs_from_start'
            with open(text_file_path, 'r') as file:
                lines = file.readlines()

            # Find the line index where 'Secs_from_start' is located
            header_line_index = None
            for i, line in enumerate(lines):
                if "Secs_from_start" in line:
                    header_line_index = i
                    break

            if header_line_index is None:
                print(f"'Secs_from_start' not found in: {text_file_path}")
                continue

            # Use pandas to read the file starting from the identified header line
            data = pd.read_csv(
                text_file_path,
                sep=r'\s+',
                skiprows=header_line_index,
                header=0
            )

            # Save the data to an Excel file
            output_excel_path = os.path.join(folder_path, f"{os.path.splitext(txt_file)[0]}_data.xlsx")
            data.to_excel(output_excel_path, index=False)
            print(f"Data successfully saved to: {output_excel_path}")

        except Exception as e:
            print(f"Error processing file {text_file_path}: {e}")


if __name__ == "__main__":
    folder_path = input("Enter the folder path containing .txt files: ").strip()
    if os.path.exists(folder_path):
        import_and_save_as_excel(folder_path)
    else:
        print("The specified folder path does not exist.")


