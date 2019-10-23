from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region
import os
import sys
import yaml
import math
import datetime


def Usage():
    print(f'{sys.argv[0]} source-path')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        Usage()

    src_path = sys.argv[1]

    if not os.path.exists(src_path):
        print(f'path not exists: {src_path}')
        sys.exit(1)

    with open("settings.yml", 'r') as ymlfile:
        settings = yaml.load(ymlfile, Loader=yaml.FullLoader)

    start = datetime.datetime.now()
    print(f'connecting to custom vision project')
    trainer = CustomVisionTrainingClient(settings['training_key'], endpoint=settings['endpoint'])

    project = trainer.get_project(settings['project_id'])
    print(f'connected to project: {project.name}')

    print(f'listing images in path: {src_path}')

    files = os.listdir(src_path)

    batch_size = int(settings['batch_size'])
    batches = math.ceil(len(files) / batch_size)
    print(f'found {len(files)} files to upload in {batches} batches, batch size set to {batch_size}')

    for batch in range(0, batches):
        timestamp = datetime.datetime.now()
        print(f'loading batch #{batch}')
        imageEntries = []
        for index in range(batch * batch_size, min((batch + 1) * batch_size, len(files))):
            file_name = files[index]
            with open(os.path.join(src_path, file_name), mode="rb") as image_contents:
                imageEntries.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=[]))
    
        print(f'uploading batch #{batch} to custom vision project')
        upload_result = trainer.create_images_from_files(project.id, images=imageEntries)
        if not upload_result.is_batch_successful:
            print("image batch upload failed:")
            for image in upload_result.images:
                print(f"image {image.source_url} failed with status: {image.status}")
            #exit(-1) # todo: handle retry
        batch_time = (datetime.datetime.now() - timestamp).seconds
        print(f'finished batch #{batch}, took {batch_time} seconds. estimated time left: {(batches - batch - 1) * batch_time} seconds')
    print(f'done, took {(datetime.datetime.now() - start).seconds} seconds.')
