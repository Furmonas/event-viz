import argparse

def PrepareArguments():
    parser = argparse.ArgumentParser(description='Event Camera Raw File Visualizer')
    parser.add_argument('-i', '--input_file', required=True, type=str,
                        help='Define CSV INPUT_FILE, where raw event data is to be found')
    parser.add_argument('-s', '--window_size', default='320x240', type=str,
                        help='Define WINDOW_SIZE of output window, default - 320x240')

    return parser