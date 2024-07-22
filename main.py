from messages import TEST_MESSAGES
from tester import test


def main() -> None:
    for index, message in enumerate(TEST_MESSAGES):
        print(f'message {index}: {test(message)}')


if __name__ == '__main__':
    main()
