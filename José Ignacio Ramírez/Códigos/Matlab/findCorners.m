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

function [corners, radii, metric] = findCorners(imgIn)
    threshold = 1.05;
    thresholdStep = 0.1;
    circleThreshold = 0.65;
    largeContours = 0.15;
    firstSweep = true;
    
    IBW=rgb2gray(imgIn);

    corners = [];
    while(length(corners) ~= 4)
        disp(strcat('Trying with\t', num2str(threshold)))
        if(length(corners) > 4 && firstSweep)
            return
            thresholdStep = -0.01;
            firstSweep = false;
        elseif(thresholdStep == 1 && not(firstSweep))
            return
        elseif(length(corners) < 4)
            thresholdStep = 0.1;
        end
        
        threshold = threshold - thresholdStep;
           
        BW = edge(IBW,'Canny',threshold);
        boundaries = bwboundaries(BW,'noholes');
        s = regionprops(BW, 'Perimeter');
        perimeters = cat(1, s.Perimeter);
        if(length(perimeters) > 1)
            IDs = 1:length(perimeters);
            [perimeters, IDs] = dependentSort(perimeters', IDs);
            perimeters = perimeters';
            for perimeterID = 1:length(perimeters)-1
                proportion = abs(perimeters(perimeterID)-perimeters(perimeterID+1))/perimeters(perimeterID);
                if(proportion > largeContours)
                    contour = cell2mat(boundaries(IDs(perimeterID)));
                    [BW] = deleteContour(contour',BW);
                end
            end
        end
        BWFilled = imfill(BW, 'holes');
        warning ('off','all');
        s = regionprops(BWFilled, 'Perimeter');
        perimeters = cat(1, s.Perimeter);
        radii = perimeters/(2*pi());
        [centers, radii, metric] = imfindcircles(BWFilled,[floor(min(radii)), ceil(max(radii))], 'Sensitivity', circleThreshold);
        corners = centers;
        disp(length(corners))
        warning ('on','all');
    end
end

