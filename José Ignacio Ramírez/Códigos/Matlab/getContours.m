% Función que encuentra los contornos de una imágen provista.
% Parámetros:
%   imgIn - Imágen que será procesada binarizada.
%   contours - Estructura que contiene arrays con los puntos 4 puntos que
%   encierran cada uno de los contornos encontrados (exceptuando los
%   primeros dos y los últimos dos, ya que estas son las esquinas).
%   lengths - Longitudes de los cuadrados que encierran los contornos en
%   pixeles.

function [contours, lengths] = getContours(imgIn)
    contours = containers.Map();
    
    boundaries = bwboundaries(imgIn, 'noholes');
    boundaries([1 2 length(boundaries)-1 length(boundaries)]) = [];
    lengths = zeros(1, length(boundaries));
    for i = 1:length(boundaries)
        C = cell2mat(boundaries(i))';
        boundingBox = minBoundingBox(C);
        contours(num2str(i)) = [boundingBox(2,:)', boundingBox(1,:)'];
        lengths(i) = norm(boundingBox(:, 1)-boundingBox(:,2));
    end
end