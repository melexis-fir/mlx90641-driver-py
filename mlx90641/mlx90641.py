import os
import ctypes


class ParamsMLX90641(ctypes.Structure):
    _fields_ = [
        ("kVdd", ctypes.c_int16),
        ("vdd25", ctypes.c_int16),
        ("KvPTAT", ctypes.c_float),
        ("KtPTAT", ctypes.c_float),
        ("vPTAT25", ctypes.c_uint16),
        ("alphaPTAT", ctypes.c_float),
        ("gainEE", ctypes.c_int16),
        ("tgc", ctypes.c_float),
        ("cpKv", ctypes.c_float),
        ("cpKta", ctypes.c_float),
        ("resolutionEE", ctypes.c_uint8),
        ("calibrationModeEE", ctypes.c_uint8),
        ("KsTa", ctypes.c_float),
        ("ksTo", ctypes.c_float * 8),
        ("ct", ctypes.c_int16 * 8),
        ("alpha", ctypes.c_uint16 * 192),
        ("alphaScale", ctypes.c_uint8),
        ("offset", ctypes.c_int16 * 2 * 192),
        ("kta", ctypes.c_int8 * 192),
        ("ktaScale", ctypes.c_uint8),
        ("kv", ctypes.c_int8 * 192),
        ("kvScale", ctypes.c_uint8),
        ("cpAlpha", ctypes.c_float),
        ("cpOffset", ctypes.c_int16),
        ("emissivityEE", ctypes.c_float),
        ("brokenPixel", ctypes.c_uint16)]


# uncovered functions in python:

# int MLX90641_SynchFrame(uint8_t slaveAddr);
# int MLX90641_TriggerMeasurement(uint8_t slaveAddr);
# int MLX90641_GetFrameData(uint8_t slaveAddr, uint16_t *frameData);
# void MLX90641_GetImage(uint16_t *frameData, const paramsMLX90641 *params, float *result);
# float MLX90641_GetEmissivity(const paramsMLX90641 *mlx90641);
# void MLX90641_BadPixelsCorrection(uint16_t pixel, float *to);
# int MLX90641_I2CRead(uint8_t slaveAddr,uint16_t startAddress, uint16_t nMemAddressRead, uint16_t *data);
# int MLX90641_I2CWrite(uint8_t slaveAddr,uint16_t writeAddress, uint16_t data);


