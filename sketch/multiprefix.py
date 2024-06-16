def main():
    my_string = "Hello Python"

    # Prefixes (Tuple): must use tuple
    prefixes = ("Javascript", "Php", "Hello")

    # Checking if starts with
    c = my_string.startswith(prefixes)

    # Print Output
    print(c)
    dictionary = {"a": "x", "b": "y"}
    print(type(tuple(dictionary.keys())))


if __name__ == "__main__":
    main()
