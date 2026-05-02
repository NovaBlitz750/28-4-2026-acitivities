import random
import time
import sys
import traceback
from blessed import Terminal

def main():
    term = Terminal()

    # Game settings
    PLAYER_CHAR = '🚀'
    ENEMY_CHAR = '👾'
    BULLET_CHAR = '🔥'
    STAR_CHAR = '.'
    EXPLOSION_CHARS = ['💥', '✨', '✴️']

    # Initial state
    player_x = term.width // 2
    player_y = term.height - 2
    bullets = []
    enemies = []
    explosions = [] # list of [x, y, start_time]
    stars = [[random.randint(0, term.width - 1), random.randint(0, term.height - 1)] for _ in range(20)]
    score = 0
    lives = 3
    game_over = False

    enemy_spawn_chance = 0.1
    enemy_speed = 0.15
    star_speed = 0.5
    last_enemy_move = time.time()
    last_star_move = time.time()

    try:
        with term.cbreak(), term.hidden_cursor(), term.fullscreen():
            while not game_over:
                # Update current dimensions in case of resize
                current_width = term.width
                current_height = term.height

                # Handle input
                key = term.inkey(timeout=0.03)

                if key.code == term.KEY_LEFT or key.lower() == 'a':
                    player_x = max(0, player_x - 1)
                elif key.code == term.KEY_RIGHT or key.lower() == 'd':
                    player_x = min(current_width - 2, player_x + 1)
                elif key == ' ':
                    bullets.append([player_x, player_y - 1])
                elif key.lower() == 'q' or key.code == term.KEY_ESCAPE:
                    return

                # Ensure player is within bounds after possible resize
                player_x = min(player_x, current_width - 2)
                player_y = current_height - 2

                # Update stars
                if time.time() - last_star_move > star_speed:
                    for star in stars:
                        star[1] += 1
                        if star[1] >= current_height:
                            star[0] = random.randint(0, current_width - 1)
                            star[1] = 0
                        # Keep stars in bounds
                        star[0] = min(star[0], current_width - 1)
                    last_star_move = time.time()

                # Update bullets
                new_bullets = []
                for bx, by in bullets:
                    if by > 0:
                        new_bullets.append([bx, by - 1])
                bullets = new_bullets

                # Spawn enemies
                if random.random() < enemy_spawn_chance:
                    enemies.append([random.randint(0, max(0, current_width - 2)), 0])

                # Update enemies
                if time.time() - last_enemy_move > enemy_speed:
                    new_enemies = []
                    for ex, ey in enemies:
                        if ey < current_height - 2:
                            new_enemies.append([ex, ey + 1])
                        else:
                            lives -= 1
                            if lives <= 0:
                                game_over = True
                    enemies = new_enemies
                    last_enemy_move = time.time()

                    # Increase difficulty
                    enemy_spawn_chance = min(0.5, 0.1 + (score / 1000))
                    enemy_speed = max(0.05, 0.15 - (score / 5000))

                # Update explosions
                current_time = time.time()
                explosions = [e for e in explosions if current_time - e[2] < 0.5]

                # Collision detection - bullets vs enemies
                remaining_enemies = []
                for ex, ey in enemies:
                    hit = False
                    for b_idx, (bx, by) in enumerate(bullets):
                        if abs(bx - ex) <= 1 and (by == ey):
                            explosions.append([ex, ey, time.time()])
                            score += 10
                            bullets.pop(b_idx)
                            hit = True
                            break
                    if not hit:
                        remaining_enemies.append([ex, ey])
                enemies = remaining_enemies

                # Player-Enemy collision
                remaining_enemies = []
                for ex, ey in enemies:
                    if abs(ex - player_x) <= 1 and ey == player_y:
                        lives -= 1
                        explosions.append([ex, ey, time.time()])
                        if lives <= 0:
                            game_over = True
                    else:
                        remaining_enemies.append([ex, ey])
                enemies = remaining_enemies

                # Drawing
                output = term.clear

                # Draw stars
                for sx, sy in stars:
                    if sx < current_width and sy < current_height:
                        output += term.move_xy(sx, sy) + term.dim + STAR_CHAR + term.normal

                # Draw score and lives
                header = f" Score: {score}  Lives: {lives}  (Q to Quit) "
                output += term.move_xy(0, 0) + term.black_on_white(header)

                # Draw bullets
                for bx, by in bullets:
                    if bx < current_width and by < current_height:
                        output += term.move_xy(bx, by) + BULLET_CHAR

                # Draw explosions
                for ex, ey, et in explosions:
                    if ex < current_width and ey < current_height:
                        char = EXPLOSION_CHARS[int((time.time() - et) * 6) % len(EXPLOSION_CHARS)]
                        output += term.move_xy(ex, ey) + char

                # Draw enemies
                for ex, ey in enemies:
                    if ex < current_width and ey < current_height:
                        output += term.move_xy(ex, ey) + ENEMY_CHAR

                # Draw player
                output += term.move_xy(player_x, player_y) + PLAYER_CHAR

                sys.stdout.write(output)
                sys.stdout.flush()

            # Game Over Screen
            print(term.clear)
            msg = "GAME OVER"
            score_msg = f"Final Score: {score}"
            exit_msg = "Press any key to exit"

            print(term.move_xy(term.width // 2 - len(msg) // 2, term.height // 2) + term.bold_red(msg))
            print(term.move_xy(term.width // 2 - len(score_msg) // 2, term.height // 2 + 1) + term.white(score_msg))
            print(term.move_xy(term.width // 2 - len(exit_msg) // 2, term.height // 2 + 2) + term.dim(exit_msg))
            term.inkey()

    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception:
        # Restore terminal before printing traceback
        print(term.normal_cursor)
        traceback.print_exc()
        # Wait a bit so the user can see the error
        time.sleep(5)
    finally:
        print(term.normal_cursor)

if __name__ == '__main__':
    main()
