from fastapi import FastAPI, HTTPException
from openstack import Openstack
import uvicorn

#import sys
#sys.setrecursionlimit(5000)

app = FastAPI()
ops = Openstack("RegionOne")

@app.get("/api/v1/servers")
async def get_all_servers(page: int = 1, limit: int = 5):
    try: 
        servers = ops._get_all_servers(page, limit)
        return servers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v1/servers/{ins_id}")
async def get_all_server_by_id(ins_id: str):
    try: 
        server = ops._get_server_by_id(ins_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v1/images")
async def get_all_images():
    try: 
        images = ops._get_images()
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v1/flavors")
async def get_all_flavors():
    try: 
        flavors = ops._get_flavors()
        return flavors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/v1/networks")
async def get_all_networks():
    try: 
        networks = ops._get_networks()
        return networks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/create_server")
async def create_server(name: str, image_id: str, flavor_id: str, network_id: str):
    try:
        server = ops._create_server(name, image=image_id, flavor=flavor_id, network=network_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/v1/create_resize")
async def create_server(ins_id: str, flavor_id: str):
    try:
        server = ops._create_server(ins_id, flavor=flavor_id)
        return server
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run(app, host="10.5.11.35", port=8000)