class MLX90641:
    def __init__(self, slave_address=0x33):
        cfp = os.path.dirname(os.path.realpath(__file__))
        machine = 'windows'
        shared_lib_file = 'mlx90641_driver.dll'
        if os.environ.get('OS', '') != 'Windows_NT':
            import platform
            machine = platform.machine()
            shared_lib_file = 'libmlx90641_driver.so'

        lib_mlx90641 = ctypes.CDLL(os.path.join(cfp, 'libs', machine, shared_lib_file), mode=ctypes.RTLD_GLOBAL)

        self.slave_address = slave_address
        self.eeprom_data = (ctypes.c_uint16 * 832)()
        self.frame_data = (ctypes.c_uint16 * 834)()
        self.params = ParamsMLX90641()
        self.mlx90641_to = (ctypes.c_float * 192)()

        # Extract functions from shared libraries
        self._i2c_init = lib_mlx90641.MLX90641_I2CInit
        self._i2c_init.restype = None
        self._i2c_init.argtypes = [ctypes.c_char_p]

        self._i2c_freq_set = lib_mlx90641.MLX90641_I2CFreqSet
        self._i2c_freq_set.restype = None
        self._i2c_freq_set.argtypes = [ctypes.c_int]

        self._i2c_tear_down = lib_mlx90641.MLX90641_I2CClose
        self._i2c_tear_down.restype = None
        self._i2c_tear_down.argtypes = []

        self._dump_eeprom = lib_mlx90641.MLX90641_DumpEE
        self._dump_eeprom.restype = ctypes.c_int
        self._dump_eeprom.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]

        self._get_frame_data = lib_mlx90641.MLX90641_GetFrameData
        self._get_frame_data.restype = ctypes.c_int
        self._get_frame_data.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]

        self._extract_parameters = lib_mlx90641.MLX90641_ExtractParameters
        self._extract_parameters.restype = ctypes.c_int
        self._extract_parameters.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ParamsMLX90641)]

        self._get_vdd = lib_mlx90641.MLX90641_GetVdd
        self._get_vdd.restype = ctypes.c_float
        self._get_vdd.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ParamsMLX90641)]

        self._get_ta = lib_mlx90641.MLX90641_GetTa
        self._get_ta.restype = ctypes.c_float
        self._get_ta.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ParamsMLX90641)]

        self._calculate_to = lib_mlx90641.MLX90641_CalculateTo
        self._calculate_to.restype = None
        self._calculate_to.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ParamsMLX90641), ctypes.c_float,
                                       ctypes.c_float, ctypes.POINTER(ctypes.c_float)]

        self._set_resolution = lib_mlx90641.MLX90641_SetResolution
        self._set_resolution.restype = ctypes.c_int
        self._set_resolution.argtypes = [ctypes.c_uint8, ctypes.c_uint8]

        self._get_resolution = lib_mlx90641.MLX90641_GetCurResolution
        self._get_resolution.restype = ctypes.c_int
        self._get_resolution.argtypes = [ctypes.c_uint8]

        self._set_refresh_rate = lib_mlx90641.MLX90641_SetRefreshRate
        self._set_refresh_rate.restype = ctypes.c_int
        self._set_refresh_rate.argtypes = [ctypes.c_uint8, ctypes.c_uint8]

        self._get_refresh_rate = lib_mlx90641.MLX90641_GetRefreshRate
        self._get_refresh_rate.restype = ctypes.c_int
        self._get_refresh_rate.argtypes = [ctypes.c_uint8]

        self._get_sub_page_number = lib_mlx90641.MLX90641_GetSubPageNumber
        self._get_sub_page_number.restype = ctypes.c_int
        self._get_sub_page_number.argtypes = [ctypes.POINTER(ctypes.c_uint16)]

        # void mlx90641_register_driver(struct MLX90641DriverRegister_t *driver);
        self._register_driver = lib_mlx90641.mlx90641_register_driver
        self._register_driver.restype = None
        self._register_driver.argtypes = [ctypes.POINTER(ctypes.c_uint16)]

        # # struct MLX90641DriverRegister_t *MLX90641_get_register_evb9064x(void);
        # self._get_register_evb9064x = libmlx90641.MLX90641_get_register_evb9064x
        # self._get_register_evb9064x.restype = ctypes.POINTER(ctypes.c_uint16)
        # self._get_register_evb9064x.argtypes = []
        # self._register_driver(self._get_register_evb9064x())

        # # struct MLX90641DriverRegister_t *MLX90641_get_register_devtree(void);
        # self._get_register_devtree = libmlx90641.MLX90641_get_register_devtree
        # self._get_register_devtree.restype = ctypes.POINTER(ctypes.c_uint16)
        # self._get_register_devtree.argtypes = []
        # self._register_driver(self._get_register_devtree())

        # struct MLX90641DriverRegister_t *MLX90641_get_register_mcp2221(void);
        self._get_register_mcp2221 = lib_mlx90641.MLX90641_get_register_mcp2221
        self._get_register_mcp2221.restype = ctypes.POINTER(ctypes.c_uint16)
        self._get_register_mcp2221.argtypes = []
        self._register_driver(self._get_register_mcp2221())

    def i2c_init(self, i2c_port=None):
        if i2c_port is None:
            i2c_port = "/dev/i2c-1"
        return self._i2c_init(i2c_port.encode())

    def i2c_set_frequency(self, frequency_hz):
        return self._i2c_freq_set(frequency_hz)

    def i2c_tear_down(self):
        return self._i2c_tear_down()

    def dump_eeprom(self):
        ret = self._dump_eeprom(self.slave_address, ctypes.cast(self.eeprom_data, ctypes.POINTER(ctypes.c_uint16)))
        if ret == -1:
            raise Exception("Acknowledge issue on I2C bus; data is not valid")
        if ret == -10:
            raise Exception("double bit error; not corrected; data is not valid")

        return [int(x) for x in self.eeprom_data]

    def get_frame_data(self):
        ret = self._get_frame_data(self.slave_address, ctypes.cast(self.frame_data, ctypes.POINTER(ctypes.c_uint16)))
        if ret == -1:
            raise Exception("Acknowledge issue on I2C bus; data is not valid")
        if ret == -8:
            raise Exception("timeout")
        return [int(x) for x in self.frame_data]

    def extract_parameters(self):
        return self._extract_parameters(self.eeprom_data, ctypes.byref(self.params))

    def get_vdd(self):
        return self._get_vdd(self.frame_data, self.params)

    def get_ta(self):
        return self._get_ta(self.frame_data, self.params)

    def calculate_to(self, emissivity, tr):
        self._calculate_to(self.frame_data, self.params, emissivity, tr, self.mlx90641_to)
        return [float(x) for x in self.mlx90641_to]

    def set_resolution(self, resolution):
        return self._set_resolution(self.slave_address, resolution)

    def get_resolution(self):
        return self._get_resolution(self.slave_address)

    def set_refresh_rate(self, refresh_rate):
        sa = ctypes.c_uint8(self.slave_address)
        rr = ctypes.c_uint8(refresh_rate)
        return self._set_refresh_rate(sa, rr)

    def get_refresh_rate(self):
        return self._get_refresh_rate(self.slave_address)

    def get_sub_page_number(self):
        return self._get_sub_page_number(self.frame_data)
