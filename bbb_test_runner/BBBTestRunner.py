import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import json
import time  # just for testing
import subprocess


class BBBTestRunner:

    def __init__(self):
        self.test_results_dict = None
        ADC.setup()

    def run_test(self, test_config_str):
        """
        :param test_config_str: str: The test configuration. Must be valid json
        :return: str: The test results. Valid json
        """
        print("Running test: {}".format(test_config_str))
        self.test_results_dict = {"inputs": {}}
        test_config_dict = BBBTestRunner.parse_config(test_config_str)
        BBBTestRunner.setup_bbb_inputs(test_config_dict["inputs"])
        BBBTestRunner.handle_i2c(test_config_dict["i2c"])
        BBBTestRunner.handle_outputs(test_config_dict["outputs"])
        time.sleep(30)  # just for testing
        self.get_inputs(test_config_dict["inputs"])

        # reset all GPIO channels used by application to inputs
        GPIO.cleanup()
        return json.dumps(self.test_results_dict)

    @staticmethod
    def parse_config(test_config):
        """
        Parses a config file to a dictionary

        :param test_config: str: The test configuration. Must be valid json
        :return: dict: The import json in dictionary form
        """
        return json.loads(test_config)

    @staticmethod
    def setup_bbb_inputs(bbb_inputs):
        for pin_number in bbb_inputs.keys():
            input_type = bbb_inputs[pin_number]["type"]
            if input_type == "digital":
                GPIO.setup(pin_number, GPIO.IN)
            elif input_type == "analog":
                # adc already started, no action required
                pass
            else:
                raise TypeError(
                    "The input type {} on pin {} is not supported".format(
                        input_type, pin_number))

    @staticmethod
    def handle_i2c(i2c_dict):
        i2c_spec_keys = sorted(i2c_dict.keys())
        for key in i2c_spec_keys:
            i2cbus = i2c_dict[key]["i2cbus"]
            chip_address = i2c_dict[key]["chip_address"]
            data_address = i2c_dict[key]["data_address"]
            subprocess_args = ["i2cset", "-y", i2cbus, chip_address,
                               data_address]
            data = i2c_dict[key]["data"]
            if data != "":
                subprocess_args.append(data)
            subprocess.run([" ".join(subprocess_args)], shell=True, check=True)

    @staticmethod
    def handle_outputs(bbb_outputs):
        for pin_number in bbb_outputs.keys():
            output_type = bbb_outputs[pin_number]["type"]
            if output_type == "digital":
                BBBTestRunner.handle_digital_output(
                    pin_number, bbb_outputs[pin_number]["value"])
            else:
                raise TypeError(
                    "Output type {} on pin {} is not supported".format(
                        output_type, pin_number))

    @staticmethod
    def handle_digital_output(pin_number, pin_value):
        if pin_value == "1":
            output_value = GPIO.HIGH
        elif pin_value == "0":
            output_value = GPIO.LOW
        else:
            raise ValueError(
                "The input value {} for digital output on pin {} is not "
                "supported".format(pin_value, pin_number))
        GPIO.setup(pin_number, GPIO.OUT, initial=output_value)

    def get_inputs(self, bbb_inputs):
        for pin_number in bbb_inputs.keys():
            input_type = bbb_inputs[pin_number]["type"]
            if input_type == "digital":
                self.get_digital_input(pin_number)
            elif input_type == "analog":
                self.get_analog_input(pin_number)
            else:
                raise TypeError(
                    "The input type {} on pin {} is not supported".format(
                        input_type, pin_number))

    def get_digital_input(self, pin_number):
        digital_input_value = GPIO.input(pin_number)
        if digital_input_value == GPIO.HIGH:
            parsed_input_value = "1"
        elif digital_input_value == GPIO.LOW:
            parsed_input_value = "0"
        else:
            raise ValueError(
                "Unexpected digital input {}".format(digital_input_value))
        self.test_results_dict["inputs"][pin_number] = parsed_input_value

    def get_analog_input(self, pin_number):
        analog_input_value = ADC.read(pin_number)
        self.test_results_dict["inputs"][pin_number] = analog_input_value
