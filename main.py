from RestrictedPython.Guards import safe_builtins,full_write_guard,guarded_iter_unpack_sequence
from asyncio import run,wait_for,TimeoutError,get_running_loop
from RestrictedPython.Eval import default_guarded_getiter
from RestrictedPython import compile_restricted_exec
from concurrent.futures import ThreadPoolExecutor
from RestrictedMessage import RestrictedMessage

class MakeshiftClass:
	def __init__(self,**kwargs) -> None:
		for k,v in kwargs.items():
			setattr(self,k,v)

# should not be touched for equivalent functionality
safe_builtins.update({
	'__metaclass__': type,
	'__name__': __name__,
	'_getiter_': default_guarded_getiter,
	'_iter_unpack_sequence_': guarded_iter_unpack_sequence,
	'_write_': full_write_guard,
	'math': __import__('math'),
	'random': __import__('random'),
	'collections': __import__('collections'),
	're': __import__('re'),
	'datetime': __import__('datetime')})

async def safe_exec(script:str,local_variables=None) -> dict:
	bytecode = compile_restricted_exec(script)
	if bytecode.errors:
		raise ValueError(bytecode.errors)
	variables = local_variables or {}
	await get_running_loop().run_in_executor(ThreadPoolExecutor(1),exec,bytecode.code,{'__builtins__': safe_builtins},variables)
	return variables

async def run_script(script:str) -> dict:
	try: output = await wait_for(safe_exec(script,{'message':RestrictedMessage()}),5)
	except TimeoutError: return
	return output

async def main():
	with open('script.py','r') as f: script = f.read().split('# ---------------------------------------------------------------------')[1]
	if len(script) > 4000: print(f'WARNING: script is {len(output)} characters long, which is over the 4000 character limit')
	output = await run_script(script)
	response = output.get('response','')
	response = '' if response is None else response
	if len(response) > 512: print(f'WARNING: response is {len(response)} characters long, which is over the 512 character limit')
	print(f'discord message response:\n{response}' if response else 'no response')

run(main())