from test_messages import TEST_MESSAGES
from tester import test_au

# ? replace example with the name of the script folder
from auto_responses.example.au import AUTO_RESPONSE


def main() -> None:
    for index, message in enumerate(TEST_MESSAGES):
        test = test_au(message, AUTO_RESPONSE)
        print(f'message {index}: {test}')


if __name__ == '__main__':
    main()
