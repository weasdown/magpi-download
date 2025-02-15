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
            link_hrefs: list[str] = [link.get('href') for link in soup.find_all('a')]

            # Get the href to download the PDF.
            try:
                download_href: str = [link for link in link_hrefs if link.startswith('/downloads/')][0]
            except IndexError as ie:
                raise RuntimeError(f'No download is available for issue {self.issue_number}')

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


def latest_issue() -> int:
    """Gets the number of the latest issue."""
    url: str = 'https://magpi.raspberrypi.com/issues'
    
    # Parse HTML soup with BeautifulSoup.
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    # Search soup for links (hrefs) that include "/issues/[issue number]" in their URL.
    # Get all the hrefs in the page.
    link_hrefs: list[str] = [link.get('href') for link in soup.find_all('a')]
    
    # Remove leading "/issues/" and trailing "/pdf" from each link in which they appear, leaving just the issue number that we then make an int.
    issue_nums: list[int] = [int(link.replace('/issues/', '').replace('/pdf', '')) for link in link_hrefs if link.startswith('/issues/')]

    # Remove duplicate issue numbers and sort ascending
    issue_nums: list[int] = list(set(issue_nums))
    latest: int = issue_nums[-1]  # As the numbers are sorted ascending, the latest issue is the last one in the list.

    return latest


def download_all() -> None:
    """Download all MagPi PDFs."""
    for issue in range(1, latest+1):
        Issue(issue).download(download_folder)


if __name__ == '__main__':
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    latest: int = latest_issue()  # TODO remove
    print(f'The latest issue is {latest}.\n')

    # To download all issues:
    # download_all()

    # To download a single issue, where 149 is the issue number:
    # Issue(149).download(download_folder)

    # To download only the latest issue:
    Issue(latest).download(download_folder)
