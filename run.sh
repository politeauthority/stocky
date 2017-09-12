if [ "${STOCKY_BUILD}" == "LIVE" ]; then
	echo 'Running with Gunicorn'
	gunicorn -w 4 -b 127.0.0.1:80 app:app
else
	echo 'Running Standalone'
	python /opt/stocky/run.py
fi
