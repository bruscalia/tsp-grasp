from PIL import Image, ImageSequence


# Function to combine two GIFs in sequence
def combine_gifs(gif1_path, gif2_path, output_path):
    # Open the two GIFs
    gif1 = Image.open(gif1_path)
    gif2 = Image.open(gif2_path)

    # Create a list to hold the frames
    frames = []
    durations = []

    # Extract frames from the first GIF
    for frame in ImageSequence.Iterator(gif1):
        frames.append(frame.copy())
        durations.append(30)

    # Extract frames from the second GIF
    for frame in ImageSequence.Iterator(gif2):
        frames.append(frame.copy())
        durations.append(150)

    # Save the combined frames as a new GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        disposal=2,
        loop=0,
        durations=durations
    )


if __name__ == "__main__":
    gif1_path = 'greedy_arc_horizontal.gif'
    gif2_path = 'ls_arc_horizontal.gif'
    output_path = 'grasp_arc_horizontal.gif'
    combine_gifs(gif1_path, gif2_path, output_path)
