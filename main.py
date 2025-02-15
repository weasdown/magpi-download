# Program to automatically download every issue of Raspberry Pi's MagPi magazine.

import argparse
from argparse import ArgumentError

from bs4 import BeautifulSoup
import os
from pathlib import Path
import requests
import sys

help_description = "A Python program to download free PDFs of Raspberry Pi's MagPi magazine."

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
latest_issue: int = 149  # as of 29/1/25


def download_all(save_path: Path) -> None:
    """Download all MagPi PDFs."""
    for issue in range(1, latest_issue+1):
        Issue(issue).download(save_path)        


if __name__ == '__main__':
    download_folder: Path = Path('D:/Resources/Raspberry Pi magazines/MagPi') if sys.platform == 'win32' else Path('MagPis')
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    # Initialize parser
    parser = argparse.ArgumentParser(description=help_description)

    # Adding optional argument
    parser.add_argument('-a', '--all', help='Download all available issues', required=False)

    # Add optional argument for download path
    parser.add_argument('-p','--path', help='The path that the PDFs will be stored in once downloaded', required=False)

    # Add optional argument for issue number
    parser.add_argument('-i', '--issue', help='A single issue number to download', required=False, type=int)

    # Read arguments from command line
    args = parser.parse_args()

    default_download_folder: Path =Path(r'D:\Resources\Raspberry Pi magazines\MagPi')
    download_folder: Path = Path(args.path) if args.path is not None else default_download_folder

    issue_num: int | None = args.issue

    print(f'Issue(s) to download: {issue_num if issue_num is not None else 'All'}')
    if issue_num is None:
        print('No issue argument was given, so downloading all issues.\n')
        download_all(download_folder)
    else:
        if args.all is not None:
            raise ArgumentError(args.all, 'Cannot determine which issues to download when -i/--issue and -a/--all are both set. Please use one or the other.')
        else:
            print(f'\nDownloading issue {issue_num} to path "{download_folder}"')
            Issue(issue_num).download(download_folder)

    print('\nDone!')
