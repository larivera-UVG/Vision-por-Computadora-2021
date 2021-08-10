% Función para eliminar un contorno de una imágen luego de una detección
% de bordes.
% Parámetros:
%   contour - Array de puntos que contiene el contorno.
%   imgIn   - Imágen binarizada de la que se desea eliminar el contorno.
%   imgOut  - Imágen binarizada con el contorno eliminado.

function [imgOut] = deleteContour(contour,imgIn)
    for point = contour
        imgIn(point(1), point(2)) = 0;
    end
    imgOut = bwareaopen(imgIn, 10);
end