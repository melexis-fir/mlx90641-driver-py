from .mlx90641 import MLX90641

__import__('pkg_resources').declare_namespace(__name__)


__version__ = '1.1.3'


# try to pre-load our 3 default I2C low level implementations!

try:
	import mlx90641_evb9064x
except Exception as e:
	pass

try:
	import mlx90641_mcp2221
except Exception as e:
	pass

try:
	import mlx90641_devicetree
except Exception as e:
	pass

