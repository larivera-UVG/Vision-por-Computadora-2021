% Función que ordena una variable (dependentVar) respecto a otra
% manteniendo la correspondencia de los índices entre estas dos variables.
% Por ejemplo, si se desea ordenar a alumnos por orden de estatura, se
% ingresan estas como el primer parámetro y los nombres como el
% segundo.
% Parámetros:
%   numbers - Vector con números bajo los cuales se ordenará (pueden ser
%   tamaños, edades o cualquier otro valor numérico que se desee).
%   dependentVar - Vector de variables dependientes que se deean ordenar
%   (por ejemplo nombres),
%   numbersOut - Vector "numbers" ordenado de manera descendiente.
%   dependentVarOut - Vector "dependentVar" ordenado manteniendo los
%   índices originales de "numbers".

function [numbersOut, dependentVarOut] = dependentSort(numbers, dependentVar)
    dictionary = containers.Map;
    index = 1;
    for number = numbers
        if(isKey(dictionary, num2str(number)))
            dictionary(num2str(number)) = [dictionary(num2str(number)), dependentVar(index)];
        else
            dictionary(num2str(number)) = dependentVar(index);
        end
        index = index + 1;
    end
    numbersOut = sort(numbers, 'descend');
    dependentVarOut = [];
    for number = numbersOut
        dependentVarOut = [dependentVarOut, dictionary(num2str(number))];
    end
end

