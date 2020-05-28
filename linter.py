###
# Erlang linter plugin for SublimeLinter3
# Uses erlc, make sure it is in your PATH
#
# Copyright (C) 2014  Clement 'cmc' Rey <cr.rey.clement@gmail.com>
#
# MIT License
###

"""This module exports the Erlc plugin class."""

import os
import tempfile
from SublimeLinter.lint import Linter, util


class Erlc(Linter):
    """Provides an interface to erlc."""

    tempfile_suffix = "-"

    # ERROR FORMAT # <file>:<line>: [Warning:|] <message> #
    regex = (
        r".+:(?P<line>\d+):"
        r"(?:(?P<warning>\sWarning:\s)|(?P<error>\s))"
        r"+(?P<message>.+)"
    )

    error_stream = util.STREAM_STDOUT

    defaults = {
        "selector": "source.erlang",
        "include_dirs": []
    }

    def lint(self, *args):
        # print("SublimeLinter-erlc lint: %s" % self.filename)
        if not self.filename.endswith(".erl"): # filter out .hrl
            return []

        return super().lint(*args)

    def cmd(self):
        """
        return the command line to execute.

        this func is overridden so we can handle included directories.
        """

        command = ['erlc', '-W']

        settings = self.settings
        dirs = settings.get('include_dirs', [])
        pa_dirs = settings.get('pa_dirs', [])
        pz_dirs = settings.get('pz_dirs', [])
        output_dir = settings.get('output_dir', tempfile.gettempdir())

        root = self.find_root(self.filename)
        if root:
            command.extend(["-I", os.path.join(root, "include")])

        for d in dirs:
            command.extend(["-I", d])

        for d in pa_dirs:
            command.extend(["-pa", d])

        for d in pz_dirs:
            command.extend(["-pz", d])

        command.extend(["-o", output_dir])

        command.extend(["$file_on_disk"])

        return command

    def find_root(self, fn):
        """find ebin folder in parent"""
        parent = os.path.dirname(fn)
        while True:
            if os.path.isdir(os.path.join(parent, 'ebin')):
                return parent

            parent = os.path.dirname(parent)
            if not parent:
                break

        return None
