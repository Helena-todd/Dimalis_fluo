# Dimalis_fluo: a new way of analysing your timelapse images fast and efficiently

<p align="center">
  <img width="500" height="300" src="https://github.com/Helena-todd/Dimalis/blob/main/dimalis_pipeline.png">
</p>

Dimalis_fluo is wrapped in a docker structure, which facilitates its installation on any operating system and allows to perform image denoising, single cell segmentation and cell tracking by running one line of code only!

*Note: On this github page, we provided a few images from a timelapse that you can use as test images for Dimalis_fluo. In order to find them, scroll up to the top of this page and click on the green "Code" button and on "Download zip". The zipped folder that you will download contains a /test_images subfolder, containing raw phase contrast and corresponding fluorescence channel images.*

## Here's a user-friendly step-by-step protocol to analyse cells in your images using Dimalis_fluo:

### Step 1: Install the Docker Desktop App

- **On Mac, Windows and Linux:** You will find the download link and instructions on this website: [Docker Desktop install](https://www.docker.com/products/docker-desktop/)

Once you have completed the installation, you can launch the Docker Desktop App

*Note: if you encounter issues with Docker Desktop on Windows, consider uninstalling it, restarting your computer, and re-installing Docker Desktop with admin rights, as explained on the docker forum (https://forums.docker.com/t/solved-docker-failed-to-start-docker-desktop-for-windows/106976).![image](https://user-images.githubusercontent.com/17719754/218061342-e727dca7-0ca3-4000-ab8a-615f1b2f1df7.png)*

### Step 2: Search for the helenatodd/dimalis_fluo image from the Docker Desktop App

In the docker Desktop App, <br />
(1) Click on the "Search" bar and type "helenatodd/dimalis_fluo"

<p align="center">
  <img width="800" height="450" src="https://github.com/Helena-todd/Dimalis_fluo/blob/main/readme_images/step21.png">
</p>

(1) Then click on "Images" and <br />
(2) click on "Hub images" and <br />
(3) select the "helenatodd/dimalis_fluo:v1.1" docker image by clicking on it. <br />
(4) Finally, click on the "Run" button to download Dimalis_fluo and launch the interface that will allow you to launch Dimalis_fluo on your raw images.

<p align="center">
  <img width="800" height="450" src="https://github.com/Helena-todd/Dimalis_fluo/blob/main/readme_images/step22.png">
</p>

### Step 3: Run Dimalis_fluo on your images

*Note: The images need to respect a certain format so that Dimalis_fluo can read them: the phase contrast or bright field images should be located in an /exported subfolder, and the corresponding fluorescent images should be located in a /fluo_channels sub_folder with one sub-subfolder per fluorescent marker. We provided test data on this github page as an example of how the data should be formatted.*


First, click on the arrow next to "Optional settings" to access the settings of Dimalis_fluo (1):

<p align="center">
  <img width="800" height="450" src="https://github.com/Helena-todd/Dimalis/blob/main/readme_images/step31.png">
</p>

You can now define the Dimalis_fluo parameters: <br />
(1) The first box can stay empty, it allows you to give a name to the container that will be launched, but docker will give it a default name if you don't. <br />
(2) By clicking on those three dots, you will be able to browse, on your computer, into the folder containing the raw images on which you wish to apply Dimalis (or into the /test_images folder that we provided) <br />
(3) Type "/home/test_images/" in this box <br />
(4) Type "DENOISING_SD" in this box. This will allow you to define the standard deviation of noise that you wish to attenuate in your images using the BM3D denoising algorithm <br />
(5) Type the standard deviation value you wish to set (typically between 0.0001 for a very light denoising effect and 0.01 to denoise highly noisy images) <br />  
(6) Click on the "+" button to enter a second parameter

<p align="center">
  <img width="800" height="450" src="https://github.com/Helena-todd/Dimalis/blob/main/readme_images/step32.png">
</p>

You can then provide information on the remaining Dimalis parameters: <br />
(1) Type "CELL_DIAM" in this box. <br />
(2) The "CELL_DIAM" parameter allows you to estimate the rough diameter of cells in your images for optimal cell segmentation (as an example, we always set the cell diameter to 29.5 pixels) <br />
(3) Type "MAX_DIST" in this box. This will allow you to define the maximum distance to look for descendance in a cell's surrounding <br />
(4) Type the maximum distance value you wish to set (as an example, we set this maximum distance to 50 pixels) <br />
(5) Type "MAXANGLE" in this box. This will allow you to define the maximum angle allowed for cell division <br />
(6) Type the maximum angle value you wish to set (as an example, we set this maximum angle to 30°) <br />
(7) Type "APPLY_DENOISING" in this box. This will allow you to skip the time-consuming denoising step if your images are of sufficient quality. <br />
(8) Type "0" if you wish to skip denoising or "1" if you wish to apply denoising on your images. <br />
(9) Finally, you can hit the "Run" button to launch Dimalis on your data <br />

<p align="center">
  <img width="800" height="500" src="https://github.com/Helena-todd/Dimalis/blob/main/readme_images/step33.png">
</p>

### Dimalis_fluo results

After running Dimalis_fluo on your raw images, new subfolders will be generated in the folder where your images are located, that contains the cell denoising, cell segmentation, cell features and cell tracking results. <br />
- the BM3D subfolder contains the denoised images (or, if you skipped denoising, the raw images copied from your original folder) <br />
- the Omnipose subfolder contains the cell masks identified during the cell segmentation step, in TIF format. <br />
- the feature_tables subfolder contains one CSV file per timepoint, in which the cells are represented in rows and their respective features (such as area in pixels, x and y coordinates, ...) are represented in columns. <br />
- the fluo_channels subfolder now contains one extra subfolder per fluorescent channel, that each contains one CSV table per timepoint, with the fluorescent measurements for each cell <br />
- the STrack subfolder contains the tracking results. For each image - 1 (the cells in the 1st image cannot be tracked by definition), STrack returns: 1) a CSV table, that contains the links from cells in the previous to cells in the current image. 2) a PNG image, in which these links are represented as red lines <br />

Dimalis will also return two additional excel formatted files:
- the "complete_tracking_table" (in the STrack subfolder) contains tracks from all timepoints combined
- the "final_merged_table" contains information on cells from all timpoints combined

These two last XLSX files can be used to import Dimalis's results into an open source software for visualizing and editing networks. We provide a tutorial on how to import the results of Dimalis into Cytoscape, and how to visualise and/or edit the tracks, here: <a href="https://github.com/Helena-todd/STrack/blob/master/tutorial.pdf">Cytoscape tutorial</a>








