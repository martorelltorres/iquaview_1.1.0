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
 Classes to load summary  dialog
"""

import datetime

from iquaview.src.ui import ui_summary_checklist
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog


class LoadSummaryDialog(QDialog, ui_summary_checklist.Ui_Summary):
    def __init__(self, checklist_name, parent=None):
        super(LoadSummaryDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Summary of " + checklist_name)
        self.checklist_name = checklist_name
        self.save_pushButton.clicked.connect(self.save_summary)
        self.comments_textEdit.setPlaceholderText("Add a comment...")

        self.summary = list()

    def set_summary(self, check_list):
        """
        Load a summary from a checklist.

        :param check_list: list with check_list items
        :type check_list: list
        """
        for item in check_list:
            for topic in item.check_topics:
                for field in topic.topic.fields:
                    self.set_summary_line(topic.name.text, item.correct_values, field.field_description.text,
                                          field.field_value)

                    if item.correct_values:
                        state = 'Ok'
                    else:
                        state = 'Fail'
                    self.summary.append(state + ', ' +
                                        topic.name.text + ', ' +
                                        field.field_description.text + ', ' +
                                        str(field.field_value))
            for action in item.check_actions:
                self.set_summary_line(action.get_name(), item.correct_values)

                if item.correct_values:
                    state = 'Ok'
                else:
                    state = 'Fail'
                self.summary.append(state + ', ' +
                                    action.get_name())

        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        scroll_layout = self.scrollContents.layout()
        scroll_layout.addItem(spacer_item)

    def set_summary_line(self, topic_name=None, check_box_value=None, field_description=None, field_value=None):
        """
        Set line in the summary.

        :param topic_name: The name of topic
        :type topic_name: string
        :param check_box_value: Indicates if topic pass or fail
        :type check_box_value: bool
        :param field_description: Description of the field
        :type field_description: string
        :param field_value: Value of the field
        :type field_value: float

        """

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.setObjectName("horizontalLayout")
        check_topic_name = QtWidgets.QLabel(self)
        check_topic_name.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        check_topic_name.setObjectName("check_topic_name")
        horizontal_layout.addWidget(check_topic_name)
        field_desc = QtWidgets.QLabel(self)
        field_desc.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        field_desc.setObjectName("field_desc")
        horizontal_layout.addWidget(field_desc)
        line_edit = QtWidgets.QLineEdit(self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(line_edit.sizePolicy().hasHeightForWidth())
        line_edit.setSizePolicy(size_policy)
        line_edit.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        line_edit.setReadOnly(True)
        line_edit.setObjectName("lineEdit")
        horizontal_layout.addWidget(line_edit)
        check_topic_name.setText(topic_name)
        field_desc.setText(field_description)
        if isinstance(field_value, float):
            line_edit.setText("%.9f" % field_value)
        elif isinstance(field_value, int):
            line_edit.setText(str(field_value))
        elif field_value:
            line_edit.setText(field_value)

        if check_box_value:
            color = '#c4df9b'  # green
            line_edit.setStyleSheet('QLineEdit { background-color: %s }' % color)
        else:
            color = '#f6989d'  # red
            line_edit.setStyleSheet('QLineEdit { background-color: %s }' % color)

        scroll_layout = self.scrollContents.layout()
        scroll_layout.addLayout(horizontal_layout)

    def save_summary(self):
        """

        save summary on a text file
        """
        comments = self.comments_textEdit.toPlainText()

        now = datetime.datetime.now()

        filename, __ = QFileDialog.getSaveFileName(None, 'Save summary',
                                                   str(now.year) + str(now.month) + str(
                                                       now.day) + "_" + self.checklist_name + ".txt",
                                                   'TXT (*.txt)')
        if filename:
            if not filename.endswith(".txt"):
                filename += ".txt"

            with open(filename, 'w') as file:
                file.write('# Summary of ' + self.checklist_name + '\n')
                file.write('# ' + comments + '\n')
                file.write('\n')
                for item in self.summary:
                    file.write(item)
                    file.write('\n')
