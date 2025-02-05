'''
script for submitting jobs to runjob on fine-tune scibert.
'''
from __future__ import print_function
from itertools import product

import os
import argparse

def main(debug):
    ## hardcord python file name and script folder name.
    # COMMAND_TEMPLATE = 'python senBERT_finetune.py ' if not debug else 'python senBERT_finetune.py --debug '
    COMMAND_TEMPLATE = 'python senBERT_finetune.py --should_continue ' if not debug else 'python senBERT_finetune.py --debug '
    SCRIPT_FILE = 'scripts'
    file_dir = os.path.dirname(os.path.realpath(__file__))

    ## hyperparameters.
    lr_list = [5e-6,2e-5,5e-5]
    bs_list = [32]
    epoch_list = [10,15]
    cnt = 0
    combinations = list(product(*[lr_list, bs_list, epoch_list]))
    for comb in combinations:
        comb = list(comb)
        output_dir = f'model-sen_SciBERT_lr-{comb[0]}_bs-{comb[1]}_epoch-{comb[2]}'
        command = COMMAND_TEMPLATE + (f'--learning_rate={comb[0]} --batch_size={comb[1]} --num_epochs={comb[2]} ')

        # print(command)
        os.makedirs(SCRIPT_FILE, exist_ok=True)
        bash_file = os.path.join(file_dir, SCRIPT_FILE, f'{output_dir}.sh')
        dest_file = os.path.join(file_dir, SCRIPT_FILE, f'{output_dir}.out')
        with open( bash_file, 'w' ) as OUT:
            OUT.write('source ~/.bashrc\n')
            OUT.write('conda activate COVID_torch\n')
            OUT.write(f'cd {file_dir}\n')
            OUT.write(command)
        print(command)
        qsub_command = f'qsub -P medifor -q ephemeral.q -j y -o {dest_file} -l h_rt=24:00:00,h_vmem=10g,gpu=1 {bash_file}'
        print(qsub_command)
        os.system( qsub_command )
        cnt += 1
        print( 'Submitted #{}'.format(cnt))
        if debug:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sci-sentence-bert on CORD_19.')
    parser.add_argument('--debug', action="store_true", help="debug mode or not.")
    args = parser.parse_args()
    main(args.debug)
