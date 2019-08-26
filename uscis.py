import requests, sys, re
from bs4 import BeautifulSoup


class USCIS(object):
    def __init__(self):
        self.header = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        self.url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
        self.payload = {"changeLocale": "", "appReceiptNum": "", "initCaseSearch": "CHECK STATUS"}

    def get_status(self, case_num, verbose=False):
        self.payload['appReceiptNum'] = case_num
        r = requests.post(self.url, headers=self.header, data=self.payload)

        try:
            bs = BeautifulSoup(r.content, "html.parser")
            current_status = bs.find('div', "current-status-sec").text.replace("Your Current Status:", "")
            current_status = re.sub(r'[\t\n\r+]', "", current_status)
            detail = bs.find('div', "rows text-center").text
            if verbose:
                return case_num, detail.strip()
            else:
                return case_num, current_status.strip()
        except Exception as e:
            print(e)
            sys.exit(-1)

    def process(self, case_number, verbose=False, print_result=True):
        case_num, status = self.get_status(case_number, verbose)
        if print_result:
            print("{}: {}".format(case_num, status))
        return (case_num, status)


if __name__ == "__main__":
    client = USCIS()
    case_number = "WAC1917550788"
    client.process(case_number)
