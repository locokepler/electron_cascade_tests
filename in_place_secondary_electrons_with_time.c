#include "TOPAS_time_record.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI 3.141592653589
#define HIST_BUFFER 100
#define MIN_ENG 0.0001
#define MAX_ELECTRONS 5
#define UNCERT_REP 12


typedef struct safestring_ {
    char* string;
    uint len;
} safestring;


typedef struct interaction_ {
    float position[3];
    float direction[2];
    float energy_MeV;
    int weight;
    int type;
    int cos_flag;
    int first_scored_flag;
    float tof;
    int run_id;
    int track_id;
} interaction;

typedef struct phasespace_ {
    interaction** data;
    uint size;
    uint internal_size;
    uint histories;
    uint histories_in_phasespace;
    uint scored_particles;
} phasespace;

// reads the .phsp file of a phase space scorer
interaction* read_pshp_line(FILE* input) {
    interaction* new = calloc(1, sizeof(interaction));
    int worked;

    worked = fscanf(input, "%f %f %f ", &(new->position[0]), &(new->position[1]), &(new->position[2]));
    worked = fscanf(input, "%f %f ", &(new->direction[0]), &(new->direction[1]));
    worked = fscanf(input, "%f ", &(new->energy_MeV));
    worked = fscanf(input, "%i %i %i %i ", &(new->weight), &(new->type), &(new->cos_flag), &(new->first_scored_flag));
    worked = fscanf(input, "%f %i %i", &(new->tof), &(new->run_id), &(new->track_id));

    if (worked == EOF) {
        free(new);
        return NULL;
    }
    return new;
}

void print_phsp_line(FILE* output, interaction* data) {
    if (output == NULL || data == NULL) {
        return;
    }
    fprintf(output, "%12f %12f %12f ", data->position[0], data->position[1], data->position[2]);
    fprintf(output, "%12f %12f %12f ", data->direction[0], data->direction[1], data->energy_MeV);
    fprintf(output, "%12i %12i %2i ", data->weight, data->type, data->cos_flag);
    fprintf(output, "%2i %12f %12i %12i\n", data->first_scored_flag, data->tof, data->run_id, data->track_id);
}

phasespace* create_phasespace() {
    phasespace* new = (phasespace*)malloc(sizeof(phasespace));
    new->data = NULL;
    new->size = 0;
    new->internal_size = 0;
    new->histories = 0;
    new->histories_in_phasespace = 0;
    return new;
}

void free_phasespace(phasespace* a) {
    for (uint i = 0; i < a->size; i++) {
        free(a->data[i]);
    }
    free(a->data);
    free(a);
}

void set_phasespace_index(phasespace* a, uint i, interaction* data) {
    if (a == NULL) {
        return;
    }
    if (i >= a->internal_size) {
        // need to make the internal array bigger
        uint new_size = a->internal_size * a->internal_size + HIST_BUFFER;
        if (new_size - a->internal_size > 800000000) {
            new_size = a->internal_size + 800000000;
        }
        interaction** new = (interaction**)calloc(new_size, sizeof(interaction*));
        for (int j = 0; j < a->size; j++) {
            // copy the old array over to the new one
            new[j] = a->data[j];
        }
        free(a->data);
        a->data = new;
        a->internal_size = new_size;
    }
    if (i >= a->size) {
        a->size = i + 1;
    }
    // if there is already data there we need to free it to be replaced
    if (a->data[i] != NULL) {
        free(a->data[i]);
    }
    a->data[i] = data;
}

// forces a phasespace to have a given internal size. If the current internal_size is
// larger than the given internal size then it will leave the size alone. Otherwise
// it will expand the phase space to hold all of that
void grow_phasespace_internal_size(phasespace* a, uint i) {
    if (a == NULL) {
        return;
    }
    if (i <= a->internal_size) {
        return;
    }
    uint new_size = i;
    interaction** new = (interaction**)calloc(new_size, sizeof(interaction*));
    for (int j = 0; j < a->size; j++) {
        new[j] = a->data[j];
    }
    free(a->data);
    a->data = new;
    a->internal_size = new_size;
}

