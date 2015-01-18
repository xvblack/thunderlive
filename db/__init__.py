from sqlalchemy import create_engine


__all__ = ['user', 'token']

engine = None
def init_engine(e):
	global engine
	engine = e

def use_url(url):
	init_engine(create_engine(url, convert_unicode=True))
