import pygame
import random
import time
from pygame.locals import *  #引入所有关键字
pygame.init()

class Plane:                     #飞机类
	def __init__(self,screen):
		self.x=150
		self.y=450
		self.screen=screen
		self.image=pygame.image.load('./3.png')
		self.bulletlist=[] #子弹列表
	def moveleft(self):
		if self.x>0:
			self.x-=25
	def moveright(self):
		if self.x<310:
			self.x+=25
	def moveup(self):
		if self.y>0:
			self.y-=25
	def movedown(self):
		if self.y<460:
			self.y+=25
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
		needItemlist=[]
		for item in self.bulletlist:
			if item.judge():
				needItemlist.append(item)
		for i in needItemlist:
			self.bulletlist.remove(i)
		for item in self.bulletlist:
			item.display()
			item.move()
	def shoot(self):
		newBullet=Bullet(self.x,self.y,self.screen)
		self.bulletlist.append(newBullet)

class Enemy:     #敌机类
	def __init__(self,screen):
		self.x=random.randint(1,330)
		self.y=0
		self.screen=screen
		self.image=pygame.image.load('./enemy_plane3.png')
		self.bulletlist=[] #子弹列表
		self.dir='right'
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
		needItemlist=[]
		for item in self.bulletlist:
			if item.judge():
				needItemlist.append(item)
		for i in needItemlist:
			self.bulletlist.remove(i)
		for item in self.bulletlist:
			item.display()
			item.move()
	def move(self):
		'''
		if self.dir=='right':
			self.x+=3
		elif self.dir=='left':
			self.x-=3
		if self.x<0:
			self.dir='right'
		elif self.x>350:
			self.dir='left'
		'''
		self.y+=10
	def shoot(self):                    #随机发射子弹
		num=random.randint(1,100)
		if num==3:
			newBullet=Enemy_bullet(self.x,self.y,self.screen)
			self.bulletlist.append(newBullet)

class Bullet:         #我机子弹类
	def __init__(self,x,y,screen):
		self.x=x+20
		self.y=y
		self.screen=screen
		self.image=pygame.image.load('./bullet5.png')
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
	def move(self):
		self.y-=20
	def judge(self):
		if self.y<0:
			return True
		else :
			return False

class Enemy_bullet:   #敌机子弹类
	def __init__(self,x,y,screen):
		self.x=x+20
		self.y=y
		self.screen=screen
		self.image=pygame.image.load('./enemy_bullet3.png')
	def display(self):
		self.screen.blit(self.image,(self.x,self.y))
	def move(self):
		self.y+=13
	def judge(self):
		if self.y>500:
			return True
		else :
			return False

 
def key_control(plane,point):   #移动控制函数
	evenlist=pygame.event.get()
	for event in evenlist:
			if event.type==QUIT:
				print('退出')
				print('最终得分为{}'.format(point))
				exit()
				
			elif event.type==KEYDOWN:
				if event.type==K_a or event.key==K_LEFT:
					print('左移')
					plane.moveleft()
				elif event.type==K_d or event.key==K_RIGHT:
					print('右移')
					plane.moveright()
				elif event.type==K_w or event.key==K_UP:
					print('上移')
					plane.moveup()
				elif event.type==K_s or event.key==K_DOWN:
					print('下移')
					plane.movedown()
				elif event.key==K_SPACE:
					print('发射')
					plane.shoot()


def main():
	#创建窗口展示
	screen=pygame.display.set_mode((350,500),depth=32)
	plane_A=Plane(screen)
	point=0
	newEnemylist=[]
	#创建一个背景图片对象
	background=pygame.image.load('./back_ground2.jpg')
	#设置一个title
	pygame.display.set_caption('飞机game')
	#添加背景音乐
	pygame.mixer.init()
	pygame.mixer.music.load('./蓑部雄崇 - 十代のテーマ.mp3')
	pygame.mixer.music.set_volume(0.2)  ##音量为0.5（一半）
	pygame.mixer.music.play(-1)  #表示无限循环
	'''
	text=pygame.font.SysFont('宋体',50)
	text_fmt=text.render('60秒打飞机',1,(225,225,225))
	screen.blit(text_fmt,(150,250))
	'''
	while 1:
		end_time=time.clock()
		if int(end_time-start_time)==60:
			print('时间到了,你获胜')
			print('最终得分为{}'.format(point))
			exit()
		screen.blit(background,(0,0))
		plane_ran=random.randint(1,100)    #随机生成敌机
		if plane_ran in range(1,12):
			enemy_planeA=Enemy(screen)
			newEnemylist.append(enemy_planeA)
		for i in newEnemylist:      #超过边界，删除
				if i.y>450:
					newEnemylist.remove(i)  
		for i in newEnemylist:            #子弹与敌机碰撞并记录得分
			for j in plane_A.bulletlist:
				if abs(i.x-j.x)<15 and abs(i.y-j.y)<15:
					newEnemylist.remove(i)
					plane_A.bulletlist.remove(j)
					point+=1
		for i in newEnemylist:             #敌机与飞机碰撞
			if abs(i.x-plane_A.x)<15 and abs(i.y-plane_A.y)<15:
				print('与敌机相撞,游戏结束')
				print('最终得分为{}'.format(point))
				exit()
		for i in newEnemylist:     #敌机展示与移动
			#pygame.time.Clock().tick(24)
			i.display()
			i.move()
			#i.shoot()
		plane_A.display()
		key_control(plane_A,point)
		pygame.display.update()
		time.sleep(0.1)  #延时一秒

if __name__=='__main__':
	start_time=time.clock()
	main()
