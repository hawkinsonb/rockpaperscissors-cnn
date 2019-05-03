echo "Converting .h5 model to .tflite model"
python3 converter.py

echo "Moving and renaming .tflite file to assets"
cp ./saved_models/converted_model.tflite ../rps_app/assets/rps.tflite

echo "Completed"