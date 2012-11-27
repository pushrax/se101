

require 'middleclass'
require 'scribbler'
require 'ai'
local waits = require 'trigger'
require 'network'
require 'awesomerectanglebutton'
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
	w = Widget(0,0,800,600)
	b1 = Button(50,50,200,30)
	b1.text = 'food demo'
	w:addChildren(b1)
	function b1:onClick()
		thread:set('fb','food demo1')
	end
	b2 = Button(50,100,200,30)
	b2.text = 'food ffwin'
	w:addChildren(b2)
	function b2:onClick()
		thread:set('fb','food ffwin')
	end
	love.graphics.setFont(love.graphics.newFont(20))

end

scale = 20
gridsize = 1200/scale
path_big = {}
function drawpath_big()
	love.graphics.setColor(0,0,0)
	if #path_big <= 2 then return end
	for i=1,#path_big-1 do
		local a,b = unpack(path_big[i])
		local c,d = unpack(path_big[i+1])
		a,b = a*gridsize+gridsize/2,invertY*b*gridsize+gridsize/2
		c,d = c*gridsize+gridsize/2,invertY*d*gridsize+gridsize/2
		t = {a,b,c,d}
		love.graphics.line(unpack(t))
	end
	local a,b = unpack(path_big[1])
	a,b = a*gridsize+gridsize/2,invertY*b*gridsize+gridsize/2
	local c,d = scrib.body:getPosition()
	love.graphics.line(a,b,c,d)
end

function getTable(line)
	--print (line)
	local sep,fields  = ' ', {}
    local pattern = "([^ ]+)"
    string.gsub(line,pattern,function(c) fields[#fields+1] = tonumber(c) end)
    --local cmd = table.remove(fields,1)
    
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
        --print (x,y,r)
		scrib.body:setPosition(x/scale,invertY*y/scale+gridsize)
		scrib.body:setAngle((r-90)*math.pi/180)
		scrib.body:applyLinearImpulse(0.01,0.01)
	end


	local block = thread:get'block'
	if block then
		x,y = unpack(getTable(block))

		local v = simObject(x*gridsize+gridsize/2,invertY*y*gridsize+gridsize/2,0,gridsize,gridsize)
		print (x*gridsize,invertY*y*gridsize,'created')
		v:createBody(world)
		table.insert(objs,v)
	end


	local path = thread:get'path'
	--path = 'path 50 50 51 50 52 50 52 49 52 48 52 47 53 47 54 47 55 47 56 47 57 47'
	if path then
		print (path)
		local path = getTable(path)
		path_big= {}
		for i = 1,#path/2 do
			--print (path[i*2-1],path[i*2])
			path_big[i] = {path[i*2-1],path[i*2]}
		end
	end
end

function love.draw()
	love.graphics.setBackgroundColor(255,255,255)
	--love.graphics.scale(1,-1)]
	local pos = thread:peek'pos'
	--print (pos)
	if pos then
		local x,y,r = unpack(getTable(pos))
		--print (x,y,r)
		love.graphics.setColor(0,0,0)
    	love.graphics.print(string.format("%d %d %d",math.floor(x/gridsize),math.floor(y/gridsize-gridsize),r),10,10)
	end

	w:draw()
	local x,y = scrib.body:getPosition()
	if x and y then
		love.graphics.translate(-scrib.body:getX()+love.graphics.getWidth()/2,
			-scrib.body:getY()+love.graphics.getHeight()/2)
	end
	love.graphics.setColor(0,0,0)
	for i = -200,200 do
		love.graphics.line(i*gridsize,-9999,i*gridsize,9999)
		love.graphics.line(-9999,i*gridsize,9999,i*gridsize)
	end
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

function love.mousereleased(x,y,b)
	w:mousereleased(x,y,b)
end

function love.mousepressed(x,y,b)
	if b~='r' then return end
	sound.play('drum3.ogg','interface')
	x = x + scrib.body:getX()
	y = y + scrib.body:getY()
	x,y = math.floor((x/gridsize))-6,math.floor(-y/gridsize)+6
	thread:set('fb',string.format('moveto %d %d',x,y))
end