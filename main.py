# Program to automatically download every issue of Raspberry Pi's MagPi magazine.

import argparse
import os
from argparse import ArgumentError
from pathlib import Path

import requests
from bs4 import BeautifulSoup

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

        print(f'\nDownloading issue {self.issue_number}')

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
                # TODO get date that issue will be available from button that replaces "No thanks, take me to the free PDF" link if not available e.g. https://magpi.raspberrypi.com/issues/150/contributions/new
                raise ValueError(f'No download is available for issue {self.issue_number}')

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
    url: str = 'https://magazine.raspberrypi.com/issues'
    
    # TODO refactor to use link on page that says 'Raspberry Pi Official Magazine issue [latest] out now!'. Will mean links can be filtered earlier, so quicker to run.

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


def download_all(save_path: Path) -> None:
    """Download all MagPi PDFs."""
    for issue in range(1, latest_issue+1):
        issue_object: Issue = Issue(issue)
        issue_object.download(save_path)


if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(description=help_description)

    # Adding optional argument
    parser.add_argument('-a', '--all', help='Download all available issues', required=False)

    # Add optional argument for download path
    parser.add_argument('-p','--path', help='The path that the PDFs will be stored in once downloaded', required=False)

    # Add optional argument for issue number
    parser.add_argument('-i', '--issue', help='A single issue number to download', required=False, type=int, action='append', nargs='+')

    # Read arguments from command line
    args = parser.parse_args()

    default_download_folder: Path = Path('MagPis')
    download_folder: Path = Path(args.path) if args.path is not None else default_download_folder
    if not os.path.exists(download_folder):
        print(f'\t- Directory {download_folder} does not exist - making it...')
        print(f'\t- Directory {download_folder} does not exist - making it...')
        os.mkdir(download_folder)
        print(f'\t- Created directory {download_folder}')

    # TODO remove
    latest: int = latest_issue()
    print(f'\nThe latest issue is {latest}.\n')

    issues: list[int] | None = args.issue[0] if args.issue is not None else None  # Get the list of issue numbers for issues that the user wants to download.
    issues_to_download: list[int] = [int(issue_number) for issue_number in issues] if issues is not None else None

    # # To download all issues:
    # download_all()

    # # To download a single issue, where 149 is the issue number:
    # Issue(149).download(download_folder)

    # # To download only the latest issue:
    # Issue(latest).download(download_folder)

    if issues_to_download is None:
        print('No issue argument was given, so downloading all issues.\n')
        download_all(download_folder)
    else:
        if args.all is not None:
            raise ArgumentError(args.all, 'Cannot determine which issues to download when -i/--issue and -a/--all are both set. Please use one or the other.')
        else:
            issues_to_download_text: str = '\n'.join([f'\t- {issue}' for issue in issues_to_download]) if issues_to_download is not None else "All"
            print(f'Issue(s) to download:\n{issues_to_download_text}\n')
            print(f'Downloading to path: {download_folder}')
            for issue_num in issues_to_download:
                issue: Issue = Issue(issue_num)
                issue.download(download_folder)

    print('\nDone!')
