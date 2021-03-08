import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import json
import subprocess

from ace_bbsm import BBB_IO_CONSTANTS as BIC


class BBBTestRunner:

    def __init__(self):
        # list of test results
        self.test_results = None
        # continuously run ADC so that we can retrieve values when needed
        ADC.setup()
        # track things set to output so that we can set them back to
        # inputs during the next test
        self.last_digital_outputs = []

    def run_test(self, test_config_str):
        """
        :param test_config_str: str: The test configuration. Must be
            valid json that represents a list
        :return: str: The test results. Valid json representing a list
        """
        # reset all outputs used by previous test back to inputs
        for pin_number in self.last_digital_outputs:
            GPIO.setup(pin_number, GPIO.IN)
        self.last_digital_outputs = []

        print("Running test: {}".format(test_config_str))

        self.test_results = []
        test_specification_list = BBBTestRunner.parse_config(test_config_str)
        for test_command in test_specification_list:
            if test_command[BIC.SPEC_TYPE] == BIC.SPEC_TYPE_OUTPUT:
                self.handle_output(test_command)
            elif test_command[BIC.SPEC_TYPE] == BIC.SPEC_TYPE_INPUT:
                self.handle_input(test_command)
            else:
                raise ValueError("spec type is neither input nor output")

        return json.dumps(self.test_results)

    @staticmethod
    def parse_config(test_config):
        """
        Parses a config file to a list

        :param test_config: str: The test configuration. Must be valid json
        :return: list: The import json in dictionary form
        """
        test_commands = json.loads(test_config)
        if not type(test_commands) == list:
            raise ValueError("inputs and outputs must be sent in a list")
        return test_commands

    def handle_output(self, output_specification):
        """
        Outputs the appropriate signal based on the parameters in the
        output specification

        :param output_specification: dict: The output specification
        """
        output_type = output_specification[BIC.OUTPUT_TYPE]
        if output_type == BIC.DIGITAL_3V3:
            self.handle_digital_output(output_specification)
        elif output_type == BIC.I2C:
            BBBTestRunner.handle_i2c(output_specification)
        else:
            raise TypeError(
                "Output type {} is not supported".format(output_type))

    def handle_digital_output(self, output_specification):
        """
        Sets a digital output on the BBB to either digital high or low.
        Required parameters in output_specification:
        - BIC.PIN_NUMBER
        - BIC.OUTPUT_VALUE

        :param output_specification: dict: The parameters for digital output
        """
        pin_number = output_specification[BIC.PIN_NUMBER]
        pin_value = output_specification[BIC.OUTPUT_VALUE]
        if pin_value == BIC.DIGITAL_HIGH:
            output_value = GPIO.HIGH
        elif pin_value == BIC.DIGITAL_LOW:
            output_value = GPIO.LOW
        else:
            raise ValueError(
                "The input value {} for digital output on pin {} is not "
                "supported".format(pin_value, pin_number))
        GPIO.setup(pin_number, GPIO.OUT, initial=output_value)
        self.last_digital_outputs.append(pin_number)

    @staticmethod
    def handle_i2c(i2c_dict):
        """
        Performs an i2cset command with the parameters in the i2c_dict.
        Required keys in the i2c_dict:
        - BIC.I2CBUS
        - BIC.I2C_CHIP_ADDRESS
        - BIC.I2C_DATA_ADDRESS
        Optional keys in the i2c_dict:
        - BIC.OUTPUT_VALUE

        :param i2c_dict: dict: The list of parameters for the I2C command
        """
        i2cbus = i2c_dict[BIC.I2CBUS]
        chip_address = i2c_dict[BIC.I2C_CHIP_ADDRESS]
        data_address = i2c_dict[BIC.I2C_DATA_ADDRESS]
        subprocess_args = ["i2cset", "-y", i2cbus, chip_address,
                           data_address]
        data = i2c_dict[BIC.I2C_DATA]
        if data != "":
            subprocess_args.append(data)
        subprocess.run([" ".join(subprocess_args)], shell=True, check=True)

    def handle_input(self, input_specification):
        """
        Inputs a value on a given input pin based on the parameters in
        the 'input_specification'
        Will append the input value(s) to 'self.test_results'

        :param input_specification: dict: Parameters for the input
        """
        input_type = input_specification[BIC.INPUT_TYPE]
        if input_type == BIC.DIGITAL_3V3:
            self.handle_digital_input(input_specification)
        elif input_type == BIC.ANALOG_1V8:
            self.handle_analog_input(input_specification)
        else:
            raise TypeError(
                "The input type {} is not supported".format(input_type))

    def handle_digital_input(self, input_specification):
        """
        Inputs a digital value on the BIC.PIN_NUMBER entry in the
        'input_specification' and append the input value to
        'self.test_results'

        :param input_specification: dict: Parameters for the digital input
        """
        pin_number = input_specification[BIC.PIN_NUMBER]
        GPIO.setup(pin_number, GPIO.IN)
        digital_input_value = GPIO.input(pin_number)
        if digital_input_value == GPIO.HIGH:
            parsed_input_value = BIC.DIGITAL_HIGH
        elif digital_input_value == GPIO.LOW:
            parsed_input_value = BIC.DIGITAL_LOW
        else:
            raise ValueError(
                "Unexpected digital input {}".format(digital_input_value))
        self.test_results.append({
            BIC.INPUT_TYPE: BIC.DIGITAL_3V3,
            BIC.PIN_NUMBER: pin_number,
            BIC.INPUT_VALUE: parsed_input_value
        })

    def handle_analog_input(self, input_specification):
        """
        Inputs an analog value on the BIC.PIN_NUMBER entry in the
        'input_specification' and append the input value to
        'self.test_results'.
        The input value will be normalized from 0 to 1

        :param input_specification: dict: Parameters for the analog input
        """
        pin_number = input_specification[BIC.PIN_NUMBER]
        analog_input_value = ADC.read(pin_number)
        self.test_results.append({
            BIC.INPUT_TYPE: BIC.ANALOG_1V8,
            BIC.PIN_NUMBER: pin_number,
            BIC.INPUT_VALUE: analog_input_value
        })
