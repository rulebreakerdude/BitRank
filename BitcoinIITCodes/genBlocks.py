from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import net_util
import json
import os


class BlockList(object):
    def __init__(self, blist):
        self.blist = blist        
    

class Block:
    def __init__(self, b):
        self.hash = b['hash']
        self.confirmations = b['confirmations']
        self.size = b['size']
        self.height = b['height']
        self.version = b['version']
        self.merkleroot = b['merkleroot']
        self.transactions = [Transaction(t) for t in b['tx']]
        self.time = b['time']
        self.nonce = b['nonce']
        self.bits = b['bits']
        self.difficulty = b['difficulty']
        self.chainwork = b['chainwork']
        if('previousblockhash' in b):
            self.previousblockhash = b['previousblockhash']
        self.nextblockhash = b['nextblockhash']        
            
                        
class Transaction:
    def __init__(self, t):
        self.txid = t['txid']
        self.version = t['version']      
        self.lock_time = t['locktime']
        self.inputs = [Input(i) for i in t['vin']]
        self.outputs = [Output(o) for o in t['vout']]


class Input:
    def __init__(self, i):
        self.sequence = i['sequence']   
        if('coinbase' in i):
            self.coinbase = i['coinbase']
        else:
            self.txid = i['txid']
            self.vout = i['vout']
            self.script_sig = ScriptSig(i['scriptSig'])                        
        

class ScriptSig:
    def __init__(self, ss):
        self.asm = ss['asm']
        self.hex = ss['hex']   


class Output:
    def __init__(self, o):
        self.value = o['value']
        self.n = o['n']
        self.script_pub_key = ScriptPubKey(o['scriptPubKey'])


class ScriptPubKey:
    def __init__(self, spk):
        self.asm = spk['asm']
        self.hex = spk['hex']       
        self.type = spk['type']
        if((spk['type'] != "nulldata") and (spk['type'] != "nonstandard")):
            self.addresses = spk['addresses']  
            self.req_sigs = spk['reqSigs']


def get_block_with_hash(hsh, api_code=None):    
    resource = 'block/{0}.json'.format(hsh)
    if api_code is not None:
        resource += '&api_code=' + api_code
    response = net_util.call_api(resource)
    json_response = json.loads(response)
    return json_response 
    
    
if __name__ == '__main__':
    rpc_user = "bitcoinrpc"
    rpc_password = "chomu"
    # rpc_user and rpc_password are set in the bitcoin.conf file
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))

    script_dir = os.path.dirname(__file__)
    blocks = []
    start_height = int(raw_input("Enter start height: "))
    end_height = int(raw_input("Enter end height: "))
    step = 10#int(raw_input("Enter step size: "))
    
    #integer division is being performed
    #start_height = ((start_height / step) * step)
    if((end_height % step) != 0):
        end_height = (((end_height / step) + 1) * step)
    
    init = start_height
    for i in range(start_height+step, (end_height + 1), step):
        commands = [["getblockhash", height] for height in range(init, i) ]
        block_hashes = rpc_connection.batch_(commands)
        #see for http rest batch processing support
        
        for hsh in block_hashes:
            #print hsh
            block = get_block_with_hash(hsh)
            blocks.append(block)
        
        f=open('JSONFiles/data%i.json' %i,'w')
        json.dump(blocks,f,indent=4)
        f.close()
        blocks=[]
        print i
        init = i
        #assert isinstance(block, Block)

        '''block_list = BlockList(blocks)                           
        print "Saving blocks_{}_to_{}.json".format(init, i)
        rel_path = "Blocks/blocks_{}_to_{}.json".format(init, i)
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'w') as fout:
            fout.write(jsonpickle.encode(block_list, max_depth=50000))
        blocks = []'''
              


'''
# batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
commands = [ [ "getblockhash", height] for height in range(100) ]
block_hashes = rpc_connection.batch_(commands)
blocks = rpc_connection.batch_([ [ "getblock", h ] for h in block_hashes ])
block_times = [ block["time"] for block in blocks ]
print(block_times)
'''

