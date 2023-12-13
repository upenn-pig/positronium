from esum_event import Event, HEADER_SIZE, EVENT_SIZE  # esum_event saved as a class
from esumprint import print_event, read_header

## This example adds two columns (1st and 2ndn column) to the original singles data
# Event number (starting from 1)
# Cumulative timestamp - converting original timestamps per frame to global scale

def main():
    input_file_name = '/Users/bdai/Documents/pennPET/data/measurement/positronium/test.esum'
    num_events_to_read = 32768  # Number of events to read in each chunk

    printEventNumber = 1
    printCummulativeTime = 1  # print global timestamps

    ctime = 0  # global timestamps (acrossing frame boundaries)     

    with open(input_file_name, 'rb') as input_file:
        read_header(input_file, HEADER_SIZE)  # Need to read and process the header first

        eventNum = 0  # total events including SOF, EOF, and data event
        singlesNum = 0 # number of singles

        while True:
            event_data_block = input_file.read(EVENT_SIZE * num_events_to_read)

            if not event_data_block:
                break

            events, num_events_read = Event.decode_multiple(event_data_block)

            for event in events:
                eventNum += 1  # Increment event number for each event
                
                if event.isData():
                    singlesNum += 1

                if eventNum < 40:
                    if printEventNumber:
                        print(f"{eventNum:10} ", end=' ')                        
                    if printCummulativeTime:
                        print(f"{(ctime + event.t()):13} ", end=' ')
                        if event.isFrameEnd():  # every frame has 24-bit time bins
                            ctime += (1 << 24)                    
                    print_event(event)  

                if (eventNum % (100 * num_events_to_read) == 0):
                    print(f"{eventNum} events processed...")
    
    print(f"Total number of events: {eventNum}")
    print(f"Total number of singles events: {singlesNum}\n")
    

if __name__ == "__main__":
    main()
