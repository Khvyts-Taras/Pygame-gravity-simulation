import pygame
import random

pygame.init()

screen = pygame.display.set_mode([800, 800])
clock = pygame.time.Clock()

cam_x = 0
cam_y = 0

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

	b1.vx = tx * tan1 + nx * m1
	b1.vy = ty * tan1 + ny * m1
	b2.vx = tx * tan2 + nx * m2
	b2.vy = ty * tan2 + ny * m2


trail_color = (50, 50, 200)
class Ball:
	def __init__(self, x, y, r):
		self.x, self.y = x, y
		self.vx, self.vy = 0, 0
		self.r = r
		self.mass = 3.14 * r * r
		# Список для хранения предыдущих позиций
		self.prev_positions = []

	def update(self):
		self.x += self.vx
		self.y += self.vy

		
		self.prev_positions.append((self.x, self.y))
		if len(self.prev_positions) > 15:
			self.prev_positions.pop(0)

	def render(self):
		# Рендеринг текущей позиции
		render_x = self.x - cam_x
		render_y = self.y - cam_y
		pygame.draw.circle(screen, (255, 255, 255), (render_x, render_y), self.r)

	def render_path(self):
		# Рендеринг следа
		for i, pos in enumerate(self.prev_positions):
			render_x = pos[0] - cam_x
			render_y = pos[1] - cam_y
			
			alpha = (i / len(self.prev_positions))
			color = (trail_color[0]*alpha, trail_color[1]*alpha, trail_color[2]*alpha)

			if i+1 < len(self.prev_positions):
				pygame.draw.line(screen, color, (render_x, render_y), (self.prev_positions[i+1][0]-cam_x, self.prev_positions[i+1][1]-cam_y), 2)



balls = []
for i in range(100):
	balls.append(Ball(random.randint(0, 800), random.randint(0, 800), random.randint(3, 6)))

kt = 0.05
G = 0.005
simulation_quality = 4


start_drag_pos = None
selected_ball = None
while 1:
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			start_drag_pos = pygame.mouse.get_pos()
			start_cam_pos = [cam_x, cam_y]
		if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
			start_drag_pos = None


	if True in pygame.mouse.get_pressed():
		pos = pygame.mouse.get_pos()
		if selected_ball == None:
			for ball in balls:
				d = ((pos[0]+cam_x - ball.x)**2 + (pos[1]+cam_y - ball.y)**2)**0.5
				if ball.r > d:
					selected_ball = ball
					break
	else:
		selected_ball = None

	if start_drag_pos != None:
		dx = (start_drag_pos[0] - pygame.mouse.get_pos()[0])
		dy = (start_drag_pos[1] - pygame.mouse.get_pos()[1])

		cam_x = start_cam_pos[0] + dx
		cam_y = start_cam_pos[1] + dy

	if pygame.mouse.get_pressed()[0]:
		if selected_ball != None:
			selected_ball.vx = pos[0]+cam_x - selected_ball.x
			selected_ball.vy = pos[1]+cam_y - selected_ball.y


	for ball in balls:
		ball.update()
		ball.render_path()


	for i in range(len(balls)):
		for j in range(i+1, len(balls)):
			ball = balls[i]
			target = balls[j]

			if ball != target:
				if touch(ball, target):
					mass = ball.mass+target.mass
					avg_vx = (ball.vx*ball.mass+target.vx*target.mass)/mass
					avg_vy = (ball.vy*ball.mass+target.vy*target.mass)/mass

					ball.vx = avg_vx*(kt) + ball.vx*(1-(kt))
					ball.vy = avg_vy*(kt) + ball.vy*(1-(kt))

					target.vx = avg_vx*(kt) + target.vx*(1-(kt))
					target.vy = avg_vy*(kt) + target.vy*(1-(kt))
				

				dx = target.x - ball.x
				dy = target.y - ball.y
				distance = (dx*dx + dy*dy)**0.5

				if distance > ball.r + target.r:
					force = G * ball.mass * target.mass / distance**2
					fx = force * dx
					fy = force * dy

					ball.vx += fx / ball.mass
					ball.vy += fy / ball.mass

					target.vx -= fx / target.mass
					target.vy -= fy / target.mass


	for k in range(simulation_quality):
		for i in range(len(balls)):
			for j in range(i+1, len(balls)):
				ball = balls[i]
				target = balls[j]

				if ball != target:
					if touch(ball, target):
						d = ((ball.x - target.x)**2 + (ball.y - target.y)**2)**0.5
						overlap = 0.5 * (d - ball.r - target.r)

						dx = ball.x - target.x
						dy = ball.y - target.y

						ball.x -= overlap * (dx)/d
						ball.y -= overlap * (dy)/d

						target.x += overlap * (dx)/d
						target.y += overlap * (dy)/d

						collide(ball, target)


	for ball in balls:
		ball.render()

	pygame.display.update()
	clock.tick(60)
