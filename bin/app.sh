#!/usr/bin/env bash

BIN=$(cd $(dirname $0);pwd)
BASE_DIR=$(cd ${BIN}/../;pwd)
LOG_DIR=${BASE_DIR}/log
PID_FILE=${BASE_DIR}/pid

USAGE="Usage: app.sh [start|stop|restart|status|help]"


function start() {
    echo "Starting app ..."

    if [ -f ${PID_FILE} ]; then
        local pid=$(cat ${PID_FILE})
        if is_app_running ${pid}; then
            echo "App has started, pid: ${pid}"
            return
        fi
    fi
    if [ ! -d ${LOG_DIR} ]; then
        mkdir -p ${LOG_DIR}
    fi
    uwsgi uwsgi.ini &> ${LOG_DIR}/uwsgi.log &
    echo $! > ${PID_FILE}
    local pid=$(cat ${PID_FILE})
    if is_app_running ${pid}; then
        echo "Start success, pid: ${pid}"
    else
	    echo "Start failed"
    fi
}

function stop() {
    if [ ! -f ${PID_FILE} ];then
	    echo "App has stopped"
	    return
    fi

    local pid=$(cat ${PID_FILE})
    echo "Stopping app, pid: ${pid}"
    attempt=1
    while [ ${attempt} -le 3 ];do
	    if ! is_app_running ${pid}; then
	        rm ${PID_FILE}
            break
        fi
	    echo "Try killing, attempt: ${attempt}"
        kill ${pid}
	    sleep 10
	    attempt=$((${attempt}+1))
    done

    if is_app_running ${pid}; then
	    echo "Stop failed, please retry"
	    return 1
    else
        echo "Stop success"
	    return 0
    fi
}

function restart() {
    if ! stop; then
	    return
    fi
    echo "Restart app"
    start
}

function status() {
   if [ ! -f ${PID_FILE} ]; then
       echo "App is not running"
   else
       local pid=$(cat ${PID_FILE})
       if ! is_app_running ${pid}; then
	       echo "App is not running"
       else
	       echo "App is running, pid: ${pid}"
       fi
    fi
}

function is_app_running() {
    local pid=$1
    app=$(ps -ef | grep "${pid}"| grep -v grep)
    if [ -z "${app}" ]; then
	    return 1
    else
	    return 0
    fi
}

case $1 in
    "start")
	     start
	 ;;
    "stop")
         stop
	 ;;
    "restart")
         restart
	 ;;
    "status")
         status
	 ;;
    "help")
         echo ${USAGE}
	 ;;

    *)
         echo ${USAGE}
	 ;;
esac
