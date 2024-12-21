import re


def parse_buffer_output(buffer_out):

    finded_values = re.findall(r'\[\s*\d+\]\s+(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+\.\d+)\s+([A-Za-z]+Bytes)\s+(\d+\.\d+)\s+([A-Za-z]+bits/sec)', buffer_out)
    parsed_data = []
    for value in finded_values:
        interval, transfer, transfer_unit, bitrate, bitrate_unit = value
        parsed_data.append({
            "Interval": interval,
            "Transfer": f"{transfer} {transfer_unit}",
            "Bitrate": f"{bitrate} {bitrate_unit}"
        })
    return parsed_data

