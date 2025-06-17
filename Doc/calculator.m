    clear; close all; clc;
    %%TODO:接口
    % 数据结构要求 字段顺序：函数名,角度值,单位数值;精度：8位小数;单位限制：仅接受degree或radian
    %%TODO:MATLAB自带函数的边界值处理
    if  type_input(3)==degree
       type_input(2)=2*pi*type_input(2)/360;%将角度转化为弧度
    end
    switch type_input(1)
        case 'sin'
            ans=sin(type_input(2));
        case 'cos'
            ans=cos(type_input(2));
        case 'tan'
            if(type_input(2))==(pi/2)||(3*pi/2)%%TODO:计算tan函数时，输入非法值时处理

            end
            ans=tan(type_input(2));
        case 'cot'
            if(type_input(2))==(pi/2)||(3*pi/2)%%TODO:计算cot函数时，输入非法值时处理
            
            end 
            ans=cot(type_input(2));
        % 输入角度情况下，检测输入，并计算三角函数
            
            
        case 
            %TODO:输入数值情况下，检测输入，并计算反三角函数
        otherwise
           %TODO:输入错误情况下的处理
    end 
    %%TODO:接口
