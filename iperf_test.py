from parser import parse_buffer_output

class TestSuite:
    def test_network_client_connection(self, client):

        client_output, client_error = client
        assert not client_error, f"Client encountered an error: {client_error}"
        processed_data = parse_buffer_output(client_output)
        
        # Verify traffic statistics
        for entry in processed_data:
            transfer_amount, transfer_unit = entry["Transfer"].split()
            bitrate_amount, bitrate_unit = entry["Bitrate"].split()
            
            # Convert values to float
            transfer_value = float(transfer_amount)
            bitrate_value = float(bitrate_amount)
            
            # Ensure correct units (e.g., GBytes, Mbits/sec)
            assert "Bytes" in transfer_unit, f"Unexpected transfer unit: {transfer_unit}"
            assert "bits/sec" in bitrate_unit, f"Unexpected bitrate unit: {bitrate_unit}"
            
            # Perform checks
            assert transfer_value > 2, f"Transfer is < 2 {transfer_unit}"
            assert bitrate_value > 20, f"Bitrate is < 20 {bitrate_unit}"
