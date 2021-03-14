
def test():
    import sys

    print(type(sys.argv))
    print('The command line arguments are:')
    for i in sys.argv:
        print(i)

    pass


def test2():
    import getopt
    import sys

    argv = sys.argv[1:]
    argv = "--length 100 --ensemble 20".split()
    # argv = "-L 100 -E 20".split()
    try:
        opts, args = getopt.getopt(argv, 'L:E:h', ['help', "length", "ensemble"])
        print(opts)
        print(args)
    except getopt.GetoptError:
        # Print a message or do something useful
        print('Something went wrong!')
        sys.exit(2)

def test3():
    import argparse

    parser = argparse.ArgumentParser()
    parser.parse_args()
    pass

def help():
    help_list = "L=100 E=20"


if __name__ == '__main__':
    # test()
    test2()
    # test3()

    pass