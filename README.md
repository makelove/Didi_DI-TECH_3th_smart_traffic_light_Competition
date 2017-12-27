# Didi_DI-TECH_3th_smart_traffic_light_Competition
滴滴Di-Tech算法大赛第3届智能信号灯https://ditech.didichuxing.com/

- 声明!注意:
    - 谁看了我的GitHub仓库,拿奖了奖金必须分我一半!:heart_eyes::thumbsup:
    - 不守信请离开!:thumbsdown::no_good:

- 参考
    - [True_Artificial_Intelligence/比赛/滴滴Di-Tech算法大赛](https://github.com/makelove/True_Artificial_Intelligence/tree/master/%E6%AF%94%E8%B5%9B/%E6%BB%B4%E6%BB%B4Di-Tech%E7%AE%97%E6%B3%95%E5%A4%A7%E8%B5%9B) github
    - 
    
- 建议
    - 使用SimPy进行模拟
    - [我的笔记](https://github.com/makelove/True_Artificial_Intelligence/tree/master/Python/SimPy)
    - 视频：[【中文字幕】SimPy仿真 Tutorial 视频教程1 - Introduction to SimPy](https://www.bilibili.com/video/av17474579/)
    
- 运行
    - 在当前目录
        - jupyter notebook
        
- 思路
    - 信号灯与车的交互
        - 红灯停
        - 路灯行
    - 相位
        - 车在十字路口，需要的相位与信号灯的相位.只有2个相位
            - 直行
            - 左转
            - ~~右转~~
            - ~~不是自己需要的相位则停止~~
    - 车道
        - 不用考虑？
        
    - 路口某方向车多，绿灯放行，时间增长
    
- 2个方法
    - 1.仿真
    - 2.统计,按分钟?