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
Helper for parsing,reading and writing config xml files
"""

from lxml import etree


class XMLConfigParser(object):
    def __init__(self, config_file_name, rm_comments=True):
        self.config_name = config_file_name
        # parser to remove comments
        parser = etree.XMLParser(remove_comments=rm_comments)
        # tree
        self.tree = etree.parse(config_file_name, parser=parser)
        self.root = self.tree.getroot()

    # returns only the first match
    def first_match(self, branch, match_name):
        return branch.find(match_name)

    # returns a list of matching Elements
    def all_matches(self, branch, match_name):
        return branch.findall(match_name)

    def write(self):
        """
        write self.tree on config file
        """
        self.tree.write(self.config_name, pretty_print=True)
