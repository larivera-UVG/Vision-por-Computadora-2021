% Función que ordena una variable (dependentVar) respecto a otra
% manteniendo la correspondencia de los índices entre estas dos variables.
% Por ejemplo, si se desea ordenar a alumnos por orden de estatura, se
% ingresan estas como el primer parámetro y los nombres como el
% segundo.
% Parámetros:
%   numbers - Vector con números bajo los cuales se ordenará (pueden ser
%   tamaños, edades o cualquier otro valor numérico que se desee).
%   dependentVar - Vector de variables dependientes que se deean ordenar
%   (por ejemplo nombres).
%   direction - 'ascend' o 'descend' dependiendo si se desea orden
%   ascendiente o descendiente.
%   numbersOut - Vector "numbers" ordenado de manera descendiente.
%   dependentVarOut - Vector "dependentVar" ordenado manteniendo los
%   índices originales de "numbers".

function [numbersOut, dependentVarOut] = dependentSort(numbers, dependentVar, direction)
    dictionary = containers.Map;
    index = 1;
    dimension = 1;
    if(size(numbers, 1)<size(numbers,2))
        dimension = 2;
        dependentVar = dependentVar';
    end
    for numberID = 1:size(numbers,dimension)
        number = numbers(numberID);
        if(isKey(dictionary, num2str(number)))
            dictionary(num2str(number)) = [dictionary(num2str(number)), dependentVar(index,:)'];
        else
            dictionary(num2str(number)) = dependentVar(index,:)';
        end
        index = index + 1;
    end
    numbersOut = sort(numbers, direction);
    dependentVarOut = [];
    last = 0;
    for numberID = 1:size(numbersOut,1)
        number = numbersOut(numberID);
        if ~(number == last)
            dependentVarOut = [dependentVarOut, dictionary(num2str(number))];
        end
        last = number;
    end
end

