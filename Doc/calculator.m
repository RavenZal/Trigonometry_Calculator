    clear; close all; clc;
    %%TODO:接口
    % 用户输入类型
    type_input = input('请输入角度或数值，若角度输入1,数值输入2。', 's');%%输入角度计算三角函数，输入数值计算反三角函数
    switch type_input
        case '1'
        % TODO:输入角度情况下，检测输入，并计算三角函数
            
            
        case '2'
            %TODO:输入数值情况下，检测输入，并计算反三角函数
        otherwise
            fprintf('输入无效，请输入角度或数值，若角度输入1,数值输入2。\n');
    end 
    %%TODO:接口