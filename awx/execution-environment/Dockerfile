FROM quay.io/ansible/awx-ee:latest

USER root

# Install OpenShift CLI (oc)
RUN curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/linux/oc.tar.gz && \
    tar -xf oc.tar.gz && \
    mv oc /usr/local/bin/oc && \
    rm oc.tar.gz

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/kubectl

# Install kustomize
RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash && \
    mv kustomize /usr/local/bin/kustomize

# Install Python and pip
RUN yum -y install python3 python3-pip && \
    pip3 install --upgrade pip

# Install AWS CLI
RUN pip3 install awscli

# Set the default working directory
WORKDIR /var/lib/awx

USER 1000

# Start the AWX task runner
CMD ["ansible-runner", "run", "/var/lib/awx/job_templates"]
