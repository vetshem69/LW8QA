import subprocess
import re

def client(server_ip):
    """
    Виконує підключення клієнта до сервера через команду iperf.
    
    :param server_ip: Адреса сервера до якого буде підключатися клієнт
    :return: Результати виконання команди та повідомлення про помилки
    """
    try:
        process = subprocess.Popen(
            ["iperf", "-c", server_ip, "-i", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return "", str(e)

def parser(result):
    """
    Parses the output of the iperf command and returns a list of intervals with parameters.
    
    :param result: Output from the iperf command
    :return: List of dictionaries with interval details
    """
    intervals = []
    pattern = r"(\d+\.\d+-\d+\.\d+)\s+sec\s+([\d.]+)\s+([MG]Bytes)\s+([\d.]+)\s+([MG]bits/sec)"
    matches = re.finditer(pattern, result)
    
    for match in matches:
        transfer = float(match.group(2))
        bitrate = float(match.group(4))
        
        # Convert GBytes to MBytes and Gbits/sec to Mbits/sec for consistency
        if match.group(3) == "GBytes":
            transfer *= 1024  # 1 GByte = 1024 MBytes
        if match.group(5) == "Gbits/sec":
            bitrate *= 1024  # 1 Gbit/sec = 1024 Mbit/sec
        
        intervals.append({
            "Interval": match.group(1),
            "Transfer": transfer,
            "Bitrate": bitrate,
        })
    return intervals


if __name__ == "__main__":
    server_ip = "127.0.0.1"  # Replace with actual server IP
    result, error = client(server_ip)
    
    print(f"Raw result: {result}")  # Debug line
    print(f"Error: {error}")       # Debug line
    
    if error:
        print(f"Error: {error}")
    else:
        intervals = parser(result)
        print(f"Parsed intervals: {intervals}")  # Debug line
        for interval in intervals:
            if interval["Transfer"] > 2 and interval["Bitrate"] > 20:
                print(f"Valid interval: {interval}")

