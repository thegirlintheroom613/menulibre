# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Sean Davis <smd.seandavis@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import os

from gi.repository import Gtk

home = os.getenv('HOME')

default_application = """
[Desktop Entry]
Version=1.0
Type=Application
Name=New Application
Comment=My New Application
Icon=
Exec=
Path=
Terminal=false
StartupNotify=false
Categories=
"""

sudo = os.getuid() == 0

class Application:
	"""Application class that uses data from .desktop files installed 
	both system-wide (/usr/share/applications) and locally 
	(/home/USERNAME/.local/share/applications)."""
    def __init__(self, filename):
        if not os.path.isfile(filename):
            self.new(filename)
        else:
            self.new_from_file(filename)

    def new(self, filename):
		"""Create a new application instance for a non-existing file."""
        self.filename = filename
        self.icon = 'gtk-missing-image'
        self.name = 'New Application'
        self.comment = 'My New Application'
        self.genericname = ''
        self.command = ''
        self.executable = ''
        self.path = ''
        self.terminal = False
        self.startupnotify = False
        self.categories = []
        self.actions = None
        self.id = None
        self.TreeViewPath = None
        self.original = default_application

    def new_from_file(self, filename):
		"""Create a new application instance for an existing filename."""
        self.filename = filename
        self.id = 0

        desktop_file = open(filename, 'r')
        settings = read_desktop_file( filename, desktop_file.read() )
        desktop_file.close()
        
        self.name = settings['name']
        self.icon = settings['icon']
        self.comment = settings['comment']
        self.genericname = settings['genericname']
        self.command = settings['command']
        self.executable = settings['executable']
        self.path = settings['path']
        self.terminal = settings['terminal']
        self.startupnotify = settings['startupnotify']
        self.hidden = settings['hidden']
        self.categories = settings['categories']
        self.quicklist_format = settings['quicklist_format']
        self.actions = settings['quicklists']
        self.original = settings['text']

    def set_filename(self, filename):
		"""Set the application filename."""
        self.filename = filename

    def get_filename(self):
		"""Return the application filename."""
        return self.filename

    def set_icon(self, name):
		"""Set the application icon name."""
        self.icon = name

    def get_icon(self):
		"""Return the application icon name."""
        return self.icon

    def set_name(self, name):
		"""Set the application proper name."""
        self.name = name

    def get_name(self):
		"""Return the application proper name."""
        return self.name

    def set_comment(self, comment):
		"""Set the application comment."""
        self.comment = comment

    def get_comment(self):
		"""Return the application comment."""
        return self.comment
        
    def set_genericname(self, name):
        self.genericname = name
        
    def get_genericname(self):
        return self.genericname

    def set_exec(self, command):
		"""Set the application command."""
        self.command = command

    def get_exec(self):
		"""Return the application command."""
        return self.command
        
    def set_executable(self, executable):
        self.executable = executable
        
    def get_executable(self):
        return self.executable

    def set_path(self, path):
		"""Set the application working directory."""
        self.path = path

    def get_path(self):
		"""Return the application working directory."""
        return self.path

    def set_terminal(self, terminal):
		"""Set whether the application runs in the terminal."""
        self.terminal = terminal

    def get_terminal(self):
		"""Return whether the application runs in the terminal."""
        return self.terminal

    def set_startupnotify(self, startupnotify):
		"""Set whether the application should notify on startup."""
        self.startupnotify = startupnotify

    def get_startupnotify(self):
		"""Return whether the application should notify on startup."""
        return self.startupnotify

    def set_categories(self, categories):
		"""Set the application categories."""
        self.categories = categories

    def get_categories(self):
		"""Return the application categories."""
        return self.categories
            
    def set_hidden(self, hidden):
		"""Set whether the application menu item is hidden."""
        self.hidden = hidden
        
    def get_hidden(self):
		"""Return whether the application menu item is hidden."""
        return self.hidden
        
    def set_quicklist_format(self, qformat):
		"""Set the application quicklist format, commonly 'Actions' or 
		'X-Ayatana-Desktop-Shortcuts'."""
        self.quicklist_format = qformat
        
    def get_quicklist_format(self):
		"""Return the application quicklist format."""
        return self.quicklist_format

    def set_actions(self, actions):
		"""Set the application quicklist items."""
        self.actions = actions

    def get_actions(self):
		"""Return the application quicklist items."""
        return self.actions

    def set_id(self, id):
		"""Set the application ID, used for identifying the launcher in 
		a selection window."""
        self.id = id

    def get_id(self):
		"""Return the application ID."""
        return self.id

    def set_original(self, original):
		"""Set the application original .desktop contents."""
        self.original = original

    def get_original(self):
		"""Return the application original .desktop contents."""
        return self.original
        
