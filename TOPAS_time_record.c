#include "TOPAS_time_record.h"
#include <stdlib.h>
#include <stdio.h>

#define BUFFER_SIZE 1000

/* set_history_time:
 * Puts a given time into the given history. If the record of histories
 * is smaller than what would be needed to record this history then it
 * is increased to occupy this index. If the index exceeds the internal
 * size of the array then the a new array is allocated bigger than the
 * currently being added history by BUFFER_SIZE. The original array
 * (up to size) is then copyed over. The new array is allocated using
 * calloc, so uninitilized values with be 0x0000
 */
int set_history_time(time_record* record, uint history, float time) {
    if (record == NULL) {
        fprintf(stderr, "set_history_time: passed null record\n");
        return 1;
    }
    if (history < 0) {
        fprintf(stderr, "set_history_time: negative index\n");
        return 1;
    }
    if (record->internal_size <= history) {
        // we need to make the internal array bigger and copy over
        // all of the internal data.
        // to avoid too many reallocations and therefore excessive time spent
        // moving memory over, this is to more than double in size if it has to grow
        uint bigger_size = history * history + BUFFER_SIZE;
        float* bigger_array = (float*)calloc(bigger_size, sizeof(float));
        // now copy over all of the old array's data
        for(int j = 0; j < record->size; j++) {
            bigger_array[j] = record->times[j];
        }
        free(record->times);
        record->times = bigger_array;
        record->internal_size = bigger_size;
    }
    if (record->size <= history) {
        // the array is now bigger, say how big it is
        record->size = history + 1;
    }
    record->times[history] = time;
    return 0;
}

// reads a history of index i from the given record
float read_history_time(time_record* record, uint i) {
    if (record == NULL) {
        fprintf(stderr, "read_history_time: passed null record\n");
        return -1;
    }
    if (i >= record->size) {
        fprintf(stderr, "read_history_time: passed too large index.\n");
        fprintf(stderr, "\texpected up to %i, got %i\n", record->size - 1, i);
        return -1;
    }
    if (i < 0) {
        fprintf(stderr, "read_history_time: passed negative index\n");
    }
    return record->times[i];
}

// reads a record from an external file. This is done until the end of the file,
// adding each one to the given record
int read_record_from_file(time_record* record, FILE* source) {
    if (record == NULL) {
        fprintf(stderr, "read_record_from_file: passed null record\n");
        return 1;
    }
    if (source == NULL) {
        fprintf(stderr, "read_record_from_file: invalid file given\n");
        return 1;
    }
    float timing_data;
    int worked;
    uint history = 0;
    worked = fscanf(source, "%f", &timing_data);
    while (worked != EOF) {
        record->set_history_time(record, history, timing_data);
        worked = fscanf(source, "%f", &timing_data);
        history++;
    }
    return 0;
}

int write_record_to_file(time_record* record, FILE* output) {
    if (record == NULL) {
        fprintf(stderr, "write_record_to_file: passed null record\n");
        return 1;
    }
    if (output == NULL) {
        fprintf(stderr, "write_record_to_file: invalid file given\n");
        return 1;
    }
    for (int i = 0; i < record->size; i++) {
        fprintf(output, "%lf\n", record->times[i]);

    }
    return 0;
}

void destroy_time_record(time_record* a) {
    // first free the internal array, then free the input
    if (a != NULL) {
        free(a->times);
        free(a);
    }
}


int time_record_tests() {
    // trys several things with a record to see if everything works right
    // first we create a time record
    time_record* new = time_record_creation();
    if (new == NULL) {
        fprintf(stderr, "time_record_tests: failed to create a record\n");
        return 1;
    }
    uint failures = 0;
    if (new->internal_size != 0) {
        fprintf(stderr, "time_record_tests: incorrect internal size of %i\n", new->internal_size);
        failures++;
    }
    if (new->size != 0) {
        fprintf(stderr, "time_record_tests: incorrect size of %i\n", new->size);
        failures++;
    }
    if (new->read_history_time != read_history_time) {
        fprintf(stderr, "time_record_tests: read_history_time pointer mismatch\n");
        failures++;
    }
    if (new->set_history_time != set_history_time) {
        fprintf(stderr, "time_record_tests: set_history_time pointer mismatch\n");
        failures++;
    }
    if (new->read_record_from_file != read_record_from_file) {
        fprintf(stderr, "time_record_tests: read_record_from_file pointer mismatch\n");
        failures++;
    }
    if (new->write_record_to_file != write_record_to_file) {
        fprintf(stderr, "time_record_tests: write_record_to_file pointer mismatch\n");
        failures++;
    }

    // now we try writing a history and reading it back
    float test_val = 3.2;
    new->set_history_time(new, 10, test_val);
    if (new->read_history_time(new, 11) != -1) {
        fprintf(stderr, "time_record_tests: incorrect response given for read off end of array\n");
        failures++;
    }
    if (new->read_history_time(new, 10) != test_val) {
        fprintf(stderr, "time_record_tests: incorrect return value.\n");
        fprintf(stderr, "\tgot %f, expected %f\n", new->read_history_time(new, 10), test_val);
        failures++;
    }
    if (new->internal_size < 20) {
        fprintf(stderr, "time_record_tests: too small internal_size given\n");
        failures++;
    }
    fprintf(stderr, "time_record_tests: %i failures\n", failures);

    return failures;
}


// Creates a time_record structure and returns the pointer to it.
// The function also populates the structure with the functions needed
// to navigate the struture. These are the read function, write function,
// read time of history, and write time of history functions.
time_record* time_record_creation() {
    time_record* new = (time_record*)malloc(sizeof(time_record));
    new->times = NULL;
    new->size = 0;
    new->internal_size = 0;
    new->read_history_time = read_history_time;
    new->read_record_from_file = read_record_from_file;
    new->write_record_to_file = write_record_to_file;
    new->set_history_time = set_history_time;
    return new;
}


