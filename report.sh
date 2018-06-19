for host in $(cat test-hosts);
do
  python report.py $host > reports/$host.html
done
