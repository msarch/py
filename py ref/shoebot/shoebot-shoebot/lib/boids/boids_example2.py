# Soaring text.

size(500, 500)
speed(100)

boids = ximport("boids")
reload(boids)

def setup():     
       
    global flock
    flock = boids.flock(2, 0, 0, WIDTH, HEIGHT)
    flock.goal(WIDTH/2, HEIGHT/2, 0)
    flock.scatter(0.01)
    #flock.noperch()
    
    global trail
    trail = []
    
    global banner
    banner = "woooosh"
    
def draw():
    
    background(0.2)

    global flock
    # Swam around the central goal, but not too tightly.
    flock.update(goal=60)
    
    global trail, banner
    # Here we add the current state of the flock to the trail.
    # The farther you go back in the trail,
    # the older the boids' positions in the flock will be.
    trail.append(flock.copy())
    # Keep a history of positions equal to the length of the banner text.
    if len(trail) > len(banner):
        trail.remove(trail[0])
    
    # Each frame, draw the trail.
    for i in range(len(trail)):
        
        # Each element in the trail is a flock object.
        # Traverse each boid in that flock.
        f = trail[i]
        for boid in f:
            
            # The fill's transparency is based on the boid's z-position.
            fill(0.8, 0.5+ boid.z/400)
            
            push()
            rotate(-boid.angle)
            fontsize(15 + boid.z/4)
            skew(boid.z / 20)
            # Each boid in this flock is represented by a banner character.
            # Boids in the first flock represent the first character,
            # boids in the last flock represent the last character.
            text(banner[i], boid.x, boid.y)
            pop()