import json
import re


def reformat_json_file(input_file_path, output_file_path):
    data_list = []

    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            try:
                # Remove newlines and extra spaces
                json_line = line.strip()

                # Replace single quotes with double quotes for keys and values
                # Using a regex pattern to handle the replacement more precisely
                json_line = re.sub(r"(?<!\\)'(.*?)'", r'"\1"', json_line)
                json_line = re.sub(r"(?<!\\)'(.*?)'", r'"\1"', json_line)
                # Replace single quotes around keys and values with double quotes
                json_line = json_line.replace("'", '"')

                # Parse the JSON string and append to the list
                data_list.append(json.loads(json_line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}")
                print(f"Error message: {e}")

    with open(output_file_path, 'w') as output_file:
        json.dump(data_list, output_file, indent=4)

    print(f"Formatted JSON file saved to {output_file_path}")


if __name__ == "__main__":
    input_file_path = '/home/imen/mobicrowd/Mobicrowd_backend/scraping/data/camera_specs1-293.json'
    output_file_path = '/home/imen/mobicrowd/Mobicrowd_backend/scraping/formatted_camera_specs.json'

    reformat_json_file(input_file_path, output_file_path)
