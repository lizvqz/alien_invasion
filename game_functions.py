import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #Respond to key presses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    #Respond to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    

def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
def update_screen(ai_settings, screen, ship, aliens, bullets):
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all the bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(aliens, bullets):
    # Update bullet position.
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # CHeck for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
            
def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def create_fleet(ai_settings, screen, aliens):
    #Create and alien and find the number of aliens in a row
    # Spacing btw each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    
    # Create the first row of aliens
    for alien_number in range(number_aliens_x):
        # Create an alien and place it in the row
        create_alien(ai_settings, screen, aliens, alien_number)
        
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width -2 * alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number):
    # Create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)
    
def update_aliens(ai_settings, aliens):
    # CHeck if fleet is at an edge,
    # and then update the positions of all aliens in the fleet.
    check_fleet_edges(ai_settings, aliens)
    # Update the positions of all aliens in the fleet
    aliens.update()
    
def check_fleet_edges(ai_settings, aliens):
    # Respond appropiately if any aliens have reached an edge.
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    # Drop the entire fleet and change the fleets direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1
    
    
 
    

    
    
    