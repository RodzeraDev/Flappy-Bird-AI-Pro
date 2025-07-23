import pygame
import random
from ai_agent import AIAgent

# bird values so i know what size and tube variables
WIDTH, HEIGHT = 800, 550
PIPE_WIDTH = 200
PIPE_GAP = 125
FPS = 60
BIRD_SIZE = 43
FLAP_STRENGTH = -8
INITIAL_GRAVITY = 0.5
INITIAL_PIPE_SPEED = 3

class Bird:
    def __init__(self):
        self.x = 150
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_SIZE, BIRD_SIZE)

    def update(self, gravity):
        self.velocity += gravity
        self.y += self.velocity
        self.rect.y = int(self.y)

    def flap(self):
        self.velocity = FLAP_STRENGTH

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(150, 450)

        self.pipe_draw_width = PIPE_WIDTH - 30  # thinner image AND hitbox
        self.x_offset = (PIPE_WIDTH - self.pipe_draw_width) // 2

        visual_top_height = self.gap_y - PIPE_GAP // 2 + 20
        visual_bottom_height = HEIGHT - (self.gap_y + PIPE_GAP // 2)

        # Match both drawing and collision
        self.top_rect = pygame.Rect(
            self.x + self.x_offset,
            -20,
            self.pipe_draw_width,
            visual_top_height
        )
        self.bottom_rect = pygame.Rect(
            self.x + self.x_offset,
            self.gap_y + PIPE_GAP // 2,
            self.pipe_draw_width,
            visual_bottom_height
        )

    def update(self, speed):
        self.x -= speed
        self.top_rect.x = self.x + self.x_offset
        self.bottom_rect.x = self.x + self.x_offset

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy AI")
    clock = pygame.time.Clock()

    # image scalings
    bird_img = pygame.image.load("assets/bird.png").convert_alpha()
    pipe_img_original = pygame.image.load("assets/pipe.png").convert_alpha()
    background_img = pygame.image.load("assets/background.png").convert()

    bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE, BIRD_SIZE))
    pipe_img_original = pygame.transform.scale(pipe_img_original, (PIPE_WIDTH, 400))
    pipe_img_flipped = pygame.transform.flip(pipe_img_original, False, True)
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    bird = Bird()
    agent = AIAgent()
    pipes = [Pipe(WIDTH + 100)]

    score = 0
    pipe_speed = INITIAL_PIPE_SPEED
    gravity = INITIAL_GRAVITY
    font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        bird.update(gravity)

        if pipes[-1].x < WIDTH - 300:
            pipes.append(Pipe(WIDTH + 100))

        for pipe in pipes:
            pipe.update(pipe_speed)
        pipes = [p for p in pipes if not p.is_off_screen()]

        next_pipe = next((p for p in pipes if p.x + PIPE_WIDTH > bird.x), pipes[0])

        if agent.decide(bird.y, next_pipe.gap_y, bird.velocity):
            bird.flap()

        for pipe in pipes:
            if pipe.collides_with(bird):
                running = False
        if bird.y < 0 or bird.y > HEIGHT:
            running = False

        for pipe in pipes:
            if pipe.x + PIPE_WIDTH < bird.x and not hasattr(pipe, "scored"):
                pipe.scored = True
                score += 1

        # make hard scaling
        if score % 5 == 0 and score > 0:
            pipe_speed = min(pipe_speed + 0.01, 8)
            gravity = min(gravity + 0.002, 1.6)

        # Draw pipes
        for pipe in pipes:
            # strechin pipes
            top_height = pipe.top_rect.height + 20     # Extend upward
            top_y = pipe.top_rect.y - 20                # Offset upward
            top_pipe_scaled = pygame.transform.scale(pipe_img_flipped, (PIPE_WIDTH, top_height))

            bottom_pipe_scaled = pygame.transform.scale(pipe_img_original, (PIPE_WIDTH, pipe.bottom_rect.height))

            screen.blit(top_pipe_scaled, (pipe.x, top_y))
            screen.blit(bottom_pipe_scaled, (pipe.x, pipe.bottom_rect.y))

        # Draw bird
        screen.blit(bird_img, bird.rect.topleft)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Border
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, WIDTH, HEIGHT), 5)

        pygame.display.flip()

    pygame.quit()
    print(f"AI Score: {score}")

if __name__ == "__main__":
    run_game()
