#-------------------------------------------------------------------------------
# qwiic_mmc5983ma.py
#
# Python library for the SparkFun Qwiic MMC5983MA Magnetometer, available here:
# https://www.sparkfun.com/products/19921
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, November 2023
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#===============================================================================
# This code was generated in part with ChatGPT, created by OpenAI. The code was
# reviewed and edited by the following human(s):
#
# Dryw Wade
#===============================================================================

"""
qwiic_mmc5983ma
============
Python module for the [SparkFun Qwiic MMC5983MA Magnetometer](https://www.sparkfun.com/products/19921)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_MMC5983MA_Magnetometer_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c
import time

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic MMC5983MA"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x30]

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicMMC5983MA(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Registers definitions
    X_OUT_0_REG = 0x0
    X_OUT_1_REG = 0x01
    Y_OUT_0_REG = 0x02
    Y_OUT_1_REG = 0x03
    Z_OUT_0_REG = 0x04
    Z_OUT_1_REG = 0x05
    XYZ_OUT_2_REG = 0x06
    T_OUT_REG = 0x07
    STATUS_REG = 0x08
    INT_CTRL_0_REG = 0x09
    INT_CTRL_1_REG = 0x0a
    INT_CTRL_2_REG = 0x0b
    INT_CTRL_3_REG = 0x0c
    PROD_ID_REG = 0x2f
    DUMMY = 0x0

    # Constants definitions
    I2C_ADDR = 0x30
    PROD_ID = 0x30

    # Bits definitions
    MEAS_M_DONE = (1 << 0)
    MEAS_T_DONE = (1 << 1)
    OTP_READ_DONE = (1 << 4)
    TM_M = (1 << 0)
    TM_T = (1 << 1)
    INT_MEAS_DONE_EN = (1 << 2)
    SET_OPERATION = (1 << 3)
    RESET_OPERATION = (1 << 4)
    AUTO_SR_EN = (1 << 5)
    OTP_READ = (1 << 6)
    BW0 = (1 << 0)
    BW1 = (1 << 1)
    X_INHIBIT = (1 << 2)
    YZ_INHIBIT = (3 << 3)
    SW_RST = (1 << 7)
    CM_FREQ_0 = (1 << 0)
    CM_FREQ_1 = (1 << 1)
    CM_FREQ_2 = (1 << 2)
    CMM_EN = (1 << 3)
    PRD_SET_0 = (1 << 4)
    PRD_SET_1 = (1 << 5)
    PRD_SET_2 = (1 << 6)
    EN_PRD_SET = (1 << 7)
    ST_ENP = (1 << 1)
    ST_ENM = (1 << 2)
    SPI_3W = (1 << 6)
    X2_MASK = (3 << 6)
    Y2_MASK = (3 << 4)
    Z2_MASK = (3 << 2)
    XYZ_0_SHIFT = 10
    XYZ_1_SHIFT = 2

    class MemoryShadow:
        def __init__(self):
            self.internal_control_0 = 0x0
            self.internal_control_1 = 0x0
            self.internal_control_2 = 0x0
            self.internal_control_3 = 0x0

    def __init__(self, address=None, i2c_driver=None):
        """
        Constructor

        :param address: The I2C address to use for the device
            If not provided, the default address is used
        :type address: int, optional
        :param i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        :type i2c_driver: I2CDriver, optional
        """

        # Use address if provided, otherwise pick the default
        self.address = self.available_addresses[0] if address is None else address

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        # Initialize shadow registers
        self.memory_shadow = self.MemoryShadow()

    def is_connected(self):
        """
        Determines if this device is connected

        :return: `True` if connected, otherwise `False`
        :rtype: bool
        """
        # Check if connected by seeing if an ACK is received
        if qwiic_i2c.isDeviceConnected(self.address) == False:
            return False
        
        # Something ACK'd, check the product ID
        return self._i2c.readByte(self.address, self.PROD_ID_REG) == self.PROD_ID

    connected = property(is_connected)

    def begin(self):
        """
        Initializes this device with default parameters

        :return: Returns `True` if successful, otherwise `False`
        :rtype: bool
        """
        # Confirm device is connected before doing anything
        if not self.is_connected():
            return False

        # Perform a reset. To revert all registers to a known state
        self.soft_reset()

        return True

    def is_bit_set(self, register_address, bit_mask):
        return self._i2c.readByte(self.address, register_address) & bit_mask

    def set_register_bit(self, register_address, bit_mask):
        reg_value = self._i2c.readByte(self.address, register_address)
        self._i2c.writeByte(self.address, register_address, reg_value | bit_mask)

    def set_shadow_bit(self, register_address, bit_mask, do_write = True):
        shadow_register = None

        # Which register are we referring to?
        if register_address == self.INT_CTRL_0_REG:
            shadow_register = self.memory_shadow.internal_control_0
        elif register_address == self.INT_CTRL_1_REG:
            shadow_register = self.memory_shadow.internal_control_1
        elif register_address == self.INT_CTRL_2_REG:
            shadow_register = self.memory_shadow.internal_control_2
        elif register_address == self.INT_CTRL_3_REG:
            shadow_register = self.memory_shadow.internal_control_3
        
        if shadow_register is not None:
            shadow_register |= bit_mask
            if do_write:
                self._i2c.writeByte(self.address, register_address, shadow_register)
            return True

        return False

    def clear_shadow_bit(self, register_address, bit_mask, do_write = True):
        shadow_register = None

        # Which register are we referring to?
        if register_address == self.INT_CTRL_0_REG:
            shadow_register = self.memory_shadow.internal_control_0
        elif register_address == self.INT_CTRL_1_REG:
            shadow_register = self.memory_shadow.internal_control_1
        elif register_address == self.INT_CTRL_2_REG:
            shadow_register = self.memory_shadow.internal_control_2
        elif register_address == self.INT_CTRL_3_REG:
            shadow_register = self.memory_shadow.internal_control_3

        if shadow_register is not None:
            shadow_register &= ~bit_mask
            if do_write:
                self._i2c.writeByte(self.address, register_address, shadow_register)
            return True

        return False

    def is_shadow_bit_set(self, register_address, bit_mask):
        # Which register are we referring to?
        if register_address == self.INT_CTRL_0_REG:
            return self.memory_shadow.internal_control_0 & bit_mask
        elif register_address == self.INT_CTRL_1_REG:
            return self.memory_shadow.internal_control_1 & bit_mask
        elif register_address == self.INT_CTRL_2_REG:
            return self.memory_shadow.internal_control_2 & bit_mask
        elif register_address == self.INT_CTRL_3_REG:
            return self.memory_shadow.internal_control_3 & bit_mask

        return False

    def get_temperature(self):
        # Set the TM_T bit to start the temperature conversion.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the Auto_SR_en bit too as that
        # always seems to read as 1...? I don't know why.
        if not self.set_shadow_bit(self.INT_CTRL_0_REG, self.TM_T):
            self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_T, False) # Clear the bit - in shadow memory only
            return -99

        # Wait until measurement is completed.
        # It is rare but there are some devices and some circumstances where the code can become
        # stuck in this loop waiting for MEAS_T_DONE to go high. The solution is to timeout after 5ms.
        time_out = 5
        while (not self.is_bit_set(self.STATUS_REG, self.MEAS_T_DONE)) and (time_out > 0):
            # Wait a little so we won't flood MMC with requests
            time.sleep(0.001)
            time_out -= 1

        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_T, False) # Clear the bit - in shadow memory only

        # Get raw temperature value from the IC
        # even if a timeout occurred - old data vs no data
        result = self._i2c.readByte(self.address, self.T_OUT_REG)

        # Convert it using the equation provided in the datasheet
        temperature = -75.0 + (float(result) * (200.0 / 255.0))

        # Return the integer part of the temperature.
        return int(temperature)

    def soft_reset(self):
        # Set the SW_RST bit to perform a software reset.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the reserved and BW_0 bits too as they
        # always seems to read as 1...? I don't know why.
        success = self.set_shadow_bit(self.INT_CTRL_1_REG, self.SW_RST)

        self.clear_shadow_bit(self.INT_CTRL_1_REG, self.SW_RST, False) # Clear the bit - in shadow memory only

        # The reset time is 10 msec. but we'll wait 15 msec. just in case.
        time.sleep(0.015)

        return success

    def enable_interrupt(self):
        # Set the INT_MEAS_DONE_EN bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_0_REG, self.INT_MEAS_DONE_EN)

    def disable_interrupt(self):
        # Clear the INT_MEAS_DONE_EN bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_0_REG, self.INT_MEAS_DONE_EN)

    def is_interrupt_enabled(self):
        # Get the value of the INT_MEAS_DONE_EN bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_0_REG, self.INT_MEAS_DONE_EN)

    def enable_3_wire_spi(self):
        # Set the SPI_3W bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_3_REG, self.SPI_3W)

    def disable_3_wire_spi(self):
        # Clear the SPI_3W bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_3_REG, self.SPI_3W)

    def is_3_wire_spi_enabled(self):
        # Get the value of the SPI_3W bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_3_REG, self.SPI_3W)

    def perform_set_operation(self):
        # Set the SET_OPERATION bit in the shadow memory
        success = self.set_shadow_bit(self.INT_CTRL_0_REG, self.SET_OPERATION)

        # Clear the SET_OPERATION bit in the shadow memory
        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.SET_OPERATION)

        # Wait for the set operation to complete (500ns)
        time.sleep(0.001)

        return success

    def perform_reset_operation(self):
        # Set the RESET_OPERATION bit in the shadow memory
        success = self.set_shadow_bit(self.INT_CTRL_0_REG, self.RESET_OPERATION)

        # Clear the RESET_OPERATION bit in the shadow memory
        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.RESET_OPERATION)

        # Wait for the reset operation to complete (500ns)
        time.sleep(0.001)

        return success

    def enable_automatic_set_reset(self):
        # Set the AUTO_SR_EN bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_0_REG, self.AUTO_SR_EN)

    def disable_automatic_set_reset(self):
        # Clear the AUTO_SR_EN bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_0_REG, self.AUTO_SR_EN)

    def is_automatic_set_reset_enabled(self):
        # Get the value of the AUTO_SR_EN bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_0_REG, self.AUTO_SR_EN)

    def enable_x_channel(self):
        # Clear the X_INHIBIT bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_1_REG, self.X_INHIBIT)

    def disable_x_channel(self):
        # Set the X_INHIBIT bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_1_REG, self.X_INHIBIT)

    def is_x_channel_enabled(self):
        # Get the value of the X_INHIBIT bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_1_REG, self.X_INHIBIT)

    def enable_yz_channels(self):
        # Clear the YZ_INHIBIT bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_1_REG, self.YZ_INHIBIT)

    def disable_yz_channels(self):
        # Set the YZ_INHIBIT bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_1_REG, self.YZ_INHIBIT)

    def are_yz_channels_enabled(self):
        # Get the value of the YZ_INHIBIT bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_1_REG, self.YZ_INHIBIT)

    def set_filter_bandwidth(self, bandwidth):
        # Set/clear the BW0 and BW1 bits in the shadow memory based on the specified bandwidth
        success = False

        if bandwidth == 800:
            success = self.set_shadow_bit(self.INT_CTRL_1_REG, self.BW1)
            success &= self.clear_shadow_bit(self.INT_CTRL_1_REG, self.BW0)
        elif bandwidth == 400:
            success = self.set_shadow_bit(self.INT_CTRL_1_REG, self.BW1)
            success &= self.set_shadow_bit(self.INT_CTRL_1_REG, self.BW0)
        elif bandwidth == 200:
            success = self.clear_shadow_bit(self.INT_CTRL_1_REG, self.BW1)
            success &= self.set_shadow_bit(self.INT_CTRL_1_REG, self.BW0)
        elif bandwidth == 100:
            success = self.clear_shadow_bit(self.INT_CTRL_1_REG, self.BW1)
            success &= self.clear_shadow_bit(self.INT_CTRL_1_REG, self.BW0)

        return success

    def get_filter_bandwidth(self):
        # Get the values of the BW0 and BW1 bits from the shadow memory
        bw0 = self.is_shadow_bit_set(self.INT_CTRL_1_REG, self.BW0)
        bw1 = self.is_shadow_bit_set(self.INT_CTRL_1_REG, self.BW1)

        # Determine the corresponding bandwidth based on the bit values
        if bw1 and not bw0:
            return 200
        elif not bw1 and bw0:
            return 400
        elif bw1 and bw0:
            return 800
        else:
            return 100

    def enable_continuous_mode(self):
        # Set the CMM_EN bit through the shadow memory
        return self.set_shadow_bit(self.INT_CTRL_2_REG, self.CMM_EN)

    def disable_continuous_mode(self):
        # Clear the CMM_EN bit through the shadow memory
        return self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CMM_EN)

    def is_continuous_mode_enabled(self):
        # Get the value of the CMM_EN bit from the shadow memory
        return self.is_shadow_bit_set(self.INT_CTRL_2_REG, self.CMM_EN)

    def set_continuous_mode_frequency(self, frequency):
        # Set/clear the CM_FREQ_0, CM_FREQ_1, and CM_FREQ_2 bits in the shadow memory based on the specified frequency
        success = False

        if frequency == 1:
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 10:
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 20:
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 50:
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 100:
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 200:
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 1000:
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)
        elif frequency == 0:
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_0)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_1)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.CM_FREQ_2)

        return success

    def get_continuous_mode_frequency(self):
        # Get the values of the CM_FREQ_0, CM_FREQ_1, and CM_FREQ_2 bits from the shadow memory
        cm_freq_0 = self.is_shadow_bit_set(self.INT_CTRL_2_REG, self.CM_FREQ_0)
        cm_freq_1 = self.is_shadow_bit_set(self.INT_CTRL_2_REG, self.CM_FREQ_1)
        cm_freq_2 = self.is_shadow_bit_set(self.INT_CTRL_2_REG, self.CM_FREQ_2)

        # Determine the corresponding frequency based on the bit values
        if cm_freq_2 and not cm_freq_1 and not cm_freq_0:
            return 1
        elif not cm_freq_2 and cm_freq_1 and not cm_freq_0:
            return 10
        elif cm_freq_2 and cm_freq_1 and not cm_freq_0:
            return 20
        elif not cm_freq_2 and not cm_freq_1 and cm_freq_0:
            return 50
        elif cm_freq_2 and not cm_freq_1 and cm_freq_0:
            return 100
        elif not cm_freq_2 and cm_freq_1 and cm_freq_0:
            return 200
        elif cm_freq_2 and cm_freq_1 and cm_freq_0:
            return 1000
        else:
            return 0

    def enable_periodic_set(self):
        # This bit must be set through the shadow memory or we won't be
        # able to check if periodic set is enabled using isContinuousModeEnabled()
        return self.set_shadow_bit(self.INT_CTRL_2_REG, self.EN_PRD_SET)

    def disable_periodic_set(self):
        # This bit must be cleared through the shadow memory or we won't be
        # able to check if periodic set is enabled using isContinuousModeEnabled()
        return self.clear_shadow_bit(self.INT_CTRL_2_REG, self.EN_PRD_SET)

    def is_periodic_set_enabled(self):
        # Get the bit value from the shadow register since the IC does not
        # allow reading INT_CTRL_2_REG register.
        return self.is_shadow_bit_set(self.INT_CTRL_2_REG, self.EN_PRD_SET)

    def set_periodic_set_samples(self, number_of_samples):
        success = False
        
        if number_of_samples == 25:
            # PRD_SET[2:0] = 001
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 75:
            # PRD_SET[2:0] = 010
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 100:
            # PRD_SET[2:0] = 011
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 250:
            # PRD_SET[2:0] = 100
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 500:
            # PRD_SET[2:0] = 101
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 1000:
            # PRD_SET[2:0] = 110
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 2000:
            # PRD_SET[2:0] = 111
            success = self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.set_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        elif number_of_samples == 1:
            # PRD_SET[2:0] = 000
            success = self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_2, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_1, False)
            success &= self.clear_shadow_bit(self.INT_CTRL_2_REG, self.PRD_SET_0)
        else:
            success = False
        
        return success

    def get_periodic_set_samples(self):
        # Since we cannot read INT_CTRL_2_REG we evaluate the shadow
        # memory contents and return the corresponding period.

        # Remove unwanted bits
        register_value = self.memory_shadow.internal_control_2 & 0x70
        period = 1

        if register_value == 0x10:
            period = 25
        elif register_value == 0x20:
            period = 75
        elif register_value == 0x30:
            period = 100
        elif register_value == 0x40:
            period = 250
        elif register_value == 0x50:
            period = 500
        elif register_value == 0x60:
            period = 1000
        elif register_value == 0x70:
            period = 2000

        return period

    def apply_extra_current_pos_to_neg(self):
        # This bit must be set through the shadow memory or we won't be
        # able to check if extra current is applied using is_extra_current_applied_pos_to_neg()
        return self.set_shadow_bit(self.INT_CTRL_3_REG, self.ST_ENP)

    def remove_extra_current_pos_to_neg(self):
        # This bit must be cleared through the shadow memory or we won't be
        # able to check if extra current is applied using is_extra_current_applied_pos_to_neg()
        return self.clear_shadow_bit(self.INT_CTRL_3_REG, self.ST_ENP)

    def is_extra_current_applied_pos_to_neg(self):
        # Get the bit value from the shadow register since the IC does not
        # allow reading INT_CTRL_3_REG register.
        return self.is_shadow_bit_set(self.INT_CTRL_3_REG, self.ST_ENP)

    def apply_extra_current_neg_to_pos(self):
        # This bit must be set through the shadow memory or we won't be
        # able to check if extra current is applied using is_extra_current_applied_neg_to_pos()
        return self.set_shadow_bit(self.INT_CTRL_3_REG, self.ST_ENM)

    def remove_extra_current_neg_to_pos(self):
        # This bit must be cleared through the shadow memory or we won't be
        # able to check if extra current is applied using is_extra_current_applied_neg_to_pos()
        return self.clear_shadow_bit(self.INT_CTRL_3_REG, self.ST_ENM)

    def is_extra_current_applied_neg_to_pos(self):
        # Get the bit value from the shadow register since the IC does not
        # allow reading INT_CTRL_3_REG register.
        return self.is_shadow_bit_set(self.INT_CTRL_3_REG, self.ST_ENM)

    def clear_meas_done_interrupt(self, meas_mask = MEAS_T_DONE | MEAS_M_DONE):
        # Ensure only the Meas_T_Done and Meas_M_Done interrupts can be cleared
        meas_mask &= (self.MEAS_T_DONE | self.MEAS_M_DONE)

        # Writing 1 into these bits will clear the corresponding interrupt
        # Read-modify-write is OK here
        self.set_register_bit(self.STATUS_REG, meas_mask)

    def get_measurement_x(self):
        # Set the TM_M bit to start the measurement.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the Auto_SR_en bit too as that
        # always seems to read as 1...? I don't know why.
        if not self.set_shadow_bit(self.INT_CTRL_0_REG, self.TM_M):
            self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only
            return 0

        # Wait until measurement is completed.
        # It is rare but there are some devices and some circumstances where the code can become
        # stuck in this loop waiting for MEAS_M_DONE to go high. The solution is to timeout after
        # 4 * the measurement time (defined by BW1/0).
        time_out = self.get_filter_bandwidth()  # Read the bandwidth (100/200/400/800Hz) from shadow
        time_out = 800 // time_out  # Convert time_out to 8/4/2/1ms
        time_out *= 4  # Convert bw to 32/16/8/4ms
        time_out += 1  # Add 1 just in case (for 800Hz)
        while (not self.is_bit_set(self.STATUS_REG, self.MEAS_M_DONE)) and (time_out > 0):
            # Wait a little so we won't flood MMC with requests
            time.sleep(0.001)
            time_out -= 1

        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only

        result = 0
        buffer = [0, 0]
        buffer_2_bit = 0

        # Read the field even if a timeout occurred - old data vs no data
        buffer = self._i2c.readBlock(self.address, self.X_OUT_0_REG, 2)
        buffer_2_bit = self._i2c.readByte(self.address, self.XYZ_OUT_2_REG)

        result = buffer[0]  # out[17:10]
        result = (result << 8) | buffer[1]  # out[9:2]
        result = (result << 2) | (buffer_2_bit >> 6)  # out[1:0]

        return result

    def get_measurement_y(self):
        # Set the TM_M bit to start the measurement.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the Auto_SR_en bit too as that
        # always seems to read as 1...? I don't know why.
        if not self.set_shadow_bit(self.INT_CTRL_0_REG, self.TM_M):
            self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only
            return 0

        # Wait until measurement is completed.
        # It is rare but there are some devices and some circumstances where the code can become
        # stuck in this loop waiting for MEAS_M_DONE to go high. The solution is to timeout after
        # 4 * the measurement time (defined by BW1/0).
        time_out = self.get_filter_bandwidth()  # Read the bandwidth (100/200/400/800Hz) from shadow
        time_out = 800 // time_out  # Convert time_out to 8/4/2/1ms
        time_out *= 4  # Convert bw to 32/16/8/4ms
        time_out += 1  # Add 1 just in case (for 800Hz)
        while (not self.is_bit_set(self.STATUS_REG, self.MEAS_M_DONE)) and (time_out > 0):
            # Wait a little so we won't flood MMC with requests
            time.sleep(0.001)
            time_out -= 1

        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only

        result = 0
        buffer = [0, 0]
        buffer_2_bit = 0

        # Read the field even if a timeout occurred - old data vs no data
        buffer = self._i2c.readBlock(self.address, self.Y_OUT_0_REG, 2)
        buffer_2_bit = self._i2c.readByte(self.address, self.XYZ_OUT_2_REG)

        result = buffer[0]  # out[17:10]
        result = (result << 8) | buffer[1]  # out[9:2]
        result = (result << 2) | ((buffer_2_bit >> 4) & 0x03)  # out[1:0]

        return result

    def get_measurement_z(self):
        # Set the TM_M bit to start the measurement.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the Auto_SR_en bit too as that
        # always seems to read as 1...? I don't know why.
        if not self.set_shadow_bit(self.INT_CTRL_0_REG, self.TM_M):
            self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only
            return 0

        # Wait until measurement is completed.
        # It is rare but there are some devices and some circumstances where the code can become
        # stuck in this loop waiting for MEAS_M_DONE to go high. The solution is to timeout after
        # 4 * the measurement time (defined by BW1/0).
        time_out = self.get_filter_bandwidth()  # Read the bandwidth (100/200/400/800Hz) from shadow
        time_out = 800 // time_out  # Convert time_out to 8/4/2/1ms
        time_out *= 4  # Convert bw to 32/16/8/4ms
        time_out += 1  # Add 1 just in case (for 800Hz)
        while (not self.is_bit_set(self.STATUS_REG, self.MEAS_M_DONE)) and (time_out > 0):
            # Wait a little so we won't flood MMC with requests
            time.sleep(0.001)
            time_out -= 1

        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only

        result = 0
        buffer = [0, 0, 0]

        # Read the field even if a timeout occurred - old data vs no data
        buffer = self._i2c.readBlock(self.address, self.Z_OUT_0_REG, 3)

        result = buffer[0]  # out[17:10]
        result = (result << 8) | buffer[1]  # out[9:2]
        result = (result << 2) | ((buffer[2] >> 2) & 0x03)  # out[1:0]

        return result

    def get_measurement_xyz(self):
        # Set the TM_M bit to start the measurement.
        # Do this using the shadow register. If we do it with set_register_bit
        # (read-modify-write) we end up setting the Auto_SR_en bit too as that
        # always seems to read as 1...? I don't know why.
        success = self.set_shadow_bit(self.INT_CTRL_0_REG, self.TM_M)

        if not success:
            self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only
            return False

        # Wait until measurement is completed.
        # It is rare but there are some devices and some circumstances where the code can become
        # stuck in this loop waiting for MEAS_M_DONE to go high. The solution is to timeout after
        # 4 * the measurement time (defined by BW1/0).
        time_out = self.get_filter_bandwidth()  # Read the bandwidth (100/200/400/800Hz) from shadow
        time_out = 800 / time_out  # Convert time_out to 8/4/2/1ms
        time_out *= 4  # Convert bw to 32/16/8/4ms
        time_out += 1  # Add 1 just in case (for 800Hz)
        while (not self.is_bit_set(self.STATUS_REG, self.MEAS_M_DONE)) and (time_out > 0):
            # Wait a little so we won't flood MMC with requests
            time.sleep(0.001)
            time_out -= 1

        self.clear_shadow_bit(self.INT_CTRL_0_REG, self.TM_M, False)  # Clear the bit - in shadow memory only

        if time_out == 0:
            return False

        # Read the fields even if a timeout occurred - old data vs no data
        # Return False if a timeout or a read error occurred
        return self.read_fields_xyz()

    def read_fields_xyz(self):
        register_values = [0] * 7

        register_values = self._i2c.readBlock(self.address, self.X_OUT_0_REG, 7)

        x = register_values[0]  # Xout[17:10]
        x = (x << 8) | register_values[1]  # Xout[9:2]
        x = (x << 2) | (register_values[6] >> 6)  # Xout[1:0]
        y = register_values[2]  # Yout[17:10]
        y = (y << 8) | register_values[3]  # Yout[9:2]
        y = (y << 2) | ((register_values[6] >> 4) & 0x03)  # Yout[1:0]
        z = register_values[4]  # Zout[17:10]
        z = (z << 8) | register_values[5]  # Zout[9:2]
        z = (z << 2) | ((register_values[6] >> 2) & 0x03)  # Zout[1:0]

        return (x, y, z)

    def get_measurement_x_gauss(self, offset = (2 ** 17), gain = 8):
        # The magnetic field values are 18-bit unsigned. The _approximate_ zero
        # (mid) point is 2^17 (131072). Here we scale each field to +/- 1.0,
        # then multiply by the gain (default 8) to get measurement in Gauss.
        #
        # Please note: to properly correct and calibrate the X, Y and Z channels, you need to determine true
        # offsets (zero points) and scale factors (gains) for all three channels. Futher details can be found at:
        # https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
        measurement_raw = self.get_measurement_x()
        mesaurement_scaled = (measurement_raw - offset) / offset
        measurement_gauss = mesaurement_scaled * gain

        return measurement_gauss
    
    def get_measurement_y_gauss(self, offset = (2 ** 17), gain = 8):
        # The magnetic field values are 18-bit unsigned. The _approximate_ zero
        # (mid) point is 2^17 (131072). Here we scale each field to +/- 1.0,
        # then multiply by the gain (default 8) to get measurement in Gauss.
        #
        # Please note: to properly correct and calibrate the X, Y and Z channels, you need to determine true
        # offsets (zero points) and scale factors (gains) for all three channels. Futher details can be found at:
        # https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
        measurement_raw = self.get_measurement_y()
        mesaurement_scaled = (measurement_raw - offset) / offset
        measurement_gauss = mesaurement_scaled * gain

        return measurement_gauss
    
    def get_measurement_z_gauss(self, offset = (2 ** 17), gain = 8):
        # The magnetic field values are 18-bit unsigned. The _approximate_ zero
        # (mid) point is 2^17 (131072). Here we scale each field to +/- 1.0,
        # then multiply by the gain (default 8) to get measurement in Gauss.
        #
        # Please note: to properly correct and calibrate the X, Y and Z channels, you need to determine true
        # offsets (zero points) and scale factors (gains) for all three channels. Futher details can be found at:
        # https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
        measurement_raw = self.get_measurement_z()
        mesaurement_scaled = (measurement_raw - offset) / offset
        measurement_gauss = mesaurement_scaled * gain

        return measurement_gauss

    def get_measurement_xyz_gauss(self, offsets = [2 ** 17] * 3, gains = [8] * 3):
        # The magnetic field values are 18-bit unsigned. The _approximate_ zero
        # (mid) point is 2^17 (131072). Here we scale each field to +/- 1.0,
        # then multiply by the gain (default 8) to get measurement in Gauss.
        #
        # Please note: to properly correct and calibrate the X, Y and Z channels, you need to determine true
        # offsets (zero points) and scale factors (gains) for all three channels. Futher details can be found at:
        # https://thecavepearlproject.org/2015/05/22/calibrating-any-compass-or-accelerometer-for-arduino/
        x_raw, y_raw, z_raw = self.get_measurement_xyz()

        x_scaled = (x_raw - offsets[0]) / offsets[0]
        x_gauss = x_scaled * gains[0]

        y_scaled = (y_raw - offsets[1]) / offsets[1]
        y_gauss = y_scaled * gains[1]

        z_scaled = (z_raw - offsets[2]) / offsets[2]
        z_gauss = z_scaled * gains[2]

        return x_gauss, y_gauss, z_gauss
