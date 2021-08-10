% Función que ordena que ordenan un set de esquinas para que estas
% coincidan con otro set de esquinas; estas se ordenan por cercanía.
% Parámetros:
%   corners - Array de esquinas a ordenar
%   fixedCorners - Array de esquinas contra las que se comparará la
%   cercanía para establecer el orden.
%   orderedCorners - Array de esquinas "corners" ordenadas

function [orderedCorners] = orderCorners(corners, fixedCorners)

orderedCorners = zeros(4,2);
for corner = corners'
    corner_number = 1;
    counter = 1;
    min_distance = inf;
    for fixed_point = fixedCorners'
        distance_to_fixed = norm(corner-fixed_point);
        if(distance_to_fixed<min_distance)
            min_distance = distance_to_fixed;
            corner_number = counter;
        end
        counter = counter+1;
    end
    orderedCorners(corner_number,:) = corner;
end
end