def get_applications():
	"""Return all installed applications for the current user.  If the
	program is started as root, only show system launchers."""
    applications = dict()
    app_counter = 1
    filenames = []
    if not sudo:
        for (path, dirs, files) in os.walk( os.path.join( home, '.local', 'share', 'applications' ) ):
            for filename in files:
                if os.path.splitext( filename )[1] == '.desktop':
                    filenames.append(filename)
                    app = Application(os.path.join( path, filename ))
                    app.id = app_counter
                    app_counter += 1
                    applications[app.id] = app
    for (path, dirs, files) in os.walk( '/usr/share/applications' ):
        for filename in files:
            if os.path.splitext( filename )[1] == '.desktop':
                filenames.append(filename)
                app = Application(os.path.join( path, filename ))
                app.id = app_counter
                app_counter += 1
                applications[app.id] = app
    return applications
    
defaults = {'filename': '', 'icon': 'application-default-icon', 'name': '', 
            'comment': '', 'command': '', 'path': '', 'terminal': False, 
            'startupnotify': False, 'hidden': False, 'categories': [], 
            'quicklists': dict(), 'quicklist_format': 'actions', 'id': 0, 
            'text': default_application}
    
def read_desktop_file(filename, contents):
    """Return the settings pulled from the application .desktop file."""
    settings = {'filename': '', 'icon': 'application-default-icon', 'name': '', 
            'comment': '', 'genericname': '', 'command': '', 'executable': '', 
            'path': '', 'terminal': False, 'startupnotify': False, 
            'hidden': False, 'categories': [], 'quicklists': dict(), 
            'quicklist_format': 'actions', 'id': 0, 'text': default_application}
    settings['text'] = contents
    settings['filename'] = filename
    quicklist_key = None
    action_order = 0
    for line in contents.split('\n'):
        try:
            if line.lower().startswith('icon='):
                settings['icon'] = line[5:]
            elif line.lower().startswith('name='):
                if settings['name'] == '':
                    settings['name'] = line[5:]
                else:
                    settings['quicklists'][quicklist_key]['name'] = line[5:]
            elif line.lower().startswith('comment='):
                settings['comment'] = line[8:]
            elif line.lower().startswith('genericname='):
                settings['genericname'] = line[12:]
            elif line.lower().startswith('exec='):
                if settings['command'] == '':
                    settings['command'] = line[5:]
                    settings['executable'] = line[5:].split(' ')[0]
                else:
                    settings['quicklists'][quicklist_key]['command'] = line[5:]
            elif line.lower().startswith('path='):
                settings['path'] = line[5:]
            elif line.lower().startswith('terminal='):
                settings['terminal'] = 'true' in line[9:]
            elif line.lower().startswith('startupnotify='):
                settings['startupnotify'] = 'true' in line[14:]
            elif line.lower().startswith('nodisplay='):
                settings['hidden'] = 'true' in line[10:]
            elif line.lower().startswith('categories='):
                settings['categories'] = line[11:].split(';')
                try:
                    settings['categories'].remove('')
                except ValueError:
                    pass
            elif line.lower().startswith('actions=') or line.lower().startswith('x-ayatana-desktop-shortcuts'):
                settings['quicklist_format'], enabled = line.split('=')
                enabled = enabled.split(';')
            elif line.startswith('[') and not line.lower().startswith('[desktop entry]'):
                if '[desktop action ' in line.lower():
                    quicklist_key = line[16:].replace(']', '')
                elif ' shortcut group]' in line.lower():
                    quicklist_key = line[1:][:len(line)-17]
                settings['quicklists'][quicklist_key] = dict()
                settings['quicklists'][quicklist_key]['order'] = action_order
                action_order += 1
                settings['quicklists'][quicklist_key]['enabled'] = quicklist_key in enabled
        except (IndexError, UnboundLocalError):
            pass
    # Check for uncategorized WINE applications...
    if len(settings['categories']) == 0:
        if 'wine' in os.path.split(settings['filename'])[0]:
            settings['categories'].append('Wine')
    return settings
