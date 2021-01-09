import json
import subprocess


class BBBTestRunner:

    def __init__(self):
        pass

    def run_test(self, test_config_str):
        """
        :param test_config_str: str: The test configuration. Must be valid json
        :return: str: The test results. Valid json
        """
        test_config_dict = BBBTestRunner.parse_config(test_config_str)
        self.handle_i2c(test_config_dict["i2c"])
        self.handle_outputs(test_config_dict["outputs"])

        test_results_dict = {
            "inputs": self.get_inputs(test_config_dict["inputs"])
        }

        return json.dumps(test_results_dict)

    @staticmethod
    def parse_config(test_config):
        """
        Parses a config file to a dictionary

        :param test_config: str: The test configuration. Must be valid json
        :return: dict: The import json in dictionary form
        """
        return json.loads(test_config)

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
        pass

    @staticmethod
    def get_inputs(bbb_inputs):
        results = {}
        for pin_number in bbb_inputs.keys():
            if bbb_inputs[pin_number]["type"] == "digital":
                # return digital high for now
                results[pin_number] = "1"
        return results
