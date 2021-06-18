from collections import defaultdict
import yaml
import re
import os
import time
import logging
import multiprocessing
from queue import Queue
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve

logger = logging.getLogger()
fhandler = logging.FileHandler(filename='logfile-comparison.log', mode='a')
formatter = logging.Formatter('[%(threadName)s, %(processName)s, %(asctime)s, %(levelname)s] %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)


class ComparisonService(object):
    def __init__(self, yml_file, home_dir='.'):
        self.home_dir = home_dir
        self.dir = "{}{}{}".format(self.home_dir, os.path.sep, 'downloaded_files')
        self.yml_file = yml_file
        self.file_list = []

    def format_yml_file(self, yml_file):
        services_lines = {}
        with open(yml_file) as file:
            services_list = yaml.load(file, Loader=yaml.FullLoader)
            for key, value in services_list.items():
                services_lines[key] = {'version': value}
        return services_lines

    def download_file(self, dl_queue):
        while not dl_queue.empty():
            try:
                url = dl_queue.get(block=False)
                logger.info("url {}".format(url))
                # download each file and save to the dir
                filename = urlparse(url).path.split('/')[-1]
                file_path = "{}{}{}".format(self.dir, os.path.sep, filename)
                urlretrieve(url, file_path)
                self.file_list.append(file_path)
                logger.info("download file {}".format(filename))
                dl_queue.task_done()
            except Queue.Empty:
                logger.info("Queue empty")

    def format_txt_file(self, txt_file, wrong_services):
        table_lines = {}
        with open(txt_file) as file_txt:
            i = 0
            for line in file_txt:
                i += 1
                if i > 1:
                    list_line = line.split()
                    first_line = list_line[0].replace('-', '_')
                    if len(list_line) == 11:
                        chart = re.split(r'\-d*\.?\d+', list_line[8])[0]
                        table_lines[first_line] = {'status': list_line[7], 'chart': chart, 'version': list_line[9]}
                    else:
                        wrong_services['MALFORMED ROW'].append('File {}:: service: {}'.format(txt_file, first_line))
        os.remove(txt_file)
        return table_lines

    def compare_file(self, txt_file):
        wrong_services = defaultdict(list)
        services_lines = self.format_yml_file(self.yml_file)
        table_lines = self.format_txt_file(txt_file, wrong_services)
        for service in services_lines:
            found = False
            for output in table_lines:
                if service == output:
                    found = True
                    if table_lines[output]['status'] != 'DEPLOYED':
                        wrong_services['FAILED'].append(output)
                    if table_lines[output]['version'] != services_lines[service]['version']:
                        wrong_services['WRONG VERSION'].append('{}:: service version: {}, output version: '
                                                                    '{}'.format(service, services_lines[service]['version']
                                                                                , table_lines[output]['version']))
                else:
                    if table_lines[output]['chart'] == service:
                        found = True
            if not found:
                wrong_services['NOT FOUND'].append(service)
        non_duplicated_values = self.unique_results(wrong_services)
        logger.info("Not repeated values {}".format(non_duplicated_values))
        logger.info("Wrong services {}".format(wrong_services))

    def unique_results(self, wrong_services):
        result = set()
        for service_key, service_value in wrong_services.items():
            result.update(service_value)
        return result

    def make_comparison(self, file_url_list):
        logger.info("START make_comparison")
        pool = multiprocessing.Pool()
        start = time.perf_counter()
        dl_queue = Queue()
        for file_url in file_url_list:
            dl_queue.put(file_url)

        num_dl_threads = 4
        for _ in range(num_dl_threads):
            t = Thread(target=self.download_file, args=(dl_queue,))
            t.start()

        dl_queue.join()

        start_eval = time.perf_counter()
        pool.map(self.compare_file, self.file_list)
        end_eval = time.perf_counter()

        pool.close()
        pool.join()

        end = time.perf_counter()
        logger.info("created {} files and compare the using multiprocess in {} seconds".format(len(self.file_list)
                                                                                               , end_eval - start_eval))
        logger.info("END comparison in {} seconds".format(end - start))

