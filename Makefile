number_thread := 1

init-database:
	rm -rf my_database.db # xoa database
	python init_database.py # chay khoi tao database

insert-account-to-database:
	python load_account_to_database.py # them account vao database

run-auto-affilitest:
	python auto_affilitest.py # run check link

target:
	number=1 ; while [[ $$number -le $(number_thread) ]] ; do \
		(python registry_affilitest.py $$number &); \
		((number = number + 1)) ; \
	done


run-auto-maps-4g-1:
	python demo_undetected_chromedriver_v3.py -p 1 --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 1 --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 2 --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 2 --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 3 --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 3 --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 4 \
	& python demo_undetected_chromedriver_v3.py -p 4


run-auto-maps-wan:
	python demo_undetected_chromedriver_v3.py -p 1 -t wan \
	& python demo_undetected_chromedriver_v3.py -p 1 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 1 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 2 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 2 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 2 -t wan



run-auto-maps-wan-1:
	python demo_undetected_chromedriver_v3.py -p 5 -t wan  --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 5 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 6 -t wan --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 6 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 3 -t wan --key 2 \
	& python demo_undetected_chromedriver_v3.py -p 3 -t wan --reset-proxy 1 \
	& python demo_undetected_chromedriver_v3.py -p 4 -t wan \
	& python demo_undetected_chromedriver_v3.py -p 4 -t wan

run-auto-maps-4g-2:
	python demo_undetected_chromedriver_v3.py -p 5 \
	& python demo_undetected_chromedriver_v3.py -p 5 \
	& python demo_undetected_chromedriver_v3.py -p 6 \
	& python demo_undetected_chromedriver_v3.py -p 6 \
	& python demo_undetected_chromedriver_v3.py -p 7 \
	& python demo_undetected_chromedriver_v3.py -p 7
