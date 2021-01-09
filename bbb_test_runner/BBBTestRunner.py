import json


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
    def handle_i2c(i2c_data_dict):
        pass

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
