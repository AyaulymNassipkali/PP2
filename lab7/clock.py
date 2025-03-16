import pygame
import time
import math
pygame.init()
screen=pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Mickey clock")
min_hand = pygame.image.load("images/min_hand.png")
sec_hand = pygame.image.load("images/sec_hand.png")
main_clock = pygame.transform.scale(pygame.image.load("images/clock.png"), (800,600))

done=False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    current_time=time.localtime()
    minute = current_time.tm_min
    second = current_time.tm_sec

    screen.blit(main_clock, (0,0))
    minut_angle = minute * 6 + (second/60)*6
    second_angle = second * 6

    rotated_sec_hand = pygame.transform.rotate(sec_hand, -second_angle)
    sec_hand_rect = rotated_sec_hand.get_rect(center=(400, 300))

    rotated_min_hand = pygame.transform.rotate(min_hand, -minut_angle)
    min_hand_rect = rotated_min_hand.get_rect(center=(400, 300))
    screen.blit(main_clock, (0, 0))
    screen.blit(rotated_sec_hand, sec_hand_rect)
    screen.blit(rotated_min_hand, min_hand_rect)


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
