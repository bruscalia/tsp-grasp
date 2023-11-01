def read_tsp_file(file_path: str):
    # Store the coordinates
    coordinates = []

    # Flags to mark the current section
    coord_section = False

    # Open the file for reading
    with open(file_path, mode="r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing white spaces

            if line == "NODE_COORD_SECTION":
                coord_section = True  # We've reached the coordinates section
                continue  # Skip the "NODE_COORD_SECTION" line

            if coord_section:
                # Stop reading at EOF or if another section starts
                if line == "EOF" or line.endswith("_SECTION"):
                    break

                # Split the line into components and convert them to integers
                _, x, y = line.split()
                coordinates.append([int(x), int(y)])

    return coordinates
