"""[Help functions]


    Automatically generate shell scripts


"""


if __name__ == '__main__':
    command_lines = []
    with open('run_repacking.sh', 'w') as f:
        # f.writelines(command_lines)
        f.writelines(['#! /bin/zsh\n', 'source activate swin\n'])
    for i in range(57):
        command_lines.append(
            'python encoding_files.py --split train_split/{:05d}.txt &\n'.format(i)
        )
    with open('run_repacking.sh', 'a') as f:
        f.writelines(command_lines)
    