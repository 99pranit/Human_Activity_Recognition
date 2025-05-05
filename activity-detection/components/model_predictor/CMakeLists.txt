idf_component_register(SRCS "predictor.cc" "model_data.cc"
                    INCLUDE_DIRS "."
                    REQUIRES espressif__esp-tflite-micro esp-tflite-micro
                    )
