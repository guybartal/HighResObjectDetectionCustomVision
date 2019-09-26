# split high resolution photos into smaller tiles and upload them into custom vision object detection

Microsft Custom Vision service has a file size limit of 6MB for training and 4MB for infrencing,
it also resizes images to 256x256 so if your goal to detect small objects inside high resolution photos and ypu want to take advantage of transfer learning with super easy service like Microsft Custom Vision then you an use this tool.  

split.py gets the following arguments:
•	source path (high res photos should be here)
•	target path (all tiles get generated here)
•	width of the tile in pixels
•	height of the tile in pixels
•	overlapping margin in pixels


upload.py gets only the source path where the generated tiles resides.

## setup
install python 3.7 (Anaconda is recommended)
clone this repo
open Anaconda Prompt
change directory to your cloned repo
pip install -r requirements.txt

## Usage
copy all your high resolution photos into "original" folder inside the repo folder
and run the following command

python split.py ./original ./tiles/ 2900 1600 200

after running this part you can validate that the photos spited to tiles correctly and under 6MB, you can play with the width, height and overlapping margin.
don't forget to delete tiles before running split.py again.

to upload the tiles to your custom vision project, rename "settings-template.yml" to "settings.yml" and configure your custom vision keys:

endpoint: <your-custom-vision-endpoint>
training_key: <your-custom-vision-project-training-key>
project_id: <your-custom-vision-project-project-id>

after that just run the following command, and refresh unlabeled images inside custom vision:

python upload.py ./tiles




