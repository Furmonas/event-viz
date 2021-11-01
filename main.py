# public inputs
import os
import sys
import pandas as pd

# personal inputs
from option_parser import PrepareArguments
from event_parser import event_info
from visualize_events import viz_events

def main():
    parser = PrepareArguments()
    args = parser.parse_args()
    fileName = args.input_file
    size = tuple(map(int, args.window_size.split('x')))
    print('Input file -', fileName)
    print('Image size -', size)
    return fileName, size

if __name__ == "__main__":
    fileName, size = main()
    FullFileName = os.path.join(sys.path[0], fileName)

    if os.path.isfile(FullFileName):
        with open(FullFileName, 'r') as file:
            print('Starting visualize process, press q to exit')
            header = pd.read_csv(FullFileName, index_col=False, nrows=0).columns.tolist()
            events = event_info()
            events.check_header(header)
            print('Header content: {}'.format(events.event_header))
            if os.path.isfile(FullFileName):
                event_visualizer = viz_events(size)
                event_visualizer.start(FullFileName)
    else:
        print('File does not exist -', FullFileName)

