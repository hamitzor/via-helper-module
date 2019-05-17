"""Extract metadata from video."""
if __name__ == "__main__":
    import cv2
    import time
    from os import path
    import argparse
    import json
    import uuid

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "video_file", help="File to extract meta data")

    parser.add_argument(
        "thumbnail_save_directory", help="Directory to save thumbnail")

    args = parser.parse_args()
    video_file = path.abspath(args.video_file)

    if not path.isfile(video_file):
        print "%s is not a file" % video_file
        exit(-1)

    # read video file to extract meta data
    video_cap = cv2.VideoCapture(video_file)
    fps = video_cap.get(cv2.CAP_PROP_FPS)
    frame_count = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, (frame_count/2)-1)
    res, frame = video_cap.read()
    random = str(uuid.uuid4())

    thumbnail_name = random+'.jpg'

    thumbnail = args.thumbnail_save_directory+'/'+thumbnail_name

    cv2.imwrite(thumbnail, frame)

    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_cap.release()

    length = (frame_count/fps)*1000
    size = path.getsize(video_file)

    data = dict(
        length=length,
        size=size,
        fps=fps,
        frame_count=frame_count,
        width=width,
        height=height,
        thumbnail=thumbnail_name)

    print json.dumps(data, indent=2)

    exit(0)
