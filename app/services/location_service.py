import requests


def get_location_from_ip(ip: str):
    url = f"https://ipwho.is/{ip}"

    response = requests.get(url, timeout=(3.05, 5))
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    print(get_location_from_ip("8.8.8.8"))
