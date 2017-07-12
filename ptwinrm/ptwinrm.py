# -*- coding: utf-8 -*-
#
# This file is part of the ptwinrm project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""WinRM console

Usage:
  winrm [--user=<user>]
        [--password=<password>]
        [--transport=<transport>]
        [--run=<cmd>] <host>

Options:
  -h --help                show this
  --user=<user>            user name
  --password=<password>    password on the command line
  --transport=<transport>  [default: ntlm]. Valid: 'kerberos', 'ntlm'
  --run=<cmd>              command to execute (if not given, a console starts)
"""

from __future__ import unicode_literals
from __future__ import print_function

import sys
from functools import partial

import winrm
import winrm.exceptions
import requests.exceptions
from docopt import docopt
from prompt_toolkit import prompt
from prompt_toolkit.keys import Keys
from prompt_toolkit.token import Token
from prompt_toolkit.filters import Always, Never
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.key_binding.manager import KeyBindingManager


class WinRMConsole(object):
    """WinRM Console"""

    def __init__(self, session):
        self.session = session
        self.multiline = False

    @property
    def username(self):
        return self.session.protocol.username

    @property
    def url(self):
        return self.session.url

    def run_cmd_line(self, cmd_line):
        try:
            return self.__run_cmd_line(cmd_line)
        except (winrm.exceptions.InvalidCredentialsError,
                requests.exceptions.ConnectionError) as error:
            print('ERROR:', error)

    def __run_cmd_line(self, cmd_line):
        if not cmd_line.strip():
            return
        if '\n' in cmd_line:
            return self.session.run_ps(cmd_line)
        else:
            cmd = cmd_line.split()
            return self.session.run_cmd(cmd[0], cmd[1:])

    def handle_cmd_result(self, result):
        if result is None:
            return
        if result.status_code:
            print('ERROR ({0}): {1}'.format(result.status_code, result.std_err))
        else:
            print(result.std_out)
            if result.std_err:
                print('ERROR: {0}'.format(result.std_err))
        return result

    def toggle_multiline(self):
        self.multiline = not self.multiline
        return self.multiline

    def get_prompt(self):
        r = self.run_cmd_line('cd')
        return r.std_out.strip()

    def rep(self, cmd_line):
        result = self.run_cmd_line(cmd_line)
        return self.handle_cmd_result(result)

    def repl(self):
        history = InMemoryHistory()
        auto_suggest = AutoSuggestFromHistory()
        manager = KeyBindingManager.for_prompt()

        @manager.registry.add_binding(Keys.ControlT)
        def _(event):
            def update_multiline():
                multiline = self.toggle_multiline()

                if multiline:
                    event.cli.current_buffer.is_multiline = Always()
                else:
                    event.cli.current_buffer.is_multiline = Never()
                print('Set multiline', multiline and 'ON' or 'off')
            event.cli.run_in_terminal(update_multiline)

        def get_bottom_toolbar_tokens(cli):
            msg = ' Connected as {0} to {1}'.format(self.username, self.url)
            ml = ' Multiline is {0}'.format(self.multiline and 'ON' or 'off')
            return [(Token.Toolbar.Connection, msg),
                    (Token.Toolbar.Multiline, ml)]

        style = style_from_dict({
            Token.Toolbar.Connection: '#ffffff bg:#009900',
            Token.Toolbar.Multiline: '#ffffff bg:#ee0000',
        })

        ppt = partial(prompt, history=history, auto_suggest=auto_suggest,
                      get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                      key_bindings_registry=manager.registry,
                      style=style)

        while True:
            try:
                cmd_line = ppt(self.get_prompt() + '>' ,
                               multiline=self.multiline)
                self.rep(cmd_line)
            except (EOFError, KeyboardInterrupt):
                print('\nCtrl-C pressed. Bailing out!')
                break
            except:
                sys.excepthook(*sys.exc_info())


def main():
    opt = docopt(__doc__, help=True)
    user = opt['--user'] or prompt('user: ')
    password = opt['--password'] or prompt('password: ', is_password=True)
    transport = opt['--transport']
    host = opt['<host>']

    session = winrm.Session(host, (user, password), transport=transport)
    console = WinRMConsole(session)

    if opt['--run']:
        cmd_result = console.rep(opt['--run'])
        code = cmd_result.status_code if cmd_result else 1
        sys.exit(code)

    console.repl()


if __name__ == '__main__':
    main()
