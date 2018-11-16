#存储让游戏‘外星人入侵’运行的函数
import sys
import pygame
from ship import Ship
from alien import Alien
from bullet import Bullet

def check_keydown_events(event,al_settings,screen,ship,bullets):
    """按下按键判断"""
    if event.key == pygame.K_RIGHT:  # 检查按下的是否是右箭头键
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(al_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:   #当按Q键时，关闭游戏
        sys.exit()

def check_keyup_events(event,ship):
    """松开按键判断"""
    if event.key == pygame.K_RIGHT:  # 确定此次松开的按键是否为右箭头键
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(al_settings,screen,ship,bullets):
    """监控键盘和鼠标事件"""
    for event in pygame.event.get():  # 为访问pygame检测到的事件，使用方法pygame.event.get() 所有键盘和鼠标事件都将促使for循环运行
        if event.type == pygame.QUIT:   #单击窗口的关闭按钮，会检测到pygame.QUIT事件
            sys.exit()   #退出游戏
        elif event.type == pygame.KEYDOWN:  #每次按键都会被注册为一个KEYDOWN事件
            check_keydown_events(event,al_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:  #松开按键
            check_keyup_events(event,ship)

def update_screen(alien_settings,screen,ship,bullets,aliens):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(alien_settings.background_color)  # 每次循环时都重绘屏幕,用背景色填充屏幕
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():  #bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
        bullet.draw_bullet()   #将所有精灵绘制出来
    ship.ship_location()
    aliens.draw(screen)   #自动绘制编组内的每个外星人
    # 让最近绘制的屏幕可见
    pygame.display.flip()  # 每次执行while循环时，都会绘制一个空屏幕，并擦去旧屏幕，使得只有新屏幕显示 。
    # 在我们移动游戏元素时，pygame.display.flip()将不断更新屏幕，以显示元素的新位置，并在原来的位置隐藏元素，从而营造平滑移动的效果

def update_bullets(aliens,bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():  # 在for循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    #检查是否有子弹击中了外星人
    #如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    #collisions ：上面这行代码遍历编组bullets中的没每颗子弹，再遍历编组aliens中的每个外星人。每当有子弹和外星人的rect重叠时，groupcollide（）就
    #在它返回的字典中添加一个键-值对。两个实参True告诉Pygame删除发生碰撞的子弹和外星人
def fire_bullet(al_settings,screen,ship,bullets):
    "如果没达到子弹限制，则发射一颗子弹"
    if len(bullets) < al_settings.bullets_allowed:  # 保证屏幕上最多 al_settings.bullets_allowed 颗子弹
        # 创建一颗子弹，并将其加入到编组bullets中
        new_bullet = Bullet(al_settings, screen,ship)  # 编组bullets传递给了check_keydown_events（）.玩家按空格键时，创建一颗子弹，并用方法add()将其加入到编组bullets中
        bullets.add(new_bullet)

def create_aliens_group(alien_settings,screen,aliens,ship):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(alien_settings,screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(alien_settings, alien_width)
    number_rows = get_number_rows(alien_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(alien_settings, screen, aliens, alien_number,number_row)

def get_number_aliens_x(alien_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = alien_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 确保为整数
    return number_aliens_x

def create_alien(alien_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(alien_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(alien_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = alien_settings.screen_height - ship_height -alien_height * 7   #7是为了缩小y的值，拉大和飞船的距离
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings,aliens):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites() : #遍历外星人群，对每个外星人调用check_edges()
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1