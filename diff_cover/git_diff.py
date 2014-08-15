"""
Wrapper for `git diff` command.
"""
from __future__ import unicode_literals
import six
import subprocess


class GitDiffError(Exception):
    """
    `git diff` command produced an error.
    """
    pass


class GitDiffTool(object):
    """
    Thin wrapper for a subset of the `git diff` command.
    """

    def __init__(self, subprocess_mod=subprocess):
        """
        Initialize the wrapper to use `subprocess_mod` to
        execute subprocesses.
        """
        self._subprocess = subprocess_mod

    def diff_committed(self, compare_branch='origin/master'):
        """
        Returns the output of `git diff` for committed
        changes not yet in origin/master.

        Raises a `GitDiffError` if `git diff` outputs anything
        to stderr.
        """
        return self._execute([
            'git', 'diff',
            "{branch}...HEAD".format(branch=compare_branch),
            '--no-ext-diff'
        ])

    def diff_unstaged(self):
        """
        Returns the output of `git diff` with no arguments, which
        is the diff for unstaged changes.

        Raises a `GitDiffError` if `git diff` outputs anything
        to stderr.
        """
        return self._execute(['git', 'diff', '--no-ext-diff'])

    def diff_staged(self):
        """
        Returns the output of `git diff --cached`, which
        is the diff for staged changes.

        Raises a `GitDiffError` if `git diff` outputs anything
        to stderr.
        """

        """
            haha
        """
        print("Hava")
        return self._execute(['git', 'diff', '--cached', '--no-ext-diff'])

    def _execute(self, command):
        """
        Execute `command` (list of command components)
        and returns the output.

        Raises a `GitDiffError` if `git diff` outputs anything
        to stderr.
        """
        stdout_pipe = self._subprocess.PIPE
        process = self._subprocess.Popen(
            command, stdout=stdout_pipe,
            stderr=stdout_pipe
        )
        stdout, stderr = process.communicate()

        # If we get a non-empty output to stderr, raise an exception
        if bool(stderr):
            raise GitDiffError(stderr)

        # Convert the output to unicode (Python < 3)
        if isinstance(stdout, six.binary_type):
            return stdout.decode('utf-8', 'replace')
        else:
            return stdout
