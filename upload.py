from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, Region
import os
import sys
import yaml

def Usage():
    print (f'{sys.argv[0]} source-path')
    sys.exit(1)

if __name__=='__main__':
    if len(sys.argv) != 2:
        Usage()

    src_path = sys.argv[1]

    if not os.path.exists(src_path): 
        print (f'path not exists: {src_path}')
        sys.exit(1)

    with open("settings.yml", 'r') as ymlfile:
        settings = yaml.load(ymlfile)

    trainer = CustomVisionTrainingClient(settings['training_key'], endpoint=settings['endpoint'])

    project = trainer.get_project(settings['project_id']) # project id

    print ("reading images...")
    imageEntries = []
    for file_name in os.listdir(src_path):
        with open(os.path.join(src_path, file_name), mode="rb") as image_contents:
            imageEntries.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=[]))

    print(f'uploading images to custom vision project [{project.name}]...')
    upload_result = trainer.create_images_from_files(project.id, images=imageEntries)
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        exit(-1)
    print('done.')