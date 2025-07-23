# ai_agent.py

class AIAgent:
    """
    A slightly smarter AI agent to play Flappy Bird using position and velocity.
    """

    def decide(self, bird_y: float, pipe_gap_y: float, bird_velocity: float) -> bool:
        """
        Decide whether the bird should flap.

        Args:
            bird_y (float): Current vertical position of the bird.
            pipe_gap_y (float): Y-position of the pipe gap center.
            bird_velocity (float): Current vertical speed.

        Returns:
            bool: True if bird should flap, else False.
        """
        distance = pipe_gap_y - bird_y

        # If bird is too low, or falling quickly near the gap
        if distance < -10 and bird_velocity > 2:
            return True
        if distance < -40:
            return True
        return False
