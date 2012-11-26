

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
gridsize = 1200/scale
path_big = {}
function drawpath_big()
	if #path_big <= 2 then return end
	for i=1,#path_big-1 do
		local a,b = unpack(path_big[i])
		local c,d = unpack(path_big[i+1])
		local t = {a,b,c,d}
		for i,v in ipairs(t) do
			t[i] = v*gridsize+.5*gridsize
		end
		love.graphics.line(unpack(t))
	end
end

function getTable(line)
	local sep,fields  = ' ', {}
    local pattern = "([^ ]+)"
    string.gsub(line,pattern,function(c) fields[#fields+1] = c end)
    local cmd = table.remove(fields,1)
    
	return fields
end


invertY = -1
function love.update(dt)
	dt = dt
	scrib:update(dt)
	world:update(dt)
	--status,err = coroutine.resume(cor)
	--if not status then print(status,err) end
	time_elasped = time_elasped + dt
	waits.update()
	local pos = thread:peek'pos'
	--print (pos)
	if pos then
		local x,y,r = unpack(getTable(pos))
        
		scrib.body:setPosition(x/scale,invertY*y/scale)
		scrib.body:setAngle((-r+90)*math.pi/180)
		scrib.body:applyLinearImpulse(0.01,0.01)
	end


	local block = thread:get'block'
	if block then

		x,y = unpack(getTable(block))

		local v = simObject(x*gridsize,invertY*y*gridsize,0,gridsize,gridsize)
		v:createBody(world)
		table.insert(objs,v)
	end


	local path = thread:get'path'
	if path then
		local path = getTable(path)
		for i = 1,#path/2 do
			--print (path[i*2-1],path[i*2])
			path_big[i] = {path[i*2-1],invertY*path[i*2]}
		end
	end
end

function love.draw()
	--love.graphics.scale(1,-1)
	drawpath_big()
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