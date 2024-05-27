CC = gcc
CFLAGS = -c
OBJS = main.o file.o msg.o des.o binaryUtil.o
TARGET = des

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET)
	del /Q $(OBJS)

binaryUtil.o: binaryUtil.c binaryUtil.h
	$(CC) $(CFLAGS) binaryUtil.c

des.o: des.c des.h msg.h
	$(CC) $(CFLAGS) des.c

msg.o: msg.c msg.h des.h binaryUtil.h
	$(CC) $(CFLAGS) msg.c

file.o: file.c file.h
	$(CC) $(CFLAGS) file.c

main.o: main.c des.h msg.h file.h
	$(CC) $(CFLAGS) main.c
