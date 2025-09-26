from transforms_py import hello, hello_t, hello_from_bin, PyRegistry

def main():
    print(hello())
    print(hello_t())
    print(hello_from_bin())

    registry = PyRegistry(60)
    registry.add_transform(1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 1.0, 1234567890, "parent_frame", "child_frame")
    transform = registry.get_transform("parent_frame", "child_frame", 1234567890)
    print(transform)

if __name__ == "__main__":
    main()