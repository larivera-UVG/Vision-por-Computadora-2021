% Script con pruebas independientes realizadas antes de la implementación
% en un código final.
%% Cam

cams = webcamlist;
cam = webcam('USB');

imgLow = snapshot(cam);

resolutions = cam.AvailableResolutions;
cam.Resolution = string(resolutions(length(resolutions)));

imgHigh = snapshot(cam);
figure()
subplot(1, 2, 1)
imshow(imgLow)
subplot(1, 2, 2)
imshow(imgHigh)

preview(cam);

%% Procesamiento

imgName = 'Calibracion_ejemplo.png';

color_im = imread(imgName);
gscale_im = rgb2gray(color_im);

%BW = imbinarize(gscale_im,'adaptive','Sensitivity',0.9);
BW = imbinarize(gscale_im,'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);

figure(1); clf
subplot(2, 1, 1)
imshow(color_im)
subplot(2, 1, 2)
imshow(BW)

maskedImg = gscale_im;
maskedImg(~BW) = 0;
subplot(2, 1, 1)
imshow(maskedImg)
