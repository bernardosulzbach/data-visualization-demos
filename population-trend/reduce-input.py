# This Python 3 script parses the raw CSV dump into a meaningful report.

import csv
import json
import statistics

if __name__ == '__main__':
    ignoring = []
    data = []
    with open('metadata.csv', newline='') as metadata_file:
        reader = csv.reader(metadata_file)
        next(reader)  # Skip the headers
        for row in reader:
            if len(row[1].strip()) == 0:  # Not a country
                ignoring.append(row[0])  # Add to the ignores
    with open('raw.csv', newline='') as input_file:
        reader = csv.reader(input_file)
        next(reader)  # Skip the headers
        for row in reader:
            labels = [row[0], row[1]]
            if labels[1] in ignoring:
                continue  # Ignore this entry because it is not a country
            last_years_strings = row[-5:-2]  # The very last value of the dump is always empty
            if '' in last_years_strings:
                continue  # Ignore this entry because there is not enough recent data
            last_years = [int(value) for value in last_years_strings]
            current = last_years[-1]
            # Simply take the average percentage change
            trend = statistics.mean((last_years[1] / last_years[0], last_years[2] / last_years[1]))
            data.append({'labels': labels, 'current': current, 'trend': trend})
    with open('processed.json', 'w') as output_file:
        json.dump(data, output_file, sort_keys=True, indent=4, separators=(',', ': '))
