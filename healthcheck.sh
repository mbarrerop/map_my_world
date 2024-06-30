#!/bin/sh

code=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8002/)
echo "response code: $code"

if [ "$code" == "200" ]
then
  echo "success";
  exit 0;
else
  echo "error";
  exit 1;
fi