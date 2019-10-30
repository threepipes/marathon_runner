import argparse
import runner


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run command and eval score')
    parser.add_argument('command', help='comma separated command')
    parser.add_argument('--run_num', default=3, help='num of running process')
    parser.add_argument('--label', default='noname', help='label of the program')
    args = parser.parse_args()

    runner.main(args)
