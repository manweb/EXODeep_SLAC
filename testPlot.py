import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cl

class APDDisplay(object):
	def __init__(self):
		self.xPos = np.array([-3.327, 2.218, 7.764, -2.218, 3.327, -1.109, 13.309, 14.418, 15.527, 8.873, 9.982, 4.436, 16.636, 12.2, 7.764, 11.091, 6.655, 5.545, 3.327, -2.218, -7.764, 2.218, -3.327, 1.109, -13.309, -14.418, -15.527, -8.873, -9.982, -4.436, 0, -16.636, -12.2, -7.764, -11.091, -6.655, -5.545, 3.327, -2.218, -7.764, 2.218, -3.327, 1.109, -13.309, -14.418, -15.527, -8.873, -9.982, -4.436, 0, -16.636, -12.2, -7.764, -11.091, -6.655, -5.545, -3.327, 2.218, 7.764, -2.218, 3.327, -1.109, 13.309, 14.418, 15.527, 8.873, 9.982, 4.436, 16.636, 12.2, 7.764, 11.091, 6.655, 5.545])
		self.yPos = np.array([17.289, 15.368, 13.447, 11.526, 9.605, 5.763, 11.526, 5.763, 0, 7.684, 1.921, 3.842, -5.763, -9.605, -13.447, -3.842, -7.684, -1.921, -17.289, -15.368, -13.447, -11.526, -9.605, -5.763, -11.526, -5.763, 0, -7.684, -1.921, -3.842, 0, 5.763, 9.605, 13.447, 3.842, 7.684, 1.921, -17.289, -15.368, -13.447, -11.526, -9.605, -5.763, -11.526, -5.763, 0, -7.684, -1.921, -3.842, 0, 5.763, 9.605, 13.447, 3.842, 7.684, 1.921, 17.289, 15.368, 13.447, 11.526, 9.605, 5.763, 11.526, 5.763, 0, 7.684, 1.921, 3.842, -5.763, -9.605, -13.447, -3.842, -7.684,
 -1.921])

	def DisplayAPDSignal(self,data):
		plt.close('all')

		fig = plt.figure(figsize=(10,5))
		ax1 = fig.add_subplot(1,2,1)
		ax2 = fig.add_subplot(1,2,2)

		ax1.set_ylim(-200,200)
		ax2.set_ylim(-200,200)
		ax1.set_xlim(-200,200)
		ax2.set_xlim(-200,200)

		ax1.set_title('+z plane')
		ax2.set_title('-z plane')

		ax1.set_xlabel('x (mm)')
		ax1.set_ylabel('y (mm)')
		ax2.set_xlabel('x (mm)')
		ax2.set_ylabel('y (mm)')

		cmap = plt.cm.get_cmap('hot', 100)

		dataMin = data.min()
		dataMax = data.max()

		offsets = np.array([[0,2.218,-2.218,1.109,1.109,-1.109,-1.109],[0,0,0,-1.921,1.921,-1.921,1.921]])

		circles = []
		for i in range(74):
			colorID = int(round(100/(dataMax-dataMin)*data[i]*(1-dataMin)))
			col = cl.rgb2hex(cmap(colorID)[:3])

			sign = 1
			if i >= 37:
				sign = -1
			for k in range(7):
				circle = plt.Circle(((self.xPos[i]+offsets[0][k])*10,sign*(self.yPos[i]+offsets[1][k])*10), radius=5, color=col)
				circles.append(circle)

		for i in range(74*7):
			if i < 37*7:
				ax1.add_patch(circles[i])
			else:
				ax2.add_patch(circles[i])

		plt.show(block=False)

	def DisplayPosition(self,data):
		fig = plt.figure(figsize=(10,5))
		ax1 = fig.add_subplot(1,2,1)
		ax2 = fig.add_subplot(1,2,2)

		ax1.set_ylim(-200,200)
		ax2.set_ylim(-200,200)
		ax1.set_xlim(-200,200)
		ax2.set_xlim(-200,200)

		ax1.set_xlabel('x (mm)')
		ax1.set_ylabel('y (mm)')
		ax2.set_xlabel('z (mm)')
		ax2.set_ylabel('y (mm)')

		circle1 = plt.Circle((data[0],data[1]), radius=2, color='b', fill=False)
		circle2 = plt.Circle((data[2],data[1]), radius=2, color='b', fill=False)

		ax1.add_patch(circle1)
		ax2.add_patch(circle2)

		plt.show(block=False)

	def DisplayPosition(self,data,trueData):
		fig = plt.figure(figsize=(10,5))
		ax1 = fig.add_subplot(1,2,1)
		ax2 = fig.add_subplot(1,2,2)

		ax1.set_ylim(-200,200)
		ax2.set_ylim(-200,200)
		ax1.set_xlim(-200,200)
		ax2.set_xlim(-200,200)

		ax1.set_xlabel('x (mm)')
		ax1.set_ylabel('y (mm)')
		ax2.set_xlabel('z (mm)')
		ax2.set_ylabel('y (mm)')

		circle1 = plt.Circle((data[0],data[1]), radius=3, color='b')
		circle2 = plt.Circle((data[2],data[1]), radius=3, color='b')
		circle3 = plt.Circle((trueData[0],trueData[1]), radius=3.5, color='r', fill=False)
		circle4 = plt.Circle((trueData[2],trueData[1]), radius=3.5, color='r', fill=False)

		ax1.add_patch(circle1)
		ax2.add_patch(circle2)
		ax1.add_patch(circle3)
		ax2.add_patch(circle4)

		plt.show(block=False)
