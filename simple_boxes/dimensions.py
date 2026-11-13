def clamp(p):
    p.wall=min(p.wall,min(p.length,p.width)/4)
    p.depth=min(p.depth,max(.1,p.height-.1))
    p.partition_height=min(p.partition_height,p.depth)
    p.seating=min(p.seating,p.height)
    p.partition=min(p.partition,(p.length-2*p.wall)/(2*p.nx),(p.width-2*p.wall)/(2*p.ny))
    p.radius=min(p.radius,min(p.length,p.width)/2-.1)

    sx=(p.length-2*p.wall-(p.nx-1)*p.partition)/p.nx
    sy=(p.width-2*p.wall-(p.ny-1)*p.partition)/p.ny
    p.radius=min(p.radius,min(sx,sy)/4+p.wall)
    p.inner_radius=min(max(p.inner_radius,p.radius-p.wall),min(sx,sy)/4)

def cells(p):
    x=p.length-2*p.wall; y=p.width-2*p.wall
    sx=(x-(p.nx-1)*p.partition)/p.nx; sy=(y-(p.ny-1)*p.partition)/p.ny
    for i in range(p.nx):
        for j in range(p.ny):
            yield -x/2+sx/2+i*(sx+p.partition),-y/2+sy/2+j*(sy+p.partition),sx,sy


