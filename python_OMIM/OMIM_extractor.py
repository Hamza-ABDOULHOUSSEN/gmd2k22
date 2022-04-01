import pandas as pd

def main():
    omim = pd.read_csv("../OMIM/omim_onto.csv", header=0)
    print(omim["Class ID"][0])
    print(omim.columns)
    First_row = []
    for col in omim.columns:
        First_row.append(omim[col][0])

    print(First_row)


if __name__ == '__main__':
    main()
