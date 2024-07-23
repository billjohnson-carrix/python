import re
import csv

def process_file(input_file, output_file, nonmatched_file):
    
    line_pattern = re.compile('^ ?([0-9]{2}/[0-9]{2}/[0-9]{4}| {10}) {2}[A-Z]{3,4} {3,4}([A-Za-z0-9]{5,9}).*')
    
    results = []
    notmatched = []
    
    try:
        # Open input file for reading
        with open(input_file, 'r') as f_input:
            # Read all lines from input file
            lines = f_input.readlines()
            
            # Initialize variables to store current record data
            current_date = None
            current_license_plate = None

            # Process each line
            for line in lines:
                # Match Line
                match_line = line_pattern.match(line)
                if match_line:
                    if match_line.group(1) != "          ":
                        current_date = match_line.group(1)
                    current_license_plate = match_line.group(2)
                else:
                    notmatched.append(line)

                # Check if all fields are populated, then store as a record
                if current_license_plate is not None:
                    #print(match_line.group(0))
                    matched_line = match_line.group(0)
                    in_time = strip(matched_line[63:72])
                    out_time = strip(matched_line[78:87])
                    
                    record = {
                        'date': current_date,
                        'license': current_license_plate,
                        'in time': in_time,
                        'out time': out_time
                    }
                    results.append(record)
                    
                    # Reset variables for next record
                    current_license_plate = None
                    current_in_gate_time = None
                    current_out_gate_time = None

#        fieldnames = ['date','license','group3','in time','out time','group6','group7','group8','group9']

        fieldnames = ['date','license','in time','out time']


        # Open output file for writing
        with open(output_file, 'w', newline = '') as f_output:
            # Write processed lines to output file
            writer = csv.DictWriter(f_output, fieldnames=fieldnames)
            writer.writeheader()
            for record in results:
                writer.writerow(record)
        
        print(f"Successfully processed and saved to {output_file}")
        
        with open(nonmatched_file, 'w') as misses:
            for line in notmatched:
                misses.write(line + '\n')
        
        print(f"Nonmatched lines written to {nonmatched_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")

# Example usage:
if __name__ == "__main__":
    input_file = "mgb055br c60 april 2024.txt"    # Replace with your input file path
    output_file = "c60 april 2024.csv"  # Replace with your desired output file path
    nonmatchedlines_file = "c60 april 2024 nonmatched lines.txt"
    
    process_file(input_file, output_file, nonmatchedlines_file)
