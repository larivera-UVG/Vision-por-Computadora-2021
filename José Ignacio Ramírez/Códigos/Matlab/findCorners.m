% Función que encuentra las esquinas (círculos) en la imágen proveida. Esto
% lo hace a través de un barrido de threshold de un filtro Canny. Se
% detiene al momento de encontrar 4 o más círculos.
% Parámetros:
%   imgIn - Imágen que será procesada en RGB.
%   corners - Array de 2Xn con los centroides de los n círculos
%   encontrados.
%   radii - Array con radios de los círculos encontrados en pixeles (en el 
%   mismo orden que "corners").
%   metric - Array con datos del 0 al 1 que denotan la "redondez" de cada
%   círculo encontrado (en el mismo orden que "corners"); 1 siendo un
%   círculo perfecto

function [corners, radii, metric, threshold] = findCorners(imgIn)
    threshold = 1.05;
    thresholdStep = 0.1;
    circleThreshold = 0.75;
    largeContours = 0.15;
    
    IBW=rgb2gray(imgIn);

    corners = [];
    while(length(corners) < 4)
        disp(strcat('Trying with\t', num2str(threshold)))
        
        threshold = threshold - thresholdStep;
           
        BW = edge(IBW,'Canny',threshold);
        BWFilled = imfill(BW, 'holes');
        boundaries = bwboundaries(BWFilled,'noholes');
        s = regionprops(BWFilled, 'Perimeter');
        perimeters = cat(1, s.Perimeter);
        figure(1);clf
        imshow(BWFilled)
        if(length(perimeters) > 1)
            IDs = 1:length(perimeters);
            [perimeters, IDs] = dependentSort(perimeters, IDs', 'descend');
            perimeters = perimeters';
            for perimeterID = 1:length(perimeters)-1
                proportion = abs(perimeters(perimeterID)-perimeters(perimeterID+1))/perimeters(perimeterID);
                if(proportion > largeContours)
                    disp('Deleting')
                    contour = cell2mat(boundaries(IDs(perimeterID)));
                    [BWFilled] = deleteContour(contour',BWFilled);
                end
            end
        end
        warning ('off','all');
        s = regionprops(BWFilled, 'Perimeter');
        perimeters = cat(1, s.Perimeter);
        radii = perimeters/(2*pi());
        disp(length(perimeters))
        [centers, radii, metric] = imfindcircles(BWFilled,[floor(min(radii)), ceil(max(radii))], 'Sensitivity', circleThreshold);
        corners = centers;
        warning ('on','all');
    end
end