// loads a phasespace file into memory with corrected timings from the given file
phasespace* load_phasespace(FILE* input, time_record* timings) {
    if (input == NULL) {
        fprintf(stderr, "load_phasespace: input is null\n");
        return NULL;
    }
    if ((timings == NULL) || (timings->times == NULL)) {
        fprintf(stderr, "load_phasespace: timings are null, must be first run, if not there is a problem\n");
        // if this is the case we will take external times to all be zero
    }
    uint hist_num = 0;
    int has_data = 1;
    interaction* line = read_pshp_line(input);
    uint line_num = 0;
    if (line == NULL) {
        has_data = 0;
    }
    // int hist_in_phasespace = 0;
    int scored_particles = 0;
    phasespace* history = create_phasespace();
    while (has_data) {
        if (timings != NULL) {
            float current_time = timings->read_history_time(timings, hist_num);
            line->tof += current_time;
        }
        if (line->weight == 1) {
            scored_particles++;
        }
        set_phasespace_index(history, line_num, line);

        line = read_pshp_line(input);
        if (line == NULL) {
            has_data = 0;
        } else {
            hist_num += line->first_scored_flag;
            line_num ++;
        }

    }
    history->histories = hist_num;
    history->histories_in_phasespace = hist_num;
    history->scored_particles = scored_particles;

    return history;
}

// takes a phasespace file and prints the contents to the given output. A
// .header file for this data output must be created seprately.
void print_phasespace_phsp(FILE* output, phasespace* a) {
    if (output == NULL) {
        fprintf(stderr, "print_phasespace_phsp: cannot print to null file\n");
        return;
    }
    if (a == NULL) {
        fprintf(stderr, "print_phasespace_phsp: cannot print null phasespace\n");
    }
    for (int i = 0; i < a->size; i++) {
        // now print each line
        print_phsp_line(output, a->data[i]);
    }
}

void print_phasespace_header(FILE* output, phasespace* a) {
    if (output == NULL) {
        fprintf(stderr, "print_phasespace_header: cannot print to null file\n");
        return;
    }
    if (a == NULL) {
        fprintf(stderr, "print_phasespace_header: cannot print null phasespace\n");
    }
    // print the header. It has a very specfic format
    fprintf(output, "TOPAS ASCII Phase Space\n");
    fprintf(output, "\n");
    fprintf(output, "Number of Original Histories: %i\n", a->histories);
    fprintf(output, "Number of Original Histories that Reached Phase Space: %i\n", a->histories_in_phasespace);
    fprintf(output, "Number of Scored Particles: %i\n", a->scored_particles);
    fprintf(output, "Columns of data are as follows:\n");
    fprintf(output, " 1: Position X [cm]\n");
    fprintf(output, " 2: Position Y [cm]\n");
    fprintf(output, " 3: Position Z [cm]\n");
    fprintf(output, " 4: Direction Cosine X\n");
    fprintf(output, " 5: Direction Cosine Y\n");
    fprintf(output, " 6: Energy [MeV]\n");
    fprintf(output, " 7: Weight\n");
    fprintf(output, " 8: Particle Type (in PDG Format)\n");
    fprintf(output, " 9: Flag to tell if Third Direction Cosine is Negative (1 means true)\n");
    fprintf(output, "10: Flag to tell if this is the First Scored Particle from this History (1 means true)\n");
    fprintf(output, "11: Time of Flight [ns]\n");
    fprintf(output, "12: Run ID\n");
    fprintf(output, "13: Track ID\n");
}

