sound = require 'sound'
sound.load()

Widget = Object:subclass'Widget'

function Widget:initialize(x,y,w,h)
	self.children = {}
	self.x,self.y,self.w,self.h = x,y,w,h
end

function Widget:isHovered(x,y)
	return x>=self.x and x<= self.x + self.w
		and y>=self.y and y<=self.y + self.h
	
end

function Widget:mousereleased(x,y,r)
	for i,v in ipairs(self.children) do
		if v:isHovered(x,y) then 
			v:mousereleased(x,y,r)
		end
	end

end

function Widget:addChildren(c)
	table.insert(self.children,c)
end

function Widget:draw()
	for i,v in ipairs(self.children) do
		v:draw()
	end
end

Button = Widget:subclass'Button'
function Button:mousereleased(x,y,r)
	if self.onClick then
		self:onClick(x,y,r)
	end
end

local quads = {
	topleft = love.graphics.newQuad(0,0,10,10,40,40),
	topright = love.graphics.newQuad(30,0,10,10,40,40),
	botleft = love.graphics.newQuad(0,30,10,10,40,40),
	botright = love.graphics.newQuad(30,30,10,10,40,40),
	top = love.graphics.newQuad(10,0,1,10,40,40),
	bot = love.graphics.newQuad(10,30,1,10,40,40),
	left = love.graphics.newQuad(0,10,10,1,40,40),
	right = love.graphics.newQuad(30,10,10,1,40,40),
	mid = love.graphics.newQuad(10,10,1,1,40,40)
}

	local attritubebackground = love.graphics.newImage"attback.png"
function Button:draw()

	local x,y = self.x,self.y
	local w,h = self.w,self.h
	love.graphics.setColor(255,255,255)
	love.graphics.drawq(attritubebackground,quads.topleft,x-10,y-10)
	love.graphics.drawq(attritubebackground,quads.topright,x+w,y-10)
	love.graphics.drawq(attritubebackground,quads.botleft,x-10,y+h)
	love.graphics.drawq(attritubebackground,quads.botright,x+w,y+h)
	love.graphics.drawq(attritubebackground,quads.top,x,y-10,0,w,1)
	love.graphics.drawq(attritubebackground,quads.bot,x,y+h,0,w,1)
	love.graphics.drawq(attritubebackground,quads.left,x-10,y,0,1,h)
	love.graphics.drawq(attritubebackground,quads.right,x+w,y,0,1,h)
	love.graphics.drawq(attritubebackground,quads.mid,x,y,0,w,h)
	self.text = self.text or ''
	if self:isHovered(love.mouse.getPosition()) then

		love.graphics.setColor(210, 152, 65)
	end
	love.graphics.printf(string.upper(self.text),self.x+10,self.y+10,self.w-20,'center')
	
end