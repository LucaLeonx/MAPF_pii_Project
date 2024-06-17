def main():
    dictionary = {"old_key": 0}
    dictionary["key"] = 10
    dictionary["old_key"] = 11
    print(dictionary["key"])
    print(dictionary["old_key"] == 11)


if __name__ == "__main__":
    main()
