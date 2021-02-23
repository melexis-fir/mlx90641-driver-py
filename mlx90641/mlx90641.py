import sys
import os
import ctypes
import pathlib


class paramsMLX90641(ctypes.Structure):
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
        ("ksTo", ctypes.c_float*8),
        ("ct", ctypes.c_int16*8),
        ("alpha", ctypes.c_uint16*192),    
        ("alphaScale", ctypes.c_uint8),
        ("offset", ctypes.c_int16*2*192),    
        ("kta", ctypes.c_int8*192),
        ("ktaScale", ctypes.c_uint8),    
        ("kv", ctypes.c_int8*192),
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


class mlx90641():
    def __init__(self, slaveAddr = 0x33):
        ## Read shared libraries
        import os
        cfp = os.path.dirname(os.path.realpath(__file__))
        machine = 'windows'
        shared_lib_file = 'mlx90641_driver.dll'
        if os.environ.get('OS','') != 'Windows_NT':
            import platform
            machine = platform.machine()
            shared_lib_file = 'libmlx90641_driver.so'

        libmlx90641 = ctypes.CDLL(os.path.join(cfp, 'libs', machine, shared_lib_file), mode=ctypes.RTLD_GLOBAL)

        self.slaveAddr = slaveAddr
        self.eepromdata = (ctypes.c_uint16*832)()
        self.frameData = (ctypes.c_uint16*834)()
        self.params = paramsMLX90641()
        self.mlx90641To = (ctypes.c_float * 192)()

        ## Extract functions from shared libraries              
        self._I2CInit = libmlx90641.MLX90641_I2CInit
        self._I2CInit.restype = None
        self._I2CInit.argtypes = [ctypes.c_char_p]

        self._I2CFreqSet = libmlx90641.MLX90641_I2CFreqSet
        self._I2CFreqSet.restype = None
        self._I2CFreqSet.argtypes = [ctypes.c_int]

        self._dumpEE = libmlx90641.MLX90641_DumpEE
        self._dumpEE.restype = ctypes.c_int
        self._dumpEE.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]
      
        self._getFrameData = libmlx90641.MLX90641_GetFrameData
        self._getFrameData.restype = ctypes.c_int
        self._getFrameData.argtypes = [ctypes.c_uint8, ctypes.POINTER(ctypes.c_uint16)]
        
        self._extractParameters = libmlx90641.MLX90641_ExtractParameters
        self._extractParameters.restype = ctypes.c_int
        self._extractParameters.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self._getVdd = libmlx90641.MLX90641_GetVdd
        self._getVdd.restype = ctypes.c_float
        self._getVdd.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self._getTa = libmlx90641.MLX90641_GetTa
        self._getTa.restype = ctypes.c_float
        self._getTa.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641)]
        
        self._calculateTo = libmlx90641.MLX90641_CalculateTo
        self._calculateTo.restype = None
        self._calculateTo.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(paramsMLX90641), ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
        
        self._setResolution = libmlx90641.MLX90641_SetResolution
        self._setResolution.restype = ctypes.c_int
        self._setResolution.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
        
        self._getResolution = libmlx90641.MLX90641_GetCurResolution
        self._getResolution.restype = ctypes.c_int
        self._getResolution.argtypes = [ctypes.c_uint8]
        
        self._setRefreshRate = libmlx90641.MLX90641_SetRefreshRate
        self._setRefreshRate.restype = ctypes.c_int
        self._setRefreshRate.argtypes = [ctypes.c_uint8, ctypes.c_uint8]
        
        self._getRefreshRate = libmlx90641.MLX90641_GetRefreshRate
        self._getRefreshRate.restype = ctypes.c_int
        self._getRefreshRate.argtypes = [ctypes.c_uint8]
        
        self._getSubPageNumber = libmlx90641.MLX90641_GetSubPageNumber
        self._getSubPageNumber.restype = ctypes.c_int
        self._getSubPageNumber.argtypes = [ctypes.POINTER(ctypes.c_uint16)]

            # void mlx90641_register_driver(struct MLX90641DriverRegister_t *driver);
        self._register_driver = libmlx90641.mlx90641_register_driver
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
        self._get_register_mcp2221 = libmlx90641.MLX90641_get_register_mcp2221
        self._get_register_mcp2221.restype = ctypes.POINTER(ctypes.c_uint16)
        self._get_register_mcp2221.argtypes = []
        self._register_driver(self._get_register_mcp2221())


    def i2c_init(self, i2cPort=None):
        if i2cPort is None:
            i2cPort = "/dev/i2c-1"
        return self._I2CInit(i2cPort.encode())
        
    def i2c_set_frequency(self, frequency_hz):
        return self._I2CFreqSet(freq)
        
    def i2c_close(self):
        return self._I2CCloseMlx90641()
    
    def dump_eeprom(self):
        ret = self._dumpEE(self.slaveAddr, ctypes.cast(self.eepromdata, ctypes.POINTER(ctypes.c_uint16)))
        if ret == -1:
            raise Exception("Acknowledge issue on I2C bus; data is not valid")
        if ret == -10:
            raise Exception("double bit error; not corrected; data is not valid")

        return [int(x) for x in self.eepromdata]
    
    def get_frame_data(self):
        ret = self._getFrameData(self.slaveAddr, ctypes.cast(self.frameData, ctypes.POINTER(ctypes.c_uint16)))
        if ret == -1:
            raise Exception("Acknowledge issue on I2C bus; data is not valid")
        if ret == -8:
            raise Exception("timeout")
        return [int(x) for x in self.frameData]
    
    def extract_parameters(self):
        return self._extractParameters(self.eepromdata, ctypes.byref(self.params))
    
    def get_vdd(self):
        return self._getVdd(self.frameData, self.params)
    
    def get_TA(self):
        return self._getTa(self.frameData, self.params)
    
    def calculate_TO(self, emissivity, tr):
        self._calculateTo(self.frameData, self.params, emissivity, tr, self.mlx90641To)
        return [float(x) for x in self.mlx90641To]

    def set_resolution(self, resolution):
        return  self._setResolution(self.slaveAddr, resolution)

    def get_resolution(self):
        return self._getResolution(self.slaveAddr)

    def set_refresh_rate(self, refresh_rate):
        sa = ctypes.c_uint8(self.slaveAddr)
        rr = ctypes.c_uint8(refresh_rate)
        return  self._setRefreshRate(sa, rr)

    def get_refresh_rate(self):
        return self._getRefreshRate(self.slaveAddr)
    
    def get_sub_page_number(self):
        return self._getSubPageNumber(self.frameData)
