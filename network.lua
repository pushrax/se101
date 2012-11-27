local socket = require 'socket'

assert(socket)
local address, port = "localhost", 12345
local entity -- entity is what we'll be controlling

local udp = socket.udp()
udp:settimeout(0)
udp:setsockname("*",port)
local world = {} -- the empty world-state
local data, msg_or_ip, port_or_nil
local cmd



local outaddress, outport = "localhost", 12346

        -- more of these funky match paterns!
        --entity, cmd, parms = data:match("^(%S*) (%S*) (.*)")
local udp2 = socket.udp()
udp2:settimeout(0)
udp2:setpeername(outaddress,outport)
--[[
function networkupdate(dt)
	cmd, msg_or_ip, port_or_nil = udp:receivefrom()
	local result
    if cmd then
    	--execute(function()
    	print (cmd)
    	result = loadstring('return '..cmd)()
    	--print (unpack(result))
	    	if result and #result > 0 then
	    		
	    	end
		--end)
    end
end]]

function returnToStart()
    udp2:send("returnToStart()")
end

function wantFood(food)
    udp2:send(string.format("wantFood(%s)",food))
end