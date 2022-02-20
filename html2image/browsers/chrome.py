from .browser import Browser
from .search_utils import find_chrome

import subprocess
import os


class ChromeHeadless(Browser):
    """
        Chrome/Chromium browser wrapper.

        Parameters
        ----------
        - `executable` : str, optional
            + Path to a chrome executable.

        - `flags` : list of str
            + Flags to be used by the headless browser.
            + Default flags are :
                - '--default-background-color=0'
                - '--hide-scrollbars'
        - `print_command` : bool
            + Whether or not to print the command used to take a screenshot.
    """

    def __init__(self, executable=None, flags=None, print_command=False):
        self.executable = executable
        if not flags:
            self.flags = [
                '--default-background-color=0',
                '--hide-scrollbars',
            ]
        else:
            self.flags = [flags] if isinstance(flags, str) else flags

        self.print_command = print_command

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        self._executable = find_chrome(value)

    def screenshot(
        self,
        input,
        output_path,
        output_file='screenshot.png',
        size=(1920, 1080),
    ):
        """ Calls Chrome or Chromium headless to take a screenshot.

            Parameters
            ----------
            - `output_file`: str
                + Name as which the screenshot will be saved.
                + File extension (e.g. .png) has to be included.
                + Default is screenshot.png
            - `input`: str
                + File or url that will be screenshotted.
                + Cannot be None
            - `size`: (int, int), optional
                + Two values representing the window size of the headless
                + browser and by extention, the screenshot size.
                + These two values must be greater than 0.
            Raises
            ------
            - `ValueError`
                + If the value of `size` is incorrect.
                + If `input` is empty.
        """

        if not input:
            raise ValueError('The `input` parameter is empty.')

        if size[0] < 1 or size[1] < 1:
            raise ValueError(
                f'Could not screenshot "{output_file}" '
                f'with a size of {size}:\n'
                'A valid size consists of two integers greater than 0.'
            )

        # command used to launch chrome in
        # headless mode and take a screenshot
        command = [
            f'{self.executable}',
            '--headless',
            f'--screenshot={os.path.join(output_path, output_file)}',
            f'--window-size={size[0]},{size[1]}',
            *self.flags,
            f'{input}',
        ]

        if self.print_command:
            print(' '.join(command))

        subprocess.run(command)

    def __enter__(self):
        print(
            'Context manager (with ... as:) is',
            f'not supported for {__class__.__name__}.'
        )

    def __exit__(self, *exc):
        pass