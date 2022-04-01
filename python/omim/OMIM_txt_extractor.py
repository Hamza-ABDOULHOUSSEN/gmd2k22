
def main():
    omim = open("../../OMIM/omim.txt", "r", encoding="utf-8")
    output = ""

    lines = omim.readlines()
    for line in lines:
        if line[0] == '*':
            output += line

    print(output)


if __name__ == '__main__':
    main()
