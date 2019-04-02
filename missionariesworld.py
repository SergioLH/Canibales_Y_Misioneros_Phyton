from Tkinter import *
import tkMessageBox

LEFT = 'left'
RIGHT = 'right'

class MissionariesWorld:

	def __init__(self, initial_state, final_state, steps):
		
		n_miss = sum(initial_state.miss)
		n_cann = sum(initial_state.cann)
		capacity = initial_state.capacity
		
		n_miss_final = sum(final_state.miss)
		n_cann_final = sum(final_state.cann)
		capacity_final = final_state.capacity
		
		if n_miss != n_miss_final or n_cann != n_cann_final or capacity != capacity_final:
			raise Exception("Initial and final states are incompatible")
		
		if n_cann > n_miss:
			raise Exception("Wrong parameters: cannibals (%d) must be less or equal than missionaries (%d)" % 
						(n_cann, n_miss))
			
		if capacity >= n_cann:
			raise Exception("Wrong parameters: boat capacity (%d) must be less than cannibals (%d)" % 
						(capacity, n_cann))
		
		self.missionaries = [initial_state.miss[0], initial_state.miss[1]]
		self.cannibals = [initial_state.cann[0], initial_state.cann[1]]
		self.boat_position = initial_state.boat_position
		self.in_boat = [0, 0]
		self.boat_capacity = capacity
		self.steps = steps
		
		self.final_miss = [final_state.miss[0], final_state.miss[1]]
		self.final_cann = [final_state.cann[0], final_state.cann[1]]
		self.final_pos = final_state.boat_position
		
		self.reduction_factor = (n_miss - 1) / 5 + 1
		if self.reduction_factor < 1:
			self.reduction_factor = 1
		self.window = Tk()
		self.window.resizable(False, False)
		self.window.title("Missionaries and Cannibals")
		self.canvas = Canvas(self.window, width=1000, height=500)
		self.cann_image = PhotoImage(file="img/cann.gif")
		self.miss_image = PhotoImage(file="img/miss.gif")
		self.scen_image = PhotoImage(file="img/scen.gif")
		self.boat_image = PhotoImage(file="img/boat.gif")
		if self.reduction_factor > 1:
			self.cann_image = self.cann_image.subsample(self.reduction_factor)
			self.miss_image = self.miss_image.subsample(self.reduction_factor)
		self.b_next = Button(self.window, text="Next Step", command=self.next_step, font=("Helvetica", 16))
		self.b_next.place(x=500, y=80, anchor=CENTER)
		if not self.steps or len(self.steps) == 0:
			self.b_next.config(state=DISABLED)
		self.l_step = Label(self.window, text="", font=("Helvetica", 16))
		self.canvas.pack()
		self.draw()
		self.window.mainloop()
		
		
		
	# NEXT STEP IN THE SOLUTION FOUND
	def next_step(self):
		
		self.b_next.config(state=DISABLED)
		
		# NEXT STEP IN THE LIST
		step = self.steps.pop(0)
		self.l_step.config(text=step)
		self.l_step.config(background="white")
		self.l_step.place(x=500, y=150, anchor=CENTER)
		direction = step[0]
		miss_in_boat = int(step[1])
		cann_in_boat = int(step[2])
		if direction == '>':
			origin = 0
			destination = 1
		else:
			origin = 1
			destination = 0
		
		# FORMAT ERRORS
		if direction == '>' and self.boat_position == RIGHT:
			tkMessageBox.showerror("Error", "Incorrect direction (>)")
			return
		if direction == '<' and self.boat_position == LEFT:
			tkMessageBox.showerror("Error", "Incorrect direction (<)")
			return
		if cann_in_boat + miss_in_boat > self.boat_capacity:
			tkMessageBox.showerror("Error", "Boat capacity exceeded")
			return
		if miss_in_boat > self.missionaries[origin]:
			tkMessageBox.showerror("Error", "Not enough missionaries")
			return
		if cann_in_boat > self.cannibals[origin]:
			tkMessageBox.showerror("Error", "Not enough cannibals")
			return
		
		# ORIGIN SHORE UPDATE
		while self.in_boat[0] < miss_in_boat:
			self.missionaries[origin] -= 1
			self.in_boat[0] += 1
			self.draw()
			self.canvas.after(300)
			
		while self.in_boat[1] < cann_in_boat:
			self.cannibals[origin] -= 1
			self.in_boat[1] += 1
			self.draw()
			self.canvas.after(300)
			
		if miss_in_boat > 0 and cann_in_boat > miss_in_boat:
			self.b_next.config(state=DISABLED)
			self.canvas.update()
			tkMessageBox.showerror("Error", "There are more cannibals in the boat")
			return
		
		self.canvas.after(200)
		
		# BOAT TRIP
		if self.boat_position == LEFT:
			self.boat_position = RIGHT
		else:
			self.boat_position = LEFT
		self.draw()
		self.canvas.after(300)
		
		# DESTINATION SHORE UPDATE
		while self.in_boat[0] > 0:
			self.missionaries[destination] += 1
			self.in_boat[0] -= 1
			self.draw()
			self.canvas.after(300)
			
		while self.in_boat[1] > 0:
			self.cannibals[destination] += 1
			self.in_boat[1] -= 1
			self.draw()
			self.canvas.after(300)
		
		# GAME OVER CONDITIONS
		if self.missionaries[0] > 0 and self.cannibals[0] > self.missionaries[0]:
			self.b_next.config(state=DISABLED)
			self.draw()
			tkMessageBox.showerror("GAME OVER!", "There are more cannibals in the left shore! :(")
			return
		if self.missionaries[1] > 0 and self.cannibals[1] > self.missionaries[1]:
			self.b_next.config(state=DISABLED)
			self.draw()
			tkMessageBox.showerror("GAME OVER!", "There are more cannibals in the right shore! :(")
			return
		
		# FINISH CONDITIONS (GOAL ACHIEVED vs GOAL NOT ACHIEVED)
		if self.missionaries == self.final_miss and self.cannibals == self.final_cann and self.boat_position == self.final_pos:
			self.b_next.config(state=DISABLED)
			self.draw()
			tkMessageBox.showinfo("Finished!", "Goal achieved! :)")
			return
		elif len(self.steps) == 0:
			self.b_next.config(state=DISABLED)
			self.draw()
			tkMessageBox.showwarning("Finished", "No steps left")
			return
		
		self.b_next.config(state=NORMAL)
		self.canvas.update()
		
		
	# DRAWS THE SCENARIO
	def draw(self):
		
		self.canvas.delete(ALL)
		
		# BACKGROUND
		self.canvas.create_image(0, 0, image=self.scen_image, anchor=NW)
		
		inc = 60/self.reduction_factor
		# LEFT SHORE
		for i in range(self.missionaries[0]):
			self.canvas.create_image(40 + i*inc, 20, image=self.miss_image, anchor=NW)
		for i in range(self.cannibals[0]):
			self.canvas.create_image(10 + i*inc, 120, image=self.cann_image, anchor=NW)
		
		# RIGHT SHORE
		for i in range(self.missionaries[1]):
			self.canvas.create_image(670 + i*inc, 20, image=self.miss_image, anchor=NW)
		for i in range(self.cannibals[1]):
			self.canvas.create_image(650 + i*inc, 120, image=self.cann_image, anchor=NW)
			
		# BOAT
		inc = 10/self.reduction_factor
		if self.boat_position == LEFT:
			self.canvas.create_image(200, 350, image=self.boat_image, anchor=NW)
			for i in range(self.in_boat[1]):
				self.canvas.create_image(280 + i*inc, 400 + i*inc, image=self.cann_image, anchor=SW)
			for i in range(self.in_boat[0]):
				self.canvas.create_image(230 + i*inc, 400 + i*inc, image=self.miss_image, anchor=SW)
		else:
			self.canvas.create_image(530, 350, image=self.boat_image, anchor=NW)
			for i in range(self.in_boat[1]):
				self.canvas.create_image(610 + i*inc, 400 + i*inc, image=self.cann_image, anchor=SW)
			for i in range(self.in_boat[0]):
				self.canvas.create_image(560 + i*inc, 400 + i*inc, image=self.miss_image, anchor=SW)	
			
		self.canvas.update()
		
