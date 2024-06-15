
def main():
    arr1 = [1, 2, 3]
    arr2 = [5, 6]
    arr3 = [1, 2]
    arr4 = [1, 2, 3]

    for a, b in zip(arr1, arr2):
        print(a, b)

    for c, d in zip(arr1, arr2):
        print(c, d)


if __name__ == '__main__':
    main()