import pygame
import collections
import enum
import random

def draw_square(x, y, color, block_size, screen):
	x_ord = x * block_size
	y_ord = y * block_size

	pygame.draw.rect(screen, color, pygame.Rect(x_ord, y_ord, block_size, block_size))

class Food:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def render(self, screen, block_size):
		draw_square(self.x, self.y, (255, 0, 0), block_size, screen)

class Direction(enum.Enum):
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3

class SnakePiece:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Snake:
	def __init__(self):
		self.body = collections.deque()
		self.direction = Direction.LEFT
		self.eaten = False

	def update(self):
		old_head = self.body[0]
		if self.direction == Direction.LEFT:
			new_head = SnakePiece(old_head.x - 1, old_head.y)
		elif self.direction == Direction.RIGHT:
			new_head = SnakePiece(old_head.x + 1, old_head.y)
		elif self.direction == Direction.UP:
			new_head = SnakePiece(old_head.x, old_head.y - 1)
		elif self.direction == Direction.DOWN:
			new_head = SnakePiece(old_head.x, old_head.y + 1)

		self.body.appendleft(new_head)

		if not self.eaten:
			self.body.pop()
		else:
			self.eaten = False

	def render(self, screen, block_size):
		for piece in self.body:
			draw_square(piece.x, piece.y, (255, 255, 255), block_size, screen)

class Game:
	def __init__(self):
		self.snake = Snake()
		self.food = Food(2, 2)
		self.eaten = False
		self.running = True
		self.score = 0

	def key_pressed(self, keys):
		if keys[pygame.K_LEFT] and self.snake.direction != Direction.RIGHT:
			self.snake.direction = Direction.LEFT
		if keys[pygame.K_RIGHT] and self.snake.direction != Direction.LEFT:
			self.snake.direction = Direction.RIGHT
		if keys[pygame.K_UP] and self.snake.direction != Direction.DOWN:
			self.snake.direction = Direction.UP
		if keys[pygame.K_DOWN] and self.snake.direction != Direction.UP:
			self.snake.direction = Direction.DOWN

	def update(self, width, height):
		self.snake.update()

		snake_head = self.snake.body[0]
		snake_body = [self.snake.body[i] for i in range(1,len(self.snake.body))]

		for piece in snake_body:
			if(piece.x == snake_head.x and piece.y == snake_head.y):
				self.running = False

		if(self.snake.body[0].x < 0 or self.snake.body[0].x >= width):
			self.running = False

		if(self.snake.body[0].y < 0 or self.snake.body[0].y >= height):
			self.running = False

		if(self.snake.body[0].x == self.food.x and self.snake.body[0].y == self.food.y):
			new_x = random.randint(0, width - 1)
			new_y = random.randint(0, height - 1)

			while not self.is_valid_food(self.snake, new_x, new_y):
				new_x = random.randint(0, width - 1)
				new_y = random.randint(0, height - 1)

			self.food.x = new_x
			self.food.y = new_y
			self.snake.eaten = True
			self.score += 1

	def render(self, screen, block_size, txt):
		screen.fill((0, 0, 0))

		self.snake.render(screen, block_size)
		self.food.render(screen, block_size)
		TextSurf = largeText.render("Score: " + str(self.score), True, (255, 255, 255))
		TextRect = TextSurf.get_rect()

		TextRect.top = 10
		TextRect.left = 10
		screen.blit(TextSurf, TextRect)

		pygame.display.flip()

	def is_valid_food(self, snake, new_x, new_y):
		for piece in snake.body:
			if(piece.x == new_x and piece.y == new_y):
				return False

		return True

if __name__ == "__main__":
	rows, cols = 20, 20
	block_size = 25
	sw, sh = (cols * block_size, rows * block_size)
	screen = pygame.display.set_mode((sw, sh))
	pygame.display.set_caption("Snake Game")

	pygame.display.flip()

	pygame.font.init()
	largeText = pygame.font.Font('freesansbold.ttf', 20)

	g = Game()
	g.snake.body.append(SnakePiece(cols//2, rows//2))
	g.snake.body.append(SnakePiece(cols//2 + 1, rows//2))
	g.snake.body.append(SnakePiece(cols//2 + 2, rows//2))

	while g.running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				g.key_pressed(pygame.key.get_pressed())

		g.update(cols, rows)
		g.render(screen, block_size, largeText)

		pygame.display.update()
		pygame.time.wait(int(100/(0.1*g.score + 1)))