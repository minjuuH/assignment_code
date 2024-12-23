# Setting for Blocks
num_blocks = (5, 3)
margin = (60, 40)
block_size = (80, 30)
spacing = (20, 20)
score_pos = (10, 10)
life_pos = (450, 10)

# Display setting
fps = 30
wall_width = 10
scoreboard_height = 50
gameboard_height_coefficient = 3

display_dimension = (600, 800)

center_x = display_dimension[0] / 2
center_y = display_dimension[1] / 2

# Setting for paddle
paddle_color = (242, 242, 0)
paddle_pos = (center_x, display_dimension[1] - 100)
paddle_size = (100, 30)
paddle_speed = 5

# Colors for blocks (and potentially for items)
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (169, 169, 169)]  # Red, Orange, Yellow, Gray (new gray wall block)
collision_limit = len(colors) - 1

# Setting for blocks (adjust block hit sequence)
block_hit_sequence = {
    (255, 0, 0): (255, 165, 0),  # Red -> Orange
    (255, 165, 0): (255, 255, 0),  # Orange -> Yellow
    (255, 255, 0): None,  # Yellow -> Block destroyed
}

# Setting for ball
ball_color = (242, 242, 0)
ball_speed = display_dimension[1] / 80
ball_pos = (center_x, paddle_pos[1] - paddle_size[1])
ball_fever_color = (255, 50, 0)
ball_size = (20, 20)

# Setting for items
item_size = (20, 20)
one_more_prob = 0.3
fever_prob = 0.1
add_score_prob = 0.1
paddle_long_prob = 0.1

fever_time = 5
add_score = 100
add_score_color = (0, 255, 0)  # Green color for score item

paddle_long_ratio = 2
paddle_long_time = 5
paddle_long_color = (0, 126, 255)  # Blue color for paddle length item

# Colors for blocks (and potentially for items)
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0)]  # Red, Orange, Yellow
collision_limit = len(colors) - 1

# Total number of life
life = 3