'''
class SimpleBlock1:
    def __init__(self, b):
        self.height = b['height']
        self.hash = b['hash']
        self.time = b['time']
        self.main_chain = b['main_chain']


class LatestBlock1:
    def __init__(self, b):
        self.hash = b['hash']
        self.time = b['time']
        self.block_index = b['block_index']
        self.height = b['height']
        self.tx_indexes = [i for i in b['txIndexes']]


class UnspentOutput1:
    def __init__(self, o):
        self.tx_hash = o['tx_hash']
        self.tx_index = o['tx_index']
        self.tx_output_n = o['tx_output_n']
        self.script = o['script']
        self.value = o['value']
        self.value_hex = o['value_hex']
        self.confirmations = o['confirmations']


class Address1:
    def __init__(self, a):
        self.hash160 = a['hash160']
        self.address = a['address']
        self.n_tx = a['n_tx']
        self.total_received = a['total_received']
        self.total_sent = a['total_sent']
        self.final_balance = a['final_balance']
        self.transactions = [Transaction(tx) for tx in a['txs']]


class Input1:
    def __init__(self, i):
        obj = i.get('prev_out')
        if obj is not None:
            # regular TX
            self.n = obj['n']
            self.value = obj['value']
            self.address = obj['addr']
            self.tx_index = obj['tx_index']
            self.type = obj['type']
            self.script = obj['script']
            self.script_sig = i['script']
            self.sequence = i['sequence']
        else:
            # coinbase TX
            self.script_sig = i['script']
            self.sequence = i['sequence']


class Block1:
    def __init__(self, b):
        self.hash = b['hash']
        self.version = b['version']
        self.prev_block = b['prev_block']
        self.merkle_root = b['merkleroot']
        self.time = b['time']
        self.bits = b['bits']
        self.fee = b['fee']
        self.nonce = b['nonce']
        self.n_tx = b['n_tx']
        self.size = b['size']
        self.block_index = b['block_index']
        self.main_chain = b['main_chain']
        self.height = b['height']
        self.received_time = b.get('received_time', b['time'])
        self.relayed_by = b.get('relayed_by')
        self.transactions = [Transaction(t) for t in b['tx']]
        for tx in self.transactions:
            tx.block_height = self.height


class InventoryData1:
    def __init__(self, i):
        self.hash = i['hash']
        self.type = i['type']
        self.initial_time = int(i['initial_time'])
        self.initial_ip = i['initial_ip']
        self.nconnected = int(i['nconnected'])
        self.relayed_count = int(i['relayed_count'])
        self.relayed_percent = int(i['relayed_percent'])




class Input1:
    def __init__(self, i):
        obj = i.get('prev_out')
        if obj is not None:
            # regular TX
            self.n = obj['n']
            self.value = obj['value']
            self.address = obj['addr']
            self.tx_index = obj['tx_index']
            self.type = obj['type']
            self.script = obj['script']
            self.script_sig = i['script']
            self.sequence = i['sequence']
        else:
            # coinbase TX
            self.script_sig = i['script']
            self.sequence = i['sequence']


class Output1:
    def __init__(self, o):
        self.n = o['n']
        self.value = o['value']
        self.address = o.get('addr')
        self.tx_index = o['tx_index']
        self.script = o['script']
        self.spent = o['spent']
        
                    
class Transaction1:
    def __init__(self, t):
        self.double_spend = t.get('double_spend', False)
        self.block_height = t.get('block_height')
        self.time = t['time']
        self.relayed_by = t['relayed_by']
        self.hash = t['hash']
        self.tx_index = t['tx_index']
        self.version = t['ver']
        self.size = t['size']
        self.inputs = [Input(i) for i in t['inputs']]
        self.outputs = [Output(o) for o in t['out']]
        
        if self.block_height is None:
            self.block_height = -1
'''                     
