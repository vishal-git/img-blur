### Blurry Image Detection App

This repository contains code to run a FastAPI app where you can upload an image and the app will tell you whether the image is blurry or not.

To run the app, follow these steps:

1. Clone the repository.
2. Install all dependencies from `requirements.txt`.
3. Run `uvicorn main:app` from the home directory of this repo. Click on the URL to open the app in a browser.
4. Click on 'Upload Image' button on the app to upload and image. Once the image is uploaded, the result will be displayed (blurry or not).

Here's what happened behind the scene:

1. The image is first resized to 224 x 224 (to reduce runtime).
2. Gaussian blur is added to the image to reduce noise.
3. The image is changed to grayscale.
4. The image is transformed by using the Laplacian filter.
5. The blurriness is determined by calculating the variance of the Laplacian. If the variance is high, the image is likely to be clear (not blurry). But if the variance is low (i.e., fewer edges) then the image is likely to be blurry.
