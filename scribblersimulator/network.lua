
local producer = love.thread.getThread('tcp')
if producer then

local socket = require 'socket'

local master = socket.tcp()
local client = socket.connect('192.168.1.111',5005)
--local client = socket.connect('localhost',5005)

function getFood(food)
    print (food,'being delievered')
    client:send(string.format('getFood %s\n',food))
end

function returnToStart()
    client:send'returnToStart\n'
end

function clientLoop()
    while true do
        local cb = producer:get('fb')
        if cb then
            client:send(cb..'\n')
        else
            client:send('TROLLFACE\n')
        end
        --print 'sent'
        --client:send('nothing happened\n')
        --print (cb,'sent')
        --client:settimeout(10)
        local line,err = client:receive()
        if not err then
            --print (line)
            if line ~= 'TROLLFACE' then
                local sep,fields  = ' ', {}
                local pattern = "([^ ]+)"
                string.gsub(line,pattern,function(c) fields[#fields+1] = c end)
                local cmd = table.remove(fields,1)
                
                producer:set(cmd,line)
            end
        else
            --print (err)
        end

    end
end
clientLoop()
end