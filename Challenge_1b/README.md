cmd-

cd Challenge_1b

docker build -t pdf-analyzer-b .

docker run --rm -v "%cd%:/app" pdf-analyzer-b

Output folder created as output
