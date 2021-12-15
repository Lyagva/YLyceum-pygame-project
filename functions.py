def normalize(a, b):
    return a / max(a, b), b / max(a, b)


if __name__ == "__main__":
    print(normalize(2, 5))