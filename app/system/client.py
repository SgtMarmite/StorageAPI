import json
import requests
import pandas as pd
import os
import urllib3


class KeboolaStorageAPI:
    """A class used for API call to https://keboola.docs.apiary.io/#reference/files/list-files/list-files
    Auth token is provided by user via a config.json file stored in os.path.dirname(os.path.abspath(__file__)).
    Uses query parameter showExpired=true. See docs above for more info.
    Uses limit and offset query parameters to iterate through the results.

    Parameters
    ----------
    url: str, mandatory
        Target url

    limit: str, default=100
        Pagination limit
        https://keboola.docs.apiary.io/#reference/files/list-files/list-files

    silent: bool, default=True
        Set to false if you want to receive InsecureRequestWarning

    Attributes
    ----------
    path: str
        This is used as a directory to look for config.json and as a directory to store results.
        Now only uses os.path.dirname(os.path.abspath(__file__))

    headers: dict
        Used to load user token into from config.json.

    Examples
    --------
    KeboolaAPITask(url='https://connection.eu-central-1.keboola.com/v2/storage/files').store_csv()
    """

    def __init__(self, url: str, limit: int = 100, silent: bool = True):
        self.url = url
        self.limit = limit
        self.silent = silent

        self.path = os.path.dirname(os.path.abspath(__file__))

        try:
            with open(os.path.join(self.path, 'config.json')) as json_file:
                self.headers = json.load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError('File config.json not found.')

    def get_to_list(self) -> list:
        """Performs a request or a series of requests to https://connection.eu-central-1.keboola.com/v2/storage/files.
        To be used with methods like to_csv.

        Returns
        -------
        results : list
            list of dicts with results from API calls

        Raises
        ------
        ConnectionError
            In case of target url being unreachable.
        """
        offset = 0
        results = []

        while True:
            payload = {
                'limit ': self.limit, 'offset': offset, 'showExpired': 'true'
            }

            try:
                if self.silent:
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

                r = requests.get(self.url,
                                 headers=self.headers,
                                 params=payload,
                                 verify=False)

                r.raise_for_status()

            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)

            json_data = json.loads(r.text)

            for item in json_data:
                results.append(item)

            if len(json_data) < self.limit:
                return results
            else:
                offset += self.limit

    def store_csv(self, sep: str = ';', output_filename: str = 'parsed_result.csv'):
        """Stores result of the get method in csv format to os.path.dirname(os.path.abspath(__file__)).

        Parameters
        ----------
        sep: str, default=';'
            Separator to be used in csv file.

        output_filename: str, default='parsed_result.csv'
            Desired name of the output file.

        """

        results = self.get_to_list()
        df = pd.DataFrame.from_records(results)
        # For now uses index=False.
        df.to_csv(os.path.join(self.path, output_filename), index=False, sep=sep)
        print(f'Successfully stored {output_filename} with {len(df)} rows.')

