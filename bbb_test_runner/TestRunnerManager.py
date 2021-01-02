import os
import socket

from bbb_test_runner import BBBTestRunner

from Submodules import ace_bbsm


class TestRunnerManager:

    def __init__(self):
        print(os.getenv("PYTHONPATH", default=""))
        self.bbb_test_runner = BBBTestRunner.BBBTestRunner()
        self.server = ace_bbsm.Server()

    def run_server(self):
        print("Starting server...")
        self.server.start_server()
        while True:
            try:
                print("Waiting for incoming connections...")
                self.server.connect_to_client()
            except socket.timeout:
                break
            while True:
                test_data = self.server.receive_from_client()
                if not test_data:
                    # Empty string indicates client is ready to close connection
                    break
                test_results = self.bbb_test_runner.run_test(test_data)
                self.server.send_to_client(test_results)
            self.server.disconnect_from_client()
        self.server.close_server()


if __name__ == "__main__":
    test_runner_manager = TestRunnerManager()
    test_runner_manager.run_server()
