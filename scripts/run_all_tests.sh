#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.
source venv/bin/activate

echo "Running unit tests..."
pytest tests/test_processor.py

echo "Running integration test (ArXiv Attention paper)..."
python3 src/main.py data/samples/attention_is_all_you_need.pdf output_attention.epub

echo "Running integration test (ArXiv ResNet paper)..."
python3 src/main.py data/samples/resnet.pdf output_resnet.epub

echo "Running integration test (IACR Dilithium paper)..."
python3 src/main.py data/samples/dilithium.pdf output_dilithium.epub

echo "All tests completed."
