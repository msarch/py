
function love.load()

  debug = false

  width = 1280
  height = 768

  success = love.window.setMode(width, height)

  tone = love.audio.newSource("tone.ogg", "stream")
  tone:setLooping(false)

  tutorial = "The keys ASDFGHJKL each represent a random color, which will be displayed in the inner box.\n\nWhen the game starts (press A to start), you will have 30 seconds to\n1. learn which key is which color and\n2. match the inner box to the outer color (by holding it down) as much as possible.\n\nFailure will not be tolerated!"

  colors = {
    {255,  62, 150},
    {139,  28,  98},
    {255, 187, 255},
    {255, 187, 155},
    {255, 187,  55},
    {255,  87, 255},
    {155, 187, 255},
    {155,  87,  55},
    { 95,  17, 255},
  }
--[[
    {220,  20,  60},
    {205, 140, 149},
    {139,  99, 108},
    {255,  87, 155},
    {255,  87,  55},
    {155, 187, 155},
    {155, 187,  55},
    {155,  87, 255},
    {155,  87, 155},
    { 55, 187, 255},
    { 55, 187, 155},
    { 55, 187,  55},
    { 55,  87, 255},
    { 55,  87, 155},
    { 55,  87,  55},
    { 95,  17, 155},
    { 95,  17,  55},
  }]]--

  keys = {
  --  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    "a", "d", "f", "g", "h", "j", "k", "l", "s"
  }

  keytocol = {}

  -- maps key values to colors
  for i,v in pairs(keys) do
    keytocol[v] = colors[i]
  end

  -- state can be pre, starting, game, end
  state = "pre"
  timer = 0
  gametimer = 30
  successtime = 0
  successrate = 0
  currentcolor = {255, 255, 255} 
end

function love.keypressed(key)
   if state == "pre" and key == "a" then
     state = "starting"
     timer = 2
   elseif state == "end" and key == "r" then
     love.load()
   elseif key == "escape" then
     love.event.push("quit")
   end
end

function love.update(dt)
  if state == "starting" then
    timer = timer - dt
    if timer < 0 then
      state = "game"
      tone:play()
    end
  elseif state == "game" then
    love.graphics.setColor(255, 255, 255)
    activekey = nil
    for i,v in pairs(keys) do
      if love.keyboard.isDown(v) then
        love.graphics.setColor(keytocol[v][1], keytocol[v][2], keytocol[v][3])
        activekey = v
      end
    end
    r1, g1, b1, a1 = love.graphics.getColor()
    currentcolor = {r1, g1, b1}
    r2, g2, b2, a2 = love.graphics.getBackgroundColor()
    currentbackground = {r2, g2, b2}
    --print("r", r1, r2, "g", g1, g2, "b", b1, b2)

    --broken for some reason
    -- if currentcolor == currentbackground then

    love.audio.setVolume(1)
    if r1 == r2 and g1 == g2 and b1 == b2 then
      successtime = successtime + dt
      love.audio.setVolume(0.1)
    end
    if timer < 0 then
      -- change color
      r = math.random(#colors)
      love.graphics.setBackgroundColor( colors[r][1], colors[r][2], colors[r][3] )
      timer = 1 + math.random(10)/10
    end
    timer = timer - dt
    if gametimer < 0 then
      successrate = (successtime/30)*100
      state = "end"
      tone:stop()
    end
    gametimer = gametimer - dt
  end
end

function love.draw()
  if state == "pre" then
    love.graphics.setBackgroundColor(255, 255, 255)
    love.graphics.setColor(0, 0, 0)
    love.graphics.rectangle("fill", width/4, height/4, width/2, height/2)
    love.graphics.setColor(255, 255, 255)
    love.graphics.printf(tutorial, width/4, height/4 + height/16, width/2, "center")
  elseif state == "starting" then
    love.graphics.setBackgroundColor(255, 255, 255)
    love.graphics.setColor(0, 0, 0)
    love.graphics.rectangle("fill", width/4, height/4, width/2, height/2)
    love.graphics.setColor(255, 255, 255)
    love.graphics.printf(math.ceil(timer), width/4, height/4 + height/16, width/2, "center")
  elseif state == "game" then
    love.graphics.setColor(currentcolor[1], currentcolor[2], currentcolor[3])
    love.graphics.rectangle("fill", width/4, height/4, width/2, height/2)
    if debug and activekey ~= nil then
      love.graphics.setColor(255, 255, 255)
      love.graphics.rectangle("fill", width/2-10, height/2-10, 20, 20)
      love.graphics.setColor(0, 0, 0)
      love.graphics.printf(activekey, width/2-10, height/2-5, 20, "center")
    end
  elseif state == "end" then
    love.graphics.setColor(0, 0, 0)
    love.graphics.rectangle("fill", width/4, height/4, width/2, height/2)
    love.graphics.setColor(255, 255, 255)
    love.graphics.printf("You were able to match " .. math.floor(successtime*100)/100 .. "s (" .. math.floor(100*successrate)/100 .. "%) of the time\n\nPress R to restart", width/4, height/4 + height/16, width/2, "center")
  end
end
