#!/bin/bash

# Set the number of days to define the age limit of backups to be deleted.
DAYS_THRESHOLD=7

oc get backup -n openshift-adp --no-headers | awk '{print $1, $2}' | while read -r name age; do
    days_difference=$(echo "$age" | grep -o '[0-9]\+d' | grep -o '[0-9]\+')
    hours_difference=$(echo "$age" | grep -o '[0-9]\+h' | grep -o '[0-9]\+')
    total_hours=$((days_difference * 24 + hours_difference))
    
    if [ $total_hours -gt $((DAYS_THRESHOLD * 24)) ]; then
        cat <<EOF | oc apply -f -
apiVersion: velero.io/v1
kind: DeleteBackupRequest
metadata:
  name: delete-${name}-backup
  namespace: openshift-adp
spec:
  backupName: $name
EOF
    fi
done
