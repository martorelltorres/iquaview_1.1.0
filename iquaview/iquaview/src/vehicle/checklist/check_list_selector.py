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
 Dialog to select from different check list xml files located in the auv_configs path.
"""

import logging
from PyQt5.QtWidgets import QDialog
from iquaview.src.ui.ui_select_checklist import Ui_ChecklistSelector
from iquaview.src.xmlconfighandler.checklisthandler import CheckListHandler

logger = logging.getLogger(__name__)


class ChecklistSelectorDlg(QDialog, Ui_ChecklistSelector):

    def __init__(self, config, parent=None):
        super(ChecklistSelectorDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Select Checklist")
        self.config = config
        self.check_list_comboBox.clear()

        cl_handler = CheckListHandler(self.config)
        lists = cl_handler.get_check_lists()

        for chk_list in lists:
            logger.debug(chk_list.get('id'))
            self.check_list_comboBox.addItem(chk_list.get('id'))

    def get_current_check_list(self):
        return str(self.check_list_comboBox.currentText())
