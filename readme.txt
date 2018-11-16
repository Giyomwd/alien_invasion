介绍：
alien_invasion.py
主文件alien_invasion.py创建一系列整个游戏都要用到的对象;存储在ai_settings中的设置、存储在screen中的主显示surface以及一个
飞船实例。文件alien_invasion.py还包含游戏的主循环。这是一个调用check_event()、ship.update()和update_screen()的while循环。

settings.py
文件settings.py包含Settings类，这个类只包含方法_init_(),它初始化控制游戏外观和飞船速度的属性

game_functions.py
文件game_functions.py包含了一系列函数，游戏的大部分工作都是由它们完成的。函数check_events()检测相关事件。如按键和松开，
并使用辅助函数check_keydown_events()和check_keyup_events()来处理这些事件。就目前而言，这些函数管理飞船 的移动。模块
game_functions还包含函数update_screen（），它用于在每次执行主循环时都重绘屏幕。

ship.py
文件ship.py包含Ship类，这个类包含方法_init_（）、管理飞船位置的方法update()以及在屏幕上绘制飞船的方法blitme().表示飞船的
图像存储在文件夹images下的文件ship.bmp