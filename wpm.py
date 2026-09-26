from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from time import perf_counter

def scraper():
    try:
        return (
            urlopen(f"https://baconipsum.com/api/?type=all-meat&paras=2&format=text")
            .read()
            .decode()
        )
    except HTTPError:
        print("Website not available")
        exit()
    except URLError:
        print("No Internet")
        exit()


def user_input(original):
    while True:
        start = perf_counter()

        typed = input(f"{original}\n: ")
        if typed == "q":
            exit()

        end = perf_counter()

        return typed, start, end


def wpm(typed, start, end):
    return (len(typed) / 5) / ((end - start) / 60)


def accuracy(typed, original):
    return (
        sum(a == b for a, b in zip(typed, original))
        / max(len(typed), len(original))
        * 100
    )


def main():
    while True:
        original = scraper()
        typed, start, end = user_input(original)
        print(
            f"\nWPM = {wpm(typed, start, end):.2f}\nAccuracy = {accuracy(typed, original):.2f} %\n"
        )


main()
