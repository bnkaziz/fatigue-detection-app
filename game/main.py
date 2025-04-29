import pygame
from config import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR
from game_manager import GameManager
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.data_utils import save_json

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Circle Game")

game = GameManager()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

start_time = pygame.time.get_ticks()

# Timer for saving performance data
save_interval = 10  # seconds
last_save_time = time.time()

def prepare_performance_data():
    return {
        "level": game.level + 1,  # your variable
        "score": game.get_total_score(),  # your variable
        "hits": game.get_total_hits(),      # your variable
        "misses": game.get_total_misses(),  # your variable
        "elapsed_time_sec": int(time.time() - start_time),  # you probably already track start_time
        "status": "Level Determination Phase" if game.determination_phase else "Experiment Phase",  # 'determination' or 'normal' phase
        "performance_history": game.global_performance_log,  # a list of past performance points
    }

running = True

while running:
    screen.fill(BG_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP1:
                game.check_hit(0)  # Check hit for circle 1
            elif event.key == pygame.K_KP2:
                game.check_hit(1)  # Check hit for circle 2
            elif event.key == pygame.K_KP3:
                game.check_hit(2)  # Check hit for circle 3

    # Update & Draw
    game.update_circles()
    for circle in game.circles:
        circle.draw(screen, font)

    # Display Total Score and Stats
    total_score_text = font.render(f"Total Score: {game.get_total_score()}", True, TEXT_COLOR)
    total_hits_text = font.render(f"Total Hits: {game.get_total_hits()}", True, (0, 255, 0))
    total_misses_text = font.render(f"Total Misses: {game.get_total_misses()}", True, (255, 0, 0))
    level_text = font.render(f"Level: {game.level + 1}", True, TEXT_COLOR)

    level_performance_text = font.render(f"Level performance: {round(game.current_level_performance[-1], 2)}%" if len(game.current_level_performance) else "Level performance: 0%", True, TEXT_COLOR)
    internal_hits_10s = font.render(f"Hits (last 10s): {game.internal_hits}", True, (0, 255, 0))
    internal_misses_10s = font.render(f"Misses (last 10s): {game.internal_misses}", True, (255, 0, 0))
    level_determination = font.render(f"Determination: {game.determination_phase}", True, TEXT_COLOR)
    # level_text = font.render(f"Level: {game.level}", True, TEXT_COLOR)

    # Timer calculation
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # total seconds
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    
    timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (200, 200, 0))

    screen.blit(total_score_text, (WIDTH // 2 - 80, 20))
    screen.blit(total_hits_text, (WIDTH // 2 - 80, 50))
    screen.blit(total_misses_text, (WIDTH // 2 - 80, 80))
    screen.blit(level_text, (WIDTH // 2 - 80, 110))
    screen.blit(level_performance_text, (50, 20))
    screen.blit(internal_hits_10s, (50, 50))
    screen.blit(internal_misses_10s, (50, 80))
    screen.blit(level_determination, (50, 110))
    screen.blit(timer_text, (WIDTH - 180, 20))
    
    # Check for level-up
    game.check_level_up()

    # Save performance data every 10 seconds
    if time.time() - last_save_time >= save_interval:
        performance_data = prepare_performance_data()
        save_path = os.path.join("data", "performance_new", "performance_live.json")
        save_json(save_path, performance_data)
        last_save_time = time.time()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
