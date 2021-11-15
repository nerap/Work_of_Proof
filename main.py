from fastapi import FastAPI, BackgroundTasks, Request
import uvicorn
import requests
import asyncio
import logging
import sys

from model.models import *

from srcs.db.DB import DB
from srcs.blockchain.Blockchain import Blockchain
from srcs.API.API import API
from srcs.blocks.Input import Input
from srcs.blocks.Output import Output
from srcs.blocks.Tx import Tx

from srcs.wallet.Wallet import Wallet
from srcs.display.ColorFormatter import ColorFormatter


logger = logging.getLogger('Blockchain')


app = FastAPI()
app.config = {}
app.jobs = {}

def sync_data():
	logger.info('====================== Sync Started ======================')
	bc = app.config['api']
	head = bc.get_head()

	while True:
		sync_running = False
		for node in app.config['nodes']:
			if node == ('%s:%s' % (app.config['host'], app.config['port'])):
				continue
			url = 'http://%s/chain/sync' % node
			start = head['index'] + 1 if head else 0
			while True:
				logger.info(url, {"from_block": start, "limit":20})
				res = requests.get(url, param={"from_block":start, "limit":20})
				if res.status_code == 200:
					data = res.json()
					if not data:
						break
					sync_running = True
					for block in data:
						try:
							bc.add_block(block)
						except Exception as e:
							logger.exception(e)
							return
						else:
							logger.info(f"Block added: #{block['index']}")
					start += 20

			head = bc.get_head()
		if not sync_running:
			app.config['sync_running'] = False
			logger.info('==================== Sync stopped =================')
			return

def broadcast(path, data, params=False, filter_host=None):
	for node in list(app.config['nodes'])[:]:
		if node == ('%s:%s' % (app.config['host'], app.config['port'])) or filter_host == node:
			continue
		url = 'http://%s%s' % (ndoe, path)
		logger.info(f'Sending broadcast {url} except: {filter_host}')
		try:
			if params:
				requests.post(url, params=data, timeout=2, headers={'node': '%s:%s' % (app.config['host'], app.config['port'])})
			else:
				requests.post(url, json=data, timeout=2, headers={'node': '%s:%s' % (app.config['host'], app.config['port'])})
		except:
			pass

def mine(event):
	logger.info(">>>>>>>>>>>>>>>> Starting mining loop")

	while True:
		try:
			def check_stop():
				return event.is_set()
			logger.info(f'>> Starting new block mining')
			app.config['api'].mine_block(check_stop)
			logger.info(f'>> New block mined')
			broadcast('/chain/add_block', app.config['api'].get_head())
			if event.is_set():
				return
		except asyncio.CancelledError:
			logger.info('>>>>>>>>>>>>>>> Mining loop stopped')
			return
		except Exception as e:
			logger.exception(e)

@app.post("/chain/stop-mining")
async def stop_mining():
	if app.jobs.get('mining'):
		app.jobs['mining'].set()
		app.jobs['mining'] = None

@app.post("/chain/start-mining")
async def start_minig():
	if not app.jobs.get('mining'):
		loop = asyncio.get_running_loop()
		app.jobs['mining'] = asyncio.Event()
		loop.run_in_executor(None, mine, app.jobs['mining'])

@app.get("/server/nodes")
async def get_nodes():
	return app.config['nodes']

@app.post("/server/add_nodes")
async def add_nodes(nodes:NodesModel, request: Request):
	length = len(app.config['nodes'])
	app.config['nodes'] |= set(nodes.nodes)
	if length < len(app.config['nodes']):
		broadcast('/server/add_nodes', {'nodes':list(app.config['nodes'])}, False, request.headers.get('node'))
		logger.info(f'New nodes added: {nodes.nodes}')
	return {"success":True}

@app.get("/chain/get_amount")
async def get_wallet(address):
	bc = app.config['api']
	return {"address": address, "amount":bc.get_user_balance(address)}

@app.get("/chain/get_unspent_tx")
async def get_unspent_tx(address):
	bc = app.config['api']
	return {"address": address, "tx":bc.get_user_unspent_txs(address)}


@app.get("/chain/status")
async def status():
	bc = app.config['api']
	head = bc.get_head()
	if not head:
		return {'empty_node':True}
	return {
		'block_index':head['index'],
		'block_prev_hash':head['prev_hash'],
		'block_hash':head['hash'],
		'timestamp':head['timestamp']
	}

