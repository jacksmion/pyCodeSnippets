#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
自定义处理SIGNAL信号的函数
'''

import sys
import os
import signal
import time
import logging


SIGUSR1_CONF = "sigusr1.conf"


def handle_signals():
    """
    注册信号处理函数
    1.SIGUSR1：调试信号，用于 dump 当前进程的所有线程堆栈，或获取当前进程的内存占用情况
    命令 kill -s SIGUSR1 <PID> 打印结果到系统日志,但不会终止该进程的运行
    """
    signal.signal(signal.SIGUSR1, _handle_sigusr1)
    signal.signal(signal.SIGUSR2, _reload_trace_conf)
    # 有其他需要统一处理的信号，可在此处添加


def _handle_sigusr1(sigv, frame):
    """
    处理信号 SIGUSR1
    """
    try:
        ppath = sys.argv[0]
        pname = os.path.basename(ppath)
        logging.info(pname, "Catch signal SIGUSR1 %d." % (sigv))

        import ConfigParser
        cfg = ConfigParser.ConfigParser()
        cfg.read(SIGUSR1_CONF)

        output_root_path = cfg.get("output", "root")

        enable_dumpstacks_str = cfg.get("dumpstacks", "enable")
        if enable_dumpstacks_str == "True" or enable_dumpstacks_str == "true":
            _dumpstacks(output_root_path)

        enable_dumpmemory_str = cfg.get("dumpmemory", "enable")
        if enable_dumpmemory_str == "True" or enable_dumpmemory_str == "true":
            _dumpmemory(output_root_path)

        logging.info(pname, "Handle on signal SIGUSR1 %d ok." % (sigv))
    except Exception, ex:
        logging.error(
            pname, "Handle on signal SIGUSR1 %d failed." % (sigv), ex, need_traceback=True)


def _dumpstacks(output_root_path):
    """
    dump 当前进程的所有线程堆栈到 $output_root_path/dumpstacks/dumpstacks_PID_TIME.log
    """
    try:
        ppath = sys.argv[0]
        pname = os.path.basename(ppath)
        pid = os.getpid()
        logger.syslog(pname, "Dump stacks for {0}(pid={1}) begin.".format(ppath, pid))

        import threading
        import traceback

        id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
        code = []
        code.append("Dump stacks for {0}(pid={1})".format(ppath, pid))
        for thread_id, stack in sys._current_frames().items():
            code.append("%s# Thread: %s(%d)" %
                        (os.linesep, id2name.get(thread_id, ""), thread_id))
            for filename, lineno, name, line in traceback.extract_stack(stack):
                code.append('File: "%s", line %d, in %s' %
                            (filename, lineno, name))
                if line:
                    code.append("  %s" % (line.strip()))

        dump_file_name = "dumpstacks_{0}_{1}_{2}.log".format(
            pname, pid, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        dump_file_path = os.path.join(output_root_path, "dumpstacks", dump_file_name)
        dump_dir_path = os.path.dirname(dump_file_path)
        if not os.path.exists(dump_dir_path):
            os.makedirs(dump_dir_path)

        with open(dump_file_path, "w") as fobj:
            fobj.write(os.linesep.join(code))
        logging.info(pname, "Saved in {0}".format(dump_file_path))

        logging.info(pname, "Dump stacks for {0}(pid={1}) end.".format(ppath, pid))
    except Exception, ex:
        logging.error(
            pname,
            "Dump stacks for {0}(pid={1}) failed.".format(ppath, pid),
            ex,
            need_traceback=True)


def _dumpmemory(output_root_path):
    """
    dump 当前进程的内存占用情况到 $output_root_path/dumpmemory/dumpmemory_PID_TIME.log
    """
    try:
        ppath = sys.argv[0]
        pname = os.path.basename(ppath)
        pid = os.getpid()
        logger.syslog(pname, "Dump memory for {0}(pid={1}) begin.".format(ppath, pid))

        dump_file_name = "dumpmemory_{0}_{1}_{2}.log".format(
            pname, pid, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        dump_file_path = os.path.join(output_root_path, "dumpmemory", dump_file_name)
        dump_dir_path = os.path.dirname(dump_file_path)
        if not os.path.exists(dump_dir_path):
            os.makedirs(dump_dir_path)

        import gc
        gc.collect()
        from meliae import scanner
        scanner.dump_gc_objects(dump_file_path)
        logging.info(pname, "Saved in {0}".format(dump_file_path))

        logging.info(pname, "Dump memory for {0}(pid={1}) end.".format(ppath, pid))
    except Exception, ex:
        logging.error(
            pname,
            "Dump memory for {0}(pid={1}) failed.".format(ppath, pid),
            ex,
            need_traceback=True)

