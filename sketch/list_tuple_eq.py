def main():
    example_list = [1, 2, 3]
    example_tuple = (1, 2, 3)
    example_set = {1, 2, 3}

    empty_list = []
    empty_tuple = ()
    empty_set = {}

    # These comparisons are all False
    print(example_list == example_tuple)
    print(example_list == example_set)

    print(empty_list == empty_tuple)
    print(empty_list == empty_set)


if __name__ == '__main__':
    main()
