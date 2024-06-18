import re
import pandas as pd

class SMFileParser:

    @staticmethod
    def parse_sm_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Variables to hold the parsed data
        renewable_resources = []
        nonrenewable_resources = []
        doubly_constrained_resources = []
        project_info = {}
        precedence_relations = []
        requests_durations = []
        resource_availabilities = []

        # Regex patterns
        resource_pattern = re.compile(r'^\s*-\s+renewable\s*:\s*(\d+)\s*')
        nonrenewable_pattern = re.compile(r'^\s*-\s+nonrenewable\s*:\s*(\d+)\s*')
        doubly_constrained_pattern = re.compile(r'^\s*-\s+doubly constrained\s*:\s*(\d+)\s*')
        project_info_pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*')
        precedence_pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)((?:\s+\d+)*)')
        request_pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)((?:\s+\d+)*)')
        availability_pattern = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*')

        # Flags to identify sections
        in_resource_section = False
        in_project_info_section = False
        in_precedence_section = False
        in_request_section = False
        in_availability_section = False

        for line in lines:
            line = line.strip()

            # Identify the section
            if line.startswith('RESOURCES'):
                in_resource_section = True
                in_project_info_section = False
                in_precedence_section = False
                in_request_section = False
                in_availability_section = False
                continue
            elif line.startswith('PROJECT INFORMATION'):
                in_resource_section = False
                in_project_info_section = True
                in_precedence_section = False
                in_request_section = False
                in_availability_section = False
                continue
            elif line.startswith('PRECEDENCE RELATIONS'):
                in_resource_section = False
                in_project_info_section = False
                in_precedence_section = True
                in_request_section = False
                in_availability_section = False
                continue
            elif line.startswith('REQUESTS/DURATIONS'):
                in_resource_section = False
                in_project_info_section = False
                in_precedence_section = False
                in_request_section = True
                in_availability_section = False
                continue
            elif line.startswith('RESOURCEAVAILABILITIES'):
                in_resource_section = False
                in_project_info_section = False
                in_precedence_section = False
                in_request_section = False
                in_availability_section = True
                continue

            # Parse resources
            if in_resource_section:
                renewable_match = resource_pattern.match(line)
                nonrenewable_match = nonrenewable_pattern.match(line)
                doubly_constrained_match = doubly_constrained_pattern.match(line)
                if renewable_match:
                    renewable_resources = int(renewable_match.group(1))
                elif nonrenewable_match:
                    nonrenewable_resources = int(nonrenewable_match.group(1))
                elif doubly_constrained_match:
                    doubly_constrained_resources = int(doubly_constrained_match.group(1))

            # Parse project information
            elif in_project_info_section:
                match = project_info_pattern.match(line)
                if match:
                    parts = match.groups()
                    project_info = {
                        'pronr': int(parts[0]),
                        'jobs': int(parts[1]),
                        'rel_date': int(parts[2]),
                        'duedate': int(parts[3]),
                        'tardcost': int(parts[4]),
                        'MPM_Time': int(parts[5])
                    }

            # Parse precedence relations
            elif in_precedence_section:
                match = precedence_pattern.match(line)
                if match:
                    jobnr, modes, successors_count, successors = match.groups()
                    successors = list(map(int, successors.strip().split())) if successors else []
                    precedence_relations.append((int(jobnr), int(modes), int(successors_count), successors))

            # Parse requests and durations
            elif in_request_section:
                match = request_pattern.match(line)
                if match:
                    jobnr, mode, duration, resources_data = match.groups()
                    resources_data = list(map(int, resources_data.strip().split())) if resources_data else []
                    requests_durations.append((int(jobnr), int(mode), int(duration), resources_data))

            # Parse resource availabilities
            elif in_availability_section:
                match = availability_pattern.match(line)
                if match:
                    resource_availabilities.append(list(map(int, match.groups())))

        # Convert to DataFrames
        resource_df = pd.DataFrame({
            'renewable': [renewable_resources],
            'nonrenewable': [nonrenewable_resources],
            'doubly_constrained': [doubly_constrained_resources]
        })

        precedence_df = pd.DataFrame(precedence_relations, columns=['jobnr', 'modes', 'successors_count', 'successors'])
        requests_df = pd.DataFrame(requests_durations, columns=['jobnr', 'mode', 'duration', 'resources'])
        availability_df = pd.DataFrame(resource_availabilities, columns=['R1', 'R2', 'R3', 'R4'])

        return resource_df, project_info, precedence_df, requests_df, availability_df

    # Path to the .sm file
    file_path = 'j30.sm/j301_1.sm'

    # Parse the file
    resource_df, project_info, precedence_df, requests_df, availability_df = parse_sm_file(file_path)

    # Display the data
    print("Resources:")
    print(resource_df)
    print("\nProject Information:")
    print(project_info)
    print("\nPrecedence Relations:")
    print(precedence_df)
    print("\nRequests and Durations:")
    print(requests_df)
    print("\nResource Availabilities:")
    print(availability_df)