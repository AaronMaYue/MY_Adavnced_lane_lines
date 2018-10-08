**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistored_output.png "distored and undistored image"
[image2]: ./output_images/dist_udist_imgs.png "dist_udist_imgs.png"
[image3]: ./output_images/HLS_channel.png "HLS"
[image4]: ./output_images/sch_and_vch_thresh.png "Color thresh"
[image5]: ./output_images/combine_sx_sy_binary.png "sx and sy"
[image6]: ./output_images/combine_sx_sy_color.png "Output"
[image7]: ./output_images/ROI_view.png "ROI view"
[image8]: ./output_images/warped_rgb_imgs.png "warped_rgb_img"
[image9]: ./output_images/warped_binary.png "warped binary image"
[image10]: ./output_images/histogram.png 'hitogram'
[image11]: ./output_images/warped_plot.png 'warped plot'
[image12]: ./output_images/recover_img.png 'recover image'
[image13]: ./output_images/yv_channel_thresh.png 'yv_channel_thresh image'


[video1]: ./project_video.mp4 "Video"

### Camera Calibration
As we know the real cameras use curved lenses to form an image, and light rays often bend a little too much or too little at the edges of these lenses. In the camera_cal folder contain checkerboard images which I will calibrate camera.
`Cv2.FindChessboardCorners` can get the corner coordinates, in comparing with  the checkerboard, can get the correction coefficient of the camera. `calibrate()` accomplish this function and store in the camera_cal folder.

The following is a picture of the camera before and after correction:

![alt text][image1]

Left images are distorted and right are undistorted.
![alt text][image2]

### Color transforms and gradient transforms
The S channel of HLS and the V channel of HLV can identify the lane lines. Here are the result which I set `s_thresh=(160, 255)`, `v_thresh=(100, 255)`,`sx_thresh=(20, 255)`,`sy_thresh=(10, 255)`. The following image are the final results, and the function that implements this result are `abs_sobel_thresh`, `color_thresh`, and `combine_img` in **`Img_process_func.py`**.

![alt text][image3]

![alt text][image6]

### Warped Image
As shown in the figure below, the region in the red line is the ROI area, which is the main expansion area for identifying the lane line, Here is the `src` and `dst` parameters.

```
src = np.float32([[597, 450], [685, 450], [1027,667], [279, 667]])
```
```
dst = np.float32([[320, 0],[960, 0],[960, 720],[320, 720]])
```
You can get the correlation coefficients by [`cv2.getPerspectiveTransform`](https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#getperspectivetransform) and get the warped image by[`cv2.warpPerspective`](https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#warpperspective).

Here is the ROI area.

![alt text][image7]

Here are the warped images and binary warped images.
![alt text][image8]
![alt text][image9]

### Detect lane pixels and fit to find the lane boundary

After applying calibration, thresholding and perspective transform to the images, then I take a histgram along all the columns in the low half of the images to find the base points, The starting point for the left and right window is determined by finding peaks within a histogram of the image. Here are the histogram plots:
![alt text][image10]

### Determine the curvature of the lane and vehicle position with respect to center.
 I use `Line()` class to keep track of all the interesting parameters you measure from frame to frame which by the `reset_detect_line` and `detect_lane_line` functions. 
 The curvature is calculated by `curvature` function, The following figure is the result of the test.
 ![alt text][image11]
 
 Here are the final results images
 
 ![alt text][image12]
 
 
### Video Pipline
After I turned on my pipline on test images, then I apply pipline on a video steam. Each time I get a new high-confidence measurement, append it to the list of recent measurements and then take an average over n past measurements. I set video frams(buffer) n=10 to soomth over last frames and set `count=0`, if Left or Right can't detected so I use the last frame fit coeffieient and fitx then `count += 1` , if count > 5 reset values and start searching from scratch using a histogram and sliding window.
Here is the final video.

<figure class="center">
<video id="video" width="640" controls="" preload="none" >
	<source id="mp4" src="output_project_video.mp4"
	type="video/mp4" width="640" height="400">
</video>
</figure>

### Discuss
This project take me long time(It does not apply to all situations. 😂 how stupid I am!). I found that different functions and values for different test videos, and find good thresh values not easy, for example:
`s_thresh=(160, 255) & v_thresh=(100, 255)`or `sobelx_thresh = (20, 255) & sobely_thresh = (10, 255)` fit for project_video but not good for challenge_video, finall I found YUV channels which `y_thresh=(180, 255)`, `v_thresh=(0, 120)` are more suitable for the challenge_viedo. Here are the test results.

 ![alt text][image13]
