from scipy.spatial.distance import squareform, pdist
from tspgrasp import Grasp


def read_tsp_file(file_path):
    # Store the coordinates
    coordinates = []

    # Flags to mark the current section
    coord_section = False

    # Open the file for reading
    with open(file_path, 'r') as file:
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


if __name__ == "__main__":
    X = read_tsp_file("instances/xqc2175.txt")
    D = squareform(pdist(X))
    grasp = Grasp(alpha=1.0, seed=42)
    sol = grasp(D, max_iter=1000, time_limit=180)
    print(sol.tour)
