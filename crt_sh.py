import requests
from bs4 import BeautifulSoup
import re


def fetch_crt_sh_html(search_domain):
    """Fetches the HTML from crt.sh for the given search domain"""

    url = f"https://crt.sh/?q=.{search_domain}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def extract_hosts(raw_html):
    """ Find the host names using regex, trim them, and append to a set (no duplicate records) """

    hosts = set()

    raw_list = re.findall(r"(\>.*?\.[a-zA-Z0-9].*?\.[a-zA-Z0-9].*?\<)", str(raw_html))
    for i in raw_list:

        if "<br/>" in i:
            host = i.split("<br/>")
            host = host[1].split("<")
            host = host[0]
            if host.startswith("*."):
                host = host.split("*.")
                host = host[1]
            if host:
                hosts.add(host)

        elif ">" in i:
            host = i.split(">")
            host = host[1].split("<")
            host = host[0]
            if host.startswith("*."):
                host = host.split("*.")
                host = host[1]
            if host:
                hosts.add(host)

    return hosts


def write_to_file(data, file, mode="a"):
    """ Write data to a file. Default write mode=append """

    with open(file, mode) as new_file:
        new_file.write(str(data + "\r\n"))
        new_file.close()


def main():
    # Ask the user for the output filename
    file_name = input("Enter the desired filename for the extracted hosts (e.g., scraped_hosts.txt): ")

    domain = input("Enter the domain to search: ")
    soup = fetch_crt_sh_html(domain)
    hosts = extract_hosts(soup)
    for i in hosts:
        write_to_file(i, file_name)

    print(f"Extracted hostnames written to: {file_name}")


if __name__ == "__main__":
    main()
