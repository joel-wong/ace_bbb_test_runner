import socket

from bbb_test_runner import BBBTestRunner

from Submodules import ace_bbsm


class TestRunnerManager:

    def __init__(self):
        self.bbb_test_runner = BBBTestRunner.BBBTestRunner()
        self.server = ace_bbsm.Server()

    def run_server(self):
        """
        Run the server. Accept an arbitrary number of clients (one at a
        time) who then send test specifications which are executed on the
        BBB
        """
        print("Starting server...")
        self.server.start_server()
        try:
            while True:
                self.handle_next_client()
        except KeyboardInterrupt or TimeoutError:
            # server intentionally stopped or has been inactive for
            # longer than the timeout specified in the BBSM_CONSTANTS
            pass
        finally:
            self.server.close_server()

    def handle_next_client(self):
        """
        Waits for a connection to a client, then executes test
        specifications sent from that client until the client either
        intentionally disconnects or there is an error
        """
        try:
            print("Waiting for incoming connections...")
            print("Press Ctrl+C to manually stop the server")
            self.server.connect_to_client()
        except socket.timeout:
            raise TimeoutError("Socket timeout, closing connection")
        try:
            while True:
                self.service_test_specification()
        except TestsCompleteInterrupt as e:
            # tests intentionally finished for a given client
            print(str(e))
        except Exception as e:
            # client has sent invalid data, print error and disconnect
            print("Error: {}".format(str(e)))
        self.server.disconnect_from_client()

    def service_test_specification(self):
        """
        Receives a test specification from a client, then runs the tests
        on 'self.bbb_test_runner'
        """
        test_config = self.server.receive_from_client()
        if not test_config:
            # Empty string indicates client is ready to
            # close connection
            raise TestsCompleteInterrupt("Tests finished normally for client")
        test_results = self.bbb_test_runner.run_test(test_config)
        self.server.send_to_client(test_results)


class TestsCompleteInterrupt(RuntimeError):
    # An error raised when a client intentionally sends a message
    # telling the BBB that its tests are completed
    def __init__(self, message):
        super().__init__(message)


if __name__ == "__main__":
    test_runner_manager = TestRunnerManager()
    test_runner_manager.run_server()
