sleep 10

URL=https://mlh.sweetsofimc.dev

RED='\033[0;31m'
GREEN='\033[0;32m'
BOLD=$(tput bold)
ERROR=false


TEST1=$(curl -o /dev/null -s -w "%{http_code}\n" $URL)
TEST2=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/about)
TEST3=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/portfolio)
TEST4=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/resume)
TEST5=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/contact)
TEST6=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/health)
TEST7=$(curl -X POST -d "username=sweetsofimc&password=12345" -o /dev/null -s -w "%{http_code}\n" $URL/register)
TEST8=$(curl -X POST -d "username=sweetsofimc&password=12345" -o /dev/null -s -w "%{http_code}\n" $URL/login)
TEST9=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/register)
TEST10=$(curl -o /dev/null -s -w "%{http_code}\n" $URL/login)


if [ $TEST1 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Root test passed"
else
    echo -e "${RED}${BOLD}✗ Root test failed"
    ERROR=true
fi

if [ $TEST2 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ About test passed"
else
    echo -e "${RED}${BOLD}✗ About test failed"
    ERROR=true
fi

if [ $TEST3 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Portfolio test passed"
else
    echo -e "${RED}${BOLD}✗ Portfolio test failed"
    ERROR=true
fi

if [ $TEST4 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Resume test passed"
else
    echo -e "${RED}${BOLD}✗ Resume test failed"
    ERROR=true
fi

if [ $TEST5 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Contact test passed"
else
    echo -e "${RED}${BOLD}✗ Contact test failed"
    ERROR=true
fi

if [ $TEST6 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Health test passed"
else
    echo -e "${RED}${BOLD}✗ Health test failed"
    ERROR=true
fi

if [[ $TEST7 == '200' ]]; then
    echo -e "${GREEN}${BOLD}✓ Register post test passed"
else
    echo -e "${RED}${BOLD}✗ Register post test failed"
    ERROR=true
fi

if [[ $TEST8 == '200' ]]; then
    echo -e "${GREEN}${BOLD}✓ Login post test passed"
else
    echo -e "${RED}${BOLD}✗ Login post test failed"
    ERROR=true
fi

if [ $TEST9 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Register test passed"
else
    echo -e "${RED}${BOLD}✗ Register test failed"
    ERROR=true
fi

if [ $TEST10 = "200" ]; then
    echo -e "${GREEN}${BOLD}✓ Login test passed"
else
    echo -e "${RED}${BOLD}✗ Login test failed"
    ERROR=true
fi

if [ "$ERROR" = true ] ; then
    exit 1
fi

exit 0
