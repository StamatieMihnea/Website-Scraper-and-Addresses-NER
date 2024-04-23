from services.webpage_scraper import ScrapingService
import concurrent.futures
import os


class AsyncScrapingService:
    def __init__(self, domains, max_workers_number, min_websites_per_worker):
        self.domains = domains
        self.workers_number = max_workers_number
        self.min_websites_per_worker = min_websites_per_worker

    def _scrape_task(self, task_domains, idx):
        scraper = ScrapingService()
        current_page_idx = 1
        for domain, location in task_domains:
            thread_info = "THREAD " + str(idx) + "   ( " + str(current_page_idx) + "/" + str(len(task_domains)) + " )  "
            current_page_idx += 1
            if not os.path.exists(location):
                os.makedirs(location)

            text_filename = os.path.join(location, 'index0.txt')
            hyperlinks_filename = os.path.join(location, 'href0.txt')
            errors_filename = os.path.join(location, 'error.txt')
            if os.path.exists(text_filename) or os.path.exists(errors_filename):
                print(thread_info + "Already scraped " + domain)
                continue

            print(thread_info + "The " + domain + " domain is being scraped")

            text, error = scraper.scrape_webpage(domain)
            if error is not None:
                with open(errors_filename, 'w') as error_file:
                    try:
                        error_file.write(error)
                    except Exception as e:
                        print(thread_info + "An error occurred while writing to file" + str(e))
                continue

            if text is not None:
                with open(text_filename, 'w') as text_file:
                    try:
                        text_file.write(text)
                    except Exception as e:
                        print(thread_info + "An error occurred while writing to file" + str(e))

            hyperlinks, error = scraper.get_hyperlinks(domain)
            if error is not None:
                with open(errors_filename, 'w') as error_file:
                    try:
                        error_file.write(error)
                    except Exception as e:
                        print(thread_info + "An error occurred while writing to file" + str(e))
                continue

            if len(hyperlinks) > 0:
                with open(hyperlinks_filename, 'w') as hyperlinks_file:
                    try:
                        list_representation = '['
                        for hyperlink in hyperlinks:
                            list_representation += '"' + str(hyperlink) + '",'
                        list_representation = list_representation[:-1]
                        list_representation += ']'

                        hyperlinks_file.write(list_representation)
                    except Exception as e:
                        print(thread_info + "An error occurred while writing to file" + str(e))
        scraper.cleanup()

    def start_scraping(self):
        maximum_required_workers = len(self.domains) // self.min_websites_per_worker + 1
        if maximum_required_workers < self.workers_number:
            self.workers_number = maximum_required_workers

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers_number) as executor:
            batch_size = len(self.domains) // self.workers_number + 1
            futures = [executor.submit(self._scrape_task, self.domains[i * batch_size:(i + 1) * batch_size], i)
                       for i in range(self.workers_number)]
            concurrent.futures.wait(futures)
