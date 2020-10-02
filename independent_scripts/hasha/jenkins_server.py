#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Ge the API token following these steps:
#    Log in to Jenkins.
#    Click your name (upper-right corner).
#    Click Configure (left-side menu).
#    Click Show API Token.
#The API token is revealed.
#You can change the token by clicking the Change API Token button.

import getopt, json, logging, os, time, urllib3, sys
from   jenkinsapi.jenkins import Jenkins

# disable warning
# http://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run_job(job_name, job_args):
    job_ret = {}

    server = JenkinsServer(job_name="Runner-v3", job_args)
    server.build()

    job_ret["status"] = server.build_succeed
    job_ret["build_num"] = server.build_number


    return job_ret


def get_jenkins_token(login = True):
    if not login:
        logging.basicConfig(level=logging.CRITICAL)
        return "", ""

    # these two lines enable the python jenkins log
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='[%H:%M:%S]->')
    logging.Formatter.converter = time.gmtime
    # TODO if we run in jenkins_user_token = "BJ_JENKINS_USER_TOKEN"
    return os.environ.get('JENKINS_USER_ID'), os.environ.get('JENKINS_USER_TOKEN')    

# https://stackoverflow.com/questions/4015417/python-class-inherits-object
class JenkinsServer(object):
    """Controlling a Jenkins server by the Jenkins REST API"""

    def __init__(self, job_name="Runner-v3", job_args, login = True):
        """Jenkins server init"""
        jenkins_url = "https://openshift-qe-jenkins.rhev-ci-vms.eng.rdu2.redhat.com"
        user_id, user_token = get_jenkins_token(login)

        self.build_succeed = False
        self.build_output = None

        try:
            self.build_vars = job_args
            server_instance = Jenkins(jenkins_url, username=user_id, password=user_token, timeout=120, ssl_verify=False)
            self.server = server_instance[job_name]
        except Exception as e: print(e)

    def build(self):
        """Trigger a Jenkins job"""
        build_no = os.environ.get('QE_REUSE_BUILDNUMBER')
        if build_no is not None and build_no != "":
            self.build_output = ""
            self.build_number = int(build_no)
            self.build_succeed = True
            try:
                self.build_instance = self.server.get_build(self.build_number)
            except:
                pass
            return

        try:
            task = self.server.invoke(build_params=self.build_vars, block=True, delay=120)
            self.build_instance = task.get_build()
            # self.build_url = self.build_instance.get_result_url()
            self.build_output = self.build_instance.get_console()
            self.build_number = self.build_instance.get_number()

            build_result = self.build_instance.get_status()
            if build_result == "SUCCESS":
                self.build_succeed = True
            elif build_result == "FAILURE":
                self.build_succeed = False
        except Exception as e: print(e)


    def fetch_artifacts(self, file_pattern, to_dir, build_id = 0):
        files = []
        try:
            if build_id != 0:
                self.build_instance = self.server.get_build(build_id)

            for artifact in self.build_instance.get_artifacts():
                if file_pattern not in artifact.relative_path:
                    continue
                fspath = artifact.save(to_dir + "/" + artifact.filename)
                if fspath != "":
                   files.append(fspath) 
        except Exception as e: print(e)

        return files