void remove_empty_histories(phasespace* a) {
    if (a == NULL) {
        return;
    }
    // work our way through the phasespace file removing all entries of weight < 0
    // done in place in the array
    int offset = 0;
    uint post_size = 0;
    uint post_histories = 0;
    for (int i = 0; i < a->size; i++) {
        if (a->data[i]->weight < 0) {
            // remove this entry, subtract 1 from the offset
            free(a->data[i]);
            a->data[i] = NULL;
            offset++;
        } else {
            a->data[i - offset] = a->data[i];
            post_size++;
            post_histories += a->data[i]->first_scored_flag;
        }
    }
    a->size = post_size;
    a->histories = post_histories;
    a->histories_in_phasespace = post_histories;
    a->scored_particles = post_size;
}



// makes an array of secondary electons from the initial one.
// does not handle the time of these, although it does handle the fact that the first
// one must have a new history flag and the rest cannot
interaction* generate_secondary_electrons(interaction* a, uint* produced) {
    if ((a == NULL) || (produced == NULL)) {
        return NULL;
    }
    int test_a = (a->type == 11);
    int test_b = (a->energy_MeV > MIN_ENG);
    if (test_a && test_b) {
        
        int max_number_of_electrons = MAX_ELECTRONS;
        interaction* output = (interaction*)calloc(MAX_ELECTRONS, sizeof(interaction));
        // lets make a linear interpolation to E_m, the energy of  peak secondary emission
        float E_m_MeV = 5e-4;
        int number_of_electrons = (int)roundf((float)max_number_of_electrons * (a->energy_MeV / E_m_MeV));
        if (number_of_electrons > max_number_of_electrons) {
            number_of_electrons = max_number_of_electrons;
        }
        produced[0] = number_of_electrons;

        for (int i = 0; i < number_of_electrons; i++) {

            output[i] = a[0]; // copy the electron we are making secondaries from into
            // the output electron location

            // if this is the first of the new set we are adding, then it needs to be a
            // new history and have the time recorded
            if (i == 0) {
                output[i].first_scored_flag = 1;
            } else {
                output[i].first_scored_flag = 0;
            }

            // set the new electron energy here
            double eng_var = 0.0;
            for (int k = 0; k < UNCERT_REP; k++) {
                eng_var += drand48();
            }
            eng_var -= ((float)(UNCERT_REP) * 0.5);
            eng_var *= 2;
            eng_var += 10;
            if (eng_var < 4) {
                eng_var = 4;
            }
            eng_var = eng_var / 1000000;
            output[i].energy_MeV = eng_var;

            // now we give each one a direction
            double dist_theta = (2 * acos((2.0 * drand48()) - 1.0)) - PI;
            double dist_phi = 2 * PI * drand48();
            double dist_x = cos(dist_phi) * sin(dist_theta);
            double dist_y = sin(dist_phi) * sin(dist_theta);
            double dist_z = cos(dist_theta);

            output[i].direction[0] = dist_x;
            output[i].direction[1] = dist_y;
            if (dist_z >= 0) {
                output[i].cos_flag = 0;
            } else {
                output[i].cos_flag = 1;
            }
        }
        return output;
    } else {
        return NULL;
    }
}

void append_backplane_file(FILE* in_backplane, FILE* out_backplane, time_record* hist_times) {
    if ((in_backplane == NULL) || (out_backplane == NULL)) {
        // we do not have a backplane input or output
        fprintf(stderr, "append_backplane_file: missing input or output!\n");
        return;
    }
    int use_times = 1;
    if (hist_times == NULL) {
        // this is our first read in, all TOFs are correct
        use_times = 0;
    }
    int current_hist = -1;
    interaction* current_interaction = read_pshp_line(in_backplane);

    // print the interactions to the backplane file, (assuming they are not empty)
    while (current_interaction != NULL) {
        // check if it is an empty history
        current_hist += current_interaction->first_scored_flag;
        if (current_interaction->weight > 0) {
            // non-empty history
            // fix tof if needed
            if (use_times) {
                current_interaction->tof += hist_times->read_history_time(hist_times, current_hist);
            }
            print_phsp_line(out_backplane, current_interaction);
        }

        free(current_interaction);
        current_interaction = read_pshp_line(in_backplane);
    }
}

