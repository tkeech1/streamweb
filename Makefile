install-deps:
	python3 -m pip install -r requirements.txt
	
run-streamlit-prd:
	cd streamweb/ && streamlit run layout_clean_sidebar.py -- prd

run-streamlit:
	cd streamweb/ && streamlit run layout_clean_sidebar.py

run-streamlit-nosb:
	cd streamweb/ && streamlit run layout_clean_no_sidebar.py

test:
	cd streamweb/ && python3 -m pytest -s