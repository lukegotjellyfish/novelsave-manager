import requests

with open ("novelpub-resolved-links.txt", "w") as np:
    with open ("novelpub-links-to-resolve.txt", "r") as f:
        for line in f.readlines():
            response = requests.get(line[:-1], headers={'User-Agent':'Google Chrome'})
            new_url = response.url
            print(f"Resolved {line[:-1]} as {new_url}")
            np.write(f"{new_url}\n")