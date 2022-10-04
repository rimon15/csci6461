import subprocess
import os
import sys
import multiprocessing

MAX_CORES = multiprocessing.cpu_count()
BENCHMARKS_DIR = '/mnt/raid0_24TB/rimon/classes/csci6461/benchmarks/'
SIMPLESIM_DIR = '/mnt/raid0_24TB/rimon/classes/csci6461/simplesim-3.0/'

def run_cmd_no_out(cmd):
    assert(subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0)

def run_cmd_print_stats_avg(cmd, num_runs=1):
    tot_ins_avg = 0
    load_avg = 0
    store_avg = 0
    uncond_avg = 0
    cond_avg = 0
    int_avg = 0
    float_avg = 0
    for _ in range(num_runs):
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        out = result.stderr
        #print(out[out.find('sim: ** simulation statistics **'):out.find('sim_inst_class_prof.end_dist')])
        tot_ins_avg += int(out[out.find('sim_num_insn'):out.find(' # total number of instructions executed')].split(' ')[-1])
        out = out[out.find('load    '):]
        load_avg += float(out[:out.find('\n')].split(' ')[-2])
        out = out[out.find('store    '):]
        store_avg += float(out[:out.find('\n')].split(' ')[-2])
        out = out[out.find('uncond branch   '):]
        uncond_avg += float(out[:out.find('\n')].split(' ')[-2])
        out = out[out.find('cond branch   ') + len('cond branch   '):]
        out = out[out.find('cond branch   '):]
        cond_avg += float(out[:out.find('\n')].split(' ')[-2])
        out = out[out.find('int computation   '):]
        int_avg += float(out[:out.find('\n')].split(' ')[-2])
        out = out[out.find('fp computation   '):]
        float_avg += float(out[:out.find('\n')].split(' ')[-2])


    print('Total instructions for ', cmd[2], ': ', tot_ins_avg / num_runs)
    print('Load for ', cmd[2], ': ', load_avg / num_runs)
    print('Store for ', cmd[2], ': ', store_avg / num_runs)
    print('Uncond branch for ', cmd[2], ': ', uncond_avg / num_runs)
    print('Cond branch for ', cmd[2], ': ', cond_avg / num_runs)
    print('Int for ', cmd[2], ': ', int_avg / num_runs)
    print('Float for ', cmd[2], ': ', float_avg / num_runs, '\n')

def make_isa(isa):
    os.chdir(SIMPLESIM_DIR)
    run_cmd_no_out(['make', 'clean'])
    run_cmd_no_out(['make', 'config-' + isa])
    run_cmd_no_out(['make', '-j' + str(MAX_CORES)])

'''
128/2:
./sim-cache -cache:il1 il1:64:16:2:l -cache:il2 none -cache:dl1 dl1:64:16:2:l -cache:dl2 none -tlb:itlb none -tlb:dtlb none tests-alpha/bin/test-math

128/2 unified:
./sim-cache -cache:il1 dl1 -cache:il2 none -cache:dl1 ul1:128:16:2:l -cache:dl2 none -tlb:itlb none -tlb:dtlb none tests-alpha/bin/test-math

CPI:
./sim-outorder -cache:il1 il1:1024:16:1:l -cache:il2 none -cache:dl1 dl1:1024:16:1:l -cache:dl2 none -tlb:itlb none -tlb:dtlb none tests-alpha/bin/test-math

'''

def part1():
    #make_isa('alpha')
    print('--------------PART 1-------------')
    run_cmd_print_stats_avg([SIMPLESIM_DIR + 'sim-cache', '-cache:dl1', 'dl1:', ])
    # run_cmd_print_stats_avg([SIMPLESIM_DIR + 'sim-profile', '-all', 'anagram.alpha', 'words', '<', 'anagram.in'])
    # run_cmd_print_stats_avg([SIMPLESIM_DIR + 'sim-profile', '-all', 'go.alpha', '50', '9', '2stone9.in'])
    # run_cmd_print_stats_avg([SIMPLESIM_DIR + 'sim-profile', '-all', 'compress95.alpha', '<', 'compress95.in'])
    # run_cmd_print_stats_avg([SIMPLESIM_DIR + 'sim-profile', '-all', 'cc1.alpha', '-O', 'lstmt.i'])

part1()