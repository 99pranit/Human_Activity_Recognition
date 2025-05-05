#include "predictor.h"
#include "model_data.h"
#include <cstdio>
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/c/common.h"
#include "esp_heap_caps.h"

#define INPUT_SIZE        16
#define OUTPUT_SIZE       7
#define TENSOR_ARENA_SIZE (40 * 1024)

static tflite::MicroInterpreter* interpreter = nullptr;
static TfLiteTensor* input = nullptr;
static TfLiteTensor* output = nullptr;
static uint8_t* tensor_arena = nullptr;

int predict(const float* input_data) {
    static bool initialized = false;
    if (!initialized) {
        // Allocate arena in PSRAM
        tensor_arena = reinterpret_cast<uint8_t*>(
            heap_caps_malloc(TENSOR_ARENA_SIZE, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT));
        if (tensor_arena == nullptr) {
            std::printf("Failed to allocate tensor arena in PSRAM\n");
            return -1;
        }

        // Load the model
        const tflite::Model* model = tflite::GetModel(activity_model_tflite);
        if (model == nullptr || model->version() != TFLITE_SCHEMA_VERSION) {
            std::printf("Model load failed\n");
            return -1;
        }

        // Setup resolver with required ops
        static tflite::MicroMutableOpResolver<5> resolver;
        resolver.AddSoftmax();
        resolver.AddFullyConnected();
        resolver.AddReshape();
        resolver.AddQuantize();
        resolver.AddDequantize();

        // Build interpreter
        static tflite::MicroInterpreter static_interpreter(
            model, resolver, tensor_arena, TENSOR_ARENA_SIZE
        );
        interpreter = &static_interpreter;

        // Allocate tensors
        if (interpreter->AllocateTensors() != kTfLiteOk) {
            std::printf("AllocateTensors failed\n");
            return -1;
        }

        // Obtain I/O tensors
        input = interpreter->input(0);
        output = interpreter->output(0);
        initialized = true;
    }

    // Fill input tensor
    for (int i = 0; i < INPUT_SIZE; ++i) {
        input->data.f[i] = input_data[i];
    }

    // Run inference
    if (interpreter->Invoke() != kTfLiteOk) {
        std::printf("Inference failed\n");
        return -1;
    }

    // Argmax over output
    int best_index = 0;
    float best_score = output->data.f[0];
    for (int i = 1; i < OUTPUT_SIZE; ++i) {
        float v = output->data.f[i];
        if (v > best_score) {
            best_score = v;
            best_index = i;
        }
    }
    return best_index;
}
