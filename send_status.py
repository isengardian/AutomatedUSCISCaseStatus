import time, argparse
from smtplib import SMTPException
from uscis import USCIS
from gmail import Gmail


def init_arg(parser):
    parser.add_argument('-v', action='store_true', help='print verbose information')
    opt = parser.parse_args()
    return vars(opt)


def run(uscis_client, gmail_client, verbose=False):
    try:
        with open('cases', 'r') as f:
            case = f.readline().strip()
            while case:
                split_case = case.split(",")
                case_number = split_case[0]
                to = split_case[1]
                case_number, status = uscis_client.process(case_number, verbose=verbose)
                email_body = gmail_client.build_body(to, Gmail.SUBJECT.format(case_number), status)
                gmail_client.send(to, email_body)
                print('Email sent to [{0}] successfully'.format(to))
                case = f.readline().strip()
                time.sleep(3)
    except SMTPException as e:
        print('Error sending mail: [Message: {0}]'.format(e))
    finally:
        gmail_client.close()


if __name__ == "__main__":
    opt = init_arg(argparse.ArgumentParser())
    run(USCIS(), Gmail(), opt["v"])
