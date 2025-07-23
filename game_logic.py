import random

SCREEN_WIDTH = 290
SCREEN_HEIGHT = 490
PIPE_WIDTH = 54
PIPE_GAP = 138
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_INTERVAL = 140  # Frames between pipe spawns

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, 300)

    def update(self):
        self.x -= 1  # Pipe moves left

    def collides_with(self, bird: Bird) -> bool:
        bird_top = bird.y - 12
        bird_bottom = bird.y + 12

        upper_pipe_bottom = self.gap_y - PIPE_GAP // 2
        lower_pipe_top = self.gap_y + PIPE_GAP // 2

        hit_pipe = (
            (bird.x + 17 > self.x and bird.x - 17 < self.x + PIPE_WIDTH) and
            (bird_top < upper_pipe_bottom or bird_bottom > lower_pipe_top)
        )

        hit_ground_or_ceiling = bird.y >= SCREEN_HEIGHT or bird.y <= 0

        return hit_pipe or hit_ground_or_ceiling

def simulate_game(agent, max_frames=1000):
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    frame = 0

    while frame < max_frames:
        frame += 1
        bird.update()

        # Add pipe
        if frame % PIPE_INTERVAL == 0:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Update pipes mess with da screen
        for pipe in pipes:
            pipe.update()
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        # Get next pipe
        next_pipe = next((p for p in pipes if p.x + PIPE_WIDTH > bird.x), None)
        if not next_pipe:
            continue

        # AI decision
        if agent.decide(bird.y, next_pipe.gap_y):
            bird.flap()

        # Check crash
        if next_pipe.collides_with(bird):
            break

        # Score
        if next_pipe.x + PIPE_WIDTH < bird.x and not hasattr(next_pipe, 'scored'):
            score += 1
            next_pipe.scored = True

    return score
