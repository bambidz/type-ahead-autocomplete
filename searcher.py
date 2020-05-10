from pathlib import Path
import os

if __name__ == "__main__":

    data_folder = Path(os.path.dirname(__file__)) / "data"
    readfile = data_folder / "prefix_dict.txt"

    with open(readfile,"r",encoding='UTF8') as f:
        content = f.read()
        f.close()

        prefix_dict = {}

        lines = content.split('\n')

        for line in lines:

            if line == "":
                continue

            word_list = []
            prefix, tmp_word_list = line.split(':')
            word_list = tmp_word_list.split()

            prefix_dict[prefix] = word_list

        while(1):
            sp = input("Next prefix to search : ")  # input search prefix
            if sp not in prefix_dict:
                print("There is no such prefix!\n")
                continue
            if sp == "q!":  # quit
                break
            print(str(prefix_dict[sp]))