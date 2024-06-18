import yaml


def main():
    dictionary = yaml.safe_load(open("C:\\Users\steve\PycharmProjects\mapfbench\src\mapfbench\\utils\default_associations.yaml"))
    print(dictionary)


if __name__ == '__main__':
    main()
