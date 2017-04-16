
def iterFlatten(root):
    if isinstance(root, (list, tuple)):
        for element in root:
            for e in iterFlatten(element):
                yield e
    else:
        yield root

def main():
    b = [["a", ("b", "c")], "d"]
    print(list(iterFlatten(b)))


if __name__ == '__main__':
    main()
    exit()
