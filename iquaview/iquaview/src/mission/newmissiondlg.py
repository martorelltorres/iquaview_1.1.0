"""
Copyright (c) 2018 Iqua Robotics SL

This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

"""
 Dialog to ask the user to name a new mission
"""

from PyQt5.QtWidgets import QDialog
from iquaview.src.ui.ui_new_mission_dlg import Ui_NewMissionDlg


class NewMissionDlg(QDialog, Ui_NewMissionDlg):
    def __init__(self):
        super(NewMissionDlg, self).__init__()
        self.setupUi(self)

    def get_mission_name(self):
        """ Get mission name"""
        name = self.nameText.text()
        if name.rfind('/') != -1:
            name = name.replace('/', '')
        return name
