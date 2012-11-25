
simObject = Object:subclass'simObject'

local lp = love.physics
local gra = love.graphics

local dot = gra.newImage'dot.png'

function drawShape(x,y,rot,w,h,r,g,b,a)
	if not r then
		gra.setColor(255,255,255)
	else
		gra.setColor(r,g,b,a)
	end
	assert(dot)
	gra.draw(dot,x,y,rot,w,h,.5,0.5)
end

function simObject:initialize(x,y,r,w,h)
	self.x,self.y = x,y
	self.r = r
	self.w,self.h = w,h
	assert(self.w and self.h)
end

function simObject:createBody(world)
	assert(self.x)
	assert(self.w and self.h)
	self.body = lp.newBody(world,self.x,self.y,'static')
	local shape = lp.newRectangleShape(self.w,self.h)
	self.fixture = lp.newFixture(self.body,shape)
	self.body:setAngle(self.r)
end

function simObject:draw()
	local x,y = self.body:getPosition()
	local r = self.body:getAngle()
	drawShape(x,y,r,self.w,self.h,0,255,0,100)
end

circleObject = Object:subclass'circleObject'
function circleObject:initialize(x,y,rad)
	self.x,self.y = x,y
	self.rad = rad
end

function circleObject:createBody(world)
	assert(self.x)
	assert(self.rad)
	self.body = lp.newBody(world,self.x,self.y,'static')
	local shape = lp.newCircleShape(self.rad)
	self.fixture = lp.newFixture(self.body,shape)
	self.body:setAngle(self.rad)
end

function circleObject:draw()
	local x,y = self.body:getPosition()
	local r = self.body:getAngle()
	gra.circle('fill',x,y,self.rad)
end