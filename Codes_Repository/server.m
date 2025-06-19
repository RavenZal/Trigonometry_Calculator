% clear; close all; clc;
function startServer()
    t = tcpip('0.0.0.0', 12345, 'NetworkRole', 'server');
    fopen(t);
    disp('Matlab Server Started.');
    % 数据结构要求 字段顺序：函数名,角度值,单位数值;精度：8位小数;单位限制：仅接受degree或radian
    try
        while true
              % TODO:读取数据

              
            if strcmpi(unit, 'degree')
                angle_rad = deg2rad(angle);
            else
                angle_rad = angle;
            end%将角度转化为弧度
        
            switch lower(func{1})
                case 'sin'
                    result = sin(angle_rad);
                case 'cos'
                    result = cos(angle_rad);
                case 'tan'
                    result = tan(angle_rad);
                otherwise
                    error('Invalid function');
            end
            fwrite(t, num2str(result, '%.8f'));% 返回结果
        end
    catch
        fclose(t);
    end
end
