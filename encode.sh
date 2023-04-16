#!/bin/bash
exec_file="encode/encode_tables.py"
exec_scpt=`basename "$0"`

help() {
    printf "\033[1;32mEncoder for TransGatacca\033[0m\n"
    echo "Usage:"
    echo "$exec_scpt --[COMMAND] SUBCOMMAND <args...> "
    echo "COMMANDs:"
    echo "--TABLE: Generate genetic tables encodings"
    echo "--FREQ: Generate codon frequency encodings"
    echo "SUBCOMMANDs:"
    echo "json: Generate JSON files"
    echo "carr: Generate C arrays"
    echo "Args:"
    echo "--TABLE: 2 files, one for each translate and reverse translate tables"
    echo "--FREQ: 1 file, for either JSON or clists"
    exit 1;
}

wrong_arg() {
    printf "\033[1;31mWrong arguments passed\033[0m\n"
    echo "Pass --help for help"
    exit 1;
}

if [[ $1 == --TABLE* ]]; then
    exec_file="encode/encode_tables.py"
    if [[ "$#" != "4" ]]; then
        wrong_arg
    fi
elif [[ $1 == --FREQ* ]]; then
    exec_file="encode/encode_cfreqs.py"
    if [[ "$#" != "3" ]]; then
        wrong_arg
    fi
elif [[ $1 == --h* ]]; then
    help
else
    wrong_arg
fi

shift

$exec_file $@
