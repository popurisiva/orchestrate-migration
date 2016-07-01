import json
import os
import sys
import argparse
from multiprocessing import Pool

from couchbase.bucket import Bucket

class_list = {
    'jobs': 'com.ctlts.wfaas.job.api.Job',
    'status': 'com.ctlts.wfaas.status.api.Status',
    'executions': 'com.ctlts.wfaas.job.api.Execution',
    'vpnconnection': 'com.ctlts.wfaas.vpn.api.repository.VpnConnection',
    'billingitems': 'com.ctlts.wfaas.job.api.Billing',
    'miniontoken': 'com.ctlts.rnr.minion.api.MinionToken',
    'productdeploys': 'com.ctlts.wfaas.catalog.api.Deploy',
    'productstars': 'com.ctlts.wfaas.catalog.api.Star',
    'catalogs': 'com.ctlts.wfaas.catalog.api.Catalog',
    'secrets': 'com.ctlts.rnr.secrets.api.Secret',
    'serviceaccounts': 'com.ctlts.wfaas.srvc.acct.api.ServiceAccount',
    'publicproducts': 'com.ctlts.wfaas.catalog.api.PublicProduct',
    'schedules': 'com.ctlts.wfaas.schedule.api.Schedule',
    'jobschedules': 'com.ctlts.wfaas.job.api.JobSchedule',
    'credentials': 'com.ctlts.wfaas.ssh.api.repository.Credentials'
}

accounts_to_exclude = ['WFTC']
documents_to_exclude = ['jobs', 'executions', 'status', 'billingitems']
couch_host = '10.101.98.22'
couch_bucket = 'sandbox'
couch_pass = None
failed_file = None
data_path = './data'


def process_line(line_to_process):
    data = json.loads(line_to_process)
    collection = data["path"]["collection"]
    key = data["path"]["key"] or 'NOTHING'
    document = data['value']
    account_alias = document.get('accountAlias', None)
    document_name = collection.lower()
    if account_alias and document_name in documents_to_exclude and account_alias in accounts_to_exclude:
        #print key + '-->' + document_name + '-->' + account_alias + '-->EXCLUDED********'
        return
    document['_class'] = class_list[document_name]
    #print key + '-->' + collection
    try:
        cb = Bucket('couchbase://' + couch_host + '/' + couch_bucket, password=couch_pass)
        cb.upsert(key, document)
    except Exception as e:
        print 'Failed to process : {0} --> {1}. Error {2}'.format(key, collection, e.message)
        failed_file.write(line_to_process)
        #print '*******Written line to failed file*******'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Couchbase data loader',
                                     description='Loads json data in couchbase')
    parser.add_argument('--couch-host', required=False, default=couch_host, dest='couch_host', help='couchbase host.')
    parser.add_argument('--couch-pass', required=False, default=couch_pass, dest='couch_pass', help='couchbase pass.')
    parser.add_argument('--couch-bucket', required=False, default=couch_bucket, dest='couch_bucket', help='bucket.')
    args = parser.parse_args()
    print 'COUCH HOST : ' + args.couch_host
    print 'COUCH BUCKET : ' + args.couch_bucket
    for file_obj in os.listdir(data_path):
        current = os.path.join(data_path, file_obj)
        if os.path.isfile(current):

            print 'Started processing file : {0}'.format(current)
            failed_file = './failures/{1}_fails'.format(data_path, file_obj)
            failed_file = open(failed_file, 'w')
            pool = Pool(300)
            with open(current) as line:
                pool.map(process_line, line, 300)
            print 'Finished processing file : {0}'.format(current)
            os.remove(current)
            pool.close()
            failed_file.close()
    print 'FINISHED MIGRATION. BYE BYE ORCHESTRATE !!!!'
