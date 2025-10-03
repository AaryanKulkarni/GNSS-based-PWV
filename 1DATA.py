#     base_url = "https://cddis.nasa.gov/archive/gnss/data/daily/2020/274/20o/iisc2740.20o.Z"
import webbrowser

def construct_links(base_url, start, end):
    links = []
    for i in range(start, end + 1):
        num_str = str(i).zfill(3) if i < 100 else str(i)
        # Replace dynamically based on user-specified start number
        new_url = base_url.replace(base_num_str, num_str).replace(f"iisc{base_num_str}0", f"iisc{num_str}0")
        links.append(new_url)
    return links

def open_links_in_browser(links):
    try:
        print(f"Opening links in the default browser.")
        for url in links:
            webbrowser.open(url)
    except Exception as e:
        print(f"Failed to open URLs: {e}")

if __name__ == "__main__":
    # Prompt the user for the starting number
    start_number = int(input("Enter the starting number: "))
    end_number = int(input("Enter the ending number: "))

    # Dynamically update the base URL
    base_num_str = str(start_number).zfill(3)
    base_url = f"https://cddis.nasa.gov/archive/gnss/data/daily/2020/{base_num_str}/20o/iisc{base_num_str}0.20o.Z"

    links = construct_links(base_url, start_number, end_number)
    open_links_in_browser(links)
