%% Jose Ignacio Ramirez 
% Codigo base para la herramienta de toma de pose de robotica swarm para la
% mesa de la UVG en version Matlab.
% Basado en el código de André Rodas y José Guerra para la Fase 1 y Fase 2 
% respectivamente de este proyecto. 

%% Calibracion
clear;clc

load('Images.mat', 'I_goodLight_small');

I = I_goodLight_small;
figure(2)
imshow(I)

[corners, radii, metric] = findCorners(I);

fixed_points=[0 0; 640 0; 640 480; 0 480]; %puntos iniciales en la imagen original
[moving_points] = orderCorners(corners(1:4,:), fixed_points);

tform = fitgeotrans(moving_points,fixed_points,'projective');

outviewref = imref2d(size(I));
Itrans = imwarp(I, tform, 'OutputView', outviewref);

%% Plot
figure(1)
subplot(1,2,1)
imshow(I)
hold on
viscircles(corners, radii,'EdgeColor','b');
if(length(corners) > 4)
    for cornerID = 1:length(corners)
        text(corners(cornerID,1), corners(cornerID,2), num2str(cornerID),'Color','blue','FontSize',36)
    end
end
title('Original Image')
subplot(1,2,2)
imshow(Itrans)
title('Calibrated Image')

save('resultados.mat', 'tform', 'outviewref')

%% Pose
clear;clc

pivotThresh = 140;
highThresh = 60;

load('Images.mat', 'I_goodLight_small');

I = I_goodLight_small;
load('resultados.mat');
tic
Itrans = imwarp(I, tform, 'OutputView', outviewref);
CalliBW = rgb2gray(Itrans);
CalliBW = edge(CalliBW,'Canny',0.5);
CalliBW = logical(iclose(CalliBW,kcircle(2))); %BW_Red = iopen(BW_Red, kcircle(2));
s = regionprops(CalliBW, 'Centroid');
centroids = cat(1, s.Centroid);
centroids([1 2],:) = [];
centroids([length(centroids)-1 length(centroids)],:) = [];
figure(1)
imshow(CalliBW)
hold on
viscircles(centroids, repmat(5, 1, length(centroids)),'EdgeColor','b');
for centroidID = 1:length(centroids)
    text(centroids(centroidID,1), centroids(centroidID,2), num2str(centroidID),'Color','red','FontSize',30)
end

Itrans = rgb2gray(Itrans);
rad = 5*ones(9, 1);
[contours, sizes] = getContours(CalliBW);
NumericIDs = zeros(1, floor(length(contours)/2) );
Angles= zeros(1, floor(length(contours)/2) );
for i = 1:length(contours)
%     corners = contours(num2str(i));
%     viscircles(corners, rad,'EdgeColor','b');
%     text(corners(1, 1), corners(1, 2), num2str(i), 'Color','green','FontSize',15)
    if(mod(i, 2) ~= 0)
        
        angle = atan2(centroids(i,2)-centroids(i+1,2), centroids(i+1,1)-centroids(i,1));
        angle = rad2deg(angle);
        if(angle < 0)
            angle = angle + 360;
        end
        angle = angle - 45;
        Angles((i+1)/2) = angle;
        
        %fixed_points=[0 0; 640 0; 640 480; 0 480]; %puntos iniciales en la imagen original
        fixed_points=[0 0; 480 0; 480 480; 0 480]; %puntos iniciales en la imagen original
        moving_points = contours(num2str(i));

        tform = fitgeotrans(moving_points,fixed_points,'projective');

        outviewref = imref2d([size(Itrans,1), size(Itrans,1)]);
        code = imwarp(Itrans, tform, 'OutputView', outviewref);
%         corners = [1/4, 1/4; 1/4, 2/4; 1/4, 3/4;
%                    2/4, 1/4; 2/4, 2/4; 2/4, 3/4;
%                    3/4, 1/4; 3/4, 2/4; 3/4, 3/4;].*flip(size(code));
        corners = [1/4, 1/4; 2/4, 1/4; 3/4, 1/4;
                   1/4, 2/4; 2/4, 2/4; 3/4, 2/4;
                   1/4, 3/4; 2/4, 3/4; 3/4, 3/4;].*flip(size(code));
        
        if(code(corners(3,2), corners(3,1)) > pivotThresh)
            code = imrotate(code, 90);
        elseif(code(corners(7,2), corners(7,1)) > pivotThresh)
            code = imrotate(code, -90);
        elseif(code(corners(9,2), corners(9,1)) > pivotThresh)
            code = imrotate(code, 180);
        end
        NumericID = zeros(1, 8);
        for k = 1:length(corners)-1
            if(code(corners(k+1,2), corners(k+1,1)) > highThresh)
                NumericID(k) = 1;
            else
                NumericID(k) = 0;
            end
        end
        NumericID = bi2de(NumericID, 'right-msb');
%         figure
%         imshow(code)
%         text(0, 0, num2str(NumericID));
        NumericIDs((i+1)/2) = NumericID;
%         disp(i)
%         dots = [];
%         for k = 1:length(corners)
%             dots = [dots;code(corners(k, 2), corners(k,1))];
%             viscircles(corners(k,:), rad(k),'EdgeColor','b');
%             input(num2str(k))
%         end
%         disp(dots)
        % viscircles(corners, rad,'EdgeColor','b');
    end
end
time = toc;
disp(strcat('Tiempo de ejecución: ', num2str(time)))
figure(14)
imshow(Itrans)
hold on
for i = 1:length(contours)
    if(mod(i, 2) ~= 0)
        viscircles(centroids(i,:), 5);
        text(centroids(i,1), centroids(i,2)+15, strcat('ID : ', num2str(NumericIDs((i+1)/2))),'Color','red','FontSize',14)
        text(centroids(i,1), centroids(i,2)+30, strcat('Ángulo : ', num2str(Angles((i+1)/2))), 'Color','red','FontSize',14)
        text(centroids(i,1), centroids(i,2)+45, strcat('Centroide : (', num2str(centroids(i,1)), ',', num2str(centroids(i,2)), ')'), 'Color','red','FontSize',14)
    end
end
