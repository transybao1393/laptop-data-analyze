setup:
	conda create -n laptop-data python=3.10.9 -y
	conda init zsh
	conda activate laptop-data
	pip install -r requirements.txt
run:
	python main.py
