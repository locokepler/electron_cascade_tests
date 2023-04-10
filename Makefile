CC=gcc
BASEFLAGS= -Wall -lm
CFLAGS= $(BASEFLAGS) -O2
CDBGFLAGS= $(BASEFLAGS) -g
CPRFFLAGS= $(BASEFLAGS) -pg
DEPS=TOPAS_time_record.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# secondaries: TOPAS_time_record.c secondary_electrons_with_time.c
# 	$(CC) -o secondaries $^ $(CFLAGS)

# debug_secondaries: TOPAS_time_record.c secondary_electrons_with_time.c
# 	$(CC) -o debug_secondaries $^ $(CDBGFLAGS)

secondaries: TOPAS_time_record.c in_place_secondary_electrons_with_time.c
	$(CC) -o secondaries $^ $(CFLAGS)

debug_secondaries: TOPAS_time_record.c in_place_secondary_electrons_with_time.c
	$(CC) -o debug_secondaries $^ $(CDBGFLAGS)