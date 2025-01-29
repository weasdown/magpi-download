# Program to automatically download every issue of Raspberry Pi's MagPi magazine.

download_folder: str = 'D:\Resources\Raspberry Pi magazines\MagPi'


def url(issue: int)-> str:
    """
    Gets the URL for an individual MagPi issue's PDF.

    :param issue: The issue number for the required magazine.
    :type issue: int
    :return: The URL to download the magazine issue's PDF.
    :rtype: str
    """
    return f'https://magpi.raspberrypi.com/issues/{issue}/pdf/download'


latest_issue: int = 149  # as of 29/1/25

