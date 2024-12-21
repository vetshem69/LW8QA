import paramiko
import subprocess
import pytest

# Server connection details
SERVER_IP = ''  # Replace with your server's IP
USERNAME = ''  # Replace with your username
PASSWORD = ''  # Replace with your password

@pytest.fixture(scope="function")
def server():
    """
    Fixture to connect to the server via SSH, start the iperf server, and clean up afterward.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        # Start iperf server
        stdin, stdout, stderr = ssh_client.exec_command('iperf -s -D')
        yield stdout.read().decode(), stderr.read().decode()
    finally:
        # Stop iperf server
        ssh_client.exec_command('pkill -f iperf')
        ssh_client.close()

@pytest.fixture(scope="function")
def client(server):
    """
    Fixture to run iperf client and return the output and error for parsing.
    """
    try:
        # Run iperf client
        process_result = subprocess.run(
            ['iperf', '-c', SERVER_IP],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process_result.stdout, process_result.stderr
    except Exception as error:
        return None, str(error)

