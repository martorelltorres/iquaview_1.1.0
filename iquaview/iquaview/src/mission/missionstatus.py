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
 Provides functions to check the mission status by decoding the error byte that comes
 either from WiFi (checking the /cola2_safety/error_code) or from the USBL messages.
"""

# from iquaview.src.usblcontroller.usblcontroller.evologics_lib.usbl_commands import USBLCommands
# from usblcontroller.evologics_lib.usbl_commands import USBLCommands
from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class StatusCode:
    """
    Class to decodify the status code represented in 32bits (4 bytes)
    into different bits representing vehicle status, errors and warnings.
    """

    """
    Definitions of each bit number 
    """

    # 31-24 TBD

    # 23-18 TBD (6 bits left)

    RA_EMERGENCY_SURFACE = 17
    RA_ABORT_SURFACE = 16
    RA_ABORT_MISSION = 15
    LOW_BATTERY_WARNING = 14
    BATTERY_ERROR = 13
    WATCHDOG_TIMER = 12
    NAVIGATION_ERROR = 11
    NO_ALTITUDE_ERROR = 10
    WATER_INSIDE = 9
    HIGH_TEMPERATURE = 8
    CURRENT_MISSION_STEPS_BASE = 7  # to 0

    def __init__(self):
        pass

    def unpack(self, status_code):
        """
        Unpacks an status code integer to a dictionary of status, errors and warnings
        """
        status_code_string = format(status_code, '032b')

        ra_emergency_surface = (status_code_string[StatusCode.RA_EMERGENCY_SURFACE] == '1')
        ra_abort_surface = (status_code_string[StatusCode.RA_ABORT_SURFACE] == '1')
        ra_abort_mission = (status_code_string[StatusCode.RA_ABORT_MISSION] == '1')
        low_battery_warning = (status_code_string[StatusCode.LOW_BATTERY_WARNING] == '1')
        battery_error = (status_code_string[StatusCode.BATTERY_ERROR] == '1')
        watchdog_timer = (status_code_string[StatusCode.WATCHDOG_TIMER] == '1')
        navigation_error = (status_code_string[StatusCode.NAVIGATION_ERROR] == '1')
        no_altitude_error = (status_code_string[StatusCode.NO_ALTITUDE_ERROR] == '1')
        water_inside = (status_code_string[StatusCode.WATER_INSIDE] == '1')
        high_temperature = (status_code_string[StatusCode.HIGH_TEMPERATURE] == '1')
        current_mission_steps_base = int(status_code_string[0:StatusCode.CURRENT_MISSION_STEPS_BASE + 1], 2)

        return {
            'ra_emergency_surface': ra_emergency_surface,
            'ra_abort_surface': ra_abort_surface,
            'ra_abort_mission': ra_abort_mission,
            'low_battery_warning': low_battery_warning,
            'battery_error': battery_error,
            'watchdog_timer': watchdog_timer,
            'navigation_error': navigation_error,
            'no_altitude_error': no_altitude_error,
            'water_inside': water_inside,
            'high_temperature': high_temperature,
            'current_mission_steps_base': current_mission_steps_base
        }


class ErrorCode:
    INIT = 15
    BAT_WARNING = 14
    BAT_ERROR = 13
    NAV_STS_WARNING = 12
    NAV_STS_ERROR = 11
    INTERNAL_SENSORS_WARNING = 10
    INTERNAL_SENSORS_ERROR = 9
    DVL_BOTTOM_FAIL = 8
    CURRENT_WAYPOINT_BASE = 7  # to 0

    def __init__(self):
        pass

    def unpack(self, error_code):
        error_code_string = format(error_code, '016b')

        init = (error_code_string[ErrorCode.INIT] == '1')
        bat_warning = (error_code_string[ErrorCode.BAT_WARNING] == '1')
        bat_error = (error_code_string[ErrorCode.BAT_ERROR] == '1')
        nav_sts_warning = (error_code_string[ErrorCode.NAV_STS_WARNING] == '1')
        nav_sts_error = (error_code_string[ErrorCode.NAV_STS_ERROR] == '1')
        internal_sensors_warning = (error_code_string[ErrorCode.INTERNAL_SENSORS_WARNING] == '1')
        internal_sensors_error = (error_code_string[ErrorCode.INTERNAL_SENSORS_ERROR] == '1')
        dvl_bottom_fail = (error_code_string[ErrorCode.DVL_BOTTOM_FAIL] == '1')
        current_waypoint = int(error_code_string[0:ErrorCode.CURRENT_WAYPOINT_BASE + 1], 2)

        return {'init': init,
                'bat_warning': bat_warning,
                'bat_error': bat_error,
                'nav_sts_warning': nav_sts_warning,
                'nav_sts_error': nav_sts_error,
                'internal_sensors_warning': internal_sensors_warning,
                'internal_sensors_error': internal_sensors_error,
                'dvl_bottom_fail': dvl_bottom_fail,
                'current_waypoint': current_waypoint}


class MissionStatus(QObject):
    mission_started = pyqtSignal()
    mission_stopped = pyqtSignal()

    def __init__(self, vehicledata, msglog):
        super(MissionStatus, self).__init__()
        # self.config = config
        self.vehicle_data = vehicledata
        self.msglog = msglog
        self.mission_sts_topic = None
        self.status = ""
        self.status_color = 'green'
        self.recovery_action_status = ""
        self.status_decoder = StatusCode()
        # back compatibility
        self.error_decoder = ErrorCode()
        self.mission_is_executing = False
        self.connected = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_mission_status)

        self.vehicle_data.state_signal.connect(self.set_vehicle_data_status)

    def init_mission_status_wifi(self):

        self.connected = True
        self.timer.start(1000)

    def set_vehicle_data_status(self):
        self.status = "No connection with COLA2"
        self.status_color = 'red'

    def check_mission_status(self):
        if self.connected:
            status_code = self.vehicle_data.get_status_code()
            recovery_action = self.vehicle_data.get_recovery_action()
            if status_code is not None:
                self.assign_status(status_code)
            else:
                # back compatibility
                error_code = self.vehicle_data.get_error_code()
                if error_code is not None:
                    self.assign_status_error_code(error_code)

            if recovery_action is not None:
                self.assign_recovery_status(recovery_action)

    def assign_status(self, status_byte):

        status_code = self.status_decoder.unpack(status_byte)
        if status_code['current_mission_steps_base'] != 0:
            self.status = "Executing mission, waypoint {}".format(status_code['current_mission_steps_base'])
            self.status_color = 'green'
            self.mission_is_executing = True
            self.mission_started.emit()

            if self.vehicle_data.get_total_steps() is not None:
                self.status = self.status + "/" + str(self.vehicle_data.get_total_steps())
        else:
            self.status = ""
            self.mission_is_executing = False
            self.mission_stopped.emit()

        if status_code['ra_emergency_surface']:
            self.status = "Recovery action: Emergency Surface!"
            self.status_color = 'red'

        if status_code['ra_abort_surface']:
            self.status = "Recovery action: Abort and Surface!"
            self.status_color = 'red'
        if status_code['ra_abort_mission']:
            self.status = "Recovery action: Abort mission!"
            self.status_color = 'red'

        if status_code['low_battery_warning']:
            self.status = "Low battery charge"
            self.status_color = 'orange'

        if status_code['battery_error']:
            self.status = "Battery charge/voltage below safety threshold"
            self.status_color = 'red'

        if status_code['watchdog_timer']:
            self.status = "Watchdog timeout reached!"
            self.status_color = 'red'

        if status_code['no_altitude_error']:
            self.status = "No altitude!"
            self.status_color = 'red'

        if status_code['high_temperature']:
            self.status = "High Temperature!"
            self.status_color = 'red'

        if status_code['navigation_error']:
            self.status = "Navigation error"
            self.status_color = 'red'

        if status_code['water_inside']:
            self.status = "Water inside!"
            self.status_color = 'red'

        if self.status != "" and self.status_color == 'red':
            self.msglog.logMessage("", "Status code:", 4)
            self.msglog.logMessage(self.status, "Status code:", 4)

    def assign_status_error_code(self, error_byte):

        error_code = self.error_decoder.unpack(error_byte)
        # print(error_code)
        if error_code['current_waypoint'] != 0:
            self.status = "Executing mission, waypoint {}".format(error_code['current_waypoint'])
            self.status_color = 'green'
            self.mission_is_executing = True
            self.mission_started.emit()

            if self.vehicle_data.get_total_steps() is not None:
                self.status = self.status + "/" + str(self.vehicle_data.get_total_steps())
        else:
            self.status = ""
            self.mission_is_executing = False
            self.mission_stopped.emit()

        if error_code['internal_sensors_error']:
            self.status = "Water inside"
            self.status_color = 'red'

        if error_code['bat_error']:
            self.status = "Battery error"
            self.status_color = 'red'

        if self.status != "" and self.status_color == 'red':
            self.msglog.logMessage("", "Error code:", 5)
            self.msglog.logMessage(self.status, "Error code:", 5)

    def assign_recovery_status(self, recovery_status):

        error_level = recovery_status[0]
        error_string = recovery_status[1]
        # if error_level == USBLCommands.ABORT_AND_SURFACE:
        if error_level == 3:
            self.recovery_action_status = "Abort and Surface: " + error_string
        # elif error_level == USBLCommands.EMERGENCY_SURFACE:
        elif error_level == 4:
            self.recovery_action_status = "Emergency Surface: " + error_string
        else:
            self.recovery_action_status = ""

        if self.recovery_action_status != "":
            self.msglog.logMessage("", "Recovery Action:", 6)
            self.msglog.logMessage(self.recovery_action_status, "Recovery Action:", 6)

    def get_status(self):
        return self.status, self.status_color

    def get_recovery_action_status(self):
        return self.recovery_action_status

    def is_mission_in_execution(self):
        return self.mission_is_executing

    def disconnect(self):
        self.status = ""
        self.recovery_action_status = ""
        self.connected = False
        self.timer.stop()
