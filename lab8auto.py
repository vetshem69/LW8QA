import unittest
from unittest.mock import patch
from lab8 import *
class TestIperfScript(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_client_connection(self, mock_popen):
        """
        Тестує успішне підключення клієнта до сервера iPerf
        """
        mock_process = mock_popen.return_value
        mock_process.communicate.return_value = (
            """[ ID] Interval       Transfer     Bandwidth
            [  1] 0.0000-10.0064 sec  48.8 GBytes  41.9 Gbits/sec
            """,
            ""
        )
        mock_process.returncode = 0
        
        result, error = client("127.0.0.1")
        self.assertEqual(error, "")  # Перевірка відсутності помилки
        self.assertIn("48.8 GBytes", result)  # Перевірка виводу

    def test_parser(self):
        """
        Тестує правильність парсингу даних
        """
        test_output = """[ ID] Interval       Transfer     Bandwidth
        [  1] 0.0000-10.0064 sec  48.8 GBytes  41.9 Gbits/sec
        """
        expected_output = [{
            "Interval": "0.0000-10.0064",
            "Transfer": 49971.2,  # Converted to MBytes
            "Bitrate": 42905.6  # Converted to Mbits/sec
        }]
        
        result = parser(test_output)
        self.assertEqual(result, expected_output)

    def test_parser_conditions(self):
        """
        Тестує умови вибору інтервалів із парсера
        """
        intervals = [{
            "Interval": "0.0000-10.0064",
            "Transfer": 49971.2,
            "Bitrate": 42905.6
        }, {
            "Interval": "10.0064-20.0000",
            "Transfer": 1.5,
            "Bitrate": 15.0
        }]

        valid_intervals = [i for i in intervals if i["Transfer"] > 2 and i["Bitrate"] > 20]
        self.assertEqual(len(valid_intervals), 1)  # Має бути 1 інтервал
        self.assertEqual(valid_intervals[0]["Interval"], "0.0000-10.0064")

if __name__ == '__main__':
    unittest.main()

