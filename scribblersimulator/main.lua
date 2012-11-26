require 'middleclass'
require 'scribbler'
require 'ai'
local waits = require 'trigger'
require 'network'
objs = {}


local thread = love.thread.newThread('tcp','network.lua')
thread:start()

function forward(...)
	scrib:forward(...)
end

function motors(...)
	scrib:motors(...)
end

function getIR()
	a,b = scrib:getIR()
	return {a,b}
end

function stop()
	scrib:stop()
end

local lp = love.physics
function love.load()
	table.insert(objs,simObject(400,300,0,50,300))
	table.insert(objs,simObject(700,300,0,50,300))
	table.insert(objs,simObject(550,150,0,300,50))
	--table.insert(objs,circleObject(550,300,100))
	scrib  = Scribbler(50,200,0,100,50)
	table.insert(objs,scrib)
	world = lp.newWorld()
	for i,v in ipairs(objs) do v:createBody(world) end
	--cor = coroutine.create(runAI)
	time_elasped = 0
	--execute(listen)


end

scale = 20

function process(msg)
	if msg ~= 'TROLLFACE' then
		print (msg)
		local sep,fields  = ' ', {}
		local pattern = "([^ ]+)"
		string.gsub(msg,pattern,function(c) fields[#fields+1] = c end)

		local command,x,y,r = unpack(fields)
		scrib.body:setPosition(x/scale,y/scale)
		scrib.body:setAngle((-r+90)*math.pi/180)
		scrib.body:applyLinearImpulse(0.01,0.01)
	end
end

function love.update(dt)
	dt = dt
	scrib:update(dt)
	world:update(dt)
	--status,err = coroutine.resume(cor)
	--if not status then print(status,err) end
	time_elasped = time_elasped + dt
	waits.update()
	msg = thread:get('cmd')
	if msg then
		process(msg)
	end
end

function love.draw()
	love.graphics.scale(1,-1)
	for i,v in ipairs(objs) do v:draw()
	end
end

response = {
	d = {1,-1},
	a = {-1,1},
	w = {1,1},
	s = {-1,-1},
}

function love.keypressed(k)
	if response[k] then
		coroutine.resume(coroutine.create(function() scrib:motors(unpack(response[k])) end))
	end
end

function love.mousepressed(x,y,b)

	thread:set('fb',string.format('moveto %d %d',x*scale,-y*scale))
end