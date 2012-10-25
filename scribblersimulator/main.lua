require 'middleclass'
require 'scribbler'
require 'ai'
require 'trigger'
objs = {}



local lp = love.physics
function love.load()
	table.insert(objs,simObject(600,200,0,100,100))
	scrib  = Scribbler(300,200,0,100,50)
	table.insert(objs,scrib)
	world = lp.newWorld()
	for i,v in ipairs(objs) do v:createBody(world) end
	cor = coroutine.create(runAI)
	time_elasped = 0
end

function love.update(dt)
	dt = dt
	scrib:update(dt)
	world:update(dt)
	status,err = coroutine.resume(cor)
	if not status then print(status,err) end
	time_elasped = time_elasped + dt
	--waits.update()
end

function love.draw()
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