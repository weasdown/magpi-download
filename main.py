# Program to automatically download every issue of Raspberry Pi's MagPi magazine.

from bs4 import BeautifulSoup
import json
import os
from pathlib import Path
import requests
import sys

# download_folder: Path = Path(r'')
download_folder: Path = Path(r'D:\Resources\Raspberry Pi magazines\MagPi') if sys.platform == 'win32' else Path('MagPis')

class Issue:
    def __init__(self, issue_number: int):
        """An individual issue of the MagPi magazine."""
        self.issue_number: int = issue_number

    def download(self, save_folder: Path) -> None:
        """
        Downloads the free PDF of an issue and saves it to the save_folder.

        :param save_folder: The folder to save the downloaded issue PDF to.
        :type save_folder: Path
        :return: None
        :rtype: NoneType
        """

        magpi_root_url: str = 'https://magpi.raspberrypi.com'

        response: requests.Response = requests.get(self.url)

        if response.status_code == 200:
            # Parse HTML soup with BeautifulSoup.
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get all the hrefs in the page.
            link_hrefs: list[str]  = [link.get('href') for link in soup.find_all('a')]

            # Get the href to download the PDF.
            download_href: str = [link for link in link_hrefs if link.startswith('/downloads/')][0]

            download_url: str = magpi_root_url + download_href  # Build the PDF download URL.
            download: requests.Response = requests.get(download_url)  # Download the PDF.

            # Save the PDF to a file
            with open(os.path.join(save_folder, self.file_name), 'wb') as file:
                file.write(download.content)
            print(f'Issue {self.issue_number} downloaded successfully')
        else:
            print(f'\n!! Failed to download issue {self.issue_number}. Status code: {response.status_code}')

    @property
    def file_name(self)->str:
        """Gets the file name for this issue."""
        return f'Magpi{self.issue_number}.pdf'

    @property
    def url(self)-> str:
        """
        Gets the URL for an individual MagPi issue's PDF.

        :return: The URL to download the magazine issue's PDF.
        :rtype: str
        """
        return f'https://magpi.raspberrypi.com/issues/{self.issue_number}/pdf/download'


# TODO find the latest_issue by reading the top item at https://magpi.raspberrypi.com/issues
def latest_issue() -> int:
    """Gets the latest issue number."""
    latest: int = 149  # as of 29/1/25
    return latest


def download_all() -> None:
    """Download all MagPi PDFs."""
    for issue in range(1, latest_issue()+1):
        issue_object: Issue = Issue(issue)
        issue_object.download(download_folder)


if __name__ == '__main__':
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    print('download_all() would now be called')
    sys.exit(0)  # TODO remove print and sys.exit()
    download_all()

    # To download a single issue:
    # Issue(149).download(download_folder)
