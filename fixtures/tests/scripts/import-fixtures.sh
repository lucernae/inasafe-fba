#!/usr/bin/env bash

source /env-data.sh

echo "Imported directory: $1"
RETVAL=0

for f in $(find $1 -name '*.sql' -o -name '*.sh' -o -name '*.py' | sort -n); do
	case "$f" in
		*.sql)
			echo "Importing $f"
			if ! PGPASSWORD=${POSTGRES_PASS} psql -d ${POSTGRES_DB} -U ${POSTGRES_USER} -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -v ON_ERROR_STOP=1 -f $f -1; then
				echo "Import failed on file $f"
				echo "Cancel import"
				RETVAL=1
				break
			fi
			;;
		*.sh)
			echo "Executing $f"
			if ! bash $f; then
				echo "Execution failed on file $f"
				echo "Cancel import"
				RETVAL=1
				break
			fi
			;;
		*.py)
			echo "Executing $f"
			export PYTHONPATH=${REPO_ROOT}/fixtures/tests
			if ! python3 $f; then
				echo "Execution failed on file $f"
				echo "Cancel import"
				RETVAL=1
				break
			fi
			;;
	esac
done

echo "Import process finished with exit code: $RETVAL"

exit $RETVAL
