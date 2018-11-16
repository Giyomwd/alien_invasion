#设置类
class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的配置"""
        #屏幕设置
        self.screen_width = 900
        self.screen_height = 700
        self.background_color = (40,40,40)

        #飞船的设置
        self.ship_speed_factor = 1.5
        #外星人设置
        self.alien_speed_factor = 0.7
        self.fleet_drop_speed = 10   #指定有外星人撞到屏幕边缘时，外星人群向下移动的速度
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        #子弹设置  宽3像素、高15像素的深灰色子弹。子弹速度比飞船稍低
        self.bullet_speed_factor =1   #子弹速度
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 10   #屏幕上未消失的子弹数限制为3颗