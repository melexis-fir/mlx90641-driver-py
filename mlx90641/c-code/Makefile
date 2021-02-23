.PHONY: clean all

ifeq ($(OS),Windows_NT)
    detected_OS := Windows
else
    detected_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif


DEP_LIBS:=-lmcp2221_hidapi_static
DEP_LIBS+=-lm
DEP_LIB_PATH:=
SHARED_LIB_NAME:=mlx90641_driver
STATIC_LIB_NAME:=mlx90641_driver_static

STATIC_LIB_FILE:=lib$(STATIC_LIB_NAME).a
SHARED_LIB_FILE:=lib$(SHARED_LIB_NAME).so

ifeq ($(detected_OS),Windows)
DEP_LIB_PATH:=-L.
SHARED_LIB_FILE:=$(SHARED_LIB_NAME).dll
MACHINE:=windows
DEP_LIBS+=-lhidapi
else
MACHINE:=$(shell uname -m)
DEP_LIBS+=-ludev
DEP_LIBS+=-lusb-1.0
DEP_LIBS+=-lhidapi-hidraw
endif

CFLAGS:=-Wall -Wextra -Wstrict-prototypes -Wunused-result -O3 -std=c99 -fmessage-length=0 -fPIC -I../libs -Iinc


all: $(SHARED_LIB_FILE) $(STATIC_LIB_FILE)

clean:
	rm -f main *.o
	rm -f src/*.o
	rm -f $(SHARED_LIB_FILE) $(STATIC_LIB_FILE)

main.o: main.c
	gcc -c -o $@ $(CFLAGS) $^

src/i2c.o: src/i2c.c
	gcc -c -o $@ $(CFLAGS) $^

src/MLX90641_I2C_Driver_devtree.o: src/MLX90641_I2C_Driver_devtree.c
	gcc -c -o $@ $(CFLAGS) $^

src/MLX90641_I2C_Driver_mcp2221.o: src/MLX90641_I2C_Driver_mcp2221.c
	gcc -c -o $@ $(CFLAGS) $^

# src/MLX90641_I2C_Driver_evb9064x.o: src/MLX90641_I2C_Driver_evb9064x.c
# 	gcc -c -o $@ $(CFLAGS) $^

src/MLX90641_API.o: src/MLX90641_API.c
	gcc -c -o $@ $(CFLAGS) $^

src/mlx90641_driver_register.o: src/mlx90641_driver_register.c
	gcc -c -o $@ $(CFLAGS) $^


main: main.o src/MLX90641_I2C_Driver_mcp2221.o src/MLX90641_API.o src/mlx90641_driver_register.o src/MLX90641_I2C_Driver_devtree.o src/i2c.o
	gcc -o $@ $^ -lm -Wl,-rpath=../libs/$(MACHINE) -L../libs/$(MACHINE) $(DEP_LIBS)


$(SHARED_LIB_FILE): src/MLX90641_API.o src/mlx90641_driver_register.o src/MLX90641_I2C_Driver_mcp2221.o src/MLX90641_I2C_Driver_devtree.o src/i2c.o
	gcc -shared -o $@ $^ -L../libs/$(MACHINE) $(DEP_LIBS) -Wl,-rpath=../libs/$(MACHINE)
	@mkdir -p ../libs/$(MACHINE)
	@cp -fv $@ ../libs/$(MACHINE)

$(STATIC_LIB_FILE): src/MLX90641_API.o src/mlx90641_driver_register.o src/MLX90641_I2C_Driver_mcp2221.o src/MLX90641_I2C_Driver_devtree.o src/i2c.o
	ar rcu $@ $<
	@mkdir -p ../libs/$(MACHINE)
	@cp -fv $@ ../libs/$(MACHINE)
