# public inputs
import os
import sys
import pandas as pd

# personal inputs
from option_parser import PrepareArguments
from event_parser import event_info
from visualize_events import viz_events
from event_reader.event_readers import FixedDurationEventReader
from event_reader.timers import Timer
from event_reader.inference_utils import events_to_voxel_grid_pytorch, get_device

def main(args):
    fileName = args.input_file
    size = tuple(map(int, args.window_size.split('x')))
    print('Input file -', fileName)
    print('Image size -', size)
    return fileName, size

if __name__ == "__main__":
    parser = PrepareArguments()
    args = parser.parse_args()
    fileName, size = main(args)
    FullFileName = os.path.join(sys.path[0], fileName)

    device = get_device(True)


    if os.path.isfile(FullFileName):
        event_window_iterator = FixedDurationEventReader(FullFileName)
        print('Starting visualize process, press q to exit')
        with Timer('Processing entire dataset'):
            for event_window in event_window_iterator:
                last_timestamp = event_window[-1, 0]
                # The event tensor here:
                # Type of every element: torch.float32 -> event_tensor.dtype
                # Number of axes: 3 -> event_tensor.ndim
                # Shape of tensor: torch.Size([5, 240, 320]) -> event_tensor.shape
                # Elements along axis 0 of tensor: 5 -> event_tensor.shape[0]
                # Elements along the last axis of tensor: 240 -> event_tensor.shape[-1]
                with Timer('Building event tensor'):
                    event_tensor = events_to_voxel_grid_pytorch(event_window, 5, 320, 240, device)
    else:
        print('File does not exist -', FullFileName)