time_record* low_memory_generate_secondaries(FILE* input, FILE* output_phsp, FILE* output_header, time_record* hist_times) {
    if ((input == NULL) || (output_phsp == NULL) || (output_header == NULL)) {
        fprintf(stderr, "low_memory_generate_secondaries: needed input NULL\n");
        return NULL;
    }
    int use_times = 0;
    if (hist_times != NULL) {
        use_times = 1;
    }
    // set up phase space record for the making of the header file
    phasespace phase_space_data;
    phase_space_data.data = NULL;
    phase_space_data.histories = 0;
    phase_space_data.histories_in_phasespace = 0;
    phase_space_data.scored_particles = 0;
    phase_space_data.internal_size = 0;
    phase_space_data.size = 0;
    
    uint iteration_count = 0;

    int current_load_hist = -1;
    time_record* time_out = time_record_creation();
    uint output_hist_num = 0;
    interaction* current_interaction = read_pshp_line(input);

    // does the following loop:
    //  record if it is a new history
    //  remove if it is empty, and skip back to top
    //  add input time to TOF giving correct time
    //  generate the new secondary electrons from this one,
    //  record the times in the output time record
    //  record the history and particles in the output phasespace
    //  print the new electrons to the output phsp
    //  read in a phase space,

    while (current_interaction != NULL) {
        if ((iteration_count % 1000000) == 0) {
            printf("Secondaries iteration count: %i\n", iteration_count);
        }
        current_load_hist += current_interaction->first_scored_flag;
        // skip if it is an empty history
        if (current_interaction->weight > 0) {
            // add input time to TOF
            if (use_times) {
                current_interaction->tof += hist_times->read_history_time(hist_times, current_load_hist);
            }

            // time to generate the secondary electrons
            uint count = 0;
            interaction* secondaries = generate_secondary_electrons(current_interaction, &count);
            // if secondaries did not make any then it returns NULL
            if (secondaries != NULL) {
                // add count to the scored particles, add one to the histories, record time record
                phase_space_data.scored_particles += count; // count more scored particles
                phase_space_data.histories++; // one more history
                phase_space_data.histories_in_phasespace++; // ibid
                // record the time
                time_out->set_history_time(time_out, output_hist_num, current_interaction->tof);
                output_hist_num++;
                // now print the new particles
                for (int i = 0; i < count; i++) {
                    print_phsp_line(output_phsp, &(secondaries[i]));
                }
                free(secondaries);
            }
            // if we did not have any new ones, do not record a time out, do not output the history
        }
        free(current_interaction);
        current_interaction = read_pshp_line(input);
        iteration_count++;
    }

    // loop now done, print out the header for the above phsp file
    print_phasespace_header(output_header, &phase_space_data);

    // return the time record of the created particles
    return time_out;
}



