from typing import List

from PIL import Image


def combine_gifs_horizontally(gif1_path, gif2_path, output_path):
    # Open the GIFs
    gif1 = Image.open(gif1_path)
    gif2 = Image.open(gif2_path)

    # Determine the combined width and the maximum height
    width = gif1.width + gif2.width
    height = max(gif1.height, gif2.height)

    # Initialize frame lists
    gif1_frames = []
    gif2_frames = []

    # Extract frames from the first GIF
    while True:
        gif1_frames.append(gif1.copy())
        try:
            gif1.seek(gif1.tell() + 1)
        except EOFError:
            break

    # Extract frames from the second GIF
    while True:
        gif2_frames.append(gif2.copy())
        try:
            gif2.seek(gif2.tell() + 1)
        except EOFError:
            break

    # Combine frames
    combined_frames = []
    durations = []
    N = max(len(gif1_frames), len(gif2_frames))
    for n in range(N):
        new_frame = Image.new('RGBA', (width, height))
        if n < len(gif1_frames):
            new_frame.paste(gif1_frames[n], (0, 0))
        else:
            new_frame.paste(gif1_frames[-1], (0, 0))
        if n < len(gif2_frames):
            new_frame.paste(gif2_frames[n], (gif1_frames[n].width, 0))
        else:
            new_frame.paste(gif2_frames[-1], (gif1_frames[n].width, 0))
        combined_frames.append(new_frame)
        if n <= 300:
            durations.append(30)
        else:
            durations.append(150)

    # Save the combined frames as a new GIF
    combined_frames[0].save(
        output_path,
        save_all=True,
        append_images=combined_frames[1:],
        duration=durations,
        disposal=2,
        loop=0,
    )


if __name__ == "__main__":
    combine_gifs_horizontally('grasp_arc.gif', 'grasp_insert.gif', 'grasp_compare.gif')
