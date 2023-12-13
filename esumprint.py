def print_event(event):
    """
    Print Esum (singles) events acquired from the PennPET Explorer in the followint format (column by column):

    1. type of data: 2-regular singles data; 14-end of frame (EOF); 15-start of frame (SOF)

    2. frame number: range 0-7

    3. timestamp: range 0-2^24-1 and is per frame. Each time bin corresponds to 5 ns/2^8 = 19.53 ps

    4. x (tangential) address, range 0-575 (each module: 2 pixels x 4 dies x 4 tiles along x; 18 modules in a ring)

    5. z (axial) address, range 0-391 (2 pixels x 4 dies x 7 tiles along z for each ring). 0-55 for ring 1, 56-111 for ring 2, ...

    6. energy: 13 bit. By default bin #1000 corresponds to 511 keV. 

    7. ring number
    """
    print(f"{event.mode():2} {event.frame():2} {event.t():8} {event.x():4} {event.z():2} {event.e():4} {event.ring():1}")


def read_header(input_file, header_size):
    """
    Read the header of Esum file
    
    This has to be done before reading the events encoded in binary format
    """
    header_data = input_file.read(header_size)
    # Process the header data as needed

