local function hasObstacle(a,b)
	return a==0 or b==0
end

local rdyToTurn = 0
function runAI()
	--print (not hasObstacle(scrib:getIR()))
	starty = scrib:getY()
	while not hasObstacle(scrib:getIR()) do
		scrib:forward()
	end
	scrib:stop()
	--pexecute(turnlefter)

	stage2()

end

function stage3()
	print 'STAGE 3 MOTHERFUCKER'
	print (scrib:getAngle())
	while (scrib:getAngle()>0.1 or scrib:getAngle()<-0.1) do
		scrib:motors(1,-1)
	end
	--scrib.body:setAngle(0)
	while (true) do
		scrib:forward()
	end
end

function stage1()

	while not hasObstacle(scrib:getIR()) do
		scrib:forward()
		if math.abs(scrib:getY() - starty)<5 and rdyToTurn > 2 then
			stage3()
		end
		if time_elasped % 2 < .5 then
			while not hasObstacle(scrib:getIR()) do
				scrib:motors(-1,1)
			end
			break
		end
	end
	scrib:stop()

	stage2()
end

function stage2()
	while true do
		-- stage 2
		while hasObstacle(scrib:getIR()) do
			scrib:motors(1,-1)
		end
		--assert(false)
		scrib:stop()

		break
		-- TODO: OVER TURN
	end
	rdyToTurn = rdyToTurn + 1
	stage1()
end

function turnlefter()
	while true do
		wait(5)

	end
end