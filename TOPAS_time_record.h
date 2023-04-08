#ifndef TOPAS_time_record_h
#define TOPAS_time_record_h
#include <stdio.h>

typedef unsigned int uint;
typedef struct time_record_ time_record;

struct time_record_ {
    float* times;
    uint size;
    uint internal_size;
    int (*set_history_time)(time_record*, uint, float);
    float (*read_history_time)(time_record*, uint);
    int (*read_record_from_file)(time_record*, FILE*);
    int (*write_record_to_file)(time_record*, FILE*);
};

// makes a new time_record
time_record* time_record_creation();

// frees a time_record
void destroy_time_record(time_record*);

int time_record_tests();


#endif