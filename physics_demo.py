import pygame
import random

pygame.init()

screen = pygame.display.set_mode([800, 800])
clock = pygame.time.Clock()


def touch(obj1, obj2):
	d = ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5
	r_s = obj1.r + obj2.r
	return d < r_s

def collide(b1, b2):
	d = ((b1.x - b2.x)**2 + (b1.y - b2.y)**2)**0.5

	nx = (b2.x - b1.x)/d
	ny = (b2.y - b1.y)/d

	tx = -ny
	ty = nx

	tan1 = b1.vx * tx + b1.vy * ty
	tan2 = b2.vx * tx + b2.vy * ty

	norm1 = b1.vx * nx + b1.vy * ny
	norm2 = b2.vx * nx + b2.vy * ny


	m1 = (norm1 * (b1.mass - b2.mass) + 2 * b2.mass * norm2) / (b1.mass + b2.mass)
	m2 = (norm2 * (b2.mass - b1.mass) + 2 * b1.mass * norm1) / (b1.mass + b2.mass)

	b1.vx = (tx * tan1 + nx * m1)
	b1.vy = (ty * tan1 + ny * m1)
	b2.vx = (tx * tan2 + nx * m2)
	b2.vy = (ty * tan2 + ny * m2)

class Ball:
	def __init__(self, x, y, r):
		self.x, self.y = x, y
		self.vx, self.vy = 0, 0
		self.r = r
		self.mass = r

	def update(self):
		self.vy += 0.3

		self.vx *= 0.99
		self.vy *= 0.99
		self.x += self.vx
		self.y += self.vy

	def render(self):
		pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.r, 1)


balls = []
for i in range(50):
	balls.append(Ball(random.randint(0, 800), random.randint(0, 800), random.randint(15, 20)))


simulation_quality = 3
selected_ball = None
moved_ball = None
while 1:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	if True in pygame.mouse.get_pressed():
		pos = pygame.mouse.get_pos()
		if selected_ball == None:
			for ball in balls:
				d = ((pos[0] - ball.x)**2 + (pos[1] - ball.y)**2)**0.5
				if ball.r > d:
					selected_ball = ball
					break
	else:
		selected_ball = None

	if pygame.mouse.get_pressed()[0]:
		if selected_ball != None:
			selected_ball.vx = pos[0] - selected_ball.x
			selected_ball.vy = pos[1] - selected_ball.y
	if pygame.mouse.get_pressed()[2]:
		pos = pygame.mouse.get_pos()
		if selected_ball != None:
			pygame.draw.line(screen, (0, 0, 255), (selected_ball.x, selected_ball.y), (pos[0], pos[1]), 1)
			moved_ball = selected_ball
	else:
		if moved_ball != None:
			moved_ball.vx = (moved_ball.x-pos[0])/5
			moved_ball.vy = (moved_ball.y-pos[1])/5
			moved_ball = None


	for ball in balls:
		ball.update()


	for k in range(simulation_quality):
		for i in range(len(balls)):
			for j in range(i+1, len(balls)):
				ball = balls[i]
				target = balls[j]

				if touch(ball, target):
					d = ((ball.x - target.x)**2 + (ball.y - target.y)**2)**0.5
					overlap = 0.5 * (d - (ball.r + target.r))

					dx = ball.x - target.x
					dy = ball.y - target.y

					ball.x -= overlap * dx/d
					ball.y -= overlap * dy/d

					target.x += overlap * dx/d
					target.y += overlap * dy/d

					collide(ball, target)


			if balls[i].x-balls[i].r < 0:
				balls[i].vy *= 0.9
				balls[i].vx *= -0.5
				balls[i].x = balls[i].r

			if balls[i].x+balls[i].r > 800:
				balls[i].vy *= 0.9
				balls[i].vx *= -0.5
				balls[i].x = 800-balls[i].r

			if balls[i].y-balls[i].r < 0:
				balls[i].vx *= 0.9
				balls[i].vy *= -0.5
				balls[i].y = balls[i].r

			if balls[i].y+balls[i].r > 800:
				balls[i].vx *= 0.9
				balls[i].vy *= -0.5
				balls[i].y = 800-balls[i].r


	for ball in balls:
		ball.render()

	pygame.display.update()
	clock.tick(60)
