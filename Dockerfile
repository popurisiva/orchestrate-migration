FROM ansible/centos7-ansible
MAINTAINER WFaaS
RUN pip install pycrypto
RUN pip install porc
RUN pip install requests==2.7
RUN pip install hvac==0.2.7
RUN pip install pika
RUN yum install -y python-devel
RUN yum group install -y "Development Tools"
RUN yum install -y wget
RUN wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-0-x86_64.rpm
RUN rpm -ivh couchbase-release-1.0-0-x86_64.rpm
RUN yum install -y libcouchbase-devel libcouchbase2-bin gcc gcc-c++
RUN pip install couchbase
RUN mkdir /data01; mkdir /data01/runner
ADD setup.py /data01/
RUN cd /data01; pip install .
ENV PYTHONPATH /data01:/usr/lib/python2.7/site-packages
ENV NSS_HASH_ALG_SUPPORT=+MD5
ENV OPENSSL_ENABLE_MD5_VERIFY=1
ADD runner/ /data01/runner/
WORKDIR /data01
CMD ["python","/data01/load_data.py"]