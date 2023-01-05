import sys
from parser_data import DataParser


# main function gor the task
def main(zip_path: str):
    with DataParser(zip_path) as parser:
        parser.parse()


if __name__ == '__main__':
    import time
    start = time.time()
    path = sys.argv[1]
    main(path)
    print(time.time() - start)
