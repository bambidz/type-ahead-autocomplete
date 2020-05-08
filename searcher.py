

if __name__ == "__main__":

    f = open("prefix_dict.txt","r",encoding='UTF8')
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
        print(str(prefix_dict[sp]))