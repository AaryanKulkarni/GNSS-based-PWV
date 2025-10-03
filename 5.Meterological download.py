import os
import requests


def construct_links(base_url, start, end):
    links = []
    for i in range(start, end + 1):
        num_str = str(i).zfill(3) if i < 100 else str(i)  # Format as 3-digit string
        url = base_url.replace(base_number_str, num_str)  # Replace dynamically
        links.append(url)
    return links


def download_all(urls, save_path):
    for url in urls:
        file_name = url.split('/')[-1]
        file_path = os.path.join(save_path, file_name)
        try:
            print(f"Downloading {file_name} from {url}")

            response = requests.get(url, verify=False)
            response.raise_for_status()  # Check that the request was successful

            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name} to {file_path}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")


if __name__ == "__main__":
    # Accept dynamic values for base_number and upper/lower range
    base_url = input("Enter the base URL (e.g., 'https://garner.ucsd.edu/pub/met/2020/363/iisc3630.20m.Z'): ").strip()
    base_number = int(input("Enter the starting numerical value in the base URL: "))
    base_number_str = str(base_number).zfill(3)  # To ensure '363' formatting matches

    start_num = int(input("Enter the starting number for the range: "))
    end_num = int(input("Enter the upper limit for the numerical range to download: "))

    save_path = input("Enter the directory path where the files should be saved: ").strip()
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    links = construct_links(base_url, start_num, end_num)
    download_all(links, save_path)