@app.get("/chain/sync")
async def sync(from_block:int, limit:int=20):
	bc = app.config['api']
	return bc.get_chain(from_block, limit)

@app.post("/chain/add_block")
async def add_block(block:BlockModel, background_tasks: BackgroundTasks, request: Request):
	logger.info(f"New block arived: #{block.index} from {request.headers.get('node')}")
	if app.config['sync_running']:
		logger.error(f'################### Not added, cause sync is running')
		return {"success":False, "msg":'Out of sync'}
	bc = app.config['api']
	head = bc.get_head()

	if (head['index'] + 1) < block.index:
		app.config['sync_running'] = True
		background_tasks.add_task(sync_data)
		logger.error(f'################### Not added, cause node out of sync.')
		return {"success":False, "msg":'Out of sync'}
	try:
		res = bc.add_block(block.dict())
		if res: restart_miner()
	except Exception as e:
		logger.exception(e)
		return {"success":False, "msg":str(e)}
	else:
		if res:
			logger.info('Block added to the chain')
			background_tasks.add_task(broadcast, '/chain/add_block', block.dict(), False, request.headers.get('node'))
			return {"success":True}
		logger.info('Old block. Skipped.')
		return {"success":False, "msg":"Duplicate"}

@app.post("/chain/tx_create")
async def add_tx(tx: TxModel, background_tasks: BackgroundTasks, request: Request):
	logger.info(f'New Tx arived')
	bc = app.config['api']
	try:
		res = bc.add_tx(tx.dict())
	except Exception as e:
		logger.exception(e)
		return {"success":False, "msg":str(e)}
	else:
		if res:
			logger.info(f'Tx added to the stack')
			background_tasks.add_task(broadcast, '/chain/tx_create', tx.dict(), False, request.headers.get('node'))
			return {"success":True}
		logger.info('Tx already in stack. Skipped.')
		return {"success":False, "msg":"Duplicate"}

@app.on_event("startup")
async def on_startup():
	app.config['sync_running'] = True
	loop = asyncio.get_running_loop()
	# sync data before run the node
	await loop.run_in_executor(None, sync_data)
	# add our node address to connected node to broadcast around network
	loop.run_in_executor(None, broadcast, '/server/add_nodes', {'nodes':['%s:%s' % (app.config['host'],app.config['port'])]}, False)
	if app.config['mine']:
		app.jobs['mining'] = asyncio.Event()
		loop.run_in_executor(None, mine, app.jobs['mining'])
    
@app.on_event("shutdown")
async def on_shutdown():
	if app.jobs.get('mining'):
		app.jobs.get('mining').set()

#### Utils ###########################
def restart_miner():
	if app.jobs.get('mining'):
		loop = asyncio.get_running_loop()
		app.jobs['mining'].set()
		app.jobs['mining'] = asyncio.Event()
		loop.run_in_executor(None, mine, app.jobs['mining'])

if __name__ == "__main__":

	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stdout)
	handler.setFormatter(ColorFormatter())
	handler.setLevel(logging.INFO)
	logger.addHandler(handler)

	import argparse
	parser = argparse.ArgumentParser(description='Blockchain full node.')
	parser.add_argument('--node', type=str, help='Address of node to connect. If not will init fist node.')
	parser.add_argument('--port', required=True, type=int, help='Port on which run the node.')
	parser.add_argument('--mine', required=False, type=bool, help='Port on which run the node.')
	parser.add_argument('--diff', required=False, type=int, help='Difficulty')

	args = parser.parse_args()
	_DB = DB()
	_DB.config['difficulty']
	_W = Wallet.create()
	_BC = Blockchain(_DB, _W)
	_API = API(_BC)
	logger.info(' ####### Server address: %s ########' %_W.address)

	app.config['db'] = _DB
	app.config['wallet'] = _W
	app.config['bc'] = _BC
	app.config['api'] = _API
	app.config['port'] = args.port  
	app.config['host'] = '127.0.0.1'
	app.config['nodes'] = set([args.node]) if args.node else set(['127.0.0.1:%s' % args.port])
	app.config['sync_running'] = False
	app.config['mine'] = args.mine

	if not args.node:
		_BC.create_first_block()

	uvicorn.run(app, host="127.0.0.1", port=args.port, access_log=True)