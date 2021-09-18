function Cod = CreadorCodigos(num_codigo)
%CREADORCODIGOS Código que genera los marcadores para identificar los
%robots en la mesa 

%   Recibe números enteros desde 1 hasta 255 ya que codifica en 8 bits para
%   la representación en una imagen de 3x3 cuadros. Los cuadros grises son
%   1 y los cuadros negros son 0. El cuadro blanco es el pivote que sirve
%   para ubicar y rotar el marcador.
%%
%Inputs: num_codigo - Número de 1 a 255 para la generación del marcador
%Outputs: Cod - Matriz de la imagen generada.

%%
num = num_codigo; 
binStr = dec2bin(num,8);
%toma el valor y lo convierte en un string binario
                %el formato es '0bxxx' por lo que se elimina el '0b' 
                %y se garantiza que siempre sean 8 bits.

k = 0; %parametro de control
Cod = zeros(200,200, 'uint8'); %crea un array de zeros que sera la 
            %matriz donde se genera el codigo. Debe ser de tipo int de 8 bits
            %para que pueda reconocer los tonos de grises
            
%variables de control para la ubicación de los cuadrons en la imagen            
control1 = 25;
control2 = 75;
control3 = 50;

for u = 0:2 
    for v = 0:2
        %para generar el pivote (ver la tesis de Andre)
        %El pivote sirve para saber que cuadro debe estar alineado.
       if k == 0
        for i  = u*control3+control1:u*control3+control2 %25:75
            for i2 = v*control3+control1:v*control3+control2
                Cod(i,i2) = 255; %llena el pivote, 255 = blanco
            end
        end
        else
            %genera los otros cuadros en escala de grises, 125 = gris
            count = 9-k;
            if count == 0
                break
            end
            t = binStr(9-k);
            n = str2num(t);
            for i3 = u*control3+control1:u*control3+control2
                for i4 =v*control3+control1:v*control3+control2
                    Cod(i3,i4) = n * 125;
                end
            end
        end
        k = k + 1;
    end
end
%imwrite(Cod,filename);
end

