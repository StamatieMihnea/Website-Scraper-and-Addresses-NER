import json


class JsonService:
    def extract_json(self, filename):
        with open(filename, 'r') as file:
            file_lines = file.readlines()

        json_lines = []
        json_started = False
        for line in file_lines:
            if line.strip().startswith('{'):
                json_started = True
            if json_started:
                json_lines.append(line)
            if line.strip().endswith('}'):
                break

        if json_lines:
            json_string = ''.join(json_lines)
            return json.loads(json_string)
        else:
            print("\nNo json found\n")
            return {
                "country": None,
                "region": None,
                "city": None,
                "postcode": None,
                "road": None,
                "road_numbers": None
            }
