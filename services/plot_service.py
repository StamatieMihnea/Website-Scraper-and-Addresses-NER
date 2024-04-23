import matplotlib.pyplot as plt
import json
import os


class PlotService:
    def __init__(self):
        self._scraped_websites_directory = 'scraped'

    def scrape_overview_pie(self):
        # Initialize counters
        with_index = 0
        with_empty_index = 0
        with_error = 0

        # Scan the directory and count the number of folders with/without index0.html
        for folder in os.listdir(self._scraped_websites_directory):
            subdir = os.path.join(self._scraped_websites_directory, folder)

            if not os.path.isdir(subdir):
                continue

            if os.path.exists(os.path.join(subdir, 'error.txt')):
                with_error += 1
                continue

            index_file_path = os.path.join(subdir, 'index0.txt')
            if not os.path.exists(index_file_path):
                continue

            with open(os.path.join(index_file_path)) as index_file:
                text = index_file.read()

            if len(text) > 1:
                with_index += 1
            else:
                with_empty_index += 1

        # Generate the pie chart
        labels = ['Body found\n' + str(with_index), 'Body empty\n' + str(with_empty_index), 'Error\n' + str(with_error)]
        sizes = [with_index, with_empty_index, with_error]
        colors = ['#66b3ff', '#7a2146', '#ff9999']

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title('Scrape overview')
        plt.show()

    def properties_distribution_bars(self):
        properties_labels = ["none", "country", "region", "city", "postcode", "road", "road_numbers"]
        properties_freq = {key: 0 for key in properties_labels}

        no_properties_labels = range(len(properties_labels))
        no_properties_freq = {key: 0 for key in no_properties_labels}

        # Scan the directory and count the number of folders with/without index0.html
        for folder in os.listdir(self._scraped_websites_directory):
            website_subdir = os.path.join(self._scraped_websites_directory, folder)
            if not os.path.isdir(website_subdir):
                continue

            address_file_path = os.path.join(website_subdir, 'address.txt')
            if not os.path.exists(address_file_path):
                continue

            with open(address_file_path) as address_file:
                address_json = json.load(address_file)

            no_properties = 0
            for address_property in properties_labels[1:]:
                if address_property not in address_json:
                    continue

                if address_json[address_property] is not None:
                    properties_freq[address_property] += 1
                    no_properties += 1

            if no_properties == 0:
                properties_freq["none"] += 1

            no_properties_freq[no_properties] += 1

        # # Generate the pie charts
        plt.bar(properties_labels, list(properties_freq.values()))
        plt.title('Property distribution Overview')
        plt.show()

        plt.bar(no_properties_labels, list(no_properties_freq.values()))
        plt.title('Number of properties distribution Overview')
        plt.show()
