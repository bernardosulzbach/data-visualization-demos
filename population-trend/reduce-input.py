# This Python 3 script parses the raw CSV dump into a meaningful report.

import csv
import json
import statistics

if __name__ == '__main__':
    data = []
    with open('raw.csv', newline='') as input_file:
        reader = csv.reader(input_file)
        next(reader)  # Skip the headers
        for row in reader:
            labels = [row[0], row[1]]
            last_years_strings = row[-5:-2]  # The very last value of the dump is always empty
            if '' in last_years_strings:
                continue
            last_years = [int(value) for value in last_years_strings]
            current = last_years[-1]
            # Simply take the average percentage change
            trend = statistics.mean((last_years[1] / last_years[0], last_years[2] / last_years[1]))
            data.append({'labels': labels, 'current': current, 'trend': trend})
    with open('processed.json', 'w') as output_file:
        json.dump(data, output_file)
