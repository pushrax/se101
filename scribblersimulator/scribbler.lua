require 'simObject'

Scribbler = simObject:subclass'Scribbler'

local lp = love.physics
local gra = love.graphics

local speedconst = 50

function Scribbler:initialize(...)
	simObject.initialize(self,...)
	self.leftspeed = 0
	self.rightspeed = 0
end

function Scribbler:createBody(world)
	assert(self.x)
	assert(self.w and self.h)
	self.body = lp.newBody(world,self.x,self.y,'dynamic')
	local shape = lp.newCircleShape(16)
	self.fixture = lp.newFixture(self.body,shape)

	local wheelshape = lp.newRectangleShape(8,4)
	self.leftwheel = lp.newBody(world,self.x,self.y-16,'dynamic')
	self.leftwheelfixture = lp.newFixture(self.leftwheel,wheelshape)
	self.rightwheel = lp.newBody(world,self.x,self.y+16,'dynamic')
	self.rightwheelfixture = lp.newFixture(self.rightwheel,wheelshape)

	self.body:setAngle(self.r)

	self.joint1 = love.physics.newWeldJoint( self.body, self.leftwheel, self.x, self.y )
	self.joint2 = love.physics.newWeldJoint( self.body, self.rightwheel, self.x, self.y )
	self.leftwheelfixture:setUserData(self)
	self.rightwheelfixture:setUserData(self)	
	self.fixture:setUserData(self)

end

function Scribbler:stop()
	self.body:setAngularVelocity(0)
	self.body:setLinearVelocity(0,0)
	self.leftspeed = 0
	self.rightspeed = 0
end

function Scribbler:forward(speed)
	self:motors(1,1)
	--self.body:setLinearVelocity(c*speed,s*speed)
	--coroutine.yield()
end
function Scribbler:stop(speed)
	self:motors(0,0)
	--self.body:setLinearVelocity(c*speed,s*speed)
	--coroutine.yield()
end

function Scribbler:getY()
	return self.body:getY()
end

function Scribbler:getAngle()
	return self.body:getAngle()
end

function Scribbler:motors(left,right)
	self.leftspeed = left
	self.rightspeed = right
	--coroutine.yield()
end

function Scribbler:update(dt)
	--print (self.leftspeed,self.rightspeed)
	local r = self.leftwheel:getAngle()
	local leftspeed = speedconst * self.leftspeed
	local c,s = math.cos(r),math.sin(r)
	--print (c*leftspeed,s*leftspeed)
	self.leftwheel:setLinearVelocity(c*leftspeed,s*leftspeed)
	local r = self.rightwheel:getAngle()
	local rightspeed = speedconst * self.rightspeed
	local c,s = math.cos(r),math.sin(r)
	self.rightwheel:setLinearVelocity(c*rightspeed,s*rightspeed)

	local minfrac
	local function worldRayCastCallback(fixture,x,y,xn,yn,fraction)
		if  fraction>=minfrac then return 1 end
		local t = fixture:getUserData()
		if not( t and t.class == Scribbler ) then
			minfrac = math.min(minfrac,fraction)
		end
		return 1
	end
	minfrac = 1
	local x1,y1 = self.leftwheel:getWorldCenter()
	local x2,y2 = self.leftwheel:getWorldPoint(100,0)
	world:rayCast(x1,y1,x2,y2,worldRayCastCallback)
	self.leftcast = minfrac


	minfrac = 1
	local x1,y1 = self.rightwheel:getWorldCenter()
	local x2,y2 = self.rightwheel:getWorldPoint(100,0)
	world:rayCast(x1,y1,x2,y2,worldRayCastCallback)
	self.rightcast = minfrac
end

function Scribbler:draw()
	local x,y = self.body:getPosition()
	local r = self.body:getAngle()
	local c,s = math.cos(r),math.sin(r)
	gra.setColor(255,0,0,100)
	gra.circle('fill',x,y,16)
	gra.line(x,y,x+c*32,y+s*32)


	local x,y = self.leftwheel:getPosition()
	local r = self.leftwheel:getAngle()
	drawShape(x,y,r,16,8,0,255,0,100)
	if self.leftcast then

		local c,s = math.cos(r),math.sin(r)
		gra.setColor(255,0,255,100)
		gra.line(x,y,x+c*self.leftcast*100,y+s*self.leftcast*100)
		--if self.leftcast ~= 1 then
		--	local nx,ny = x+c*self.leftcast*100,y+s*self.leftcast*100
		--	gra.draw(p,nx,ny)
		--end
	end

	local x,y = self.rightwheel:getPosition()
	local r = self.rightwheel:getAngle()
	drawShape(x,y,r,16,8,0,255,0,100)

	if self.rightcast then
		local c,s = math.cos(r),math.sin(r)
		gra.setColor(255,0,255,100)
		gra.line(x,y,x+c*self.rightcast*100,y+s*self.rightcast*100)
	end
end

function Scribbler:getIR()
	--coroutine.yield()
	return math.floor(self.leftcast),math.floor(self.rightcast)
end