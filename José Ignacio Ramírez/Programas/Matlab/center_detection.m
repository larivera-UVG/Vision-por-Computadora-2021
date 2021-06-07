%% Trabajo de graduacion - Swarm Robotics UVG
%  Función para la detección de centros y esquinas para calibración y
%  detección de pose.
%  Autor: Jose Pablo Guerra
%  Fecha: 10 de enero 2021
%  Entradas: figure_number - numero de figura para mostrar las imagenes y
%                            puntos identificados
%            B - Contornos detectados mediante Canny o algun otro metodo
%            max_size - discriminante de contornos. Este sirve para
%                       eliminar contornos pequeños que no sean de interes o
%                       identificar todos los contornos de de B.
%            FindCorners - Parametro que indica si de los contornos
%                          detectados debe buscar las 4 esquinas para la calibración o no.
% Salidas:  centers_esquinas - array con todos los centros en formato [x,y]
%           esquinas_temporales - array con las 4 esquinas detectadas en
%                                 formato [x,y]

function [centers_esquinas, esquinas_temporales] = center_detection(figure_number,B, max_size, FindCorners)


center_count = 1; %para el conteo de los centros. 

for i=1:length(B)
    C = cell2mat(B(i)); %transforma los datos la posicion i en B a formato matriz.
    Cont = C'; %transpuesta para utilizar la funcion minBoundingBox
    boundingBox = minBoundingBox(Cont); %Genera el cuadro mas pequeño que puede encerar el contorno.
    
    % Ubica las cuatro esquinas del cuadro.
    C2 = boundingBox(:,2); 
    C4 = boundingBox(:,4);
    C3 = boundingBox(:,4);
    sizeX = abs(C2(1) - C4(1));
    sizeY = abs(C2(2) - C4(2));
    
    
    C1 = boundingBox(:,1);
    %plotea las bounding boxes encontradas.
    figure(figure_number);
    plot(boundingBox(2,[1:end 1]),boundingBox(1,[1:end 1]),'r');
    hold on;
    axis equal
    
    %discriminante del contorno, si el contorno esta entre el tamaño maximo
    %entonces procede a ubicar sus centros, sino, lo ignora. 
    if sizeX > max_size || sizeY > max_size
    
    Point2 = [(C2(1)+C4(1))/2,(C2(2)+C4(2))/2];
    
    %Cx = Point2(1);
    %Cy = Point2(2);
    %X = abs(C1(1) - C2(1));
    %Y = abs(C1(2) - C4(2));    
    
    dummy_center = [Point2(2),Point2(1)]; %variable dummy para guardar el centro temporal
    
    
    centers_esquinas(center_count,:) = dummy_center; %[x,y] array de centros identificados.

    %plotea centros identificados por contorno deseado. 
    plot(Point2(2),Point2(1),'go');
    axis equal
    
    center_count=center_count+1;

    end
end

%Encuentra las esquinas. 
%Una vez ubicado todos los contornos de interes, procede a buscar los 2
%maximos y los 2 minimos en la coordenada X. Estos seran las 4 esquinas de
%interes para la calibración de la cámara.

if strcmp(FindCorners,'FindCorners')
    
    esquinas_temporales = zeros(4,2); %genera el array 4x2
    
    for index = 1:2 %setea los primeros indices

        %busca el indicie de los minimos.
        k = find(centers_esquinas(:,2) == min(centers_esquinas(:,2))); 
        esquinas_temporales(index,:) = centers_esquinas(k,:); %agrega ese minimo al arary.
        centers_esquinas(k,:) = []; %elimina el dato encontrado para evitar duplicididad.
    end
    
    for index = 3:4%setea los últimos indices      
        %busca el indicie de los maximos.
        k = find(centers_esquinas(:,2) == max(centers_esquinas(:,2)));
        esquinas_temporales(index,:) = centers_esquinas(k,:);  %agrega ese maximo al arary.
        centers_esquinas(k,:) = []; %elimina el dato encontrado para evitar duplicididad.
    end
else 
    esquinas_temporales = 0;
end


end

