# Shell Setup for ROBOTAPI imports
# setup.sh
# bhgomes

import_list='
    numpy
'

importer () {
    array="$1";
    error_state=0;
    for var in "${array[@]}"; do
        pip install $var
        if [ "$?" ]; then
            echo "Error installing $var";
            let "error_state += 1";
        else
            echo "Imported $var successfully";
        fi
    done
    return "$error_state";
}

importer "$import_list" # import the necessary modules
python robotapi.py        # run tests from robotapi
