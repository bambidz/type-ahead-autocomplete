from pathlib import Path
import os
import json

if __name__ == "__main__":

    data_folder = Path(os.path.dirname(__file__)).parent / "data"
    readfile = data_folder / "prefix_dict.json"

    with open(readfile,"r") as json_file:
        data = json.load(json_file)
        prefix_dict = data
        # lines = content.split('\n')
        # for line in lines:
        #     if line == "":
        #         continue
        #     prefix, tmp_word_list = line.split(':')
        #     word_list = tmp_word_list.split()
        #     prefix_dict[prefix] = word_list

        while(1):
            sp = input("Next prefix to search : ")  # input search prefix
            if sp == "q!":  # quit
                break
            if sp not in prefix_dict:
                print("There is no such prefix!\n")
                continue
            print(str(prefix_dict[sp]))