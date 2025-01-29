# Program to automatically download every issue of Raspberry Pi's MagPi magazine.

from bs4 import BeautifulSoup
import json
import os
from pathlib import Path
import requests

download_folder: Path = Path(r'D:\Resources\Raspberry Pi magazines\MagPi')


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

        print(f'\nIssue {self.issue_number}:')
        print(f'\t- Downloading from {self.url}')

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
            print(f'\t- Issue {self.issue_number} downloaded successfully')
        else:
            print(f'\t- Failed to download issue {self.issue_number}! Status code: {response.status_code}')

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


latest_issue: int = 149  # as of 29/1/25


def download_all() -> None:
    """Download all MagPi PDFs."""
    for issue in range(1, latest_issue+1):
        issue_object: Issue = Issue(issue)
        issue_object.download(download_folder)


download_all()
