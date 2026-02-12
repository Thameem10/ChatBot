// 1. install all the package

python -m venv venv

source venv/bin/activate

// 2. cmd to install the packages with version is present in the reuirement.txt . using it , you can install it

pip install -r requirements.txt

// 3. cmd to run a seed file

python3 seed.py

// 4. Enter the script folder in backend folder where the build_vector_store.py is present . It help you to run a build_vector_store.py which help to create a vector store and break the files into chunks . convert and save this in faiss index

cd scripts

python3 build_vector_store.py

// 5. Since you're on Linux (I can see from your terminal path), run:

curl -fsSL https://ollama.com/install.sh | sh

// 6. After install, verify:

ollama --version

// 7. Download a Model

ollama pull llama3

// 8. Before starting FastAPI:

ollama serve

// 9. Finally run a fast api server . It will help to create a tables and run a service , routes , controller and all

./runserver.sh