int main(int argc, char const *argv[]) {

    // if (time_record_tests()) {
    //     return 1;
    // }

    FILE* input_phasespace;
    FILE* input_timings;

    FILE* backplane_input_file;
    FILE* backplane_output_file;

    FILE* output_phasespace_tuple_file;
    FILE* output_phasespace_header_file;

    if (argc == 6) {
        safestring input_detector_phasespace_tuple_name;
        input_detector_phasespace_tuple_name.len = strlen(argv[1]) + 10;
        input_detector_phasespace_tuple_name.string = (char*)calloc(strlen(argv[1]) + 10, sizeof(char));

        // safestring input_detector_phasespace_header_name;
        // input_detector_phasespace_header_name.len = strlen(argv[1]) + 10;
        // input_detector_phasespace_header_name.string = (char*)calloc(strlen(argv[1]) + 10, sizeof(char));

        strncpy(input_detector_phasespace_tuple_name.string, argv[1], input_detector_phasespace_tuple_name.len);
        // strncpy(input_detector_phasespace_header_name.string, argv[1], input_detector_phasespace_header_name.len);

        strncat(input_detector_phasespace_tuple_name.string, ".phsp", input_detector_phasespace_tuple_name.len);
        // strncat(input_detector_phasespace_header_name.string, ".header", input_detector_phasespace_header_name.len);

        safestring output_detector_phasespace_tuple_name;
        output_detector_phasespace_tuple_name.len = strlen(argv[3]) + 10;
        output_detector_phasespace_tuple_name.string = (char*)calloc(strlen(argv[3]) + 10, sizeof(char));

        safestring output_detector_phasespace_header_name;
        output_detector_phasespace_header_name.len = strlen(argv[3]) + 10;
        output_detector_phasespace_header_name.string = (char*)calloc(strlen(argv[3]) + 10, sizeof(char));

        strncpy(output_detector_phasespace_tuple_name.string, argv[3], output_detector_phasespace_tuple_name.len);
        strncpy(output_detector_phasespace_header_name.string, argv[3], output_detector_phasespace_header_name.len);

        strncat(output_detector_phasespace_tuple_name.string, ".phsp", output_detector_phasespace_tuple_name.len);
        strncat(output_detector_phasespace_header_name.string, ".header", output_detector_phasespace_header_name.len);


        input_phasespace = fopen(input_detector_phasespace_tuple_name.string, "r");
        input_timings = fopen(argv[2], "r");

        output_phasespace_tuple_file = fopen(output_detector_phasespace_tuple_name.string, "w");
        output_phasespace_header_file = fopen(output_detector_phasespace_header_name.string, "w");

        safestring backplane_input_tuple_name;
        backplane_input_tuple_name.len = strlen(argv[4]);
        backplane_input_tuple_name.string = (char*)calloc(strlen(argv[4]), sizeof(char));

        safestring backplane_output_tuple_name;
        backplane_output_tuple_name.len = strlen(argv[5]);
        backplane_output_tuple_name.string = (char*)calloc(strlen(argv[5]), sizeof(char));

        strncpy(backplane_input_tuple_name.string, argv[4], backplane_input_tuple_name.len);
        strncpy(backplane_output_tuple_name.string, argv[5], backplane_output_tuple_name.len);

        backplane_input_file = fopen(backplane_input_tuple_name.string, "r");
        backplane_output_file = fopen(backplane_output_tuple_name.string, "a");

    } else {
        fprintf(stderr, "Incorrect number of arguments, expected 5:\n");
        fprintf(stderr, "\t1: input detector phasespace\n");
        fprintf(stderr, "\t2: input detector timings (output of timings will also be written to here)\n");
        fprintf(stderr, "\t3: output detector phasespace\n");
        fprintf(stderr, "\t4: input backplane\n");
        fprintf(stderr, "\t5: output backplane\n");
        return 1;
    }

    time_record* input_times = NULL;
    if (input_timings != NULL) {
        // only try to load times if there is a file, otherwise we pass 
        input_times = time_record_creation();
        input_times->read_record_from_file(input_times, input_timings);
        fclose(input_timings);
    }
    printf("Finished loading of timings\n");

    // handle the backplane information, if the backplane exists
    if (backplane_input_file != NULL) {
        append_backplane_file(backplane_input_file, backplane_output_file, input_times);

        fclose(backplane_input_file);
        fclose(backplane_output_file);
    }
    printf("Finished loading and saving of backplane file\n");

    time_record* result_times = low_memory_generate_secondaries(input_phasespace, output_phasespace_tuple_file, output_phasespace_header_file, input_times);

    FILE* time_output = fopen(argv[2], "w");
    // open the timings file again, this time for writing
    result_times->write_record_to_file(result_times, time_output);
    fclose(time_output);
    // close the output timings
    printf("wrote %i times out!\n", result_times->size);
    destroy_time_record(input_times);
    destroy_time_record(result_times);
    // clean up the timing handling

    

    return 0;
}
