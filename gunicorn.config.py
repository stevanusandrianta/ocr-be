import multiprocessing

bind = ':8080'

workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2 + 1

timeout = 600

forwarded_allow_ips = '*'
