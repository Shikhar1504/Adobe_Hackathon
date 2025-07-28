cmd-

cd Challenge_1a

docker build --platform linux/amd64 -t pdf-processor .

docker run --rm -v "%cd%\sample_dataset\pdfs":/app/input:ro -v "%cd%\sample_dataset\outputs":/app/output --network none pdf-processor

Outputs displayed in sample_dataset/outputs
